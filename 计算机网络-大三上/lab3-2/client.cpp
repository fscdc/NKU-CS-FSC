#include <winsock2.h>
#include <windows.h>
#include <iostream>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <string>
#include <time.h>
#include <fstream>
#include <queue>
#include <vector>
#include "Message.h"

#pragma comment (lib, "ws2_32.lib")

using namespace std;



//根据实验ppt原理图，这次实验中client是直接发送到router后再进行转发到server
//所以可以简单理解为对于client来说router就是双端通信中的“server”
const int RouterPORT = 30000; 
const int ClientPORT = 20230;



//定义创建ACK接收线程时候传过去的参数，由于创建线程只能传一个参数，所以这里将需要传过去的信息绑定成结构体
struct parameters {
	SOCKET clientSocket;
	SOCKADDR_IN serverAddr;
	int nummessage;
};

// 定义窗口大小为10
#define windowssize 16

//缓冲区存已发送未确认的message
queue<Message> messageBuffer;

//辅助加锁
HANDLE mutex;
//client端维护的序列号
int initrelseq = 0;
//滑动窗口的开始和到达
int start = 0;
int arrive = 0;
//计时
int messagestart;
//标志位
bool finish = false;
bool resend = false;

//缓冲区更新，收到了ACK报文，则需要把缓冲区那些seq值小于等于ACK报文的ack值的那些message弹出队列
void updateBuffer(int ackNum) {
    while (!messageBuffer.empty()) {
        const Message& frontMsg = messageBuffer.front();
        if (frontMsg.SeqNum <= ackNum) {
            messageBuffer.pop();  // 删除已确认的消息
        } else {
            break;  // 一旦遇到一个未确认的消息，停止循环
        }
    }
}


//实现client的三次握手
bool threewayhandshake(SOCKET clientSocket, SOCKADDR_IN serverAddr)
{
	int AddrLen = sizeof(serverAddr);
	Message buffer1,buffer2,buffer3;

	//发送第一次握手的消息（SYN有效，seq=x（相对seq就是0））
	buffer1.SrcPort = ClientPORT;
	buffer1.DestPort = RouterPORT;
	buffer1.flag += SYN;
	buffer1.SeqNum = initrelseq;
	buffer1.setCheck();

	int sendByte = sendto(clientSocket, (char*)&buffer1, sizeof(buffer1), 0, (sockaddr*)&serverAddr, AddrLen);
	clock_t buffer1start = clock();
	if (sendByte > 0)
	{
		cout << "client发送第一次握手："
		<< "源端口: " << buffer1.SrcPort << ", "
		<< "目的端口: " << buffer1.DestPort << ", "
		<< "序列号: " << buffer1.SeqNum << ", "
		<< "标志位: " << "[SYN: " << (buffer1.flag & SYN ? "SET" : "NOT SET") 
		<< "] [ACK: " << (buffer1.flag & ACK ? "SET" : "NOT SET") 
		<< "] [FIN: " << (buffer1.flag & FIN ? "SET" : "NOT SET") << "], "
		<< "校验和: " << buffer1.checkNum << endl;
	}

	int resendtimes = 0;
	//接收第二次握手的消息
	while (true)
	{
		int recvByte = recvfrom(clientSocket, (char*)&buffer2, sizeof(buffer2), 0, (sockaddr*)&serverAddr, &AddrLen);
		if (recvByte > 0)
		{
			//成功收到消息，检查校验和、ACK、SYN、ack
			if ((buffer2.flag & ACK) && (buffer2.flag & SYN) && buffer2.check() && (buffer2.AckNum == buffer1.SeqNum+1))
			{
				cout << "client接收第二次握手成功" << endl;
				break;
			}
			else{
				cout<<"接收第二次握手消息检查失败"<<endl;
			}
		}

		//client发送第一次挥手超时，重新发送并重新计时
		if (clock() - buffer1start > MAX_WAIT_TIME)
		{
            if (++resendtimes > MAX_SEND_TIMES) {
                cout << "client发送第一次握手超时重传已到最大次数，发送失败" << endl;
                return false;
            }
			cout << "client发送第一次握手，第"<< resendtimes <<"次超时，正在重传......" << endl;
			int sendBtye = sendto(clientSocket, (char*)&buffer1, sizeof(buffer1), 0, (sockaddr*)&serverAddr, AddrLen);
			buffer1start = clock();
            if (sendByte <= 0) {
                cout << "client第一次握手重传失败" << endl;
				return false;
            } 
		}
	}

	//发送第三次握手的消息（ACK有效，seq=x+1（相对seq就是1）ack=y+1（也就是1））
	buffer3.SrcPort = ClientPORT;
	buffer3.DestPort = RouterPORT;
	buffer3.flag += ACK;
	buffer3.SeqNum = ++initrelseq;
	buffer3.AckNum = buffer2.SeqNum+1;
	buffer3.setCheck();

	sendByte = sendto(clientSocket, (char*)&buffer3, sizeof(buffer3), 0, (sockaddr*)&serverAddr, AddrLen);
	clock_t buffer3start = clock();
	if (sendByte == 0)
	{
		cout << "client发送第三次握手失败" << endl;
		return false;
	}
	cout << "client发送第三次握手:"
	<< "源端口: " << buffer3.SrcPort << ", "
	<< "目的端口: " << buffer3.DestPort << ", "
	<< "序列号: " << buffer3.SeqNum << ", "
	<< "确认号: " << (buffer3.flag & ACK ? to_string(buffer3.AckNum) : "0") << ", "
	<< "标志位: " << "[SYN: " << (buffer3.flag & SYN ? "SET" : "NOT SET") 
	<< "] [ACK: " << (buffer3.flag & ACK ? "SET" : "NOT SET") 
	<< "] [FIN: " << (buffer3.flag & FIN ? "SET" : "NOT SET") << "], "
	<< "校验和: " << buffer3.checkNum << endl;
	cout << "client连接成功！" << endl;
	start=initrelseq+1;
	arrive=initrelseq+1;
	return true;
}




//接收ack的线程
DWORD WINAPI recvackthread(PVOID useparameter)
{
	mutex = CreateMutex(NULL, FALSE, NULL); // 创建互斥锁
	parameters* p = (parameters*)useparameter;
	SOCKADDR_IN serverAddr = p->serverAddr;
	SOCKET clientSocket = p->clientSocket;
	int nummessage = p->nummessage;
	int AddrLen = sizeof(serverAddr);

	int errorack = -1;
	int errorcount = 0;

	unsigned long mode = 1;
	ioctlsocket(clientSocket, FIONBIO, &mode);
	while (1)
	{
		Message recvMsg;
		int recvByte = recvfrom(clientSocket, (char*)&recvMsg, sizeof(recvMsg), 0, (sockaddr*)&serverAddr, &AddrLen);
		//成功收到消息
		if (recvByte > 0)
		{
			//检查校验和
			if (recvMsg.check())
			{
				if (recvMsg.AckNum >= start){
					{
					WaitForSingleObject(mutex, INFINITE);  // 等待并获取互斥锁
					updateBuffer(recvMsg.AckNum);
					start = recvMsg.AckNum + 1;				
					cout << "client收到: ack = " << recvMsg.AckNum << "的ACK报文" << endl;
					cout <<"[窗口情况（接收到消息后瞬间）] 窗口大小为"<<windowssize<<"已发送但未收到确认的报文数量为"<<(arrive-start)<<endl<<endl;
					ReleaseMutex(mutex);                   // 释放互斥锁
					}
				}
				if (start != arrive){
					messagestart = clock();
				}
				//判断结束的情况
				if (recvMsg.AckNum == nummessage + 1)
				{
					cout << "\n文件传输结束" << endl;
					finish = true;
					return 0;
				}
				//连续收到三个相同的错误ACK触发快速重传
				//快速重传，基于TCP的快速重传算法实现，减少超时重传的等待时间
				if (errorack != recvMsg.AckNum)
				{
					errorcount = 0;
					errorack = recvMsg.AckNum;
				}
				else
				{
					errorcount++;
				}
				if (errorcount == 3)
				{
					resend = true;
				}
				
			}
			//若校验失败不对，忽略并继续等待
		}
	}
	CloseHandle(mutex); // 清理互斥锁
	return 0;
}

//实现文件传输
void sendFileToServer(string filename, SOCKADDR_IN serverAddr, SOCKET clientSocket)
{
	mutex = CreateMutex(NULL, FALSE, NULL); // 创建互斥锁
	int starttime = clock();
	string realname = filename;
	filename="测试文件\\"+filename;
	//将文件读成字节流
	ifstream fin(filename.c_str(), ifstream::binary);
	if (!fin) {
		printf("无法打开文件！\n");
		return;
	}
	
	//文件读取到fileBuffer
	BYTE* fileBuffer = new BYTE[MaxFileSize];
	unsigned int fileSize = 0;
	BYTE byte = fin.get();
	while (fin) {
		fileBuffer[fileSize++] = byte;
		byte = fin.get();
	}
	fin.close();


	int batchNum = fileSize / MaxMsgSize;//可以装满的报文数量
	int leftNum = fileSize % MaxMsgSize;//剩余数据量大小
	int nummessage;
    //算出一共要发送的数据报文数量
	if(leftNum!=0){
		nummessage=batchNum+2;
	}
	else{
		nummessage=batchNum+1;
	}
	
	parameters useparameter;
	useparameter.serverAddr = serverAddr;
	useparameter.clientSocket = clientSocket;
	useparameter.nummessage = nummessage;
	HANDLE hThread = CreateThread(NULL, 0, (LPTHREAD_START_ROUTINE)recvackthread, &useparameter, 0, 0);
	
	int count=0;
    while(1){
		if (arrive < start + windowssize && arrive < nummessage + 2){
			Message datamessage;
			if (arrive == 2){
				//发送文件名和文件大小，文件大小放在头部的size字段了，设置了SFileName标志位datamessage
				datamessage.SrcPort = ClientPORT;
				datamessage.DestPort = RouterPORT;
				datamessage.size = fileSize;
				datamessage.flag += SFileName;
				datamessage.SeqNum = arrive;
				//将文件名放在前面并加一个结束符
				for (int i = 0; i < realname.size(); i++)
					datamessage.data[i] = realname[i];
				datamessage.data[realname.size()] = '\0';
				datamessage.setCheck();
			}
			else if (arrive == batchNum + 3 && leftNum > 0){
				//未满载的数据报文段发送，如果是整除就不发送这个报文了
				datamessage.SrcPort = ClientPORT;
				datamessage.DestPort = RouterPORT;
				datamessage.SeqNum = arrive;
				for (int j = 0; j < leftNum; j++)
				{
					datamessage.data[j] = fileBuffer[batchNum * MaxMsgSize + j];
				}
				datamessage.setCheck();
			}
			else{
				//满载的数据报文段发送，类似批量发送，这里为了简便并没有设置标志位
				//发送的数据报文并不需要设置标志位，这里是为了方便快捷
				datamessage.SrcPort = ClientPORT;
				datamessage.DestPort = RouterPORT;
				datamessage.SeqNum = arrive;
				for (int j = 0; j < MaxMsgSize; j++)
				{
					datamessage.data[j] = fileBuffer[count * MaxMsgSize + j];
				}
				datamessage.setCheck();
				count++;
			}
			if (start == arrive)
			{
				messagestart = clock();
			}
			{
			WaitForSingleObject(mutex, INFINITE);  // 等待并获取互斥锁
			//存到缓冲区中
			messageBuffer.push(datamessage);
			sendto(clientSocket, (char*)&datamessage, sizeof(datamessage), 0, (sockaddr*)&serverAddr, sizeof(SOCKADDR_IN));
			arrive++;
			cout << "client发送: seq = " << datamessage.SeqNum << ", 校验和 = " << datamessage.checkNum<<"的数据报文"<<endl;
			cout <<"[窗口情况（发送消息后瞬间）] 窗口大小为"<<windowssize<<"已发送但未收到确认的报文数量为"<<(arrive-start)<<endl<<endl;
			ReleaseMutex(mutex);    // 释放互斥锁
			}               	
		}

		// 超时重传+快速重传
		if (resend  || clock() - messagestart > MAX_WAIT_TIME)
		{
			if(resend){
				cout<<"三次相同冗余ACK报文触发快速重传机制"<<endl;
			}
			{
			WaitForSingleObject(mutex, INFINITE);  // 等待并获取互斥锁
			// 从缓冲区中重传消息
			for (int i = 0; i < arrive-start; i++) {
				Message resendMsg = messageBuffer.front();

				sendto(clientSocket, (char*)&resendMsg, sizeof(resendMsg), 0, (sockaddr*)&serverAddr, sizeof(SOCKADDR_IN));
				cout<<"正在重传: seq = "<<resendMsg.SeqNum<<"的数据报文"<<endl;

				// 将消息重新放入队尾，以便后续可能的再次重传
				messageBuffer.push(resendMsg);
				messageBuffer.pop();
			}
			ReleaseMutex(mutex);    // 释放互斥锁
			}
			messagestart = clock();
			resend = false;
		}

		//如果结束就退出
		if(finish == true){
			break;
		}
	}
	CloseHandle(hThread);

	//计算传输时间和吞吐率
	int endtime = clock();
	cout << "\n总传输时间为:" << (endtime - starttime) << "ms" << endl;
	cout << "平均吞吐率:" << ((float)fileSize) / (endtime - starttime)  << "bytes/ms" << endl << endl;
	delete[] fileBuffer;//释放内存
	CloseHandle(mutex); // 清理互斥锁
	return;
}


//实现client的四次挥手
bool fourwayhandwave(SOCKET clientSocket, SOCKADDR_IN serverAddr)
{
	//用这个更新initrelseq
	initrelseq=arrive;
	int AddrLen = sizeof(serverAddr);
	Message buffer1;
	Message buffer2;
	Message buffer3;
	Message buffer4;

	//发送第一次挥手（FIN、ACK有效，seq是之前的发送完数据包后的序列号，之前的序列号每次+1
	//（对于0延时和0丢包的1.jpg文件的发送来说，seq这里已经到了189）
	buffer1.SrcPort = ClientPORT;
	buffer1.DestPort = RouterPORT;
	buffer1.flag += FIN;
	buffer1.flag += ACK;
	buffer1.SeqNum = initrelseq++;
	buffer1.setCheck();
	int sendByte = sendto(clientSocket, (char*)&buffer1, sizeof(buffer1), 0, (sockaddr*)&serverAddr, AddrLen);
	clock_t buffer1start = clock();
	if (sendByte == 0)
	{
		cout << "client发送第一次挥手失败，退出" << endl;
		return false;
	}
	cout << "client发送第一次挥手："
	<< "源端口: " << buffer1.SrcPort << ", "
	<< "目的端口: " << buffer1.DestPort << ", "
	<< "序列号: " << buffer1.SeqNum << ", "
	<< "标志位: " << "[SYN: " << (buffer1.flag & SYN ? "SET" : "NOT SET") 
	<< "] [ACK: " << (buffer1.flag & ACK ? "SET" : "NOT SET") 
	<< "] [FIN: " << (buffer1.flag & FIN ? "SET" : "NOT SET") 
	<< "] [SFileName: " << (buffer1.flag & SFileName ? "SET" : "NOT SET") <<"], "
	<< "校验和: " << buffer1.checkNum << endl;
	int resendtimes=0;
	//接收第二次挥手的消息
	while (1)
	{
		int recvByte = recvfrom(clientSocket, (char*)&buffer2, sizeof(buffer2), 0, (sockaddr*)&serverAddr, &AddrLen);
		if (recvByte == 0)
		{
			cout << "client第二次挥手接收失败" << endl;
			return false;
		}
		else if (recvByte > 0)
		{
			//成功收到消息，检查校验和、ACK、ack
			if ((buffer2.flag & ACK) && buffer2.check() && (buffer2.AckNum == buffer1.SeqNum+1))
			{
				cout << "client接收第二次挥手成功" << endl;
				break;
			}
			else
			{
				//cout << "client第二次挥手接收成功，检查失败" << endl;
				continue;
			}
		}
		//client发送第一次挥手超时，重新发送并重新计时
		if (clock() - buffer1start > MAX_WAIT_TIME)
		{
			cout << "client发送第一次挥手，第"<< ++resendtimes <<"次超时，正在重传......" << endl;
			int sendByte = sendto(clientSocket, (char*)&buffer1, sizeof(buffer1), 0, (sockaddr*)&serverAddr, AddrLen);
			buffer1start = clock();
			if(sendByte>0){
				cout<<"client发送第一次挥手重传成功"<<endl;
				break;
			}
			else{
				cout<<"client发送第一次挥手重传失败"<<endl;
			}			
		}
		if (resendtimes == MAX_SEND_TIMES)
        {
			cout << "client发送第一次挥手超时重传已到最大次数，发送失败" << endl;
			return false;
        }
	}

	//接收第三次挥手的消息
	while (1)
	{
		int recvByte = recvfrom(clientSocket, (char*)&buffer3, sizeof(buffer3), 0, (sockaddr*)&serverAddr, &AddrLen);
		if (recvByte == 0)
		{
			cout << "client接收第三次挥手失败" << endl;
			return false;
		}
		else if (recvByte > 0)
		{
			//收到消息，检查校验和、FIN、ACK
			if ((buffer3.flag & ACK)&& (buffer3.flag & FIN) && buffer3.check())
			{
				cout << "client接收第三次挥手成功" << endl;
				break;
			}
			else
			{
				continue;
			}
		}
	}
	
	//发送第四次挥手的消息（ACK有效，ack等于第三次挥手消息的seq+1，seq自动向下递增）
	buffer4.SrcPort = ClientPORT;
	buffer4.DestPort = RouterPORT;
	buffer4.flag += ACK;
	buffer4.SeqNum=initrelseq;
	buffer4.AckNum = buffer3.SeqNum+1;
	buffer4.setCheck();
	sendByte = sendto(clientSocket, (char*)&buffer4, sizeof(buffer4), 0, (sockaddr*)&serverAddr, AddrLen);
	if (sendByte == 0)
	{
		cout << "client发送第四次挥手失败" << endl;
		return false;
	}
	
	cout << "client发送第四次挥手："
	<< "源端口: " << buffer4.SrcPort << ", "
	<< "目的端口: " << buffer4.DestPort << ", "
	<< "序列号: " << buffer4.SeqNum << ", "
	<< "确认号: " << (buffer4.flag & ACK ? to_string(buffer4.AckNum) : "N/A") << ", "
	<< "标志位: " << "[SYN: " << (buffer4.flag & SYN ? "SET" : "NOT SET") 
	<< "] [ACK: " << (buffer4.flag & ACK ? "SET" : "NOT SET") 
	<< "] [FIN: " << (buffer4.flag & FIN ? "SET" : "NOT SET")
	<< "] [SFileName: " << (buffer4.flag & SFileName ? "SET" : "NOT SET") <<"], "
	<< "校验和: " << buffer4.checkNum << endl;
	
	//第四次挥手之后还需等待2MSL，防止最后一个ACK丢失
	//此时client处于TIME_WAIT状态
	int tempclock = clock();
	cout << "client正处于2MSL的等待时间" << endl;
	Message tmp;
	while (clock() - tempclock < 2 * MAX_WAIT_TIME)
	{
		int recvByte = recvfrom(clientSocket, (char*)&tmp, sizeof(tmp), 0, (sockaddr*)&serverAddr, &AddrLen);
		if (recvByte == 0)
		{
			cout << "TIME_WAIT状态时收到错误消息，退出" << endl;
			return false;
		}
		else if (recvByte > 0)
		{
			sendByte = sendto(clientSocket, (char*)&buffer4, sizeof(buffer4), 0, (sockaddr*)&serverAddr, AddrLen);
			cout << "TIME_WAIT状态时发现最后一个ACK丢失，重发" << endl;
		}
	}
	cout << "\nclient关闭连接成功！" << endl;
	return true;
}


int main()
{
	
	//初始化Winsock服务
	WSADATA wsaDataStruct;
	int result = WSAStartup(MAKEWORD(2, 2), &wsaDataStruct);
	if (result != 0) {
		cout << "初始化Winsock服务失败" << endl;
		return -1;
	}
	if (wsaDataStruct.wVersion != MAKEWORD(2, 2)) {
		cout << "不支持所需的Winsock版本" << endl;
		WSACleanup(); 
		return -1;
	}
	cout << "初始化Winsock服务成功" << endl; 

	//创建socket，是UDP套接字，UDP是一种无连接的协议
	SOCKET clientSocket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
	if (clientSocket == INVALID_SOCKET)
	{
		cerr << "创建socket失败" << endl;
		return -1;
	}

	// 设置套接字为非阻塞模式，这是关键的一点
	unsigned long mode = 1;
	if (ioctlsocket(clientSocket, FIONBIO, &mode) != NO_ERROR)
	{
		cerr << "无法设置套接字为非阻塞模式。\n" << endl;
		closesocket(clientSocket); 
		return -1;
	}
	cout << "创建socket成功" << endl;

	//初始化路由器地址
	SOCKADDR_IN serverAddr;
	serverAddr.sin_family = AF_INET;//使用IPv4地址
	serverAddr.sin_addr.S_un.S_addr = inet_addr("127.0.0.1"); 
	serverAddr.sin_port = htons(RouterPORT); 

	//初始化客户端地址
	SOCKADDR_IN clientAddr;
	clientAddr.sin_family = AF_INET;
	clientAddr.sin_addr.S_un.S_addr = inet_addr("127.0.0.1"); 
	clientAddr.sin_port = htons(ClientPORT); 
	
	//bind
	bind(clientSocket, (LPSOCKADDR)&clientAddr, sizeof(clientAddr));
	
	//建立连接
	bool connected = threewayhandshake(clientSocket, serverAddr);
	if (!connected) {
		cerr << "client连接失败，退出" << endl;
		return -1;
	}

	//这里设计的是发送一次文件就会退出
	string filename;
	cout << "请输入要发送的文件名：" << endl;
	cin >> filename;
	cout << endl;
	sendFileToServer(filename, serverAddr, clientSocket);


	//断开连接
	cout << "client将断开连接" << endl;
	bool breaked = fourwayhandwave(clientSocket, serverAddr);
	if (!breaked) {
		cerr << "client断开连接失败，退出" << endl;
		return -1;
	}
	
	closesocket(clientSocket);
	WSACleanup();
	system("pause");
	return 0;
}
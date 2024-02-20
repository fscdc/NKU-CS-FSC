#include <iostream>
#include <winsock2.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
#include <fstream>
#include "Message.h"

#pragma comment (lib, "ws2_32.lib")

using namespace std;



//根据实验ppt原理图，这次实验中client是直接发送到router后再进行转发到server
//所以可以简单理解为对于server来说router就是双端通信中的“client”
const int ServerPORT = 40460; 
const int RouterPORT = 30000; 




int initrelseq = 0;


//实现server的三次握手
bool threewayhandshake(SOCKET serverSocket, SOCKADDR_IN clientAddr)
{
	int AddrLen = sizeof(clientAddr);
	Message buffer1,buffer2,buffer3;
	int resendtimes = 0;

	while (true)
	{
		//接收第一次握手的消息
		int recvByte = recvfrom(serverSocket, (char*)&buffer1, sizeof(buffer1), 0, (sockaddr*)&clientAddr, &AddrLen);
		
		if (recvByte > 0)
		{
			//成功收到消息，检查SYN、检验和
			if (!(buffer1.flag & SYN) || !buffer1.check())
			{
				cout << "server接收第一次握手成功，检查失败" << endl;
				return false;
			}
			cout << "server接收第一次握手成功"<< endl;

			//发送第二次握手的消息（SYN、ACK有效，seq=y（相对seq也是0）ack=x+1（也就是1））
			//我的协议设计双端的seq是各自维护的，并不会相互影响，所以这里是y，但是相对seq还是0。
			buffer2.SrcPort = ServerPORT;
			buffer2.DestPort = RouterPORT;
			buffer2.SeqNum = initrelseq;
			buffer2.AckNum = buffer1.SeqNum+1;
			buffer2.flag += SYN;
			buffer2.flag += ACK;
			buffer2.setCheck();

			int sendByte = sendto(serverSocket, (char*)&buffer2, sizeof(buffer2), 0, (sockaddr*)&clientAddr, AddrLen);
			clock_t buffer2start = clock();
			
			if (sendByte == 0)
			{
				cout << "server发送第二次握手失败" << endl;
				return false;
			}
			cout << "server发送第二次握手："
			<< "源端口: " << buffer2.SrcPort << ", "
			<< "目的端口: " << buffer2.DestPort << ", "
			<< "序列号: " << buffer2.SeqNum << ", "
			<< "确认号: " << (buffer2.flag & ACK ? to_string(buffer2.AckNum) : "N/A") << ", "
			<< "标志位: " << "[SYN: " << (buffer2.flag & SYN ? "SET" : "NOT SET") 
			<< "] [ACK: " << (buffer2.flag & ACK ? "SET" : "NOT SET") 
			<< "] [FIN: " << (buffer2.flag & FIN ? "SET" : "NOT SET") << "], "
			<< "校验和: " << buffer2.checkNum << endl;

			
			//接收第三次握手的消息
			while (true)
			{
				int recvByte = recvfrom(serverSocket, (char*)&buffer3, sizeof(buffer3), 0, (sockaddr*)&clientAddr, &AddrLen);
				if (recvByte > 0)
				{
					//成功收到消息，检查ACK、校验和、ack
					if ((buffer3.flag & ACK) && buffer3.check() && (buffer3.AckNum == buffer2.SeqNum+1))
					{
						initrelseq++;
						cout << "server接收第三次握手成功"<< endl;
						cout << "server连接成功！" << endl;
						return true;
					}
					else
					{
						cout << "server接收第三次握手成功，检查失败" << endl;
						return false;
					}
				}

				//server发送第二次握手超时，重新发送并重新计时
				if (clock() - buffer2start > MAX_WAIT_TIME)
				{
					if (++resendtimes > MAX_SEND_TIMES) {
						cout << "server发送第二次握手超时重传已到最大次数，发送失败" << endl;
						return false;
					}			
					cout << "server发送第二次握手，第"<< resendtimes <<"次超时，正在重传......" << endl;
					int sendByte = sendto(serverSocket, (char*)&buffer2, sizeof(buffer2), 0, (sockaddr*)&clientAddr, AddrLen);
					buffer2start = clock();
					if(sendByte>0){
						cout<<"server发送第二次握手重传成功"<<endl;
					}
					else{
						cout<<"server第二次握手重传失败"<<endl;
					}
				}
			}
		}
	}
	return false;
}

//实现单个报文接收
bool recvMessage(Message& recvMsg, SOCKET serverSocket, SOCKADDR_IN clientAddr)
{
	int AddrLen = sizeof(clientAddr);
	while (1)
	{
		int recvByte = recvfrom(serverSocket, (char*)&recvMsg, sizeof(recvMsg), 0, (sockaddr*)&clientAddr, &AddrLen);
		if (recvByte > 0)
		{
			//成功收到消息，回复ACK报文
			if (recvMsg.check() && (recvMsg.SeqNum == initrelseq + 1))
			{
				Message replyMessage;
				replyMessage.SrcPort = ServerPORT;
				replyMessage.DestPort = RouterPORT;
				replyMessage.flag += ACK;
				replyMessage.SeqNum=initrelseq++;
				replyMessage.AckNum = recvMsg.SeqNum;
				replyMessage.setCheck();
				sendto(serverSocket, (char*)&replyMessage, sizeof(replyMessage), 0, (sockaddr*)&clientAddr, sizeof(SOCKADDR_IN));
				cout << "server收到：seq = " << recvMsg.SeqNum << "的数据报文"<< endl;
				cout << "server发送：seq = "<<replyMessage.SeqNum<<"，ack = " << replyMessage.AckNum << "的ACK报文，检验和"<<replyMessage.checkNum << endl;
				return true;
			}

			//如果seq值不正确，则丢弃报文，返回累计确认的ACK报文（ack=initrelseq-1）
			else if (recvMsg.check() && (recvMsg.SeqNum != initrelseq + 1))
			{
				Message replyMessage;
				replyMessage.SrcPort = ServerPORT;
				replyMessage.DestPort = RouterPORT;
				replyMessage.flag += ACK;
				replyMessage.SeqNum = initrelseq;
				replyMessage.AckNum = initrelseq;
				replyMessage.setCheck();
				sendto(serverSocket, (char*)&replyMessage, sizeof(replyMessage), 0, (sockaddr*)&clientAddr, sizeof(SOCKADDR_IN));
				cout << "[累计确认（错误seq值）] server收到 seq = " << recvMsg.SeqNum << "的数据报文，并发送 ack = " << replyMessage.AckNum << " 的累计确认的ACK报文" << endl;
			}
		}
		else if (recvByte == 0)
		{
			return false;
		}
	}
	return true;
}

//实现文件接收
void recvFileFormClient(SOCKET serverSocket, SOCKADDR_IN clientAddr)
{
	int AddrLen = sizeof(clientAddr);
	//接收文件名和文件大小
	Message nameMessage;
	unsigned int fileSize;
	char fileName[40] = {0};
	while (1)
	{
		int recvByte = recvfrom(serverSocket, (char*)&nameMessage, sizeof(nameMessage), 0, (sockaddr*)&clientAddr, &AddrLen);
		if (recvByte > 0)
		{
			//如果成功收到装载文件名和文件大小的消息，则进行一下输出并回复对应的ACK报文
			//这里我设计的是基于rdt3.0协议，将ack值设为发来报文的seq值
			if (nameMessage.check() && (nameMessage.SeqNum == initrelseq + 1) && (nameMessage.flag & SFileName))
			{
				fileSize = nameMessage.size;
				for (int i = 0; nameMessage.data[i]; i++)
					fileName[i] = nameMessage.data[i];
				cout << "\n接收文件名：" << fileName << "，文件大小：" << fileSize << endl<<endl;
				
				Message replyMessage;
				replyMessage.SrcPort = ServerPORT;
				replyMessage.DestPort = RouterPORT;
				replyMessage.flag += ACK;
				replyMessage.SeqNum=initrelseq++;
				replyMessage.AckNum = nameMessage.SeqNum;
				replyMessage.setCheck();
				sendto(serverSocket, (char*)&replyMessage, sizeof(replyMessage), 0, (sockaddr*)&clientAddr, sizeof(SOCKADDR_IN));
				cout << "server收到：seq = " << nameMessage.SeqNum << "的数据报文"<<endl;
				cout << "server发送：seq = "<<replyMessage.SeqNum<<"，ack = " << replyMessage.AckNum << " 的ACK报文，检验和是" <<replyMessage.checkNum<< endl<<"装载文件名和文件大小的报文接收成功，下面开始正式传送数据段"<< endl<< endl;
				break;
			}

			//如果seq值不正确，则丢弃报文，返回累计确认的ACK报文（ack=initrelseq-1）
			else if (nameMessage.check() && (nameMessage.SeqNum != initrelseq + 1) && (nameMessage.flag & SFileName))
			{
				Message replyMessage;
				replyMessage.SrcPort = ServerPORT;
				replyMessage.DestPort = RouterPORT;
				replyMessage.flag += ACK;
				replyMessage.SeqNum=initrelseq+1;
				replyMessage.AckNum = initrelseq;
				replyMessage.setCheck();
				sendto(serverSocket, (char*)&replyMessage, sizeof(replyMessage), 0, (sockaddr*)&clientAddr, sizeof(SOCKADDR_IN));
				cout << "[累计确认（错误seq值）]server收到 seq = " << nameMessage.SeqNum << "的数据报文，并发送 ack = " << replyMessage.AckNum << "的ACK报文" << endl;
			}
		}
	}


	int batchNum = fileSize / MaxMsgSize;//可以装满的报文数量
	int leftNum = fileSize % MaxMsgSize;//剩余数据量大小
	BYTE* fileBuffer = new BYTE[fileSize];

	//满载的数据报文段接收
	for (int i = 0; i < batchNum; i++)
	{
		Message dataMsg;
		if (recvMessage(dataMsg, serverSocket, clientAddr))
		{
			cout << "第" << i+1 << "个满载数据报文接收成功" << endl<< endl;
		}
		else
		{
			cout << "第" << i+1 << "个满载数据报文接收失败" << endl<< endl;
			return;
		}
		//读取数据
		for (int j = 0; j < MaxMsgSize; j++)
		{
			fileBuffer[i * MaxMsgSize + j] = dataMsg.data[j];
		}
	}

	//未满载的数据报文段接收，如果是整除就不接收这个报文了
	if (leftNum > 0)
	{
		Message dataMsg;
		if (recvMessage(dataMsg, serverSocket, clientAddr))
		{
			cout << "未满载的数据报文接收成功" << endl<< endl;
		}
		else
		{
			cout << "未满载的数据报文接收失败" << endl<< endl;
			return;
		}
		//读取数据
		for (int j = 0; j < leftNum; j++)
		{
			fileBuffer[batchNum * MaxMsgSize + j] = dataMsg.data[j];
		}
	}

	//写入文件
	cout << "\n文件传输成功，开始写入文件" << endl;
	FILE* outputfile;
	outputfile = fopen(fileName, "wb");
	if (fileBuffer != 0)
	{
		fwrite(fileBuffer, fileSize, 1, outputfile);
		fclose(outputfile);
	}
	cout << "文件写入成功" << endl<<endl;
	delete[] fileBuffer;//释放内存
}


//实现server的四次挥手
bool fourwayhandwave(SOCKET serverSocket, SOCKADDR_IN clientAddr)
{
	int AddrLen = sizeof(clientAddr);
	Message buffer1;
	Message buffer2;
	Message buffer3;
	Message buffer4;
	while (1)
	{
		//接收第一次挥手的消息
		int recvByte = recvfrom(serverSocket, (char*)&buffer1, sizeof(buffer1), 0, (sockaddr*)&clientAddr, &AddrLen);
		if (recvByte == 0)
		{
			cout << "第一次挥手接收失败，退出" << endl;
			return false;
		}

		else if (recvByte > 0)
		{
			//检查FIN、ACK、检验和
			if (!(buffer1.flag & FIN) || !(buffer1.flag & ACK) || !buffer1.check())
			{
				cout << "第一次挥手接收成功，检查失败" << endl;
				return false;
			}
			cout << "server接收第一次挥手成功" << endl;

			//发送第二次挥手的消息（ACK有效，ack是第一次挥手消息的seq+1,seq值自动向下递增）
			buffer2.SrcPort = ServerPORT;
			buffer2.DestPort = RouterPORT;
			buffer2.SeqNum = initrelseq++;
			buffer2.AckNum = buffer1.SeqNum+1;
			buffer2.flag += ACK;
			buffer2.setCheck();//设置校验和
			int sendByte = sendto(serverSocket, (char*)&buffer2, sizeof(buffer2), 0, (sockaddr*)&clientAddr, AddrLen);
			clock_t buffer2start = clock();
			if (sendByte == 0)
			{
				cout << "server发送第二次挥手失败" << endl;
				return false;
			}
			cout << "server发送第二次挥手："
			<< "源端口: " << buffer2.SrcPort << ", "
			<< "目的端口: " << buffer2.DestPort << ", "
			<< "序列号: " << buffer2.SeqNum << ", "
			<< "确认号: " << (buffer2.flag & ACK ? to_string(buffer2.AckNum) : "N/A") << ", "
			<< "标志位: " << "[SYN: " << (buffer2.flag & SYN ? "SET" : "NOT SET") 
			<< "] [ACK: " << (buffer2.flag & ACK ? "SET" : "NOT SET") 
			<< "] [FIN: " << (buffer2.flag & FIN ? "SET" : "NOT SET")
			<< "] [SFileName: " << (buffer2.flag & SFileName ? "SET" : "NOT SET") <<"], "
			<< "校验和: " << buffer2.checkNum << endl;
			break;
		}
	}

	//server发送第三次挥手的消息（FIN、ACK有效，seq自动向下递增）
	buffer3.SrcPort = ServerPORT;
	buffer3.DestPort = RouterPORT;
	buffer3.flag += FIN;//设置FIN
	buffer3.flag += ACK;//设置ACK
	buffer3.SeqNum = initrelseq++;//设置序号seq
	buffer3.setCheck();//设置校验和
	int sendByte = sendto(serverSocket, (char*)&buffer3, sizeof(buffer3), 0, (sockaddr*)&clientAddr, AddrLen);
	clock_t buffer3start = clock();
	if (sendByte == 0)
	{
		cout << "server发送第三次挥手失败" << endl;
		return false;
	}
	cout << "server发送第三次挥手："
	<< "源端口: " << buffer3.SrcPort << ", "
	<< "目的端口: " << buffer3.DestPort << ", "
	<< "序列号: " << buffer3.SeqNum << ", "
	<< "标志位: " << "[SYN: " << (buffer3.flag & SYN ? "SET" : "NOT SET") 
	<< "] [ACK: " << (buffer3.flag & ACK ? "SET" : "NOT SET") 
	<< "] [FIN: " << (buffer3.flag & FIN ? "SET" : "NOT SET")
	<< "] [SFileName: " << (buffer3.flag & SFileName ? "SET" : "NOT SET") <<"], "
	<< "校验和: " << buffer3.checkNum << endl;
	int resendtimes=0;
	
	//接收第四次挥手的消息
	while (1)
	{
		int recvByte = recvfrom(serverSocket, (char*)&buffer4, sizeof(buffer4), 0, (sockaddr*)&clientAddr, &AddrLen);
		if (recvByte == 0)
		{
			cout << "server接收第四次挥手失败" << endl;
			return false;
		}
		else if (recvByte > 0)
		{
			//成功收到消息，检查校验和、ACK、ack
			if ((buffer4.flag & ACK) && buffer4.check() && (buffer4.AckNum == buffer3.SeqNum+1))
			{
				cout << "server接收第四次挥手成功" << endl;
				break;
			}
			else
			{
				cout << "server接收第四次挥手成功，检查失败" << endl;
				return false;
			}
		}
		//server发送第三次挥手超时，重新发送并重新计时
		if (clock() - buffer3start > MAX_WAIT_TIME)
		{
			cout << "server发送第三次挥手，第"<< ++resendtimes <<"次超时，正在重传......" << endl;
			int sendByte = sendto(serverSocket, (char*)&buffer3, sizeof(buffer3), 0, (sockaddr*)&clientAddr, AddrLen);
			buffer3start = clock();
			if(sendByte>0){
				cout<<"server发送第三次挥手重传成功"<<endl;
				//break;
				continue;
			}
			else{
				cout<<"server发送第三次挥手重传失败"<<endl;
			}			
		}
		if (resendtimes == MAX_SEND_TIMES)
        {
			cout << "server发送第三次挥手超时重传已到最大次数，发送失败" << endl;
			return false;
        }
	}
	cout << "\nserver关闭连接成功！" << endl;
	return true;
}


int main()
{
	//初始化Winsock服务
	WSADATA wsaDataStruct;
	int result = WSAStartup(MAKEWORD(2, 2), &wsaDataStruct);
	if (result != 0) {
		cout << "初始化Winsock服务成功" << endl;
		return -1;
	}
	if (wsaDataStruct.wVersion != MAKEWORD(2, 2)) {
		cout << "不支持所需的Winsock版本" << endl;
		WSACleanup(); 
		return -1;
	}
	cout << "初始化Winsock服务成功" << endl; 

	//创建socket，是UDP套接字，UDP是一种无连接的协议
	SOCKET serverSocket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
	if (serverSocket == INVALID_SOCKET)
	{
		cerr << "创建socket失败" << endl;
		return -1;
	}

	// 设置套接字为非阻塞模式，这是关键的一点
	unsigned long mode = 1;
	if (ioctlsocket(serverSocket, FIONBIO, &mode) != NO_ERROR)
	{
		cerr << "无法设置套接字为非阻塞模式" << endl;
		closesocket(serverSocket); 
		return -1;
	}
	cout << "创建socket成功" << endl;

	//初始化服务器地址
	SOCKADDR_IN serverAddr;
	serverAddr.sin_family = AF_INET;
	serverAddr.sin_addr.S_un.S_addr = inet_addr("127.0.0.1");
	serverAddr.sin_port = htons(ServerPORT); 

	//bind
	int tem = bind(serverSocket, (LPSOCKADDR)&serverAddr, sizeof(serverAddr));
	if (tem == SOCKET_ERROR)
	{
		cout << "bind失败" << endl;
		return -1;
	}
	cout << "Server的bind成功，准备接收" << endl << endl;

	//初始化路由器地址
	SOCKADDR_IN clientAddr;
	clientAddr.sin_family = AF_INET; 
	clientAddr.sin_addr.S_un.S_addr = inet_addr("127.0.0.1");
	clientAddr.sin_port = htons(RouterPORT); //端口号

	//建立连接
	bool isConn = threewayhandshake(serverSocket, clientAddr);
	if (isConn == 0){
		cerr << "server连接失败，退出" << endl;
		return -1;
	}
	//接收文件
	recvFileFormClient(serverSocket, clientAddr);

	//关闭连接
	cout << "server将断开连接" << endl;
	bool breaked = fourwayhandwave(serverSocket, clientAddr);
	if (!breaked) {
		cerr << "server断开连接失败，退出" << endl;
		return -1;
	}
	closesocket(serverSocket);
	WSACleanup();
	system("pause");
	return 0;
}

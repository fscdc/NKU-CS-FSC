#include <WinSock2.h>
#include <windows.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string>
#include <iostream>
#include <process.h>
#include <conio.h>
#include <limits>

# define PORT 2023
# define IP "127.0.0.1"
using namespace std;

//用time_t表示时间是从1970年1月1日0时0分0秒到此时的秒数，其是一个长整型数。str是存格式化后的时间字符串的
time_t t;
char str[26];

char username[10] = { 0 };

//接收线程
DWORD WINAPI rdeal(void* data)
{
	char bufferget[128] = { 0 };
	while (true)//一直等待接收
	{
		if (recv(*(SOCKET*)data, bufferget, sizeof(bufferget), 0) == SOCKET_ERROR){
			break;
		}
		if (strlen(bufferget) != 0)
		{
			// 检查服务器是否发送关闭信号
			if (strcmp(bufferget, "龙神服务器端已关闭") == 0) 
			{
				cout << "龙神服务器已关闭，三秒后该界面自动退出" << endl;
				closesocket(*(SOCKET*)data);
				break;
			}
			//'\b'光标迁移，功能是清除上一行输出的等待用户输入信息的字符串，例如：(2023-10-17 20:24:03)  [fsc] :
			for (int i = 0; i <= strlen(username) + 40; i++){
				cout << "\b";
			}
			// 打印时间以及接收到的消息
			time(&t);
			strftime(str, 20, "%Y-%m-%d %X", localtime(&t));
			cout << '(' << str << ")    " << bufferget << endl;
			//刚才把输出等待用户输入的字符串给退回了，这里需要再把这个字符串打印出来
			cout << '(' << str << ")  ["<< username << "] : ";
		}
	}
	Sleep(3000);
	exit(1);
	return 0;
}

int main()
{
	WSADATA wd = { 0 };//存放套接字信息
	SOCKET ClientSocket = INVALID_SOCKET;//客户端套接字

	//用于初始化套接字，请求是2.2winsock版本，返回非零值表示初始化失败，下文代码包含初始化错误处理
	if (WSAStartup(MAKEWORD(2, 2), &wd))
	{
		char errMsg[512];
        FormatMessageA(
            FORMAT_MESSAGE_FROM_SYSTEM | FORMAT_MESSAGE_IGNORE_INSERTS,
            NULL,
            WSAGetLastError(),
            MAKELANGID(LANG_NEUTRAL, SUBLANG_DEFAULT),
            errMsg,
            sizeof(errMsg),
            NULL
        );
		cout << "[龙神] WSAStartup创建失败，报错信息：" <<errMsg<< endl;
		return -1;
	}

	/*根据实验要求，这里我创建了IP地址类型为AF_INET（IPV-4协议），
	服务类型为流式(SOCK_STREAM)，使用TCP协议的套接字*/
	ClientSocket = socket(AF_INET, SOCK_STREAM, 0);
	//socket函数的错误处理	
	if (ClientSocket == INVALID_SOCKET)
	{
		char errMsg[512];
        FormatMessageA(
            FORMAT_MESSAGE_FROM_SYSTEM | FORMAT_MESSAGE_IGNORE_INSERTS,
            NULL,
            WSAGetLastError(),
            MAKELANGID(LANG_NEUTRAL, SUBLANG_DEFAULT),
            errMsg,
            sizeof(errMsg),
            NULL
        );
		cout << "[龙神] Socket创建错误，报错信息：" <<errMsg<< endl;
		return -1;
	}

	/*初始化并设置服务器地址，并设定监听端口，使用IPv4地址，这里地址是我设置好的IP地址。*/
	SOCKADDR_IN saddr = { 0 };      
	USHORT port = PORT;           
	saddr.sin_family = AF_INET;
	saddr.sin_port = htons(port);
	saddr.sin_addr.S_un.S_addr = inet_addr(IP);

	//连接服务器，包含报错信息
	if (SOCKET_ERROR == connect(ClientSocket, (SOCKADDR*)&saddr, sizeof(saddr)))
	{
		char errMsg[512];
        FormatMessageA(
            FORMAT_MESSAGE_FROM_SYSTEM | FORMAT_MESSAGE_IGNORE_INSERTS,
            NULL,
            WSAGetLastError(),
            MAKELANGID(LANG_NEUTRAL, SUBLANG_DEFAULT),
            errMsg,
            sizeof(errMsg),
            NULL
        );
		cout << "[龙神] Connect连接错误，报错信息：" <<errMsg<< endl;
		closesocket(ClientSocket);
		WSACleanup();
		return -1;
	}

	cout << "[龙神] 连接龙神服务器成功!，服务器端地址信息为：" << endl;
	cout << "[龙神] IP ：" << inet_ntoa(saddr.sin_addr) << "     " << "端口号 ：" << htons(saddr.sin_port) << endl;
	cout << "[龙神] 成功进入龙神聊天室，请说出您的称号（您的称号不应该是all）: ";

	// 发送名字
	string name;
	cin>>name;
	while (name.length() > 9) {
        cout << "输入用户名非法，请重新输入：";
		cin>>name;
    }
	strcpy(username, name.c_str());
	send(ClientSocket, username, sizeof(username), 0);//发送用户名到服务器
	
	cout << "[龙神] 如果您想退出，请输入 quit " << endl;
	cout << "=========================================================" << endl;

	// 创建接收线程
	HANDLE recvthread = CreateThread(NULL, 0, (LPTHREAD_START_ROUTINE)rdeal, &ClientSocket, 0, 0);

	char bufferSend[128] = { 0 };
	bool start = false;
	while (true)
	{
		if (start){
			//输出
			time(&t);
			strftime(str, 20, "%Y-%m-%d %X", localtime(&t));
			cout << "(" << str << ")  "<< "[" << username << "] : ";
		}
		start = true;

		// 用户输入发送消息
		cin.getline(bufferSend, 128);

		if (cin.fail()) // 检查是否因为输入超过限制
		{
			cin.clear(); // 清除错误标志
			cin.ignore(numeric_limits<streamsize>::max(), '\n'); // 丢弃输入流中的剩余字符
			cout << "输入超限，请重新输入" << endl;
			continue;
		}

		//如果用户输入quit准备退出
		if (strcmp(bufferSend, "quit") == 0)
		{
			cout << "您已离开聊天室" << endl;
			send(ClientSocket, bufferSend, sizeof(bufferSend), 0);
			break;
		}
		send(ClientSocket, bufferSend, sizeof(bufferSend), 0);
	}
	closesocket(ClientSocket);
	CloseHandle(recvthread);
	WSACleanup();
	system("pause");
	return 0;
}
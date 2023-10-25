#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string>
#include <iostream>
#include <WinSock2.h>
#include <process.h>
# define PORT 2023
using namespace std;

SOCKET ServerSocket = INVALID_SOCKET;//定义了一个套接字变量 ServerSocket 并初始化它为 INVALID_SOCKET，方便后续检测其状态
SOCKADDR_IN caddr = { 0 };	         //客户端地址
int caddrlen = sizeof(caddr);        //客户端地址长度
//用time_t表示时间是从1970年1月1日0时0分0秒到此时的秒数，其是一个长整型数。str是存格式化后的时间字符串的
time_t t;
char str[26];

//定义客户端信息结构体，依次声明客户端套接字、数据缓冲区、用户名、IP、客户端标志成员、用于标识转发的范围(用于实现特定用户转发功能)
struct Client
{
	SOCKET ClientSocket;    
	char buffer[128];		 
	char username[10];   
	char IP[20];		
	UINT_PTR flag;   
	char targetarea[20];      
} realclient[20];   //创建一个实例，最多同时容纳20个用户同时在线

//在服务器端，每个客户端的服务都由一个单独的线程进行管理，同时这些线程共享一个用户列表
HANDLE HandleR[20] = { NULL };				 //接收消息线程句柄
HANDLE Handle;							 //用于accept的线程句柄

int i = 0; //多次用到，为了方便就声明一下全局变量

DWORD WINAPI resendthread(void* data);

//接收数据线程
DWORD WINAPI acceptthread(void* data)
{
	int flag[20] = { 0 };//标志数组，一一对应客户端，代表其状态
	while (true)//服务器一直等待客户端的连接
	{
		if (realclient[i].flag != 0)   //找到空闲客户端位置
		{
			i++;
			continue;
		}

		/*调用accept函数等待客户端连接，其会阻塞进程，这里通过accept函数创建的新套接字
		不需要使用过bind函数绑定，因为新套接字会自动集成accept函数提供的服务器地址信息*/
		if ((realclient[i].ClientSocket = accept(ServerSocket, (SOCKADDR*)&caddr, &caddrlen)) == INVALID_SOCKET)
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
			cout << "[龙神] Accept错误，报错信息：" <<errMsg<< endl;
			closesocket(ServerSocket);
			WSACleanup();
			return -1;
		}

		//接收用户名并输出，然后记录下用户IP，并使用socket描述符作为一个独特的标识符来标记或区分不同的客户端
		recv(realclient[i].ClientSocket, realclient[i].username, sizeof(realclient[i].username), 0);
		cout << "[龙神] 用户 [" << realclient[i].username << "]" << " 连接成功" << endl;
		memcpy(realclient[i].IP, inet_ntoa(caddr.sin_addr), sizeof(realclient[i].IP));
		realclient[i].flag = realclient[i].ClientSocket;
		i++;

		//遍历其他客户端并创建进程，对于状态改变的客户端，会重新创建接受消息线程
		for (int j = 0; j < i; j++)
		{
			if (realclient[j].flag != flag[j])
			{
				if (HandleR[j]) //句柄有效
					CloseHandle(HandleR[j]);
				HandleR[j] = CreateThread(NULL, 0, (LPTHREAD_START_ROUTINE)resendthread, &realclient[j].flag, 0, 0);
			}
		}
		for (int j = 0; j < i; j++)
			flag[j] = realclient[j].flag;//同步flag，防止线程重复启动
		Sleep(500);
	}
	return 0;
}


//接收并发送数据的线程函数，WINAPI表示这个函数的调用约定是标准调用约定
DWORD WINAPI resendthread(void* data)
{
	bool first = true;
	SOCKET client = INVALID_SOCKET;
	int flag = 0;
	for (int j = 0; j < i; j++) {
		if (*(int*)data == realclient[j].flag)//找到那个接受线程的客户端
		{
			client = realclient[j].ClientSocket;
			flag = j;
		}
	}
	char temp[128] = { 0 };  //声明一个临时字符数组存消息
	string target, content;//消息可以分两段，发送目标用户和内容。
	while (true)
	{
		memset(temp, 0, sizeof(temp));//每次循环会清空temp
		if (recv(client, temp, sizeof(temp), 0) == SOCKET_ERROR){
			continue;
		}
		//获取第一个英文冒号前的内容为发送目标用户，冒号后是信息内容
		string contents = temp;
		target = contents.substr(0, contents.find(':'));
		content = contents.substr(contents.find(':') + 1 == 0 ? contents.length() : contents.find(':') + 1);
		if (content.length() == 0)//这表示contents中无英文冒号，此时target中存了完整的contents
		{
			strcpy(realclient[flag].targetarea, "all");
			strcpy(temp, target.c_str());
		}
		else
		{
			strcpy(realclient[flag].targetarea, target.c_str());
			strcpy(temp, content.c_str());
		}

		memcpy(realclient[flag].buffer, temp, sizeof(realclient[flag].buffer));//把内容存到buffer成员中

		if (strcmp(temp, "quit") == 0)   //这里是为了实现用户可以正常退出聊天室的功能，如果检测到用户发送quit请求，那么直接关闭线程，不打开转发线程
		{
			//依次关闭套接字、线程句柄，并把位置空出留给以后进入的线程使用
			closesocket(realclient[flag].ClientSocket);
			CloseHandle(HandleR[flag]);   
			realclient[flag].ClientSocket = 0;  
			HandleR[flag]=NULL;
			cout << "[龙神] 用户 [" << realclient[flag].username << "] " << "离开龙神聊天室 " << endl;
		}
		else if (first == true)//确保一个用户第一次连接的时候消息不会被转发，因为这次连接是发送用户名
		{
			first = false;
			continue;
		}
		else
		{
			//格式化输出时间，以及用户名和发送的消息内容
			time(&t);
			strftime(str, 20, "%Y-%m-%d %X", localtime(&t));
			cout << '(' << str << ")  [" << realclient[flag].username << "] :" << temp << endl;

			char temp[128] = { 0 };		   
			memcpy(temp, realclient[flag].buffer, sizeof(temp));//复制内容
			sprintf(realclient[flag].buffer, "%s: %s", realclient[flag].username, temp); //把发送信息的用户名添加进转发的信息里
			if (strlen(temp) != 0) //如果数据不为空则转发
			{
				// 向所有用户发送(群发)，即向除自己之外的所有客户端发送信息
				if (strcmp(realclient[flag].targetarea, "all") == 0)
				{
					for (int j = 0; j < i; j++){
						if (j != flag){
							if (send(realclient[j].ClientSocket, realclient[flag].buffer, sizeof(realclient[j].buffer), 0) == SOCKET_ERROR){
								return -1;
							}
						}
					}
				}
				// 向特定用户发送(私聊)
				else{
					for (int j = 0; j < i; j++){
						if (strcmp(realclient[flag].targetarea, realclient[j].username) == 0){
							if (send(realclient[j].ClientSocket, realclient[flag].buffer, sizeof(realclient[j].buffer), 0) == SOCKET_ERROR){
								return -1;	
							}
						}
					}
				}
			}
		}
	}
	return 0;
}





int main()
{
	//初始化WSADATA结构体，用于接收WSAStartup函数详细信息
	WSADATA wd = { 0 };
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
		cout << "[龙神] WSAStartup发生错误，报错信息：" <<errMsg<< endl;
		return -1;
	}

	/*根据实验要求，这里我创建了IP地址类型为AF_INET（IPV-4协议），
	服务类型为流式(SOCK_STREAM)，使用TCP协议的套接字*/
	ServerSocket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
	//socket函数的错误处理
	if (ServerSocket == INVALID_SOCKET)
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
		WSACleanup();
		return -1;
	}
    /*初始化并设置服务器地址，并设定监听端口，使用IPv4地址，值得注意的是
	INADDR_ANY 是一个特殊宏，其值为0.0.0.0，表示服务器将在所有网络接口上进行监听。*/
	SOCKADDR_IN saddr = { 0 };				
	unsigned short port = PORT;					
	saddr.sin_family = AF_INET;
	saddr.sin_port = htons(port);
	saddr.sin_addr.S_un.S_addr = htonl(INADDR_ANY);

	//bind阶段，将服务器套接字与地址端口绑定，下文包括错误处理
	if (SOCKET_ERROR == bind(ServerSocket, (SOCKADDR*)&saddr, sizeof(saddr)))
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
		cout << "[龙神] Bind绑定出现错误，报错信息：" <<errMsg<< endl;
		closesocket(ServerSocket);//这里发生错误需要额外关闭套接字
		WSACleanup();
		return -1;
	}

	//bind阶段完成后进入listen阶段，设置待处理的连接请求队列的最大长度为3，下文包括错误处理
	if (listen(ServerSocket, 3) == SOCKET_ERROR)
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
		cout << "Listen监听出现错误，报错信息：" <<errMsg<< endl;
		closesocket(ServerSocket);//这里发生错误需要额外关闭套接字
		WSACleanup();
		return -1;
	}

	//上述过程均不报错，说明服务器已经准备就绪，创建线程句柄
	cout << "[龙神] 启动!" << endl;
	cout << "[龙神] 温馨提示：如想关闭龙神聊天室服务器，请输入 quit " << endl;
	cout << "=========================================================" << endl;
	Handle = CreateThread(NULL, 0, (LPTHREAD_START_ROUTINE)acceptthread, NULL, 0, 0);
	
	//实现实验要求：服务器可以主动退出，输入quit即可关闭服务器
	char ssignal[8];
	cin.getline(ssignal, 8);
	if (strcmp(ssignal, "quit") == 0)
	{
		cout << "[龙神] 龙神服务器准备关闭" << endl;
		const char* cshutsignal = "龙神服务器端已关闭";
		for (int j = 0; j <= i; j++)
		{
			if (realclient[j].ClientSocket != INVALID_SOCKET){
				//对于每个有效客户端，发送服务器关闭消息后关闭连接
				send(realclient[j].ClientSocket, cshutsignal, strlen(cshutsignal), 0);
				closesocket(realclient[j].ClientSocket);
			}
		}
		CloseHandle(Handle);
		closesocket(ServerSocket);
		WSACleanup();
		cout << "[龙神] 龙神服务器已经关闭" << endl;
	}
	else{
		cout<<"指令无效，自动退出服务器和客户端"<<endl;
	}
}
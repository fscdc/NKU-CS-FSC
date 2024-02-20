#include <iostream>

using namespace std;


#define MAX_WAIT_TIME  3000 //超时时限（单位ms）
#define MAX_SEND_TIMES  10 //最大重传次数
#define MaxFileSize 15000000 //最大文件大小，查看了要测试的文件后确定
#define MaxMsgSize 10000 //最大数据段大小

//设置不同的标志位，用到的包括SYN、ACK、FIN，SFileName表示传输了文件名字
const unsigned short SYN = 0x1;//0001
const unsigned short ACK = 0x2;//0010
const unsigned short FIN = 0x4;//0100
const unsigned short SFileName = 0x8;//1000

//修改编译器默认的数据成员对齐方式，为1字节，确保所有的成员都会紧密排列
#pragma pack(1)
struct Message
{
	//头部（一共28字节）
	//源IP、目的IP
	unsigned int SrcIP, DestIP;//4字节、4字节
	//源端口号、目的端口号
	unsigned short SrcPort, DestPort;//2字节、2字节
	//序号，这个表示相对序列号
	unsigned int SeqNum;//4字节
	//确认号
	unsigned int AckNum;//4字节
	//数据段大小
	unsigned int size;//4字节
	//标志位
	unsigned short flag;//2字节
	//校验和
	unsigned short checkNum;//2字节
	//报文数据段，实验要求一共不能超过15000字节，这里我设定不超过10000字节
	BYTE data[MaxMsgSize];
	//下面是实现的方法
	Message();
	bool check();
	void setCheck();
};


#pragma pack()//恢复到编译器默认的对齐方式
//构造函数，初始化全为0
Message::Message()
{
	SrcIP = 0;
	DestIP = 0;
	//本次实验使用的是本地回环地址（127.0.0.1），所以IP这俩字段没用上
	SeqNum = 0;
	AckNum = 0;
	size = 0;
	flag = 0;
	memset(&data, 0, sizeof(data));
}
/*
验证Message结构体的校验和是否正确。
这里采用的粒度同上是2字节（16位）
该函数通过对整个结构体包括校验和字段进行端进位加法，来验证数据的完整性。
如果在将所有16位加起来之后，计算得到的32位和的低16位全为1，
则说明校验和是正确的，数据在传输或存储过程中未发生变化，返回true。
如果低16位不全为1，则校验和验证失败，返回false。
*/
bool Message::check()
{

	unsigned int sum = 0;
	unsigned short* msgStream = (unsigned short*)this;

	for (int i = 0; i < sizeof(*this) / 2; i++)
	{
		sum += *msgStream++;
		if (sum & 0xFFFF0000)
		{
			sum &= 0xFFFF;
			sum++;
		}
	}
	if ((sum & 0xFFFF) == 0xFFFF)
	{
		return true;
	}
	return false;

}
/*
计算并设置Message结构体的校验和。
这里采用的粒度是2字节（16位）
校验和计算遵循互联网校验和的标准计算方法，通过对结构体中每16位进行端进位加法。
首先将校验和字段清零，然后对结构体的其余部分执行端进位加法。
最后将计算得到的32位和的低16位取反，存储为校验和。
这确保了在传输或存储过程中数据包的完整性可以被接收方验证。
 */
void Message::setCheck()
{
	this->checkNum = 0;
	int sum = 0;
	unsigned short* msgStream = (unsigned short*)this;


	for (int i = 0; i < sizeof(*this) / 2; i++)
	{
		sum += *msgStream++;
		if (sum & 0xFFFF0000)
		{
			sum &= 0xFFFF;
			sum++;
		}
	}
	this->checkNum = ~(sum & 0xFFFF);

}



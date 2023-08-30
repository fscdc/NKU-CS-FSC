/*稳定匹配*/

#include<iostream>
using namespace std;

int findbestwoman(int n, int oneman, bool** date, int** man) {//遍历寻找在某个男人优先表上没求过婚而且排名最高的女人
    for (int i = 0; i < n; i++) {
        int potentialwife = man[oneman][i];
        if (date[oneman][potentialwife] == false) {
            return potentialwife;
        }
        else {
        }

    }
    return -1;
}
bool manisfree(int n, bool* manstate, int& index) {//遍历判断男人是否都处于配对的状态中，如果有单身的男人返回true，否则相反，同时如果存在没配对的男人，将其编号赋给index
    for (int i = 0; i < n; i++) {
        if (manstate[i] == false) {
            index = i;
            return true;
        }
        else {
        }
    }
    return  false;
}

int main() {
    //初始化有n个男人、女人进行配对
    int n;
    cin >> n;
    int** man = new int* [n];
    int** woman = new int* [n];
    for (int i = 0; i < n; i++) {
        man[i] = new int[n];
        woman[i] = new int[n];
    }
    for (int i = 0; i < n; i++) {//正序输入男人的优先表，由于数组下标从0开始所以要每个值减1
        for (int j = 0; j < n; j++) {
            cin >> man[i][j];
            man[i][j]--;
        }
    }
    for (int i = 0; i < n; i++) {//正序输入女生的优先表，但是存入时候进行对男生的优先赋值，对女生来说，所有男生的优先程度被赋值成0-4，数值小优先级更高，便于女生来选择原配还是新求婚者
        for (int j = 0; j < n; j++) {
            int num;
            cin >> num;
            woman[i][num - 1] = j;
        }
    }
    bool* manstate = new bool[n];//true为配对状态
    for (int i = 0; i < n; i++) {
        manstate[i] = false;
    }
    bool* womanstate = new bool[n];
    for (int i = 0; i < n; i++) {
        womanstate[i] = false;
    }
    bool** date = new bool* [n];//date是用于判断i对j是否求过婚，初始化为都没求婚的状态false
    for (int i = 0; i < n; i++) {
        date[i] = new bool[n];
    }
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            date[i][j] = false;
        }
    }
    int* couple = new int[n];//初始化记录男女配对的数组，初始值设置成-1
    for (int i = 0; i < n; i++) {
        couple[i] = -1;
    }
    int index = 0;//从下标为0的初始位置开始GS算法
    while (manisfree(n, manstate, index)) {//当还有单身的男人时进行循环
        /*for (int i = 0; i < n; i++) {//将配对结果进行输出
            cout<<couple[i]+1<<" ";
        }
        cout<<endl;


        cout<<index<<endl;*/
        int i;
        for (i = 0; i < n; i++)
        {
            if (!date[index][i]) {
                break;
            }
                
        }
        if (i >= n)
            break;

        int oneman = index;//由男生发起邀请
        int onewoman = findbestwoman(n, oneman, date, man);//找到oneman优先表的第一个没求婚的女人
        date[oneman][onewoman] = true;//求婚，同时更改date的值
        if (womanstate[onewoman] == false) {//若女人没配对，则这俩人配对
            couple[onewoman] = oneman;
            womanstate[onewoman] = true;
            manstate[oneman] = true;
        }
        else {//若女人配对了
            int otherman = couple[onewoman];//找出与女人配对的男人
            if (woman[onewoman][otherman] < woman[onewoman][oneman]) {//若对于女人来说，新求婚者的优先级没有原配高，则女人继续和原配配对，男人继续求婚优先表的下一个女人

                continue;
            }
            else {//若相反，则新求婚者与女人配对，原配男人状态变为单身
                couple[onewoman] = oneman;
                manstate[oneman] = true;
                manstate[otherman] = false;
            }
        }
    }
    for (int i = 0; i < n; i++) {//将配对结果进行输出
        for (int j = 0; j < n; j++)
            if (couple[j] == i)
            {
                cout << j + 1 << " ";
                break;
            }
        
    }
    return 0;
}


/*拓扑排序*/


#include<iostream>
#include<queue>
using namespace std;
#define maxV 51
class edge{//图的边类，包括与边相连的两个节点，V1是边的起点，V2是边的终点
public:
    int V1;
    int V2;
};
class DAG{//DAG的类，包括顶点数和边数和一个邻接矩阵，和两个函数
public:
    int Vnumber;
    int Enumber;
    int DAGmatrix[maxV][maxV];//由题意矩阵最大规模给出限制
    void CreateDAGmatrix(int n){//初始化邻接矩阵，使值都为0
        Vnumber=n;
        Enumber=0;
        for(int i=0;i<n;i++){
            for(int j=0;j<n;j++){
                DAGmatrix[i][j]=0;
            }
        }
    }
    void Edgeinsert(edge *e){//边的插入，令对应的邻接矩阵值为1
        DAGmatrix[e->V1-1][e->V2-1]=1;
    }
};
DAG *BuildDAG(){//建立DAG图
    DAG *oneDAG=new DAG();
    edge *oneedge=new edge();
    int Vnumber,Enumber;
    cin>>Vnumber>>Enumber;
    oneDAG->CreateDAGmatrix(Vnumber);
    for(int i=1;i<=Enumber;i++){//将输入的边依次插入到该DAG中
        cin>>oneedge->V1>>oneedge->V2;
        oneDAG->Edgeinsert(oneedge);
    }
    return oneDAG;
}

int main(){
    DAG *oneDAG=NULL;
    oneDAG=BuildDAG();//初始化DAG，根据输入建立该DAG
    for(int i=0;i<oneDAG->Vnumber;i++){//如果有边将一个点自己相连则一定不是DAG，圈就是该自连环
            if(oneDAG->DAGmatrix[i][i]==1){
                cout<<"NO"<<endl;
                cout<<int(i+1)<<","<<int(i+1)<<endl;
            }
    }
    int sumresult[maxV];
    for(int i=0;i<oneDAG->Vnumber;i++){//用sumresult数组存储每个节点的入度，若等于0则说明该节点没有输入边
        int sum=0;
        for(int j=0;j<oneDAG->Vnumber;j++){
            sum+=oneDAG->DAGmatrix[j][i];
        }
        sumresult[i]=sum;
    }
    queue<int>resultget;//声明队列用来获取结果
    int result[maxV]={0};//声明数组存储最后拓扑排序的结果
    for(int i=0;i<oneDAG->Vnumber;i++){
        if(sumresult[i]==0){//如果存在没有输入边的节点，将其入队
            resultget.push(i+1);
        }
    }
    int k=0;
    while(!resultget.empty()){//如果队列非空则一直循环
        int QFront=resultget.front();//获取队首
        resultget.pop();//队首出队
        result[k]=QFront;
        k++;
        for(int i=0;i<oneDAG->Vnumber;i++){//遍历和队首相邻的节点，入度减1，如果更新完入度之后，入度为0则进队
            if(oneDAG->DAGmatrix[QFront-1][i]==1){
                sumresult[i]-=1;
                if(sumresult[i]==0){
                    resultget.push(i+1);
                }
            }
        }
        continue;
    }
    int num=0;
    for(int i=0;i<oneDAG->Vnumber;i++){//算一下result数组中不为零元素个数，即为序列的长度
        if(result[i]!=0){
            num+=1;
        }
    }
    if(oneDAG->Vnumber==num){//如果序列长度等于图的顶点数，说明存在拓扑序列
        cout<<"YES"<<endl;
        for(int i=0;i<num-1;i++){//输出拓扑序列
            cout<<result[i]<<",";
        }
        cout<<result[num-1];
    }
    
    else{//否则则无法形成拓扑序列
        cout<<"NO"<<endl;
        int start=1;
        int total=0;
        for(int j=0;j<oneDAG->Vnumber;j++){
            total+=oneDAG->DAGmatrix[start-1][j];
        }
        for(int i=0;i<num;i++){//判断start是否符合作为寻找圈的起始节点的要求
            if(total==0||result[i]==start){
                start+=1;
            }
        }
        queue<int>resultadd;//声明寻找圈过程所用到的队列
        resultadd.push(start);//起始节点入队
        int result2[maxV]={0};//声明存圈的数组
        
        int m=0;
        bool exist=true;
        int l=0;
        while(exist){//圈没出现之前一直循环
            int numadd=0;
            int QFrontadd=resultadd.front();//获取队首
            resultadd.pop();//队首出队
            result2[m]=QFrontadd;
            m++;
            for(int i=0;i<oneDAG->Vnumber;i++){//遍历以队首为相邻边的终点节点，将符合要求的第一个节点进队
                if(oneDAG->DAGmatrix[i][QFrontadd-1]==1){
                        resultadd.push(i+1);
                    break;
                }
            }
            for(int i=0;i<oneDAG->Vnumber;i++){//算一下result2数组中不为零元素个数，即为序列的长度
                if(result2[i]!=0){
                    numadd+=1;
                }
            }
            for(l=0;l<numadd-1;l++){//如果新插入圈数组的有和之前的值重复的，说明圈被找到了
                if(result2[l]==result2[numadd-1]){
                    exist=false;
                    break;
                }
            }
        }
        int numaddd=0;
        for(int i=0;i<oneDAG->Vnumber;i++){//算一下result2数组中不为零元素个数，即为序列的长度
            if(result2[i]!=0){
                numaddd+=1;
            }
        }
        for(int i=l;i<numaddd-1;i++){
            cout<<result2[i]<<",";
        }
        cout<<result2[numaddd-1];
    }
    return 0;
}


/*最小生成树*/

#include<iostream>
using namespace std;
#define maxV 51
class edge{//图的边类，包括与边相连的两个节点，V1是边的起点，V2是边的终点，p是边的权值
public:
    int V1;
    int V2;
    int p;

};
class G{//G的类，包括顶点数和边数和一个邻接矩阵，和两个函数
public:
    int Vnumber;
    int Enumber;
    int Gmatrix[maxV][maxV];//由题意矩阵最大规模给出限制
    void CreateGmatrix(int n){//初始化邻接矩阵，使值都为100，因为测试数据给定权值小于100，所以其他不存在的边只需设置成100就可以保证不被选择到
        Vnumber=n;
        Enumber=0;
        for(int i=0;i<n;i++){
            for(int j=0;j<n;j++){
                Gmatrix[i][j]=100;
            }
        }
    }
    void Edgeinsert(edge *e){//边的插入，令对应的邻接矩阵值为相应权值,无向图需要将两个位置都置为权值
        Gmatrix[e->V1-1][e->V2-1]=e->p;
        Gmatrix[e->V2-1][e->V1-1]=e->p;
    }
};
G *BuildG(){//建立G图
    G *oneG=new G();
    edge *oneedge=new edge();
    int Vnumber,Enumber;
    cin>>Vnumber>>Enumber;
    oneG->CreateGmatrix(Vnumber);
    for(int i=1;i<=Enumber;i++){//将输入的边依次插入到该G中
        cin>>oneedge->V1>>oneedge->V2>>oneedge->p;
        oneG->Edgeinsert(oneedge);
    }
    return oneG;
}
int main(){
    G *oneG=NULL;
    oneG=BuildG();//初始化G，根据输入建立该G
    int cost=0;//记录最小生成树的权值
    int CV[maxV];//标记选取prim算法所选取的节点,没选的对应是0，选取过的设置成1
    for(int i=0;i<oneG->Vnumber;i++){
        CV[i]=0;
    }
    CV[0]=1;//从顶点1开始选取
    int SV[maxV]={0};//按数组下标顺序存选取的顶点
    SV[0]=1;//从1号顶点开始
    int sum=0;
    while(sum<oneG->Vnumber){
         sum++;
         int V=0;
         int minp=100;//每次选取的符合条件的最小权边
         for(int k=0;k<sum;k++){
             for(int i=0;i<oneG->Vnumber;i++){
                 if(oneG->Gmatrix[SV[k]-1][i]<minp && CV[i]!=1){
                    minp=oneG->Gmatrix[SV[k]-1][i];
                    V=i+1;
                 }
             }
         }
         cost+=minp;
         CV[V-1]=1;
         SV[sum]=V;
    }
    int cost2=cost-100;
    cout<<cost2;
    return 0;
}

/*哈夫曼编码*/



#include <iostream>
#include <algorithm>
#include <vector>
#include <queue>
#include<iomanip>
#define Max 10000;
using namespace std;
typedef struct HTree
{
    int weight;  // 字符出现的频数，即为权重
    int key;//字符，这里由于默认成1-n，所以类型定义成int型
    HTree *left;//左右节点
    HTree *right;
    HTree(int w = 0, int k = '\0', HTree *l = nullptr, HTree *r = nullptr):
        weight(w), key(k), left(l), right(r) {};//对属性进行缩写，构造函数初始化
}HTree, *pHTree;
 
struct compare//仿函数进行比较
{
    bool operator() (HTree *a, HTree *b)
    {
        return a->weight > b->weight;  //用升序排列
    }
};
priority_queue<pHTree, vector<pHTree>, compare> Pqueue;  //优先队列
void getCodesum(HTree *root, string st,int A[],int B[])//获得每个字符的huffman编码的长度与频度乘积和每个字符的频度
{
    if(root==nullptr){
        return;
    }
    if (root->left)//左0
    {
        st += '0';
    }
    getCodesum(root->left, st,A,B);
    if (!root->left && !root->right)  // 叶子结点
    {
        /*cout<<root->key<<"的编码是";//能实现对每个字符编码的输出
        for (size_t i = 0; i < st.size(); ++i)
        {
            cout<<st[i];
        }
        cout<<endl;*/
        A[root->key]=st.size()*root->weight;
        B[root->key]=root->weight;
    }
    st.pop_back();  // 迭代完一次退回一个字符
    if (root->right)//右1
    {
        st += '1';
    }
    getCodesum(root->right, st,A,B);
}
int main()
{
        int n;//需要编码的个数
        cin>>n;
        int A[10000]={0};//存每个字符的频度乘编码长度
        int B[10000]={0};//存每个字符的频度
        for (int i = 0; i < n; i++)
        {
            HTree *temp = new HTree;
            int wtemp;
            cin>>wtemp;
            temp->key = i+1;//由于没有输入具体的字符，所以字符这里默认成1-n
            temp->weight= wtemp;//输入每个字符的频数，即为权重
            Pqueue.push(temp);
        }
        //将队列中最小的两个频度组成树，形成新频度放回，直到队列中只有一个频度。
        while (Pqueue.size() > 1)
        {
            HTree *root = new HTree;//根结点
            pHTree rootl, rootr;//左右节点
            rootl = Pqueue.top(); Pqueue.pop();//分别获取优先队列的顶部的前两个来合并
            rootr = Pqueue.top(); Pqueue.pop();
     
            root->weight = rootl->weight + rootr->weight;//更新频度为两个合并频度之和
            root->left = rootl;//两个分别为树的左右节点
            root->right = rootr;
            Pqueue.push(root);//更新的频度入队
        }
        string s = "";
        int sum=0;
        getCodesum(Pqueue.top(),s,A,B);//获取频度与编码长度等一些数据
    for(int j=1;j<=n;j++){//计算频度与编码长度乘积和
        sum+=A[j];
    }
        int weightsum=0;
    for(int j=1;j<=n;j++){//计算频度之和
        weightsum+=B[j];
    }
        cout<<setprecision(2)<<setiosflags(ios::fixed)<<(float)sum/(float)weightsum<<endl;
    return 0;
}



/*最邻近点对*/


#include <iostream>
#include <vector>
#include <algorithm>
#include <cmath>
#include <iomanip>
#include <cfloat>
#define Max 30001
using namespace std;
class spot{//点类
public:
    double x;//x坐标
    double y;//y坐标
    spot(){//默认构造函数
    };
    spot(double x,double y){//带参数的构造函数
        this->x=x;
        this->y=y;
    }
};
double Dis(spot s1,spot s2){//获得两个点的距离的平方
    return (s1.x-s2.x)*(s1.x-s2.x)+(s1.y-s2.y)*(s1.y-s2.y);
}
bool cmpx(spot s1,spot s2){//按x坐标排序时候的排序规则
    return s1.x<s2.x;
}
bool cmpy(spot s1,spot s2){//按y坐标排序时候的排序规则
    return s1.y<s2.y;
}
double getminDis(spot *X,spot *Y,int left,int right){//根据分治思想获得最邻近点对的距离平方
    if(left>=right){//只有一个点的时候返回float型最大值
        return FLT_MAX;
    }
    if(right-left==1){//只有两个点，最邻近点对就是这两个点
        return Dis(X[left],X[right]);
    }
    int xmid=(left+right)/2;//中间分隔线的x坐标
    double d1=getminDis(X,Y,left,xmid);//递归左半部分
    double d2=getminDis(X,Y,xmid+1,right);//递归右半部分
    double d=min(d1,d2);
    vector<spot> strip;//定义包含中间的一条的点
    for(int i=left; i<=right;i++){//中间x坐标小于d的点都加入进来
        if(fabs(X[i].x-X[xmid].x)<d){
            strip.push_back(X[i]);
        }
    }
    sort(strip.begin(),strip.end(),cmpy);//按y坐标排序
    for(int i=0;i<strip.size();i++){//枚举strip中的每个点
        for(int j=i+1;j<strip.size()&&strip[j].y-strip[i].y<d;j++){
            //若找到有y坐标差小于d的则算一下距离
            double dis=Dis(strip[i],strip[j]);
            d=min(d,dis);//若距离更小则更新一下d
        }
    }
    return d;
}
int main(){
    int n;
    cin>>n;//输入点数
    spot *X=new spot[Max];
    spot *Y=new spot[Max];
    for(int i=0;i<n;i++){//输入点的x，y坐标
        double x;
        double y;
        cin>>x>>y;
        X[i]=spot(x,y);
        Y[i]=spot(x,y);
    }
    sort(X,X+n,cmpx);//按x坐标进行排序
    sort(Y,Y+n,cmpy);//按y坐标进行排序
    double min=getminDis(X,Y,0,n-1);
    cout<<setprecision(2)<<fixed<<min;//输出最小距离保持两位小数
    return 0;
}




/*分段最优直线拟合*/



#include <iostream>
#include <vector>
#include <limits>
#include <iomanip>
#include <cmath>

using namespace std;

// 计算误差函数，还可以得到拟合直线
double Error(const vector<double>& x, const vector<double>& y, int left, int right) {
    double sumx = 0;
    double sumy = 0;
    double sumxmuly = 0;
    double sumxsquare =0;//初始化一些中间值
    int n = right - left + 1;
    double Error = 0;
    for (int i = left; i <=right; i++) {//计算一些需要的中间值
        sumx+=x[i];//x坐标求和
        sumy+=y[i];//y坐标求和
        sumxmuly+=x[i]*y[i];//xy求和
        sumxsquare+=x[i]*x[i];//x方求和
    }
    double a;
    double b;
    a=(n*sumxmuly-sumx*sumy)/(n*sumxsquare-sumx*sumx);//根据公式计算最小误差直线的a、b值
    b=(sumy-a*sumx)/n;
    
    for (int i =left; i <=right; i++) {//计算最小误差
        double fity;
        fity=a*x[i]+b;//计算拟合直线上的y值
        Error+=(fity-y[i])*(fity-y[i]);//计算最小误差
    }
    return Error;//返回最小误差值
}

// 根据动态规划算法求解最小罚分Penalty score
double minPS(const vector<double>& x, const vector<double>& y, int n, int C) {
    vector<double> Echart((n + 1) * (n + 1), numeric_limits<double>::max());//定义一个长度为（n+1）平方的动态数组，初始值是一个很大的正数
    for (int i = 0; i < n; i++) {//循环计算出每个e（i，j）
        for (int j = i; j < n; j++) {
            int num=i*(n+1)+j;
            Echart[num] = Error(x,y,i,j);
        }
    }
    vector<double> PS(n + 1, numeric_limits<double>::max());//定义一个PS动态数组存储从第1个点到第i个点的最小罚分，初始值是一个很大的正数，这里长度是n+1
    PS[0] = 0;//没有点的时候罚分是0
    for (int i = 1; i <= n; i++) {//计算每个1到i点集的最小罚分
        for (int j = 0; j < i; j++) {//要去遍历所有前面节点的情况，选择一个最小值存入
            int num2=j*(n+1)+i-1;
            if((PS[j] + Echart[num2] + C)<PS[i]){
            PS[i] = PS[j] + Echart[num2] + C;//根据算法的递推公式计算，用更小值去不断更新
            }
        }
    }
    return PS[n];//返回1点到n点的最小罚分就是我们想要的结果
}

int main() {
    int n, C;//输入点数和预先权重值
    cin>>n>>C;
    vector<double> x(n);
    vector<double> y(n);
    for (int i= 0;i<n; i++) {
        cin>>x[i]>>y[i];
    }
    double min= minPS(x,y, n, C);//计算最小误差
    cout << fixed << setprecision(2) <<min<< endl;//保留两位小数输出
    return 0;
}


/*字符串匹配*/



#include <iostream>
#include <vector>
#include <cmath>
#include <string>
using namespace std;
//算法的主要逻辑还是动态规划，利用递推公式来进行计算，递推公式如下：val(i, j) = min{ val(i-1, j) + k，val(i, j-1) + k，val(i-1, j-1) + dist(ai , bi) }
//为了优化到线性空间需要利用书上说的将数组折叠成2列数组来进行保存结果，并需要不断的更新结果。
int main(){
    string S1;
    string S2;
    cin>>S1;//输入两个字符串
    cin>>S2;
    int k;
    cin>>k;//输入k值
    int len1;
    int len2;
    len1=static_cast<int>(S1.size());
    len2=static_cast<int>(S2.size());
    int better[len1+1][2];//定义用来存储中间结果的二维数组，第一列代表之前的状态，第二列代表现在的状态
    for(int i=0;i<len1+1;i++){//初始化为字符串为空字符串
        better[i][0]=i*k;
    }
    for(int j=1;j<len2+1;j++){
        better[0][1]=better[0][0]+k;//初始化当前第一个为空字符串匹配
        for(int l=1;l<len1+1;l++){
            if(S1[l-1]==S2[j-1]){//如果字符相同
                better[l][1]=better[l-1][0];//当前状态的值等于之前状态的值
            }
            else{
                better[l][1]=min(better[l-1][0]+abs(S1[l-1]-S2[j-1]),min(k+better[l-1][1],k+better[l][0]));//取递归中的最小值
            }
        }
        
        for(int m=0;m<len1+1;m++){//复制第二列到第一列
            better[m][0]=better[m][1];
        }
    }
    cout<<better[len1][1]<<endl;//输出结果
    return 0;
}
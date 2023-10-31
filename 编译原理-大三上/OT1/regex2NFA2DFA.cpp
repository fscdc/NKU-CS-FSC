#include <bits/stdc++.h>
#define col 5
using namespace std;

//init 和 fin：存储NFA的初始和最终状态的整数数组。a 和 b：init 和 fin 的元素数量。
int init[20],fin[20];
int a=0,b=0;
//init_dfa 和 fin_dfa：存储DFA的初始和最终状态的字符串数组。_a 和 _b：init_dfa 和 fin_dfa 的元素数量。
string init_dfa[20],fin_dfa[20];
int _a = 0, _b = 0;

//用.表示连接操作，方便后续操作
string preprocessor(string s){
    char x[5000];
    int l=s.length();
    int j=0;
    x[j]='(';//先插入一个左括号
    j += 1;
    for(int i=0;i<l;i++){
            x[j]=s[i];
            j += 1;
        if(islower(s[i]) && islower(s[i+1])){
            x[j]='.';
            j += 1;
        }else if(s[i]==')'&&s[i+1]=='('){
            x[j]='.';
            j += 1;
        }else if(islower(s[i])&&s[i+1]=='('){
            x[j]='.';
            j += 1;
        }else if(s[i]==')'&&islower(s[i+1])){
            x[j]='.';
            j += 1;
        }else if(s[i]=='*'&&(s[i+1]=='(' || (islower(s[i+1])))){
            x[j]='.';
            j += 1;
        }
    }
    x[j] = ')';
    j += 1;
    string p;
    for(int i=0;i<j;i++)
       p += x[i];
    return p;
}
//中缀转后缀，遇到字母存入，遇到左括号入栈，遇到右括号则将出栈并存入直到遇到第一个左括号
string postfix(string s){
    int l=s.length();
    char a[5000];
    stack <char> ch;
    int j=0;
    for(int i=0;i<l;i++){
         char x = s[i];
         switch(x){
            case 'a':   a[j]='a';
                        j += 1;
                        break;
            case 'b':   a[j]='b';
                        j+=1;
                        break;
            case '(':   ch.push('(');
                        break;
            case ')':   while(!ch.empty()){
                            if(ch.top()=='('){
                                ch.pop();
                                break;
                            }else{
                                a[j]=ch.top();
                                    ch.pop();
                                    j += 1;
                            }
                        }
                        break;
            //基于运算符的优先级来决定何时从堆栈中弹出操作符并将它们添加到输出数组
            case '.':   if(ch.empty()){
                            ch.push('.');
                        }else {
                            char temp = ch.top();
                            if(temp=='(')
                                ch.push('.');
                            else if(temp=='*'){
                                a[j]=ch.top();
                                ch.pop();
                                j += 1;
                                if(ch.top()== '.'){
                                    a[j] = '.';
                                    j += 1;
                                }else{
                                    ch.push('.');
                                }
                            }else if(temp=='.'){
                                a[j]=ch.top();
                                ch.pop();
                                j += 1;
                                ch.push('.');
                        }else if(temp == '|'){
                               ch.push('.');
                        }
                    }
                        break;
            case '|':   if(ch.empty()){
                            ch.push('|');
                        }else{
                            char temp = ch.top();
                            if(temp == '(')
                                ch.push('|');
                            else if(temp == '*'){
                                a[j] = ch.top();
                                ch.pop();
                                j += 1;
                                ch.push('|');
                            }else if(temp == '.'){
                                a[j] = ch.top();
                                j += 1;
                                ch.pop();
                                ch.push('|');
                            }
                        }
                            break;
            case '*':   if(ch.empty()){
                            ch.push('*');
                        }else{
                            char temp = ch.top();
                            if(temp == '(' || temp == '.' || temp == '|' )
                                ch.push('*');
                            else{
                                a[j] = ch.top();
                                ch.pop();
                                j += 1;
                                ch.push('*');
                            }
                        }
                        break;
         }
    }
    string p;
    for(int i=0;i<j;i++){
        p += a[i];
    }
    return p;
}
//后缀转NFA
int regex2nfa(string s,int nfa_table[][col]){
    int l = s.length();
    int states = 1;
    int m,n,j,counter;
    for(int i=0;i<l;i++){
        char x = s[i];
        switch(x){
            case 'a': nfa_table[states][0] = states;
                        init[a] = states;
                         a += 1;
                            states += 1;
                      nfa_table[states-1][1] = states;
                        fin[b] = states;
                        b += 1;
                      nfa_table[states][0] = states;
                            states +=1;
                      break;
            case 'b': nfa_table[states][0] = states;
                        init[a] = states;
                         a += 1;
                            states += 1;
                      nfa_table[states-1][2] = states;
                          fin[b] = states;
                          b += 1;
                      nfa_table[states][0] = states;
                            states +=1;
                      break;
            case '.': m = fin[b-2];
                      n = init[a-1];
                      nfa_table[m][3]=n;
                      //删除fin数组中索引为x的元素，并将后面的元素向前移动一个位置。
                      for(int i=b-2; i<b-1; i++)
                        fin[i] = fin[i+1];
                      b -= 1;
                      a -= 1;         
                      break;
            case '|': for(j=a-1,counter=0;counter<2;counter++){
                        m = init[j-counter];
                        nfa_table[states][3+counter]=m;
                      }
                      a=a-2;
                      init[a]=states;
                      a += 1;
                      nfa_table[states][0] = states;
                      states += 1;
                      for(j=b-1,counter=0;counter<2;counter++){
                        m = fin[j-counter];
                        nfa_table[m][3]=states;
                      }
                      b=b-2;
                      fin[b]=states;
                      b += 1;
                      nfa_table[states][0] = states;
                      states += 1;
                      break;
            case '*': m = init[a-1];
                      nfa_table[states][3] = m;
                      nfa_table[states][0] = states;
                      init[a-1] = states;

                      states += 1;
                      n = fin[b-1];
                      nfa_table[n][3]=m;
                      nfa_table[n][4]=states;
                      nfa_table[states-1][4]=states;
                      fin[b-1]=states;
                      nfa_table[states][0]=states;
                      states += 1;
                        break;
        }
    }
  return states;
}
//打印NFA的状态转换表，其中-1表示状态不变
void print_nfa_table(int nfa_table[][col],int states){
    cout<<endl;
    for(int i=0;i<60;i++){
        cout<<"*";
    }
    cout<<endl;
    cout<<setw(50)<<"TRANSITION TABLE FOR NFA(e for enpty str)"<<endl;
    cout<<setw(10)<<"States"<<setw(10)<<"a"<<setw(10)<<"b"<<setw(10)<<"e"<<setw(10)<<"e"<<endl;
    for(int i=0;i<60;i++)
        cout<<"-";
    cout<<endl;
    for(int i=1;i<states;i++){
        for(int j=0;j<col;j++){
            cout<<setw(10)<<nfa_table[i][j];
        }
        cout<<endl;
    }
    for(int i=0;i<60;i++)
        cout<<"*";
    cout<<endl;
    cout<<"initial state: ";
    for(int i=0;i<a;i++)
        cout<<init[i]<<" ";
    cout<<endl;
    cout<<"final state: ";
    for(int i=0;i<b;i++)
        cout<<fin[i]<<" ";
}
//打印DFA的状态转换表，其中-1表示状态不变
void print_dfa_table(string dfa_tab[][3],int state){
    cout<<endl<<endl;
    for(int i=0;i<60;i++)
        cout<<"*";
    cout<<endl;
    cout<<setw(35)<<"TRANSITION TABLE FOR DFA"<<endl;
    cout<<setw(10)<<"States"<<setw(10)<<"a"<<setw(10)<<"b"<<endl;
    for(int i=0;i<60;i++)
        cout<<"-";
    cout<<endl;
    for(int i=0;i<state;i++){
        for(int j=0;j<3;j++){
            cout<<setw(10)<<dfa_tab[i][j];
        }
        cout<<endl;
    }
    for(int i=0;i<60;i++)
        cout<<"*";
    cout<<endl;
    cout<<"initial state: ";
    for(int i=0;i<_a;i++)
        cout<<init_dfa[i]<<" ";
    cout<<endl<<"final state: ";
    for(int i=0;i<_b;i++)
        cout<<fin_dfa[i]<<" ";
    cout<<endl<<endl<<endl;
}

//计算闭包函数，用于子集构造法
vector <int> eclosure(int nfa_table[][col], int x){
    stack <int> s;
    map <int, int> m;
    vector <int> v;
    int y;

    s.push(x);
    m[x] = 1;

    while(!s.empty()){
        y = s.top();
            s.pop();
        if(nfa_table[y][3] == -1)
            continue;
        else{
            s.push(nfa_table[y][3]);
            m[nfa_table[y][3]] = 1;

            if(nfa_table[y][4] == -1)
                continue;
            else{
                s.push(nfa_table[y][4]);
                m[nfa_table[y][4]] == -1;
            }
        }
    }
    map <int, int> ::iterator itr;
    itr = m.begin();

    while(itr != m.end()){
        v.push_back(itr->first);
        itr++;
    }
    return v;
}
//该函数检查给定的状态集合是否包含NFA的初始状态。如果是，它将新的DFA状态名添加到init_dfa数组，并递增计数器_a。
void check_init(vector <int> v, string s){
    for(int i=0;i<v.size();i++){
        if(v[i] == init[0]){
            init_dfa[_a] = s;
            _a += 1;
        }
    }
}
//此函数的工作方式与check_init函数相似，但是是检查给定的状态集合是否包含NFA的最终状态。
void check_fin(vector <int> v, string s){
    for(int i=0;i<v.size();i++){
        if(v[i] == fin[0]){
            fin_dfa[_b] = s;
            _b += 1;
        }
    }
}



//子集构造法进行从NFA到DFA的转换
int nfa2dfa(int nfa_table[][col],int states,string dfa_tab[][3]){
    bool flag[states];
    memset(flag,true,sizeof(flag));

    int state = 0,j = 0;
    map <vector<int>,string> map_state;
    vector <int> v,v1,v2,v3,v4;

    v = eclosure(nfa_table,init[0]);
    flag[init[a]] = false;

    map_state[v] = "q" + std::to_string(j++);
    check_init(v,map_state[v]);
    check_fin(v,map_state[v]);

    stack < vector<int> > st;
    st.push(v);
    
    int counter = 0;
    while(true){

       while(!st.empty()){
        vector <int> v ;
        v  = st.top();
             st.pop();
        counter += 1;
        dfa_tab[state][0] = map_state[v];      

        for(int i=0;i<v.size();i++){
            flag[v[i]] = false;
            int temp = nfa_table[v[i]][1];    
            int temp1 = nfa_table[v[i]][2];  
            if(temp>=0)
                v1.push_back(temp);
            if(temp1>=0)
                v3.push_back(temp1);
        }

        map <int,int> map_temp,map_temp1;  
        map <int,int> ::iterator it;

        for(int i=0;i<v1.size();i++){
            v2 = eclosure(nfa_table,v1[i]);
            for(int j=0;j<v2.size();j++){
                map_temp[v2[j]] = 1;
            }
            v2.clear();
        }

        for(int i=0;i<v3.size();i++){
            v4 = eclosure(nfa_table,v3[i]);
            for(int j=0;j<v4.size();j++){
                map_temp1[v4[j]] = 1;
            }
            v4.clear();
        }


        for(it = map_temp.begin(); it != map_temp.end(); it++){
            v2.push_back(it->first);
            flag[it->first] = false;
        }

        for(it = map_temp1.begin(); it != map_temp1.end(); it++){
            v4.push_back(it->first);
            flag[it->first] = false;
        }

        if(v2.empty()){
            dfa_tab[state][1] = "-1";
        } else {
            string t = map_state[v2];
            char flag1 = t[0];
            if( flag1 == 'q'){
                dfa_tab[state][1] = map_state[v2];  
            } else {
                dfa_tab[state][1] = "q" + std::to_string(j++);
                map_state[v2] = dfa_tab[state][1];
                check_init(v2,map_state[v2]);
                check_fin(v2,map_state[v2]);
                st.push(v2);               
            }
        }

        if(v4.empty()){
            dfa_tab[state][2] = "-1";
        } else {
            string t = map_state[v4];
            char flag1 = t[0];
            if( flag1 == 'q'){
                dfa_tab[state][2] = map_state[v4];
            } else {
                dfa_tab[state][2] = "q" + std::to_string(j++);
                map_state[v4] = dfa_tab[state][2];
                check_init(v4,map_state[v4]);
                check_fin(v4,map_state[v4]);
                st.push(v4);
            }
        }
        v1.clear();
        v2.clear();
        v3.clear();
        v4.clear();
       state += 1;
    }

        int k = 1;
        for(k=1;k<states;k++){
            if(flag[k]){
                v = eclosure(nfa_table,k);
                map_state[v] = "q" + std::to_string(j++);
                check_init(v,map_state[v]);
                check_fin(v,map_state[v]);
                cout<<endl<<map_state[v]<<" represents :- ";
                for(int i=0;i<v.size();i++)
                    cout<<v[i]<<" ";
                cout<<endl;
                st.push(v);
                break;
            }
        }

        if(k == states)
                break;
    }
    return state;
}

int minimizedfa(string dfa[][3], int stateCount, string minimizedDFA[][3]) {
    map<string, map<string, string>> transitions;
    map<string, int> toPartition;
    vector<set<string>> partitions;

    for (int i = 0; i < stateCount; ++i) {
        transitions[dfa[i][0]]["a"] = dfa[i][1];
        transitions[dfa[i][0]]["b"] = dfa[i][2];
    }

    // Initial partition
    set<string> finalStates(fin_dfa, fin_dfa + _b);
    partitions.push_back(set<string>());  // 非终结
    partitions.push_back(set<string>());  // 终结
    for (int i = 0; i < stateCount; ++i) {
        if (finalStates.find(dfa[i][0]) != finalStates.end()) {
            partitions[1].insert(dfa[i][0]);
        } else {
            partitions[0].insert(dfa[i][0]);
        }
    }

    partitions.push_back(set<string>());

    partitions[2].insert("-1");  //死状态

    for (auto &state : partitions[0]) {
        toPartition[state] = 0;
    }
    for (auto &state : partitions[1]) {
        toPartition[state] = 1;
    }
    toPartition["-1"] = -1; 

    bool changed = true;
    while (changed) {
        changed = false;
        vector<set<string>> newPartitions;

        for (auto &partition : partitions) {
            map<pair<int, int>, set<string>> signatureToStates;
            for (auto &state : partition) {
                int aPartition = state == "-1" ? -1 : toPartition[transitions[state]["a"]];
                int bPartition = state == "-1" ? -1 : toPartition[transitions[state]["b"]];
                signatureToStates[make_pair(aPartition, bPartition)].insert(state);
            }

            for (auto &entry : signatureToStates) {
                if (entry.second.size() < partition.size()) {
                    changed = true;
                }
                newPartitions.push_back(entry.second);
            }
        }

        partitions = newPartitions;
        toPartition.clear();
        int index = 0;
        for (auto &partition : partitions) {
            for (auto &state : partition) {
                toPartition[state] = index;
            }
            ++index;
        }
    }
    int index = 0;
    for (auto &partition : partitions) {
        string representative = *partition.begin();
        // 忽略"-1"代表状态的分区
        if (representative == "-1") {
            continue;
        }
        minimizedDFA[index][0] = "q" + to_string(index);  // New state name
        minimizedDFA[index][1] = transitions[representative]["a"] == "-1" ? "-1" : "q" + to_string(toPartition[transitions[representative]["a"]]);
        minimizedDFA[index][2] = transitions[representative]["b"] == "-1" ? "-1" : "q" + to_string(toPartition[transitions[representative]["b"]]);
        ++index;
    }

    _a = 0;

    string originalInitialState = init_dfa[0];

    // 如果某个分区包含原始的初始状态，则该分区代表新的初始状态
    for (auto &partition : partitions) {
        if (partition.find(originalInitialState) != partition.end()) {
            init_dfa[_a++] = "q" + to_string(toPartition[*partition.begin()]);
            break;
        }
    }

    int originalFinalStateCount = _b;
    string copy_fin_dfa[20];
    for (int i = 0; i < 20; ++i) {
        copy_fin_dfa[i] = fin_dfa[i];
    }
    _b=0;
    // 检查每个原始的终结状态，看它们在哪个分区，并标记该分区为新的终结状态
    for (int i = 0; i < originalFinalStateCount; ++i) {
        string originalFinalState = copy_fin_dfa[i];
        for (auto &partition : partitions) {
            if (partition.find(originalFinalState) != partition.end()) {
                fin_dfa[_b++] = "q" + to_string(toPartition[*partition.begin()]);
                // 注意这里我不使用break，因为可能有多个原始的终结状态在同一分区
            }
        }
    }

    return index;
}

void testex(string mindfa_tab[][3],string word,int state){
    int len = word.length();
    string temp = init_dfa[0];
    for(int i = 0; i < len; i++){
        if(word[i] != 'a' && word[i] != 'b'){
            temp = "-1";
        }
    }
    int i=0;
    for(i = 0;i < len; i++){
        if(temp == "-1"){
            cout<<endl<<"The str DOES NOT belong to given Regex"<<endl<<endl;
            cout<<"----------------------------------------------"<<endl;
            break;
        } else {
            int _xtate;
            int j=0;

            for(j=0;j<state;j++){      
                if(temp == mindfa_tab[j][0])
                    break;
            }
            if(word[i]=='a'){
                temp = mindfa_tab[j][1];
            } else if(word[i]=='b'){
                temp = mindfa_tab[j][2];
            }
        }
    }
    if(i == len){
            int j=0;
        for(j=0;j<_b;j++){
            if(temp == fin_dfa[j]){
                cout<<endl<<"The str DOES belong to given Regex"<<endl<<endl;
                cout<<"----------------------------------------------"<<endl;
                break;
            }
        }
        if(j==_b){
            cout<<endl<<"The str DOES NOT belong to given Regex"<<endl<<endl;
            cout<<"----------------------------------------------"<<endl;
        }
    }
}



int main(){
    int nfa_table[1000][col];
    memset(nfa_table, -1, sizeof(nfa_table));

    cout<<"EX: abb(a|b)*aab"<<endl<<"Enter a Regex :  ";
    string s;
    cin>>s;

    s=preprocessor(s);
    cout<<"after preprocessed :"<<s<<endl;

    s=postfix(s);
    cout<<"postfix :"<<s<<endl;

    int states = regex2nfa(s,nfa_table);
    //cout<<states<<endl;
    print_nfa_table(nfa_table,states);

    string dfa_tab[states][3];
    int dfa_state = nfa2dfa(nfa_table,states,dfa_tab);
    print_dfa_table(dfa_tab,dfa_state);

    int mindfa_state;
    string mindfa_tab[dfa_state][3];
    mindfa_state= minimizedfa(dfa_tab,dfa_state,mindfa_tab);
    cout<<"After minimize: ";
    print_dfa_table(mindfa_tab,mindfa_state);

    while(true){
        string word;
        cout<<"enter the str to check whether it belongs to given Regex or not."<<endl;
        cout<<"or you can enter q to QUIT"<<endl;
        cout<<"Enter String :";
        cin>>word;
        if(word[0] == 'q')
            break;
        testex(mindfa_tab,word,mindfa_state);
    }
    return 0;
}



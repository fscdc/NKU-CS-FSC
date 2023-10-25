; 函数声明
declare i32 @getint()
declare void @putint(i32)

; 全局变量声明
@a = global i32 5
; 全局常量声明
@pi = constant float 0x400921FB40000000

; 定义函数getarea，输入是半径，返回float类型的圆面积
define float @getarea(float %r) {
entry:
  %0 = load float, float* @pi
  %1 = fmul float %r, %r ;计算半径平方
  %2 = fmul float %1, %0 ;用半径平方乘圆周率算出面积
  ret float %2
}

; 定义main函数，函数无输入，返回值是默认值0
define i32 @main() {
entry:
  %i = alloca i32
  %d = alloca i32
  %r = alloca float
  %arr = alloca [5 x i32] ; 声明一维数组
  %matrix = alloca [2 x [2 x i32]] ; 声明二维数组
  %s = alloca float 
  %sm = alloca i32

  store i32 10, i32* %i
  %0 = call i32 @getint() ; 调用外部函数getint获取输入
  store i32 %0, i32* %d
  %1 = sitofp i32 %0 to float ; 类型转换将%3转换为float类型
  %2 = fdiv float %1, 2.0 ; 除法
  store float %2, float* %r

  ; 获取arr[0]并赋值成10
  %3 = getelementptr [5 x i32], [5 x i32]* %arr, i32 0, i32 0
  store i32 10, i32* %3

  ; 获取matrix[0][0]并赋值成5
  %4 = getelementptr [2 x [2 x i32]], [2 x [2 x i32]]* %matrix, i32 0, i32 0, i32 0
  store i32 5, i32* %4

  ; 调用getarea函数获取面积
  %5 = call float @getarea(float %2)
  store float %5, float* %s

  ; 无条件跳转到loop代码块
  br label %loop

; loop代码块，是循环能否继续的条件判定块
loop:
  %i_val = load i32, i32* %i
  %6 = icmp sgt i32 %i_val, 0
  ; i如果大于0则跳转到loop_body块，如果不满足则跳转到loop_end代码块
  br i1 %6, label %loop_body, label %loop_end
  

; loop_body代码块，是循环主体块
loop_body:
  %s_val = load float, float* %s
  %7 = load i32, i32* %3
  %yb =sitofp i32 %7 to float
  %8 = fadd float %s_val, %yb ; 浮点数加法，实现sysy语句：s = s + arr[0];
  store float %8, float* %s
  %9 = load float, float* %s
  %10 = fcmp ogt float %9, 100.0
  %11 = fcmp olt float %9, 150.0
  %12 = and i1 %10, %11
  ; if判断，如果同时满足两个条件，则跳转到loop_end代码块，否则继续循环。
  br i1 %12, label %loop_end, label %loop


; loop_end代码块，是循环结束块，也就是循环后面顺序执行的代码块
loop_end:
  %s_final = load float, float* %s
  %s_finalint = fptosi float %s_final to i32 ;
  %matrix_val = load i32, i32* %4
  %a_val = load i32, i32* @a
  %13 = add i32 %s_finalint, %matrix_val
  %14 = add i32 %13, %a_val
  ; 调用外部函数putint进行输出
  call void @putint(i32 %14)
  ret i32 0
}

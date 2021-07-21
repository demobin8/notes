> 十年前笔记，贴的地址页面都不存在了。。。

linux进程地址空间结构及缓冲区溢出原理http://www.ibm.com/developerworks/cn/linux/l-overflow/

GCC 中的编译器堆栈保护技术http://www.ibm.com/developerworks/cn/linux/l-cn-gccstack/

下面记录几个我自己容易混淆的要点：

### 1、esp、ebp、eip的区别

eip是指令寄存器，保存cpu下一个要执行的指令的地址。

ebp是栈基址指针，是当前栈的栈底（其实也是上一个栈的栈顶的指针esp）。

esp是栈顶指针会随着push、pop指令自动调整esp的值，始终指向栈顶。


栈底上来就是函数的参数、返回地址和局部变量等，因此一进入函数时保存当前esp到一个ebp中保持不变，后续用ebp来访问参数和局部变量就很清楚，当然ebp不是必须的，虽然esp不停在变，但具体变化编译器是可以计算出来的，因此直接使用esp来访问局部变量和参数也是可行的，gcc有个编译参数 -fomit-frame-pointer 就是干这个事的。


### 2、栈的释放流程

在正常的流程中，函数结束末尾是一个ret指令，ret会弹出ebp给esp，即释放了变量，接着将ret的值弹给eip找到下一条执行的指令，再可能由下一条指令释放参数，而在return-to-libc攻击中，把ret改写成libc函数地址，此时arg 1就成了system的参数arg2就成了ret地址了。

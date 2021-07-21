> py注入的代码已经集成到tool.py了

一般来说我们逆向的大型程序都有自己的log，程序员会在release版本中关掉，开关一般是一个函数的返回值，甚至有直接写在配置文件中，后者好办，如果是前者如何打开呢？

IDA打开程序，打开strings window，找到一个你觉得像是日志的字符串，双击转到汇编窗口，按X看看是不是有很多CALL，如果是一般就找到了日志输出的函数，按X进入调用它的函数，在CALL点往上找判断，最好多比较几个CALL，找到之后进入判断是否开关即可。

然后打开OD，根据计算偏移地址，在OD中找到代码的位置，修改，右键复制到可执行文件，保存即可。

最后运行修改后的程序，并打开procmon，选择我们的程序过滤，然后关掉注册表、网络等输出，监视程序的log输出在哪个文件即可。

如下以风X视频的服务端进行演示：

那如果说要修改的汇编代码比较多，我一般就dll注入一个写输出的小函数，然后在一些地方自己调用，下面是方法：

先实现一个dll

`notepad log.c`
log.c
```
#include "stdio.h"

#include "windows.h"



#pragma comment(lib, "User32.lib")



BOOL APIENTRY DllMain(HMODULE hModule, DWORD ul_reason_for_call, LPVOID lpReserved)

{

switch(ul_reason_for_call)

{

case DLL_PROCESS_ATTACH:

MessageBoxA(NULL, "inject to the process", "success! go on for more interest!", MB_OK);

case DLL_THREAD_ATTACH:

case DLL_THREAD_DETACH:

case DLL_PROCESS_DETACH:

break;

}

return TRUE;

}



int logtofile(char *str)

{

FILE *fd;

fd = fopen("E:\\log.txt", "wt");

fprintf(fd, "%s\n", str);

fclose(fd);

return 1;

}
```
```
cl /c log.c

notepad log.def

LIBRARY log

EXPORTS

logtofile @1

link log.obj /def:log.def /dll
```
注入用py实现
```
import binascii

import ctypes

import sys

import struct

import socket

#####################inject process and kill a process######################

def inject(pid, data, injecttype):

    PAGE_EXECUTE_READWRITE = 0x40

    PROCESS_ALL_ACCESS = (0x000F0000 | 0x00100000 | 0xfff)

    VIRTUAL_MEM = (0x1000 | 0x2000)



    #get process handler

    procHandler = ctypes.windll.kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, int(pid))

    if not procHandler:

        print "couldn't acquire a handle to pid: %s" % pid

        sys.exit(0)



    #allocte mem for shellcode

    argAddr = ctypes.windll.kernel32.VirtualAllocEx(procHandler, 0, len(data), VIRTUAL_MEM, PAGE_EXECUTE_READWRITE)



    #write shellcode

    written = ctypes.c_int(0)

    ctypes.windll.kernel32.WriteProcessMemory(procHandler, argAddr, data, len(data), ctypes.byref(written))



    #create remote process and set point to shellcode

    tid = ctypes.c_ulong(0)

    if not injecttype:

        startAddr = argAddr

    else:

        kernelHandler = ctypes.windll.kernel32.GetModuleHandleA("kernel32.dll")

        startAddr = ctypes.windll.kernel32.GetProcAddress(kernelHandler, "LoadLibraryA")

        injecttype = argAddr

        

    if not ctypes.windll.kernel32.CreateRemoteThread(procHandler, None, 0, startAddr, injecttype, 0, ctypes.byref(tid)):

        print "failed to inject process killer shellcode"

        sys.exit(0)



    print "process inject success"
```
调用方法是inject("pid", "path_to_dll", 1)

最后找到一些要输出的地方，调用打印。

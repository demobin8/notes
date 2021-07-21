> 不知道是不是最佳实践，但那个时候我是这样发布的

首先下载并安装qt-sdk-win-opensource-2010.05。

打开QT工程文件，设置release编译，试运行，将安装路径\2010.05\qt\bin下的提示的对应的.dll文件拷贝到系统盘system32中，或者将可执行文件的路径添加到PATH环境变量中。

打包发布。

install.bat

@echo off  #关闭回显，前面的@表示包括本行

set PATH=E:/QT/TEST;%PATH%

pause

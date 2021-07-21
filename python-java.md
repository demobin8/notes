# Python调用Java的方法
> 这个当年是为了调用hanlp，现在hanlp已经支持python了
### 1. 几种常见的方式
常见的Python调用Java的库包括，JPype、Py4j、javabridge、PyJniUs、Jython等。

综合比较来看，PyJniUs是最便于使用且速度较快的方式。

### 2. PyJniUs安装
依赖：Cython、JDK
[gihub](https://github.com/kivy/pyjnius)clone或者下载解压

`python setup.py install`
### 3. 使用
```
>>> from jnius import autoclass
>>> autoclass('java.lang.System').out.println('Hello world')
Hello world
```

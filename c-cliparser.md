> cliparser和klish让我第一次参与开源社区，gmail上一个老外通过邮件求助相关的问题。。。

clipaser是加速CLI开发的，负责命令行解释的开源项目，可以从SF.NET上免费获取。

http://sourceforge.net/projects/cliparser/

基于CLIPASER开发时，开发者要做的有两步：

### 1：编辑cli文件

格式可以参考test.cli。

注释和C一样用//开头；

空行可以随便添加增加阅读性；

命令行就是在CLI中要输入的指令，用<>符号括起来的是用户输入的变量参数，用{}符号括起来的是可选的变量参数；

若一个cli文件太长，可以用#include "filename"插入；

若是命令分层则用#submode "parent cmd" ..submode cmd.. #endsubmode括起来。

写好cli之后在该目录下运行：./mk_parser.py生成cparser_tree.c和cparser_tree.h两个文件。

在cparser_tree.c中调用了cpaser_cmd_xxx的函数，这些函数就是开发者要实现的。

### 2：实现对应各命令行的程序

模版可以参考test_cli_cmd.c。

函数的返回值是一个cparser_result_t结构体类型的值，它在cparser.h中都有说明。

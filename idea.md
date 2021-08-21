### 插件
- GitToolBox
- IdeaVim
- Alibaba Java Coding Guidelines
- CodeGlance
- Maven Helper
- Lombok
- MyBatisCodeHelper
- MyBatis Log Plugin
- JRebel

### 列编辑
按住alt键，鼠标拖动选择，编辑

### unresolved reference 红标

file -> invalidate caches

### 设置git bash作为terminal

file->settings->tools->terminal
bashrc
```
function git_branch {
branch="`git branch 2>/dev/null | grep "^\*" | sed -e "s/^\*\ //"`"
if [ "${branch}" != "" ];then
    if [ "${branch}" = "(no branch)" ];then
        branch="(`git rev-parse --short HEAD`...)"
    fi
    echo "($branch)"
fi
}
function get_pwd {
# echo `pwd`;
git_url="`git remote get-url origin 2>/dev/null`"
if [ "${git_url}" != "" ];then
         git_url="${git_url##*/}"
fi
project_path=$(basename `pwd`)
username=`git config --global user.name 2>/dev/null`
if [ "${username}" != "" ];then
         username="@${username}:"
fi
echo "${git_url}${username}${project_path}"
}
#export PS1='[$(get_pwd)]\033[01;36m$(git_branch)\[\033[00m\]\$ '
export PS1='[\u@`pwd`]# '
export LANG="zh_CN.UTF-8"
export LC_ALL="zh_CN.UTF-8"
```

### 返回上次查看代码的位置

CTRL + ALT + <- 或者 ->

### 全局搜索

SHIFT 两次

### 指定路径搜索
CTRL + SHIFT + F

### 快速切换编辑的文件
ALT + <- 或者 ->

### 美化代码
CTRL + ALT + L

### 合并多行
CTRL + SHIFT + J

### 快速跳转错误行
SHIFT + F2

### 跳转定义
CTRL + B

### 跳转实现
CTRL + ALT + B

### 跳转项目
CTRL + ALT + ]

### 跳转下一个错误
F2

### 最近编辑的代码
CTRL + E

### 清理没用的package
CTRL + ALT + O

### 小窗查看类
CTRL + SHIFT + I

### 设置新建文件模板
file->setttings->editor->file and code templates->includes->file header
```
/**     * Created by ${USER} on ${DATE}     */
```

### 设置用户名
help->edit custom vm option
```
-Duser.name=demobin
```

### 查看pom.xml依赖树
打开pom.xml，然后快捷键Ctrl+Shift+Alt+U

### properties展示中文
settting->file encoding->勾选Transparent native-to-ascii conversion

### 试用
https://zhile.io/2020/11/18/jetbrains-eval-reset-da33a93d.html

### Serialization
settting->[搜索serialization]->勾选Serializable class without serializationVersionUID

### Vim shortcut
setting->[vim emulation]

### 快捷键ctrl+shift+f失效
搜狗按键

## 版本
对于多个版本共存的系统
sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-4.8 100
sudo update-alternatives --config gcc
### g++ version is lower than expect
```
demobin@kalamodo:~/work/github/warp-ctc/pytorch_binding$ sudo python setup.py install
c++: error: unrecognized command line option ‘-Wdate-time’
c++: error: unrecognized command line option ‘-fstack-protector-strong’
c++: error: unrecognized command line option ‘-Wdate-time’
c++: error: unrecognized command line option ‘-fstack-protector-strong’
error: command 'c++' failed with exit status 1
```
### solution
```
demobin@kalamodo:~/work/github/warp-ctc/pytorch_binding$ sudo update-alternatives --config g++
有 2 个候选项可用于替换 g++ (提供 /usr/bin/g++)。

  选择 路径 优先级 状态
------------------------------------------------------------
* 0 /usr/bin/g++-4.8 100 自动模式
  1 /usr/bin/g++-4.8 100 手动模式
  2 /usr/bin/g++-5 10 手动模式

要维持当前值[*]请按<回车键>，或者键入选择的编号：2
update-alternatives: 使用 /usr/bin/g++-5 来在手动模式中提供 /usr/bin/g++ (g++)
```


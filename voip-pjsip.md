### 1. Error
`/home/demobin/pjproject-2.5.5/pjsip/lib/libpjsua-x86_64-unknown-linux-gnu.a: 无法添加符号: 错误的值`
### 2. Sulotion
```
cd /home/demobin/pjproject-2.5.5/
make clean
export CFLAG=-fPIC
./configure && make dep && make
cd pjsip-apps/src/python
sudo make
sudo python setup.py install
```

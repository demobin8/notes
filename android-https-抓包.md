### 下载安装软件
charles 夜神 xposed justtrustme
### 生成证书
Help->SSL Proxy->Install Charles Root Certificate
### 信任证书
打开IE浏览器—>工具—>Internet选项—>内容—>证书—>把中级证书颁发机构中的charles证书导出来—>再把导出来的证书导入到受信任的根证书颁发机构中。
### 抓ssl报文
Proxy->SSL Proxy Settings 勾选Enable SSL Proxying
### 模拟器设置代理
安装xposed、安装justtrustme，从wifi点进去设置代理

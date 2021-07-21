### 编辑war包中的文件
安装vim，zip，unzip后直接vim app-pc.war
### 查询文件在war包的路径
`jar -tvf app-pc.war |grep app.prop`
### 取出war包中的文件
`jar -xvf app-pc.war WEB-INF/classes/config/app.properties`
### 更新war包中的文件
`jar -uvf app-pc.war WEB-INF/classes/config/app.properties`
`zip -d xxx.war /xxx/xxx`


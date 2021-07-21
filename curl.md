### follow 302
`curl -I -L --http1.1 'https://openapi.alipaydev.com/gateway.do?_input_charset=utf-8`

### json
`curl -s -H "Content-type: application/json" -d '{"text":"测试", "topic":"1"}' http://192.168.88.3:8098/rsp | jq '.text'`

### cookie
```
//先登录获取cookie
curl --cookie-jar cookie.txt -d '{"username": "demobin@folozs.com", "password": "123456", "type": "email"}' https://127.0.0.1/api/v0.1/login`
//再带cookie访问
curl -b @cookie.txt -d '{"name": "stephen"}' http://127.0.0.1/api/v0.1/star_info_update
```

### upload
```
curl 'http://10.16.8.96:8080/app/fileServer/fileUpload' -F "app=admin-pc" -F "module=doc" -F "user=wyn" -F "name=1.png" -F "type=image/png" -F "file=@1.png" -v
```

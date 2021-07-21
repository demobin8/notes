### git status
```
file permission
git config --global core.filemode false
crlf different
git config --global core.autocrlf true
```

### vmmen内存大
C:\Users\demobin\.wslconfig
```
[wsl2]
memory=6GB
swap=2GB
```

### wsl2找不到docker
```
The command 'docker' could not be found in this WSL 1 distro. We recommend to convert this distro to WSL 2 and activate the WSL integration in Docker Desktop settings.
https://stackoverflow.com/questions/63497928/ubuntu-wsl-with-docker-could-not-be-found

wsl --set-version Ubuntu-20.04 2
wsl --set-default Ubuntu-20.04
```

### wsl 安装

https://docs.microsoft.com/en-us/windows/wsl/install-win10

### wsl 本机vpn

https://github.com/microsoft/WSL/issues/4277

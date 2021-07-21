### 查看所有nodes
`kubectl get nodes`

### 查看所有nodes，带label
`kubectl get node --show-labels`

### 查看所有nodes，使用label过滤
`kubectl get node -l tester=chenqiang`

### 查看所有pods
`kubectl get pods -n kube-system`

### 删除namespace
`kubectl delete ns istio-system`

### 创建namespace
`kubectl create namespace istio-system`

### 查看namespace
`kubectl get namespaces`

### 查看svc
```
kubectl get svc -n kube-system
kubectl get pods --all-namespaces -o wide
```

### 创建svc
```
kubectl create service -h
kubectl create service nodeport test-service-nodeport -h
kubectl create service nodeport test-service-nodeport --tcp=9527:8080
```

### 查看logs
`kubectl logs coredns-5644d7b6d9-69dwb -n kube-system`

### 持续查看logs
`kubectl logs -f qingzhou-parking-lot-management-648764f7c8-slzjv -n qingzhou qingzhou-parking-lot-management`

### 查看endpoints
`kubectl get ep`

### 应用配置
`kubectl apply -f recommended.yaml`

### 查看pods详细信息
`kubectl describe pods kube-apiserver-testserver1 -n kube-system`

### 登录容器
`kubectl exec -it <pod-name> -c <container-name> -- bash`
  
### 删除pods
```
kubectl delete pods kuboard-756d46c4d4-482wj -n kube-system
kubectl delete --force
```
  
### 查看api-version
`kubectl api-versions`
  
### 创建deployment
`kubectl create deployment qingzhou-demo --image=registry.worldlinking.org:5000/qingzhou/qingzhou-demo:latest`
  
### 查看deployment
`kubectl get deployment -n qingzhou`

### 删除deployment
`kubectl delete deployment qingzhou-demo -n qingzhou`
  
### 编辑资源
`kubectl edit deployment qingzhou-demo`
  
### 查看event
`kubectl get events`
  
### 打开自动注入
`kubectl label namespace qingzhou istio-injection=enabled`
  
### 查看是否自动注入
`kubectl get ns -L istio-injection`
  
### 让master节点加入工作负载
`kubectl taint nodes --all node-role.kubernetes.io/master-`
  
### 取消master加入负载
`kubectl taint nodes k8s-master node-role.kubernetes.io/master=true:NoSchedule`
  
### 取消master加入负载后驱逐pods
`kubectl taint nodes <node-name> node-role.kubernetes.io/master=:NoExecute`
  
### 查看资源
```
kubectl top node k8s-save2
kubectl top node
kubectl top pod
```
  
### 查看支持的资源
`kubectl api-resources |grep statefulsets`
  
### 查看支持的版本
`kubectl api-versions |grep apps`
  
### 解释资源
`kubectl explain statefulsets`

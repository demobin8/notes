### 创建namespace
```
kubectl create ns argo
kubectl apply -n argo -f https://raw.githubusercontent.com/argoproj/argo-workflows/stable/manifests/quick-start-postgres.yaml
```
### 创建ui forward
`kubectl -n argo port-forward deployment/argo-server 2746:2746 `

### ui地址
https://127.0.0.1:2746/workflows?limit=500

### cli
https://github.com/argoproj/argo-workflows/releases


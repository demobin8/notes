
	* 创建3个pv -- 确保有3个pv，每个pv的persistentVolumeReclaimPolicy为Retain，storageClassName为sc创建的名称，nodeAffinity不同，且空间足够，注意，如果pv有master，则需手动开启master节点加入工作负载
	* 创建pvc -- 这个redis-ha自己会创建，如果helm install一直pending的状态，且pv创建后pvc一直无法绑定到pv则，先kubectl delete pvc，再kubectl delete pod redis-server-ha-0，等到pod再次重启，绑定成功
	* 创建sc
	* 暴露服务到外部 -- 可以不做

### pv
```
apiVersion: v1
kind: PersistentVolume
metadata:
  name: redis-pv1
spec:
  capacity:
    storage: 5Gi
  volumeMode: Filesystem
  accessModes:
  - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  storageClassName: local-storage
  local:
    path: /opt/redis
  nodeAffinity:
    required:
      nodeSelectorTerms:
      - matchExpressions:
        - key: kubernetes.io/hostname
          operator: In
          values:
          - k8s-slave1
---
apiVersion: v1
kind: PersistentVolume
metadata:
  name: redis-pv2
spec:
  capacity:
    storage: 5Gi
  volumeMode: Filesystem
  accessModes:
  - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  storageClassName: local-storage
  local:
    path: /opt/redis
  nodeAffinity:
    required:
      nodeSelectorTerms:
      - matchExpressions:
        - key: kubernetes.io/hostname
          operator: In
          values:
          - k8s-slave2
```
### pvc
```
kind: PersistentVolumeClaim
apiVersion: v1
metadata:
  name: local-claim
spec:
  accessModes:
  - ReadWriteOnce
  storageClassName: local-storage
  resources:
    requests:
      storage: 10Gi
storage

kind: StorageClass
apiVersion: storage.k8s.io/v1
metadata:
  name: local-storage
provisioner: kubernetes.io/no-provisioner
volumeBindingMode: WaitForFirstConsumer
```
### svc
```
apiVersion: v1
kind: Service
metadata:
  name: redis-ha-service
  labels:
    app: redis-ha
spec:
  ports:
  - name: redis-ha
    protocol: "TCP"
    port: 26379
    targetPort: 6379
    nodePort: 30379
  selector:
    statefulset.kubernetes.io/pod-name: redis-ha-server-0
  type: NodePort
```
### 设置默认sc
```
kubectl patch storageclass local-storage -p '{"metadata": {"annotations":{"storageclass.kubernetes.io/is-default-class":"true"}}}'
```
### 安装
```
helm install --set replicas=2 --set haproxy.replicas=2 --set auth=true --set haproxy.enabled=true --set redisPassword=wwzl2025 --set hostPath.path=/opt/redis redis-ha stable/redis-ha
```
### 查看values信息
```
helm inspect values stable/redis-ha
```


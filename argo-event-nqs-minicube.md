### 创建namespace
`kubectl.exe create ns argo-events`

### 安装
```
kubectl apply -f https://raw.githubusercontent.com/argoproj/argo-events/stable/manifests/install.yaml
# Install with a validating admission controller
kubectl apply -f https://raw.githubusercontent.com/argoproj/argo-events/stable/manifests/install-validating-webhook.yaml
```

### 创建nsq的svc和pod
官网的版本不行
```
apiVersion: v1
kind: Service
metadata:
  name: nsqlookupd
  labels:
    app: nsq
spec:
  ports:
    - port: 4160
      targetPort: 4160
      name: tcp
    - port: 4161
      targetPort: 4161
      name: http
  clusterIP: None
  selector:
    app: nsq
    component: nsqlookupd
---
apiVersion: v1
kind: Service
metadata:
  name: nsqd
  labels:
    app: nsq
spec:
  ports:
    - port: 4150
      targetPort: 4150
      name: tcp
    - port: 4151
      targetPort: 4151
      name: http
  clusterIP: None
  selector:
    app: nsq
    component: nsqd
---
apiVersion: v1
kind: Service
metadata:
  name: nsqadmin
  labels:
    app: nsq
spec:
  ports:
    - port: 4170
      targetPort: 4170
      name: tcp
    - port: 4171
      targetPort: 4171
      name: http
  selector:
    app: nsq
    component: nsqadmin
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: nsqlookupd
spec:
  serviceName: "nsqlookupd"
  replicas: 1
  updateStrategy:
    type: RollingUpdate
  selector:
    matchLabels:
      app: nsq
      component: nsqlookupd
  template:
    metadata:
      labels:
        app: nsq
        component: nsqlookupd
    spec:
      containers:
        - name: nsqlookupd
          image: nsqio/nsq:v1.2.0
          imagePullPolicy: Always
          resources:
            requests:
              cpu: 30m
              memory: 64Mi
          ports:
            - containerPort: 4160
              name: tcp
            - containerPort: 4161
              name: http
          livenessProbe:
            httpGet:
              path: /ping
              port: http
            initialDelaySeconds: 5
          readinessProbe:
            httpGet:
              path: /ping
              port: http
            initialDelaySeconds: 2
          command:
            - /nsqlookupd
      terminationGracePeriodSeconds: 5
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nsqd
spec:
  replicas: 1
  selector:
    matchLabels:
      app: nsq
      component: nsqd
  template:
    metadata:
      labels:
        app: nsq
        component: nsqd
    spec:
      containers:
        - name: nsqd
          image: nsqio/nsq:v1.2.0
          imagePullPolicy: Always
          resources:
            requests:
              cpu: 30m
              memory: 64Mi
          ports:
            - containerPort: 4150
              name: tcp
            - containerPort: 4151
              name: http
          livenessProbe:
            httpGet:
              path: /ping
              port: http
            initialDelaySeconds: 5
          readinessProbe:
            httpGet:
              path: /ping
              port: http
            initialDelaySeconds: 2
          volumeMounts:
            - name: datadir
              mountPath: /data
          command:
            - /nsqd
            - -data-path
            - /data
            - -lookupd-tcp-address
            - nsqlookupd.argo-events.svc:4160
            - -broadcast-address
            - nsqd.argo-events.svc
          env:
            - name: HOSTNAME
              valueFrom:
                fieldRef:
                  fieldPath: metadata.name
      terminationGracePeriodSeconds: 5
      volumes:
        - name: datadir
          emptyDir: {}
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nsqadmin
spec:
  replicas: 1
  selector:
    matchLabels:
      app: nsq
      component: nsqadmin
  template:
    metadata:
      labels:
        app: nsq
        component: nsqadmin
    spec:
      containers:
        - name: nsqadmin
          image: nsqio/nsq:v1.2.0
          imagePullPolicy: Always
          resources:
            requests:
              cpu: 30m
              memory: 64Mi
          ports:
            - containerPort: 4170
              name: tcp
            - containerPort: 4171
              name: http
          livenessProbe:
            httpGet:
              path: /ping
              port: http
            initialDelaySeconds: 10
          readinessProbe:
            httpGet:
              path: /ping
              port: http
            initialDelaySeconds: 5
          command:
            - /nsqadmin
            - -lookupd-http-address
            - nsqlookupd.argo-events.svc:4161
      terminationGracePeriodSeconds: 5
```      
### 创建minikube service（仅window-docker driver需要？）
`minikube.exe service nsqadmin -n argo-events`


### deployment
```
---
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: test-payment-service
  name: test-payment-service
  namespace: test
spec:
  progressDeadlineSeconds: 600
  replicas: 1
  revisionHistoryLimit: 10
  selector:
    matchLabels:
      app: test-payment-service
  strategy:
    rollingUpdate:
      maxSurge: 25%
      maxUnavailable: 25%
    type: RollingUpdate
  template:
    metadata:
      labels:
        app: test-payment-service
    spec:
      containers:
        - env:
            - name: MEM_MIN
              value: '-Xms1024m'
            - name: MEM_MAX
              value: '-Xmx2048m'
            - name: LC_ALL
              value: C.UTF-8
            - name: MY_NODE_NAME
              valueFrom:
                fieldRef:
                  apiVersion: v1
                  fieldPath: spec.nodeName
            - name: MY_NODE_IP
              valueFrom:
                fieldRef:
                  apiVersion: v1
                  fieldPath: status.hostIP
          image: '192.168.1.2/test/test-payment-service/test-payment-service:52'
          imagePullPolicy: Always
          name: test-payment-service
          ports:
            - containerPort: 7134
              protocol: TCP
          readinessProbe:
            failureThreshold: 3
            periodSeconds: 10
            successThreshold: 1
            tcpSocket:
              port: 7134
            timeoutSeconds: 1
          resources:
            limits:
              cpu: '4'
              memory: 2457Mi
            requests:
              cpu: 200m
              memory: 1Gi
          terminationMessagePath: /dev/termination-log
          terminationMessagePolicy: File
          volumeMounts:
            - mountPath: /HOME/PROJECT/test-PAYMENT-SERVICE/log/
              name: app-logs
        - args:
            - '-c'
            - /etc/filebeat/filebeat.yml
            - '-e'
          image: '192.168.1.2/test-base/beats/filebeat:6.5.4'
          imagePullPolicy: IfNotPresent
          name: test-payment-service-filebeat
          terminationMessagePath: /dev/termination-log
          terminationMessagePolicy: File
          volumeMounts:
            - mountPath: /HOME/PROJECT/test-PAYMENT-SERVICE/log/
              name: app-logs
            - mountPath: /etc/filebeat/
              name: test-payment-service-config
      dnsPolicy: ClusterFirst
      nodeSelector:
        type: test
      restartPolicy: Always
      schedulerName: default-scheduler
      terminationGracePeriodSeconds: 30
      volumes:
        - emptyDir: {}
          name: app-logs
        - configMap:
            defaultMode: 420
            name: test-payment-service-config
          name: test-payment-service-config
```
### config map
```
---
apiVersion: v1
data:
  filebeat.yml: |-
    filebeat.inputs:
    - type: log
      enabled: true
      paths:
        - /HOME/PROJECT/PAYMENT-SERVICE/log/applog-*.log
      multiline.pattern: '^[0-9][4]-[0-9][2]-[0-9][2]'
      multiline.negate: true
      multiline.match: after
      fields:
        envName: dev
        logType: applog
        product: test
        service: payment-service
      fields_under_root: true
    - type: log
      enabled: true
      paths:
        - /HOME/PROJECT/PAYMENT-SERVICE/log/access-*.log
      multiline.pattern: '^\['
      multiline.negate: true
      multiline.match: after
      fields:
        envName: dev
        logType: access
        product: test
        service: payment-service
      fields_under_root: true
    filebeat.config.modules:
      path: ${path.config}/modules.d/*.yml
      reload.enabled: false
    setup.template.settings:
      index.number_of_shards: 3
    setup.kibana:
    output.kafka:
      hosts: ["192.168.1.2:9092"]
      topic: elk_logs
      partition.round_robin:
        reachable_only: false
      required_acks: 1
      compression: gzip
      max_message_bytes: 1000000
    processors:
      - add_host_metadata: ~
      - add_cloud_metadata: ~
kind: ConfigMap
metadata:
  labels:
    k8s-app: test-payment-service
  name: test-payment-service-config
  namespace: test
```
### service
```
---
apiVersion: v1
kind: Service
metadata:
  labels:
    run: test-payment-service
  name: test-payment-service
  namespace: test
spec:
  externalTrafficPolicy: Cluster
  ports:
    - nodePort: 37134
      port: 7134
      protocol: TCP
      targetPort: 7134
  selector:
    app: test-payment-service
  sessionAffinity: None
  type: NodePort
```

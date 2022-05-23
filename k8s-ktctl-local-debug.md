## Prepare
### Kubectl use dev context
```
kubectl.exe config get-contexts
```
If not, switch to dev environment
```
kubectl.exe config use-context FTIDevAKSClusterV2
```

### KT-CONNECT
Download KT-CONNECT tool from Releases · alibaba/kt-connect 

### JSON2YAML, OPENAPI2POSTMANV2
Install through npm
```
npm i -g json2yaml openapi-to-postmanv2
```

### Connect to Kubernetes Service
```
ktctl.exe -n millitrans connect
```

### Import Open-API Schema to Postman
```
curl http://millitrans-site:8080/_sys/open-api | json2yaml > api.yaml

openapi2postmanv2 -s api.yaml -o collection.json -p -O folderStrategy=Tags,includeAuthInfoInExample=false
```
Open Postman, select File → Import, select collection.json

Edit Collection

Change the baseUrl to your Service URL

And then, the postman can invoke all the APIs with the schema defined.

## Route the specific VERSION request in Kubernetes to your local IDEA for debugging
Execute KTCTL mesh command

```
ktctl.exe -n millitrans mesh millitrans-site --expose 8080:8080 --versionMark demobin
millitrans → namespace
```
- millitrans-site → Service name
- 8080 → Service port
- 8080 → Idea project service listened Local port 
- demobin → your Service version

### Check deploy

Add header in postman

Creating preview...
Send request and have the fun of debugging now ^ - ^

The requests will route to the old Service if the VERSION header is not set.

### Clean
Don’t forget clean all the resources of KT-CONNECT in Kubernetes
```
ktctl.exe clean
```

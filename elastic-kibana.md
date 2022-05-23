### docker run services
```
docker run -d --name elasticsearch -p 9200:9200 -p 9300:9300 --network etl_project_network -e "discovery.type=single-node" -e "ES_JAVA_OPTS=-Xms512m -Xmx512m" elasticsearch:8.2.0
docker run -d --name kibana --network etl_project_network -p 5601:5601 kibana:8.2.0
```
get kibana url from kibana log, using localhost instead of 0.0.0.0 under windows
generate erollment token and password
```
./bin/elasticsearch-create-enrollment-token --scope kibana
./bin/elasticsearch-reset-password -u elastic
```
### create api key
open kibana dev tool console http://localhost:5601/app/dev_tools#/console
execute following query
```
POST _security/api_key
{
  "name": "log-api-key"
}
view on http://localhost:5601/app/management/security/api_keys
```
### java connect
error: "PKIX path building failed" and "unable to find valid certification path to requested target"
> https://stackoverflow.com/questions/21076179/pkix-path-building-failed-and-unable-to-find-valid-certification-path-to-requ
```
# vist https://localhost:9200, export the der encode cert from chrome
# execute cmd as admin, password 'changeit'
keytool -import -alias example -keystore "C:\Program Files\Java\jdk-17.0.1\lib\security\cacerts" -file C:\Users\dev\Documents\elasticsearch.cer
```
### update
```
POST trace-2022.05.18/_update/80D6A61B99F6C9B5B477
{
  "script": {
    "source": "ctx._source.impact = 'No Impact'",
    "lang": "painless"
  }
}
```

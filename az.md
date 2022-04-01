
> AZ CLI Reference: https://docs.microsoft.com/en-us/cli/azure/reference-index?view=azure-cli-latest

### list location
```
az account list-locations -o table
```
![image](https://user-images.githubusercontent.com/16394555/161241254-f00410e7-b445-41c1-ba90-8a6094dfbbf7.png)
### list vm usage
```
az vm list-usage --location eastus2 -o table
```
![image](https://user-images.githubusercontent.com/16394555/161241824-ae76e727-4810-4937-abc5-6177e81e8685.png)
### list subscriptions
```
az account list -o table
```
![image](https://user-images.githubusercontent.com/16394555/161243020-23de4ebf-c7f0-4943-ad7b-d16b865a7fc3.png)
### show subscription
```
az account show -n FTI-QA
```
![image](https://user-images.githubusercontent.com/16394555/161243269-6be2d41c-8714-4001-97d8-5adfc5314203.png)
### set subscription
```
az account set --subscription FTI-QA
```
### list groups
```
az group list -o table
```
![image](https://user-images.githubusercontent.com/16394555/161244402-2f6d72b5-6ed5-4ef1-aaa0-92bc18bd6d51.png)
### show group
```
az group show -g FTIDev
```
![image](https://user-images.githubusercontent.com/16394555/161244700-3f197c98-ea09-4849-8528-a3921507b737.png)
### list resources
```
az resource list
```
![image](https://user-images.githubusercontent.com/16394555/161245762-6516a4fd-17d0-4224-ae01-bffab6b1889a.png)
### show resource
```
az resource show --resource-group FTIDev --resource-type "Microsoft.Compute/virtualMachines" --name FTIDevVMVM
```
![image](https://user-images.githubusercontent.com/16394555/161246117-0a5c6341-4dab-48c5-aff1-50a57aaf96a9.png)
### list aks
```
az aks list -o table
```
![image](https://user-images.githubusercontent.com/16394555/161243995-aa4bba9c-a3ec-42e4-85d0-db336260b448.png)
### aks get-credentials
```
az aks get-credentials --name FTIDevAKSClusterV2 --resource-group FTIDev --admin
```

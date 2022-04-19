
> AZ CLI Reference: https://docs.microsoft.com/en-us/cli/azure/reference-index?view=azure-cli-latest

### help
```
az --help
az network --help
az network vnet --help
```
resource have these commands normally
```
Commands:
    create                       : Create a xxx.
    delete                       : Delete a xxx.
    list                         : List xxx.
    show                         : Get the details of a xxx.
    update                       : Update a xxx.
```
### az subgroups
```
az --help
...
Subgroups:
    account                                   : Manage Azure subscription information.
    acr                                       : Manage private registries with Azure Container Registries.
    ad                                        : Manage Azure Active Directory Graph entities needed for Role Based Access Control.
    advisor                                   : Manage Azure Advisor.
    afd                             [Preview] : Manage Azure Front Door.
    aks                                       : Manage Azure Kubernetes Services.
    ams                                       : Manage Azure Media Services resources.
    apim                       [Experimental] : Manage Azure API Management services.
    appconfig                                 : Manage App Configurations.
    appservice                                : Manage App Service plans.
    aro                                       : Manage Azure Red Hat OpenShift clusters.
    backup                                    : Manage Azure Backups.
    batch                                     : Manage Azure Batch.
    bicep                                     : Bicep CLI command group.
    billing                                   : Manage Azure Billing.
    bot                                       : Manage Microsoft Azure Bot Service.
    cache                                     : Commands to manage CLI objects cached using the `--defer` argument.
    capacity                                  : Manage capacity.
    cdn                                       : Manage Azure Content Delivery Networks (CDNs).
    cloud                                     : Manage registered Azure clouds.
    cognitiveservices                         : Manage Azure Cognitive Services accounts.
    config                     [Experimental] : Manage Azure CLI configuration.
    consumption                     [Preview] : Manage consumption of Azure resources.
    container                                 : Manage Azure Container Instances.
    cosmosdb                                  : Manage Azure Cosmos DB database accounts.
    databoxedge                     [Preview] : Support data box edge device and management.
    deployment                                : Manage Azure Resource Manager template deployment at subscription scope.
    deployment-scripts                        : Manage deployment scripts at subscription or resource group scope.
    deploymentmanager               [Preview] : Create and manage rollouts for your service.
    disk                                      : Manage Azure Managed Disks.
    disk-access                               : Manage disk access resources.
    disk-encryption-set                       : Disk Encryption Set resource.
    dla                             [Preview] : Manage Data Lake Analytics accounts, jobs, and catalogs.
    dls                             [Preview] : Manage Data Lake Store accounts and filesystems.
    dms                                       : Manage Azure Data Migration Service (DMS) instances.
    eventgrid                                 : Manage Azure Event Grid topics, domains, domain topics, system topics partner topics, event
                                                subscriptions, system topic event subscriptions and partner topic event subscriptions.
    eventhubs                                 : Manage Azure Event Hubs namespaces, eventhubs, consumergroups and geo recovery configurations - Alias.
    extension                                 : Manage and update CLI extensions.
    feature                                   : Manage resource provider features.
    functionapp                               : Manage function apps. To install the Azure FunctionsCore tools see https://github.com/Azure/azure-functions-core-tools.
    group                                     : Manage resource groups and template deployments.
    hdinsight                                 : Manage HDInsight resources.
    identity                                  : Managed Identities.
    image                                     : Manage custom virtual machine images.
    iot                                       : Manage Internet of Things (IoT) assets.
    keyvault                                  : Manage KeyVault keys, secrets, and certificates.
    kusto                                     : Manage Azure Kusto resources.
    lab                             [Preview] : Manage Azure DevTest Labs.
    local-context [Deprecated] [Experimental] : Manage Local Context.
    lock                                      : Manage Azure locks.
    logicapp                                  : Manage logic apps.
    managed-cassandra                         : Azure Managed Cassandra.
    managedapp                                : Manage template solutions provided and maintained by Independent Software Vendors (ISVs).
    managedservices                           : Manage the registration assignments and definitions in Azure.
    maps                                      : Manage Azure Maps.
    mariadb                                   : Manage Azure Database for MariaDB servers.
    monitor                                   : Manage the Azure Monitor Service.
    mysql                                     : Manage Azure Database for MySQL servers.
    netappfiles                               : Manage Azure NetApp Files (ANF) Resources.
    network                                   : Manage Azure Network resources.
    policy                                    : Manage resource policies.
    postgres                                  : Manage Azure Database for PostgreSQL servers.
    ppg                                       : Manage Proximity Placement Groups.
    provider                                  : Manage resource providers.
    redis                                     : Manage dedicated Redis caches for your Azure applications.
    relay                                     : Manage Azure Relay Service namespaces, WCF relays,hybrid connections, and rules.
    reservations                    [Preview] : Manage Azure Reservations.
    resource                                  : Manage Azure resources.
    restore-point                             : Manage restore point with res.
    role                                      : Manage user roles for access control with Azure Active Directory and service principals.
    search                                    : Manage Azure Search services, admin keys and query keys.
    security                                  : Manage your security posture with Azure Security Center.
    servicebus                                : Manage Azure Service Bus namespaces, queues, topics,subscriptions, rules and geo-disaster recovery configuration alias.
    sf                                        : Manage and administer Azure Service Fabric clusters.
    sig                                       : Manage shared image gallery.
    signalr                                   : Manage Azure SignalR Service.
    snapshot                                  : Manage point-in-time copies of managed disks, native blobs, or other snapshots.
    sql                                       : Manage Azure SQL Databases and Data Warehouses.
    sshkey                                    : Manage ssh public key with vm.
    staticwebapp                              : Manage static apps.
    storage                                   : Manage Azure Cloud Storage resources.
    synapse                         [Preview] : Manage and operate Synapse Workspace, Spark Pool, SQL Pool.
    tag                                       : Tag Management on a resource.
    term                       [Experimental] : Manage marketplace agreement with
                                                marketplaceordering.
    ts                                        : Manage template specs at subscription or resource group scope.
    vm                                        : Manage Linux or Windows virtual machines.
    vmss                                      : Manage groupings of virtual machines in an Azure Virtual Machine Scale Set (VMSS).
    webapp                                    : Manage web apps.
```
### list locations
```
az account list-locations -o table
```
![image](https://user-images.githubusercontent.com/16394555/161241254-f00410e7-b445-41c1-ba90-8a6094dfbbf7.png)
### list vm usages
```
az vm list-usage --location eastus2 -o table
```
![image](https://user-images.githubusercontent.com/16394555/161241824-ae76e727-4810-4937-abc5-6177e81e8685.png)
### list vm sizes
```
az vm list-sizes --location eastus2 -o table
```
### list vm skus
```
az vm list-skus -o table
```
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
### show group
```
az group show -g FTIDev
```
### list resources
```
az resource list
```
### show resource
```
az resource show --resource-group FTIDev --resource-type "Microsoft.Compute/virtualMachines" --name FTIDevVMVM
```
### vm subgroups
```
az vm --help
...
Subgroups:
    application            : Manage appliations for VM.
    availability-set       : Group resources into availability sets.
    boot-diagnostics       : Troubleshoot the startup of an Azure Virtual Machine.
    diagnostics            : Configure the Azure Virtual Machine diagnostics extension.
    disk                   : Manage the managed data disks attached to a VM.
    encryption             : Manage encryption of VM disks.
    extension              : Manage extensions on VMs.
    host                   : Manage Dedicated Hosts for Virtual Machines.
    identity               : Manage service identities of a VM.
    image                  : Information on available virtual machine images.
    monitor                : Manage monitor aspect for a vm.
    nic                    : Manage network interfaces. See also `az network nic`.
    run-command            : Manage run commands on a Virtual Machine.
    secret                 : Manage VM secrets.
    unmanaged-disk         : Manage the unmanaged data disks attached to a VM.
    user                   : Manage user accounts for a VM.
```
### list vms
```
az vm list -o table
```
### list aks
```
az aks list -o table
```
### aks get-credentials
```
az aks get-credentials --name FTIDevAKSClusterV2 --resource-group FTIDev --admin
```
### network subgroups
```
...
Subgroups:
    application-gateway                 : Manage application-level routing and load balancing services.
    asg                                 : Manage application security groups (ASGs).
    bastion                   [Preview] : Manage Azure bastion host.
    cross-region-lb                     : Manage and configure cross-region load balancers.
    custom-ip                           : Manage custom IP.
    ddos-protection                     : Manage DDoS Protection Plans.
    dns                                 : Manage DNS domains in Azure.
    express-route                       : Manage dedicated private network fiber connections to Azure.
    lb                                  : Manage and configure load balancers.
    local-gateway                       : Manage local gateways.
    nat                                 : Commands to manage NAT resources.
    nic                                 : Manage network interfaces.
    nsg                                 : Manage Azure Network Security Groups (NSGs).
    private-dns                         : Manage Private DNS domains in Azure.
    private-endpoint                    : Manage private endpoints.
    private-endpoint-connection         : Manage private endpoint connections.
    private-link-resource               : Manage private link resources.
    private-link-service                : Manage private link services.
    profile                             : Manage network profiles.
    public-ip                           : Manage public IP addresses.
    route-filter              [Preview] : Manage route filters.
    route-table                         : Manage route tables.
    routeserver                         : Manage the route server.
    security-partner-provider [Preview] : Manage Azure security partner provider.
    service-endpoint                    : Manage policies related to service endpoints.
    traffic-manager                     : Manage the routing of incoming traffic.
    virtual-appliance         [Preview] : Manage Azure Network Virtual Appliance.
    vnet                                : Manage Azure Virtual Networks.
    vnet-gateway                        : Use an Azure Virtual Network Gateway to establish secure, cross-premises connectivity.
    vpn-connection                      : Manage VPN connections.
    watcher                             : Manage the Azure Network Watcher.
```
### network xxx list
```
az network application-gateway list -o table
```
### show vnet
```
az network vnet show --name FTIUatVnet -g FTIUat
```
### show network security group
```
az network nsg show -n FTIDevApp -g FTIDev
```
### keyvault subgroups
```
Subgroups:
    backup                      : Manage full HSM backup.
    certificate                 : Manage certificates.
    key                         : Manage keys.
    network-rule                : Manage vault network ACLs.
    private-endpoint-connection : Manage vault/HSM private endpoint connections.
    private-link-resource       : Manage vault/HSM private link resources.
    restore                     : Manage full HSM restore.
    role                        : Manage user roles for access control.
    secret                      : Manage secrets.
    security-domain             : Manage security domain operations.
    storage                     : Manage storage accounts.
```
### list key
```
az keyvault key list --vault-name FTIDevKV
```
### mysql subgroups
```
Subgroups:
    db              : Manage MySQL databases on a server.
    flexible-server : Manage Azure Database for MySQL Flexible Servers.
    server          : Manage MySQL servers.
    server-logs     : Manage server logs.
```

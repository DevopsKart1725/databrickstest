# az account list -o table
# az account set --subscription "SYNH-EUSDEV-CR-IEPDATA-LANDING"

$projectName="privatedp"

# Create a RG
$resourceGroupName="$projectName-rg"
az group create -l eastus -n $resourceGroupName 

# Create Subnet
$snetAddressPrefixes="10.224.42.128/27"
$vnetResourceGroup="iepdlz01-dev-network"
$vnetName="iepdlz01-dev-vnet"
$nsgName="iepdlz01-dev-nsg" 
$rtName="iepdlz01-dev-routetable"
$snetName="$projectName-snet"

az network vnet subnet create -g $vnetResourceGroup `
    --vnet-name $vnetName `
    -n $snetName `
    --network-security-group $nsgName --route-table $rtName `
    --address-prefixes $snetAddressPrefixes

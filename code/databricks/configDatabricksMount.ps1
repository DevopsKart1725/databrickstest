# Set variables for Databricks workspace
# Define script arguments
[CmdletBinding()]
param (

    [Parameter(Mandatory = $true)]
    [ValidateNotNullOrEmpty()]
    [String]
    $DatabricksApiUrl,

    [Parameter(Mandatory = $true)]
    [ValidateNotNullOrEmpty()]
    [String]
    $databricksPAT,

    [Parameter(Mandatory = $true)]
    [ValidateNotNullOrEmpty()]
    [String]
    $clientid,

    [Parameter(Mandatory = $true)]
    [ValidateNotNullOrEmpty()]
    [String]
    $clientsecret,

    [Parameter(Mandatory = $true)]
    [ValidateNotNullOrEmpty()]
    [String]
    $endpoint,


    [Parameter(Mandatory = $true)]
    [ValidateNotNullOrEmpty()]
    [String]
    $adlsContainerName


)
# Install Databricks PS Module
Set-PSRepository -Name "PSGallery" -InstallationPolicy Trusted
Install-Module -Name DatabricksPS
Update-Module -Name DatabricksPS

Set-DatabricksEnvironment -AccessToken $databricksPAT -ApiRootUrl $DatabricksApiUrl 
$pythonPath = "$PSScriptRoot/configDataBricksWorkspace.py"
# Set variables for job and notebook

$jobName = "Mount_Job"

$notebookPath = "/ConfigureDatabricksWorkspace"
Import-DatabricksWorkspaceItem -Path $notebookPath -Format SOURCE -Language PYTHON -LocalPath $pythonPath -Overwrite $true
$notebookParams = @{
    "paramclientsecret" =$clientsecret
    "paramclientid" =$clientid
    "paramendpoint" =$endpoint
    "paramadlsContainerName" =$adlsContainerName
}

# Create a Databricks job

$jobBody = @{

    name = $jobName

    new_cluster = @{

        spark_version = "11.3.x-scala2.12"

        node_type_id = "Standard_DS3_v2"

        num_workers = 1

    }

    notebook_task = @{

        notebook_path = $notebookPath

        base_parameters = $notebookParams

    }

}

$jobUri = "$DatabricksApiUrl/api/2.0/jobs/create" 
$jobResponse = Invoke-RestMethod -Uri $jobUri -Headers @{Authorization = "Bearer $databricksPAT"} -Method POST -Body ($jobBody | ConvertTo-Json -Depth 10)

Write-Host "job with the name $($jobName) is created"
$jobsUrl = "$DatabricksApiUrl/api/2.0/jobs/list"

$jobsResponse = Invoke-RestMethod -Method GET -Uri $jobsUrl -Headers @{Authorization = "Bearer $databricksPAT"}
$jobs = $jobsResponse.jobs

# Trigger the job run
foreach($jobsName in $jobs){
if($jobsName.settings.name -eq $jobName){
$runNotebookUrl = "$DatabricksApiUrl/api/2.0/jobs/run-now"
$body = @{
"job_id" = $jobsName.job_id
"notebook_params" = $notebookContent
}
$runNotebookResponse = Invoke-RestMethod -Method POST -Uri $runNotebookUrl -Headers @{Authorization = "Bearer $databricksPAT"} -Body ($body | ConvertTo-Json)
Write-Output "Notebook $notebookPath has been started with run ID $($runNotebookResponse.run_id)"
Write-Output "job is running"
Start-Sleep -Seconds 300
$status = Get-DatabricksJobRun -JobID $jobsName.job_id

if($status.state.result_state -eq "SUCCESS"){
Write-Host "$($jobName) is succeeded "
}else{"not succeeded"}
}
}
# Remove Workspace Configuration Notebook
Write-Output "Removing Workspace Configuration Notebook"
Remove-DatabricksWorkspaceItem $notebookPath
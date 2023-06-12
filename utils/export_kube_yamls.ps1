param (
    [Parameter(Mandatory=$true)]
    [string]$namespace
)

# Get the list of resources
$resourceList = kubectl get -o=name -n $namespace pvc,configmap,serviceaccount,secret,ingress,service,deployment,statefulset,hpa,job,cronjob

# Split the resource list into an array by newline character
$resources = $resourceList -split "`n"

# Iterate over each resource
foreach ($n in $resources) {
    # Make directory based on resource name
    $dirPath = [System.IO.Path]::GetDirectoryName($n)
    if (!(Test-Path -Path $dirPath)) {
        New-Item -ItemType Directory -Force -Path $dirPath
    }

    # Export the resource to a yaml file
    kubectl get -o=yaml -n $namespace $n | Out-File "$n.yaml"
}

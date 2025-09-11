# IT Helpdesk AKS Deployment Script (PowerShell)
# This script automates the deployment of IT Helpdesk app to Azure Kubernetes Service

param(
    [string]$ResourceGroup = "it-helpdesk-rg",
    [string]$ACRName = "ithelpdeskreg",
    [string]$AKSName = "it-helpdesk-aks",
    [string]$Location = "eastus",
    [string]$ImageName = "it-helpdesk",
    [string]$ImageTag = "latest"
)

$ErrorActionPreference = "Stop"

Write-Host "🚀 Starting IT Helpdesk AKS Deployment..." -ForegroundColor Green

# Function to check if command exists
function Test-Command {
    param($CommandName)
    $null = Get-Command $CommandName -ErrorAction SilentlyContinue
    return $?
}

# Check prerequisites
Write-Host "📋 Checking prerequisites..." -ForegroundColor Yellow

if (-not (Test-Command "az")) {
    Write-Host "❌ Azure CLI is not installed. Please install it first." -ForegroundColor Red
    exit 1
}

if (-not (Test-Command "docker")) {
    Write-Host "❌ Docker is not installed. Please install it first." -ForegroundColor Red
    exit 1
}

if (-not (Test-Command "kubectl")) {
    Write-Host "❌ kubectl is not installed. Please install it first." -ForegroundColor Red
    exit 1
}

Write-Host "✅ All prerequisites are met!" -ForegroundColor Green

# Check Azure login status
Write-Host "🔐 Checking Azure login status..." -ForegroundColor Yellow
try {
    az account show | Out-Null
    Write-Host "✅ Azure login confirmed!" -ForegroundColor Green
}
catch {
    Write-Host "Please login to Azure:" -ForegroundColor Yellow
    az login
}

# Create Resource Group
Write-Host "📦 Creating resource group..." -ForegroundColor Yellow
az group create --name $ResourceGroup --location $Location --output table

# Create ACR
Write-Host "🏗️ Creating Azure Container Registry..." -ForegroundColor Yellow
az acr create --resource-group $ResourceGroup --name $ACRName --sku Basic --output table

# Create AKS Cluster
Write-Host "☸️ Creating AKS cluster (this may take 10-15 minutes)..." -ForegroundColor Yellow
az aks create `
  --resource-group $ResourceGroup `
  --name $AKSName `
  --node-count 2 `
  --enable-addons monitoring `
  --generate-ssh-keys `
  --attach-acr $ACRName `
  --output table

# Login to ACR
Write-Host "🔑 Logging into ACR..." -ForegroundColor Yellow
az acr login --name $ACRName

# Build Docker image
Write-Host "🐳 Building Docker image..." -ForegroundColor Yellow
docker build -t "${ImageName}:${ImageTag}" .

# Tag image for ACR
Write-Host "🏷️ Tagging image for ACR..." -ForegroundColor Yellow
docker tag "${ImageName}:${ImageTag}" "${ACRName}.azurecr.io/${ImageName}:${ImageTag}"

# Push image to ACR
Write-Host "⬆️ Pushing image to ACR..." -ForegroundColor Yellow
docker push "${ACRName}.azurecr.io/${ImageName}:${ImageTag}"

# Get AKS credentials
Write-Host "🔑 Getting AKS credentials..." -ForegroundColor Yellow
az aks get-credentials --resource-group $ResourceGroup --name $AKSName --overwrite-existing

# Update deployment manifest with correct image name
Write-Host "📝 Updating Kubernetes manifests..." -ForegroundColor Yellow
$deploymentContent = Get-Content "k8s/deployment.yaml" -Raw
$deploymentContent = $deploymentContent -replace "your-registry.azurecr.io", "${ACRName}.azurecr.io"
Set-Content "k8s/deployment.yaml" $deploymentContent

# Deploy to Kubernetes
Write-Host "☸️ Deploying to Kubernetes..." -ForegroundColor Yellow
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/secrets.yaml
kubectl apply -f k8s/pvc.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

# Wait for deployment to be ready
Write-Host "⏳ Waiting for deployment to be ready..." -ForegroundColor Yellow
kubectl wait --for=condition=available --timeout=300s deployment/it-helpdesk-app -n it-helpdesk

# Get pod status
Write-Host "📊 Checking pod status..." -ForegroundColor Yellow
kubectl get pods -n it-helpdesk

# Get service info
Write-Host "🌐 Getting service information..." -ForegroundColor Yellow
kubectl get services -n it-helpdesk

Write-Host ""
Write-Host "🎉 Deployment completed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Next steps:" -ForegroundColor Cyan
Write-Host "1. Check pod logs: kubectl logs -f deployment/it-helpdesk-app -n it-helpdesk"
Write-Host "2. Access app locally: kubectl port-forward service/it-helpdesk-service 8501:8501 -n it-helpdesk"
Write-Host "3. Then visit: http://localhost:8501"
Write-Host ""
Write-Host "🔧 To scale the application:" -ForegroundColor Cyan
Write-Host "kubectl scale deployment it-helpdesk-app --replicas=3 -n it-helpdesk"
Write-Host ""
Write-Host "🗑️ To clean up resources:" -ForegroundColor Cyan
Write-Host "az group delete --name $ResourceGroup --yes --no-wait"

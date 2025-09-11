#!/bin/bash

# IT Helpdesk AKS Deployment Script
# This script automates the deployment of IT Helpdesk app to Azure Kubernetes Service

set -e

# Configuration
RESOURCE_GROUP="it-helpdesk-rg"
ACR_NAME="ithelpdeskreg"
AKS_NAME="it-helpdesk-aks"
LOCATION="eastus"
IMAGE_NAME="it-helpdesk"
IMAGE_TAG="latest"

echo "🚀 Starting IT Helpdesk AKS Deployment..."

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo "📋 Checking prerequisites..."
if ! command_exists az; then
    echo "❌ Azure CLI is not installed. Please install it first."
    exit 1
fi

if ! command_exists docker; then
    echo "❌ Docker is not installed. Please install it first."
    exit 1
fi

if ! command_exists kubectl; then
    echo "❌ kubectl is not installed. Please install it first."
    exit 1
fi

echo "✅ All prerequisites are met!"

# Login to Azure (if not already logged in)
echo "🔐 Checking Azure login status..."
if ! az account show >/dev/null 2>&1; then
    echo "Please login to Azure:"
    az login
fi

echo "✅ Azure login confirmed!"

# Create Resource Group
echo "📦 Creating resource group..."
az group create --name $RESOURCE_GROUP --location $LOCATION --output table

# Create ACR
echo "🏗️ Creating Azure Container Registry..."
az acr create --resource-group $RESOURCE_GROUP --name $ACR_NAME --sku Basic --output table

# Create AKS Cluster
echo "☸️ Creating AKS cluster (this may take 10-15 minutes)..."
az aks create \
  --resource-group $RESOURCE_GROUP \
  --name $AKS_NAME \
  --node-count 2 \
  --enable-addons monitoring \
  --generate-ssh-keys \
  --attach-acr $ACR_NAME \
  --output table

# Login to ACR
echo "🔑 Logging into ACR..."
az acr login --name $ACR_NAME

# Build Docker image
echo "🐳 Building Docker image..."
docker build -t $IMAGE_NAME:$IMAGE_TAG .

# Tag image for ACR
echo "🏷️ Tagging image for ACR..."
docker tag $IMAGE_NAME:$IMAGE_TAG $ACR_NAME.azurecr.io/$IMAGE_NAME:$IMAGE_TAG

# Push image to ACR
echo "⬆️ Pushing image to ACR..."
docker push $ACR_NAME.azurecr.io/$IMAGE_NAME:$IMAGE_TAG

# Get AKS credentials
echo "🔑 Getting AKS credentials..."
az aks get-credentials --resource-group $RESOURCE_GROUP --name $AKS_NAME --overwrite-existing

# Update deployment manifest with correct image name
echo "📝 Updating Kubernetes manifests..."
sed -i.bak "s|your-registry.azurecr.io|$ACR_NAME.azurecr.io|g" k8s/deployment.yaml

# Deploy to Kubernetes
echo "☸️ Deploying to Kubernetes..."
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/secrets.yaml
kubectl apply -f k8s/pvc.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

# Wait for deployment to be ready
echo "⏳ Waiting for deployment to be ready..."
kubectl wait --for=condition=available --timeout=300s deployment/it-helpdesk-app -n it-helpdesk

# Get pod status
echo "📊 Checking pod status..."
kubectl get pods -n it-helpdesk

# Get service info
echo "🌐 Getting service information..."
kubectl get services -n it-helpdesk

echo ""
echo "🎉 Deployment completed successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Check pod logs: kubectl logs -f deployment/it-helpdesk-app -n it-helpdesk"
echo "2. Access app locally: kubectl port-forward service/it-helpdesk-service 8501:8501 -n it-helpdesk"
echo "3. Then visit: http://localhost:8501"
echo ""
echo "🔧 To scale the application:"
echo "kubectl scale deployment it-helpdesk-app --replicas=3 -n it-helpdesk"
echo ""
echo "🗑️ To clean up resources:"
echo "az group delete --name $RESOURCE_GROUP --yes --no-wait"

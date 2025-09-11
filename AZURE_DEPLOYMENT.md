# Azure Kubernetes Service (AKS) Deployment Guide

This guide will help you deploy the IT Helpdesk application to Azure Kubernetes Service using Docker containers.

## Prerequisites

- Azure CLI installed and configured
- Docker installed
- kubectl installed
- An Azure subscription
- Azure Container Registry (ACR) or Docker Hub account

## Step 1: Setup Azure Resources

### 1.1 Create Resource Group
```bash
az group create --name it-helpdesk-rg --location eastus
```

### 1.2 Create Azure Container Registry (ACR)
```bash
az acr create --resource-group it-helpdesk-rg --name ithelpdeskreg --sku Basic
```

### 1.3 Create AKS Cluster
```bash
az aks create \
  --resource-group it-helpdesk-rg \
  --name it-helpdesk-aks \
  --node-count 2 \
  --enable-addons monitoring \
  --generate-ssh-keys \
  --attach-acr ithelpdeskreg
```

## Step 2: Build and Push Docker Image

### 2.1 Login to ACR
```bash
az acr login --name ithelpdeskreg
```

### 2.2 Build Docker Image
```bash
docker build -t it-helpdesk:latest .
```

### 2.3 Tag Image for ACR
```bash
docker tag it-helpdesk:latest ithelpdeskreg.azurecr.io/it-helpdesk:latest
```

### 2.4 Push Image to ACR
```bash
docker push ithelpdeskreg.azurecr.io/it-helpdesk:latest
```

## Step 3: Configure kubectl

### 3.1 Get AKS Credentials
```bash
az aks get-credentials --resource-group it-helpdesk-rg --name it-helpdesk-aks
```

### 3.2 Verify Connection
```bash
kubectl get nodes
```

## Step 4: Update Kubernetes Manifests

### 4.1 Update deployment.yaml
Replace `your-registry.azurecr.io` with `ithelpdeskreg.azurecr.io` in `k8s/deployment.yaml`

### 4.2 Update secrets.yaml
Add your actual API keys and secrets in `k8s/secrets.yaml`

### 4.3 Update ingress.yaml (Optional)
Replace `your-domain.com` with your actual domain in `k8s/ingress.yaml`

## Step 5: Deploy to Kubernetes

### 5.1 Create Namespace
```bash
kubectl apply -f k8s/namespace.yaml
```

### 5.2 Create Secrets
```bash
kubectl apply -f k8s/secrets.yaml
```

### 5.3 Create Persistent Volume Claim
```bash
kubectl apply -f k8s/pvc.yaml
```

### 5.4 Deploy Application
```bash
kubectl apply -f k8s/deployment.yaml
```

### 5.5 Create Service
```bash
kubectl apply -f k8s/service.yaml
```

### 5.6 Create Ingress (Optional)
```bash
kubectl apply -f k8s/ingress.yaml
```

## Step 6: Verify Deployment

### 6.1 Check Pods
```bash
kubectl get pods -n it-helpdesk
```

### 6.2 Check Services
```bash
kubectl get services -n it-helpdesk
```

### 6.3 Check Logs
```bash
kubectl logs -f deployment/it-helpdesk-app -n it-helpdesk
```

## Step 7: Access Application

### 7.1 Port Forward (For Testing)
```bash
kubectl port-forward service/it-helpdesk-service 8501:8501 -n it-helpdesk
```
Then access: http://localhost:8501

### 7.2 Load Balancer Service (Production)
Update `k8s/service.yaml` to use `type: LoadBalancer` and get external IP:
```bash
kubectl get service it-helpdesk-service -n it-helpdesk
```

## Monitoring and Maintenance

### View Application Logs
```bash
kubectl logs -f deployment/it-helpdesk-app -n it-helpdesk
```

### Scale Application
```bash
kubectl scale deployment it-helpdesk-app --replicas=3 -n it-helpdesk
```

### Update Application
```bash
# Build and push new image
docker build -t it-helpdesk:v2 .
docker tag it-helpdesk:v2 ithelpdeskreg.azurecr.io/it-helpdesk:v2
docker push ithelpdeskreg.azurecr.io/it-helpdesk:v2

# Update deployment
kubectl set image deployment/it-helpdesk-app it-helpdesk=ithelpdeskreg.azurecr.io/it-helpdesk:v2 -n it-helpdesk
```

### Delete Resources
```bash
kubectl delete namespace it-helpdesk
az group delete --name it-helpdesk-rg --yes --no-wait
```

## Security Notes

1. **Secrets Management**: Never commit actual API keys to version control
2. **RBAC**: Configure proper role-based access control
3. **Network Policies**: Implement network policies for security
4. **Image Scanning**: Scan images for vulnerabilities
5. **Resource Limits**: Set appropriate CPU/memory limits

## Troubleshooting

### Common Issues

1. **Pod not starting**: Check logs and resource limits
2. **Image pull errors**: Verify ACR authentication
3. **Service not accessible**: Check service and ingress configuration
4. **Storage issues**: Verify PVC status

### Useful Commands
```bash
# Describe pod for detailed info
kubectl describe pod <pod-name> -n it-helpdesk

# Get events
kubectl get events -n it-helpdesk --sort-by='.lastTimestamp'

# Access pod shell
kubectl exec -it <pod-name> -n it-helpdesk -- /bin/bash
```

# IT Helpdesk Application - Azure Kubernetes Deployment Guide for Team Lead

## 📋 Quick Summary
This package contains everything needed to deploy the IT Helpdesk application on Azure Kubernetes Service (AKS). The application is a Streamlit-based AI-powered helpdesk with multilingual support.

## 📦 Package Contents
- `it-helpdesk-docker-image.tar` - Docker image file (325MB)
- `k8s/` - Kubernetes manifests
- `Dockerfile` - For rebuilding if needed
- `deploy-to-aks.ps1` - Automated deployment script (PowerShell)
- `deploy-to-aks.sh` - Automated deployment script (Bash)
- `AZURE_DEPLOYMENT.md` - Detailed deployment documentation

## 🚀 Option 1: Quick Automated Deployment (Recommended)

### Prerequisites
- Azure CLI installed and logged in
- Docker installed 
- kubectl installed
- Azure subscription with appropriate permissions

### Step 1: Load Docker Image
```powershell
docker load -i it-helpdesk-docker-image.tar
```

### Step 2: Run Deployment Script
```powershell
# For PowerShell (Windows)
.\deploy-to-aks.ps1

# For Bash (Linux/Mac)
chmod +x deploy-to-aks.sh
./deploy-to-aks.sh
```

The script will:
- Create Azure Resource Group
- Create Azure Container Registry (ACR)
- Create AKS cluster
- Push Docker image to ACR
- Deploy application to Kubernetes
- Configure all services

**Estimated time: 15-20 minutes**

## 🛠️ Option 2: Manual Step-by-Step Deployment

### Step 1: Azure Setup
```bash
# Login to Azure
az login

# Create resource group
az group create --name it-helpdesk-rg --location eastus

# Create Azure Container Registry
az acr create --resource-group it-helpdesk-rg --name ithelpdeskreg --sku Basic

# Create AKS cluster
az aks create \
  --resource-group it-helpdesk-rg \
  --name it-helpdesk-aks \
  --node-count 2 \
  --enable-addons monitoring \
  --generate-ssh-keys \
  --attach-acr ithelpdeskreg
```

### Step 2: Docker Image Setup
```bash
# Load the provided Docker image
docker load -i it-helpdesk-docker-image.tar

# Login to ACR
az acr login --name ithelpdeskreg

# Tag image for ACR
docker tag it-helpdesk:test ithelpdeskreg.azurecr.io/it-helpdesk:latest

# Push to ACR
docker push ithelpdeskreg.azurecr.io/it-helpdesk:latest
```

### Step 3: Configure kubectl
```bash
# Get AKS credentials
az aks get-credentials --resource-group it-helpdesk-rg --name it-helpdesk-aks

# Verify connection
kubectl get nodes
```

### Step 4: Update Kubernetes Manifests
Edit `k8s/deployment.yaml` and replace:
```yaml
image: your-registry.azurecr.io/it-helpdesk:latest
```
With:
```yaml
image: ithelpdeskreg.azurecr.io/it-helpdesk:latest
```

Edit `k8s/secrets.yaml` and add your actual values:
```yaml
stringData:
  GROK_API_KEY: "your_actual_grok_api_key"
  JWT_SECRET_KEY: "your_secure_random_string"
```

### Step 5: Deploy to Kubernetes
```bash
# Apply manifests in order
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/secrets.yaml
kubectl apply -f k8s/pvc.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

### Step 6: Verify Deployment
```bash
# Check pod status
kubectl get pods -n it-helpdesk

# Check service
kubectl get services -n it-helpdesk

# View logs
kubectl logs -f deployment/it-helpdesk-app -n it-helpdesk
```

## 🌐 Accessing the Application

### Option A: Port Forward (Testing)
```bash
kubectl port-forward service/it-helpdesk-service 8501:8501 -n it-helpdesk
```
Access at: http://localhost:8501

### Option B: Load Balancer (Production)
Edit `k8s/service.yaml` and change:
```yaml
type: ClusterIP
```
To:
```yaml
type: LoadBalancer
```

Then apply and get external IP:
```bash
kubectl apply -f k8s/service.yaml
kubectl get service it-helpdesk-service -n it-helpdesk
```

### Option C: Ingress with Domain (Production)
Update `k8s/ingress.yaml` with your domain and apply:
```bash
kubectl apply -f k8s/ingress.yaml
```

## 🔧 Configuration Requirements

### Required Environment Variables (in k8s/secrets.yaml)
- `GROK_API_KEY`: Your Grok AI API key (optional but recommended)
- `JWT_SECRET_KEY`: Random secure string for authentication
- `GROK_API_URL`: https://api.x.ai/v1 (default)
- `GROK_MODEL`: grok-beta (default)

### Application Features
- 🔐 Session-based authentication
- 🤖 AI-powered responses (Grok AI)
- 💬 WhatsApp-style chat interface
- 🌍 Multi-language support (13+ languages)
- 🎫 Ticket management system
- 📱 Responsive design

## 📊 Resource Requirements

### Minimum Requirements
- **CPU**: 500m (0.5 cores) per pod
- **Memory**: 512Mi per pod
- **Storage**: 1Gi for persistent data
- **Pods**: 2 replicas (configurable)

### Scaling
```bash
# Scale to 3 replicas
kubectl scale deployment it-helpdesk-app --replicas=3 -n it-helpdesk

# Auto-scaling (optional)
kubectl autoscale deployment it-helpdesk-app --cpu-percent=70 --min=2 --max=10 -n it-helpdesk
```

## 🔍 Troubleshooting

### Common Issues

1. **Pod not starting**
   ```bash
   kubectl describe pod <pod-name> -n it-helpdesk
   kubectl logs <pod-name> -n it-helpdesk
   ```

2. **Image pull errors**
   ```bash
   # Verify ACR connection
   az acr login --name ithelpdeskreg
   kubectl get secret acr-secret -n it-helpdesk
   ```

3. **Service not accessible**
   ```bash
   kubectl get endpoints -n it-helpdesk
   kubectl port-forward service/it-helpdesk-service 8501:8501 -n it-helpdesk
   ```

### Health Checks
The application includes built-in health checks at:
- `http://pod-ip:8501/_stcore/health`

### Monitoring
```bash
# Watch pod status
kubectl get pods -n it-helpdesk -w

# View recent events
kubectl get events -n it-helpdesk --sort-by='.lastTimestamp'

# Resource usage
kubectl top pods -n it-helpdesk
```

## 🗑️ Cleanup (When needed)
```bash
# Delete application
kubectl delete namespace it-helpdesk

# Delete Azure resources
az group delete --name it-helpdesk-rg --yes --no-wait
```

## 📞 Support Information

- **GitHub Repository**: https://github.com/Nahid305/it_helpdesk_app
- **Application Type**: Streamlit Web Application
- **Docker Base Image**: python:3.11-slim
- **Deployment Method**: Kubernetes on Azure AKS

## 🎯 Quick Validation Checklist

After deployment, verify:
- [ ] Pods are running: `kubectl get pods -n it-helpdesk`
- [ ] Service is active: `kubectl get svc -n it-helpdesk`
- [ ] Application responds: Port-forward and access http://localhost:8501
- [ ] Health check passes: curl http://localhost:8501/_stcore/health
- [ ] Authentication works: Try logging in with test credentials
- [ ] AI responses work: Test chat functionality

## 📋 Default Login Credentials
The application includes default credentials for testing:
- **Username**: admin
- **Password**: admin123

⚠️ **Security Note**: Change default credentials in production by updating the user data files.

---

**Total Deployment Time**: 15-25 minutes (depending on Azure resource creation)
**Application URL**: Will be provided after successful deployment

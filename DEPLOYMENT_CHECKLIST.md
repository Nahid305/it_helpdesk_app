# IT Helpdesk AKS Deployment - Quick Checklist

## 📋 Pre-Deployment Checklist
- [ ] Azure CLI installed and configured (`az --version`)
- [ ] Docker installed and running (`docker --version`)
- [ ] kubectl installed (`kubectl version --client`)
- [ ] Azure subscription access confirmed (`az account show`)
- [ ] Required permissions for creating Azure resources

## 🚀 Deployment Steps Checklist

### Phase 1: Load Docker Image
- [ ] Navigate to project directory
- [ ] Load Docker image: `docker load -i it-helpdesk-docker-image.tar`
- [ ] Verify image loaded: `docker images | grep it-helpdesk`

### Phase 2: Azure Setup (Automated Script)
- [ ] Run deployment script: `.\deploy-to-aks.ps1` (Windows) or `./deploy-to-aks.sh` (Linux/Mac)
- [ ] Wait for script completion (15-20 minutes)
- [ ] Verify resources created in Azure portal

### Phase 3: Configuration
- [ ] Update `k8s/secrets.yaml` with actual API keys
- [ ] Apply updated secrets: `kubectl apply -f k8s/secrets.yaml`

### Phase 4: Verification
- [ ] Check pods running: `kubectl get pods -n it-helpdesk`
- [ ] Check services: `kubectl get svc -n it-helpdesk`
- [ ] Port forward: `kubectl port-forward service/it-helpdesk-service 8501:8501 -n it-helpdesk`
- [ ] Access application: http://localhost:8501
- [ ] Test login with admin/admin123
- [ ] Test chat functionality

## 🔧 Post-Deployment Tasks
- [ ] Configure external access (LoadBalancer or Ingress)
- [ ] Set up monitoring and logging
- [ ] Update default credentials
- [ ] Configure backup strategy
- [ ] Document access URLs for team

## 🚨 Emergency Contacts
- **Developer**: [Your contact information]
- **Repository**: https://github.com/Nahid305/it_helpdesk_app
- **Documentation**: See TEAM_LEAD_DEPLOYMENT_GUIDE.md

## 📊 Expected Resources Created
- Resource Group: `it-helpdesk-rg`
- Container Registry: `ithelpdeskreg`
- AKS Cluster: `it-helpdesk-aks`
- Kubernetes Namespace: `it-helpdesk`
- Pods: 2 replicas
- Service: ClusterIP on port 8501
- Storage: 1Gi persistent volume

## ⏱️ Estimated Timeline
- Azure resource creation: 10-15 minutes
- Docker image push: 2-5 minutes
- Kubernetes deployment: 2-3 minutes
- **Total**: 15-25 minutes

---
**Last Updated**: September 11, 2025
**Version**: 1.0

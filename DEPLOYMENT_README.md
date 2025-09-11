# IT Helpdesk Application - Azure Kubernetes Deployment Package

## 📦 What's Included
This package contains everything needed to deploy the IT Helpdesk application on Azure Kubernetes Service.

## 🎯 Quick Start (For Team Lead)
1. **Load Docker Image**: `docker load -i it-helpdesk-docker-image.tar`
2. **Run Deployment**: `.\deploy-to-aks.ps1` (PowerShell) or `./deploy-to-aks.sh` (Bash)
3. **Access App**: Follow the on-screen instructions

## 📋 Files Overview
- `it-helpdesk-docker-image.tar` - Pre-built Docker image (325MB)
- `TEAM_LEAD_DEPLOYMENT_GUIDE.md` - Complete deployment guide
- `DEPLOYMENT_CHECKLIST.md` - Quick checklist
- `deploy-to-aks.ps1` / `deploy-to-aks.sh` - Automated deployment scripts
- `k8s/` - Kubernetes manifests
- `Dockerfile` - For custom builds

## ⚡ Prerequisites
- Azure CLI
- Docker
- kubectl
- Azure subscription

## 🎯 Application Features
- AI-powered IT helpdesk
- Multi-language support (13+ languages)
- WhatsApp-style chat interface
- Ticket management system
- Secure authentication

## 📞 Support
- Repository: https://github.com/Nahid305/it_helpdesk_app
- Contact: [Your contact information]

---
**Deployment Time**: ~20 minutes | **Default Port**: 8501

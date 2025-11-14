#!/bin/bash

# Azure Deployment Script using Azure Container Registry
# Resource Group: lana-dev-01

set -e

echo "🚀 Deploying Agent Framework DevUI to Azure..."

# Configuration
RESOURCE_GROUP="lana-dev-01"
APP_NAME="ignite-agent-framework"
PLAN_NAME="ignite-agents-plan"
ACR_NAME="igniteagentsacr"
IMAGE_NAME="agent-framework:latest"

echo "📦 Creating Azure Container Registry..."
az acr create \
  --resource-group $RESOURCE_GROUP \
  --name $ACR_NAME \
  --sku Basic \
  --admin-enabled true \
  --output none 2>/dev/null || echo "ACR already exists"

echo "🔨 Building and pushing to ACR..."
az acr build \
  --registry $ACR_NAME \
  --image $IMAGE_NAME \
  .

echo "☁️  Deploying to Azure..."

# Create App Service Plan (skip if exists)
az appservice plan create \
  --name $PLAN_NAME \
  --resource-group $RESOURCE_GROUP \
  --sku B1 \
  --is-linux \
  --output none 2>/dev/null || echo "App Service Plan already exists"

# Create Web App with ACR image
az webapp create \
  --resource-group $RESOURCE_GROUP \
  --plan $PLAN_NAME \
  --name $APP_NAME \
  --deployment-container-image-name ${ACR_NAME}.azurecr.io/${IMAGE_NAME} \
  --output none

# Configure basic settings
az webapp config appsettings set \
  --resource-group $RESOURCE_GROUP \
  --name $APP_NAME \
  --settings \
    ENTITIES_DIR="./agents" \
    MODE="user" \
    HOST="0.0.0.0" \
    PORT="8080" \
    AUTH_ENABLED="false" \
    LOG_LEVEL="INFO" \
    WEBSITES_ENABLE_APP_SERVICE_STORAGE="false" \
  --output none

# Get the app URL
APP_URL=$(az webapp show \
  --resource-group $RESOURCE_GROUP \
  --name $APP_NAME \
  --query "defaultHostName" \
  --output tsv)

echo "✅ Deployment completed!"
echo "🌐 Your DevUI is available at: https://$APP_URL"
echo ""
echo "📝 Optional: Add API keys if needed:"
echo "az webapp config appsettings set --resource-group $RESOURCE_GROUP --name $APP_NAME --settings OPENAI_API_KEY=\"your-key\""

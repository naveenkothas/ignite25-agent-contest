#!/bin/bash

# Azure Deployment Script for Agent Framework
# Resource Group: lana-dev-01

set -e

echo "🚀 Starting Azure deployment for Agent Framework..."

# Configuration
RESOURCE_GROUP="lana-dev-01"
APP_NAME="ignite-agent-framework"
PLAN_NAME="ignite-agents-plan"
IMAGE_NAME="naveenkothas/ignite-agent-framework:latest"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}📦 Step 1: Building Docker image...${NC}"
docker build -t $IMAGE_NAME .

echo -e "${BLUE}🔐 Step 2: Pushing to Docker Hub...${NC}"
echo "Please make sure you're logged in to Docker Hub (run 'docker login' if needed)"
docker push $IMAGE_NAME

echo -e "${BLUE}☁️  Step 3: Deploying to Azure...${NC}"

# Check if logged in to Azure
if ! az account show >/dev/null 2>&1; then
    echo -e "${YELLOW}Please login to Azure first:${NC}"
    az login
fi

echo -e "${GREEN}Creating App Service Plan...${NC}"
az appservice plan create \
  --name $PLAN_NAME \
  --resource-group $RESOURCE_GROUP \
  --sku B1 \
  --is-linux \
  --output table

echo -e "${GREEN}Creating Web App...${NC}"
az webapp create \
  --resource-group $RESOURCE_GROUP \
  --plan $PLAN_NAME \
  --name $APP_NAME \
  --deployment-container-image-name $IMAGE_NAME \
  --output table

echo -e "${GREEN}Configuring app settings...${NC}"
az webapp config appsettings set \
  --resource-group $RESOURCE_GROUP \
  --name $APP_NAME \
  --settings \
    ENTITIES_DIR="./agents" \
    MODE="user" \
    HOST="0.0.0.0" \
    PORT="8080" \
    AUTH_ENABLED="true" \
    LOG_LEVEL="INFO" \
    WEBSITES_ENABLE_APP_SERVICE_STORAGE="false" \
  --output table

echo -e "${YELLOW}⚠️  IMPORTANT: Add your API keys manually:${NC}"
echo -e "${YELLOW}Run this command with your actual API keys:${NC}"
echo ""
echo "az webapp config appsettings set \\"
echo "  --resource-group $RESOURCE_GROUP \\"
echo "  --name $APP_NAME \\"
echo "  --settings \\"
echo "    OPENAI_API_KEY=\"your-openai-api-key-here\" \\"
echo "    AZURE_OPENAI_API_KEY=\"your-azure-openai-key-here\" \\"
echo "    AZURE_OPENAI_ENDPOINT=\"https://your-resource.openai.azure.com/\""
echo ""

# Get the app URL
APP_URL=$(az webapp show \
  --resource-group $RESOURCE_GROUP \
  --name $APP_NAME \
  --query "defaultHostName" \
  --output tsv)

echo -e "${GREEN}✅ Deployment completed!${NC}"
echo -e "${GREEN}🌐 Your app will be available at: https://$APP_URL${NC}"
echo -e "${YELLOW}📝 Don't forget to add your API keys using the command above!${NC}"

echo ""
echo -e "${BLUE}📊 To view logs:${NC}"
echo "az webapp log tail --resource-group $RESOURCE_GROUP --name $APP_NAME"
echo ""
echo -e "${BLUE}🔧 To update the container:${NC}"
echo "az webapp config container set --resource-group $RESOURCE_GROUP --name $APP_NAME --docker-custom-image-name $IMAGE_NAME"

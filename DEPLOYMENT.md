# Azure App Service Deployment Guide

This guide explains how to deploy the Agent Framework to Azure App Service using Docker containers.

## Prerequisites

- Azure subscription
- Docker Hub account (or Azure Container Registry)
- Azure CLI installed locally
- Git repository with the code

## Deployment Options

### Option 1: Manual Deployment via Azure Portal

1. **Build and Push Docker Image**
   ```bash
   # Build the image
   docker build -t naveenkothas/ignite-agent-framework:latest .
   
   # Push to Docker Hub
   docker push naveenkothas/ignite-agent-framework:latest
   ```

2. **Create Azure Resources**
   - Go to Azure Portal
   - Create a new "Web App"
   - Choose "Docker Container" as publish option
   - Select "Linux" as OS
   - Choose your subscription and resource group
   - Configure the app:
     - Name: `ignite-agent-framework` (or your preferred name)
     - Region: Choose closest to your users
     - Pricing tier: B1 or higher recommended
     - Docker settings:
       - Image Source: Docker Hub
       - Image: `naveenkothas/ignite-agent-framework:latest`

3. **Configure Environment Variables**
   In the App Service Configuration section, add these application settings:
   ```
   ENTITIES_DIR=./agents
   MODE=user
   HOST=0.0.0.0
   PORT=8080
   AUTH_ENABLED=true
   LOG_LEVEL=INFO
   OPENAI_API_KEY=your-openai-api-key
   AZURE_OPENAI_API_KEY=your-azure-openai-key
   AZURE_OPENAI_ENDPOINT=your-azure-endpoint
   ```

### Option 2: Azure CLI Deployment

1. **Login to Azure**
   ```bash
   az login
   ```

2. **Create Resource Group**
   ```bash
   az group create --name ignite-agents-rg --location "East US"
   ```

3. **Create App Service Plan**
   ```bash
   az appservice plan create \
     --name ignite-agents-plan \
     --resource-group ignite-agents-rg \
     --sku B1 \
     --is-linux
   ```

4. **Create Web App**
   ```bash
   az webapp create \
     --resource-group ignite-agents-rg \
     --plan ignite-agents-plan \
     --name ignite-agent-framework \
     --deployment-container-image-name naveenkothas/ignite-agent-framework:latest
   ```

5. **Configure App Settings**
   ```bash
   az webapp config appsettings set \
     --resource-group ignite-agents-rg \
     --name ignite-agent-framework \
     --settings \
       ENTITIES_DIR="./agents" \
       MODE="user" \
       HOST="0.0.0.0" \
       PORT="8080" \
       AUTH_ENABLED="true" \
       LOG_LEVEL="INFO"
   ```

### Option 3: ARM Template Deployment

Use the provided `azure-deploy.json` template:

```bash
az deployment group create \
  --resource-group ignite-agents-rg \
  --template-file azure-deploy.json \
  --parameters appName=ignite-agent-framework
```

### Option 4: GitHub Actions CI/CD

1. **Set up GitHub Secrets**
   In your GitHub repository settings, add these secrets:
   - `DOCKER_USERNAME`: Your Docker Hub username
   - `DOCKER_PASSWORD`: Your Docker Hub password/token
   - `AZURE_CREDENTIALS`: Azure service principal credentials

2. **Create Service Principal**
   ```bash
   az ad sp create-for-rbac \
     --name "ignite-agents-sp" \
     --role contributor \
     --scopes /subscriptions/{subscription-id}/resourceGroups/ignite-agents-rg \
     --sdk-auth
   ```
   Copy the output JSON to `AZURE_CREDENTIALS` secret.

3. **Copy GitHub Actions Workflow**
   Copy `deploy.yml` to `.github/workflows/deploy.yml` in your repository.

4. **Push to Main Branch**
   The deployment will trigger automatically on push to main branch.

## Environment Configuration

### Required Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `ENTITIES_DIR` | Path to agents directory | `./agents` |
| `MODE` | Application mode (user/admin) | `user` |
| `HOST` | Host to bind to | `0.0.0.0` |
| `PORT` | Port to listen on | `8080` |
| `AUTH_ENABLED` | Enable authentication | `true` |

### Optional Environment Variables

| Variable | Description |
|----------|-------------|
| `OPENAI_API_KEY` | OpenAI API key for AI models |
| `AZURE_OPENAI_API_KEY` | Azure OpenAI API key |
| `AZURE_OPENAI_ENDPOINT` | Azure OpenAI endpoint URL |
| `LOG_LEVEL` | Logging level (DEBUG, INFO, WARNING, ERROR) |
| `SECRET_KEY` | Secret key for session management |

## Local Testing

Before deploying, test the application locally:

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up Environment**
   ```bash
   cp env.template .env
   # Edit .env with your values
   ```

3. **Run Locally**
   ```bash
   # Option 1: Using devui directly
   devui ./agents --host 0.0.0.0 --port 8080 --mode user --auth
   
   # Option 2: Using the app.py wrapper
   python app.py
   
   # Option 3: Using Docker
   docker build -t agent-framework .
   docker run -p 8080:8080 --env-file .env agent-framework
   ```

4. **Access Application**
   Open http://localhost:8080 in your browser

## Troubleshooting

### Common Issues

1. **Container fails to start**
   - Check application logs in Azure Portal
   - Verify Docker image exists and is accessible
   - Check environment variables are set correctly

2. **Authentication issues**
   - Ensure `AUTH_ENABLED` is set correctly
   - Check if `SECRET_KEY` is configured for production

3. **Agent loading issues**
   - Verify agents directory structure
   - Check agent configuration files (config.yaml)
   - Review application logs for specific errors

### Viewing Logs

```bash
# Stream logs from Azure CLI
az webapp log tail --resource-group ignite-agents-rg --name ignite-agent-framework

# Download logs
az webapp log download --resource-group ignite-agents-rg --name ignite-agent-framework
```

## Security Considerations

1. **Environment Variables**: Never commit sensitive data like API keys to git
2. **HTTPS**: Azure App Service provides HTTPS by default
3. **Authentication**: Enable authentication for production deployments
4. **Network Security**: Consider using Azure Private Endpoints for enhanced security
5. **Monitoring**: Set up Application Insights for monitoring and alerting

## Scaling

- **Vertical Scaling**: Upgrade App Service Plan SKU (B1 → B2 → B3 → S1, etc.)
- **Horizontal Scaling**: Enable auto-scaling rules based on CPU/memory usage
- **Performance**: Consider using Azure CDN for static content

## Cost Optimization

- Use **F1 (Free)** tier for development/testing
- Use **B1 (Basic)** for small production workloads
- Monitor usage with Azure Cost Management
- Set up billing alerts

## Support

For issues related to:
- **Agent Framework**: Check the agent-framework-devui documentation
- **Azure Deployment**: Consult Azure App Service documentation
- **This Implementation**: Check the project repository issues

# Agent Framework Project Structure

This project contains a complete agent framework setup ready for deployment to Azure App Service.

## 📁 Project Structure

```
ignite25-agent-contest/
├── agents/                          # Agents directory
│   ├── assistant_agent/            # General AI assistant agent
│   │   ├── config.yaml             # Agent configuration
│   │   └── main.py                 # Agent implementation
│   └── shipment_agent/             # Logistics/shipment agent
│       ├── config.yaml             # Agent configuration
│       └── logic.py                # Agent business logic
├── .dockerignore                   # Docker ignore file
├── .github/workflows/              # GitHub Actions (optional)
│   └── deploy.yml                  # CI/CD pipeline
├── app.py                          # Main application entry point
├── azure-deploy.json               # Azure ARM template
├── DEPLOYMENT.md                   # Deployment instructions
├── Dockerfile                      # Docker configuration
├── env.template                    # Environment variables template
├── PROJECT_STRUCTURE.md            # This file
├── requirements.txt                # Python dependencies
└── startup.sh                      # Azure App Service startup script
```

## 🤖 Available Agents

### 1. Assistant Agent (`assistant_agent`)
- **Purpose**: General AI assistant for queries and support
- **Model**: GPT-4o-mini (configurable)
- **Capabilities**: Text generation, Q&A, task assistance, conversation
- **Configuration**: `agents/assistant_agent/config.yaml`
- **Implementation**: `agents/assistant_agent/main.py`

### 2. Shipment Agent (`shipment_agent`)
- **Purpose**: Logistics and supply chain operations
- **Model**: GPT-4o (configurable)
- **Capabilities**: Shipment tracking, route optimization, delivery estimation
- **Configuration**: `agents/shipment_agent/config.yaml`
- **Implementation**: `agents/shipment_agent/logic.py`

## 🚀 Quick Start

### Local Development

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Setup Environment**
   ```bash
   cp env.template .env
   # Edit .env with your API keys and configuration
   ```

3. **Run the Application**
   ```bash
   # Option 1: Direct devui command
   devui ./agents --host 0.0.0.0 --port 8080 --mode user --auth
   
   # Option 2: Using app.py wrapper
   python3 app.py
   ```

4. **Access the UI**
   Open http://localhost:8080 in your browser

### Test Agents Individually

```bash
# Test assistant agent
python3 agents/assistant_agent/main.py

# Test shipment agent
python3 agents/shipment_agent/logic.py
```

## ☁️ Azure Deployment

### Prerequisites
- Azure subscription
- Docker Hub account
- Azure CLI

### Deployment Methods

1. **Docker + Azure Portal** (Recommended for beginners)
2. **Azure CLI** (For automation)
3. **ARM Template** (For infrastructure as code)
4. **GitHub Actions** (For CI/CD)

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

### Quick Deploy with Azure CLI

```bash
# Build and push Docker image
docker build -t yourusername/ignite-agent-framework:latest .
docker push yourusername/ignite-agent-framework:latest

# Deploy to Azure
az group create --name ignite-agents-rg --location "East US"
az appservice plan create --name ignite-agents-plan --resource-group ignite-agents-rg --sku B1 --is-linux
az webapp create --resource-group ignite-agents-rg --plan ignite-agents-plan --name your-app-name --deployment-container-image-name yourusername/ignite-agent-framework:latest
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `ENTITIES_DIR` | Path to agents directory | `./agents` |
| `MODE` | Application mode (user/admin) | `user` |
| `HOST` | Host to bind to | `0.0.0.0` |
| `PORT` | Port to listen on | `8080` |
| `AUTH_ENABLED` | Enable authentication | `true` |
| `OPENAI_API_KEY` | OpenAI API key | Required |
| `LOG_LEVEL` | Logging level | `INFO` |

### Agent Configuration

Each agent has its own `config.yaml` file with:
- Model selection and parameters
- Capabilities and features
- Environment variables
- Agent-specific settings

## 🔒 Security

- Environment variables are not committed to git
- Authentication is enabled by default in production
- Docker container runs as non-root user
- Secrets should be managed through Azure Key Vault or App Service configuration

## 📊 Monitoring

- Application logs available in Azure Portal
- Health check endpoint: `/health`
- Structured logging with configurable levels
- Ready for Application Insights integration

## 🛠️ Development

### Adding New Agents

1. Create new directory in `agents/`
2. Add `config.yaml` with agent configuration
3. Implement agent logic in Python file
4. Test locally before deployment

### Customization

- Modify `requirements.txt` for additional dependencies
- Update `Dockerfile` for custom setup
- Adjust `startup.sh` for custom initialization
- Configure environment variables in `env.template`

## 🆘 Troubleshooting

### Common Issues

1. **Port conflicts**: Change `PORT` environment variable
2. **Agent loading errors**: Check `config.yaml` syntax
3. **Docker build failures**: Verify `requirements.txt`
4. **Azure deployment issues**: Check application logs

### Getting Help

1. Check [DEPLOYMENT.md](DEPLOYMENT.md) for deployment issues
2. Review Azure App Service logs
3. Test agents individually for debugging
4. Validate configuration files

## 📝 License

This project is part of the Microsoft Ignite 2025 Agent Contest. See the original repository for licensing information.

## 🎯 Contest Context

This agent framework is designed for the **Mission Agent Possible** contest at Microsoft Ignite 2025, focusing on:
- Smart model selection
- Crisis response scenarios
- Effective agent design
- Production-ready deployment

The framework provides a solid foundation for building contest-winning agents! 🏆

# 🤖 Agent Framework - IT Outage Management System

**Microsoft Ignite 2025 Contest Entry**

An intelligent multi-agent system for IT outage management, built with the Microsoft Agent Framework.

## 🎥 Demo

Check out our demo video: [`demo/Demo.mp4`](demo/Demo.mp4)

## 🏗️ Architecture

### 🤖 Intelligent Agents

- **🔍 Analysis Agent** - AI-powered root cause analysis using Azure OpenAI
- **🎯 Triage Agent** - Intelligent incident prioritization and severity assessment  
- **📊 Monitoring Agent** - Real-time system monitoring and alerting
- **🚨 Crisis Manager** - Emergency response coordination and crisis management

### 📁 Project Structure

```
├── 📂 src/
│   ├── 📂 agents/          # Agent implementations
│   └── 📂 utils/           # Utility functions and tools
├── 📂 demo/                # Demo video and assets
├── 📂 docs/                # Documentation
├── 📂 deployment/          # Deployment configurations
├── 📂 deployments/         # Azure deployment tools
├── 📄 requirements.txt     # Python dependencies
└── 📄 .env.example        # Environment configuration template
```

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Clone the repository
git clone <your-repo-url>
cd ignite25-agent-contest

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Azure OpenAI

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your Azure OpenAI credentials
# AZURE_OPENAI_API_KEY=your-key-here
# AZURE_OPENAI_ENDPOINT=https://your-endpoint.openai.azure.com
```

### 3. Run Locally

```bash
# Start the Agent Framework DevUI
devui src/agents --host 0.0.0.0 --port 8080 --mode user

# Open browser to http://localhost:8080
```

## 🌐 Azure Deployment

Deploy to Azure Container Apps:

```bash
cd deployment
chmod +x deploy-to-azure.sh
./deploy-to-azure.sh
```

## 🎯 Features

- ✅ **Multi-Agent Coordination** - Specialized agents working together
- ✅ **Azure OpenAI Integration** - GPT-powered analysis and responses
- ✅ **Real-time Monitoring** - Live system health tracking
- ✅ **Incident Management** - Complete triage and response workflow
- ✅ **Container Ready** - Docker support for easy deployment
- ✅ **Azure Native** - Optimized for Azure cloud services

## 🏆 Microsoft Ignite Contest

This project demonstrates the power of the Microsoft Agent Framework for building intelligent, coordinated AI systems for enterprise IT operations.

**Key Innovations:**
- Intelligent agent orchestration for complex IT scenarios
- Real-time incident response automation
- Azure OpenAI-powered root cause analysis
- Scalable cloud-native architecture

---

*Built with ❤️ for Microsoft Ignite 2025*

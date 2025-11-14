"""
Assistant Agent - Main implementation
Handles general queries and provides AI assistance
"""

import os
import yaml
import logging
from typing import Dict, Any, Optional
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AssistantAgent:
    """Main Assistant Agent class"""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize the assistant agent"""
        if config_path is None:
            config_path = Path(__file__).parent / "config.yaml"
        
        self.config = self._load_config(config_path)
        self.setup_agent()
    
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load agent configuration from YAML file"""
        try:
            with open(config_path, 'r') as file:
                config = yaml.safe_load(file)
            logger.info(f"Loaded configuration for {config.get('name', 'assistant_agent')}")
            return config
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
            return {}
    
    def setup_agent(self):
        """Setup the agent with configuration"""
        self.name = self.config.get('name', 'assistant_agent')
        self.model = self.config.get('settings', {}).get('model', 'gpt-4o-mini')
        self.temperature = self.config.get('settings', {}).get('temperature', 0.7)
        
        # Setup environment variables
        env_vars = self.config.get('environment', {})
        for key, value in env_vars.items():
            if key not in os.environ and not value.startswith('${'):
                os.environ[key] = str(value)
        
        logger.info(f"Agent {self.name} initialized with model {self.model}")
    
    def process_message(self, message: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Process incoming message and return response"""
        try:
            # This is a placeholder - in a real implementation, you'd integrate with
            # your chosen AI model (OpenAI, Azure OpenAI, etc.)
            
            response = {
                "agent": self.name,
                "message": f"Hello! I'm your assistant agent. You said: '{message}'. How can I help you today?",
                "status": "success",
                "model_used": self.model,
                "context": context or {}
            }
            
            logger.info(f"Processed message from {self.name}")
            return response
            
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            return {
                "agent": self.name,
                "message": "Sorry, I encountered an error processing your request.",
                "status": "error",
                "error": str(e)
            }
    
    def get_capabilities(self) -> Dict[str, Any]:
        """Return agent capabilities"""
        return {
            "name": self.name,
            "capabilities": self.config.get('capabilities', []),
            "model": self.model,
            "description": self.config.get('description', 'AI Assistant Agent')
        }

def main():
    """Main function for testing the agent"""
    agent = AssistantAgent()
    
    # Test the agent
    test_message = "Hello, how are you?"
    response = agent.process_message(test_message)
    
    print(f"Agent Response: {response}")
    print(f"Agent Capabilities: {agent.get_capabilities()}")

if __name__ == "__main__":
    main()

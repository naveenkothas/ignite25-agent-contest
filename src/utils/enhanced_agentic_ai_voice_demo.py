# enhanced_agentic_ai_demo.py
import os
import asyncio
import time
import sys
import random
import json
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from enum import Enum
from flask import Flask, render_template_string, request, jsonify
from flask_socketio import SocketIO
import threading
import requests
from dotenv import load_dotenv
import uuid
import base64
import io

# Try to import Microsoft Agent Framework
try:
    from agent_framework import AgentRunResponseUpdate, ChatAgent, ChatMessage, FunctionResultContent, Role
    from agent_framework.azure import AzureOpenAIChatClient

    AGENT_FRAMEWORK_AVAILABLE = True
except ImportError:
    AGENT_FRAMEWORK_AVAILABLE = False
    print("⚠️ Microsoft Agent Framework not available - using enhanced mock implementations")

load_dotenv()


# ------------------------------------------------------------
# 0. Enhanced Logging Configuration
# ------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()  # This ensures logs go to stdout/stderr
    ]
)

# Create logger instances for different components
logger = logging.getLogger('agentic_ai_demo')
agent_logger = logging.getLogger('agentic_ai_agents')
system_logger = logging.getLogger('agentic_ai_system')

# Set levels
logger.setLevel(logging.INFO)
agent_logger.setLevel(logging.INFO)
system_logger.setLevel(logging.INFO)

def setup_logging():
    # Force flush after each log
    for handler in logging.getLogger().handlers:
        handler.flush = sys.stdout.flush




# ------------------------------------------------------------
# 1. Flask Application Setup
# ------------------------------------------------------------
app = Flask(__name__)
app.secret_key = 'enhanced_agentic_ai_demo_secret_key'
socketio = SocketIO(app, cors_allowed_origins="*")

# ------------------------------------------------------------
# 2. Configuration and Data
# ------------------------------------------------------------

# Sample product database
PRODUCTS = [
    # Electronics (15 products)
    {"id": 1, "name": "Wireless Bluetooth Headphones", "category": "Electronics", "price": 129.99,
     "description": "Noise-cancelling wireless headphones with 30hr battery", "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=300&fit=crop"},
    {"id": 2, "name": "Smart Fitness Watch", "category": "Electronics", "price": 199.99,
     "description": "Track your heart rate, sleep, and workouts", "image": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400&h=300&fit=crop"},
    {"id": 3, "name": "Gaming Mechanical Keyboard", "category": "Electronics", "price": 89.99,
     "description": "RGB mechanical keyboard with customizable keys", "image": "https://images.unsplash.com/photo-1541140532154-b024d705b90a?w=400&h=300&fit=crop"},
    {"id": 4, "name": "Wireless Gaming Mouse", "category": "Electronics", "price": 59.99,
     "description": "High-precision wireless gaming mouse with RGB lighting", "image": "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=400&h=300&fit=crop"},
    {"id": 5, "name": "4K Ultra HD Smart TV", "category": "Electronics", "price": 499.99,
     "description": "55-inch 4K Smart TV with HDR and streaming apps", "image": "https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?w=400&h=300&fit=crop"},
    {"id": 6, "name": "Wireless Earbuds Pro", "category": "Electronics", "price": 149.99,
     "description": "True wireless earbuds with active noise cancellation", "image": "https://images.unsplash.com/photo-1606220945770-b5b6c2c55bf1?w=400&h=300&fit=crop"},
    {"id": 7, "name": "Tablet Pro 12.9-inch", "category": "Electronics", "price": 899.99,
     "description": "Professional tablet with stylus for creative work", "image": "https://images.unsplash.com/photo-1561154464-82e9adf32764?w=400&h=300&fit=crop"},
    {"id": 8, "name": "Digital Camera DSLR", "category": "Electronics", "price": 699.99,
     "description": "24MP DSLR camera with 4K video and kit lens", "image": "https://images.unsplash.com/photo-1502920917128-1aa500764cbd?w=400&h=300&fit=crop"},
    {"id": 9, "name": "Portable Bluetooth Speaker", "category": "Electronics", "price": 79.99,
     "description": "Waterproof Bluetooth speaker with 20hr battery", "image": "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=400&h=300&fit=crop"},
    {"id": 10, "name": "Gaming Laptop RTX 4060", "category": "Electronics", "price": 1299.99,
     "description": "High-performance gaming laptop with RTX graphics", "image": "https://images.unsplash.com/photo-1603302576837-37561b2e2302?w=400&h=300&fit=crop"},
    {"id": 11, "name": "Smart Home Hub", "category": "Electronics", "price": 89.99,
     "description": "Voice-controlled smart home hub with Alexa", "image": "https://picsum.photos/id/119/400/300"},
    {"id": 12, "name": "Wireless Charging Pad", "category": "Electronics", "price": 29.99,
     "description": "Fast wireless charging pad for smartphones", "image": "https://picsum.photos/id/160/400/300"},
    {"id": 13, "name": "Noise Cancelling Headphones", "category": "Electronics", "price": 299.99,
     "description": "Premium over-ear headphones with ANC", "image": "https://images.unsplash.com/photo-1583394838336-acd977736f90?w=400&h=300&fit=crop"},
    {"id": 14, "name": "Smartphone Pro Max", "category": "Electronics", "price": 1099.99,
     "description": "Latest smartphone with triple camera system", "image": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400&h=300&fit=crop"},
    {"id": 15, "name": "VR Headset Gaming", "category": "Electronics", "price": 399.99,
     "description": "Virtual reality headset for immersive gaming", "image": "https://images.unsplash.com/photo-1593508512255-86ab42a8e620?w=400&h=300&fit=crop"},

    # Clothing & Fashion (10 products)
    {"id": 16, "name": "Organic Cotton T-Shirt", "category": "Clothing", "price": 24.99,
     "description": "Comfortable organic cotton t-shirt in multiple colors", "image": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&h=300&fit=crop"},
    {"id": 17, "name": "Denim Jacket", "category": "Clothing", "price": 79.99,
     "description": "Classic denim jacket for casual wear", "image": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400&h=300&fit=crop"},
    {"id": 18, "name": "Running Shoes", "category": "Clothing", "price": 119.99,
     "description": "Lightweight running shoes with cushion technology", "image": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&h=300&fit=crop"},
    {"id": 19, "name": "Winter Parka Jacket", "category": "Clothing", "price": 199.99,
     "description": "Warm winter parka with waterproof coating", "image": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400&h=300&fit=crop"},
    {"id": 20, "name": "Casual Sneakers", "category": "Clothing", "price": 89.99,
     "description": "Comfortable everyday sneakers in various colors", "image": "https://images.unsplash.com/photo-1460353581641-37baddab0fa2?w=400&h=300&fit=crop"},
    {"id": 21, "name": "Leather Handbag", "category": "Clothing", "price": 149.99,
     "description": "Genuine leather handbag with multiple compartments", "image": "https://images.unsplash.com/photo-1584917865442-de89df76afd3?w=400&h=300&fit=crop"},
    {"id": 22, "name": "Sports Leggings", "category": "Clothing", "price": 39.99,
     "description": "High-waist sports leggings for workout and yoga", "image": "https://picsum.photos/id/21/400/300"},
    {"id": 23, "name": "Designer Sunglasses", "category": "Clothing", "price": 159.99,
     "description": "UV protection sunglasses with polarized lenses", "image": "https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=400&h=300&fit=crop"},
    {"id": 24, "name": "Wool Sweater", "category": "Clothing", "price": 69.99,
     "description": "100% merino wool sweater for cold weather", "image": "https://images.unsplash.com/photo-1434389677669-e08b4cac3105?w=400&h=300&fit=crop"},
    {"id": 25, "name": "Formal Dress Shirt", "category": "Clothing", "price": 49.99,
     "description": "Classic formal dress shirt for business occasions", "image": "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=400&h=300&fit=crop"},

    # Sports & Outdoors (8 products)
    {"id": 26, "name": "Stainless Steel Water Bottle", "category": "Sports", "price": 34.99,
     "description": "Keep your drinks cold for 24 hours or hot for 12", "image": "https://images.unsplash.com/photo-1523362628745-0c100150b504?w=400&h=300&fit=crop"},
    {"id": 27, "name": "Yoga Mat Premium", "category": "Sports", "price": 45.99,
     "description": "Non-slip yoga mat with carrying strap", "image": "https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=400&h=300&fit=crop"},
    {"id": 28, "name": "Camping Tent 4-Person", "category": "Sports", "price": 149.99,
     "description": "Waterproof camping tent for family outdoor trips", "image": "https://images.unsplash.com/photo-1504851149312-7a075b496cc7?w=400&h=300&fit=crop"},
    {"id": 29, "name": "Mountain Bike", "category": "Sports", "price": 599.99,
     "description": "21-speed mountain bike with suspension fork", "image": "https://images.unsplash.com/photo-1485965120184-e220f721d03e?w=400&h=300&fit=crop"},
    {"id": 30, "name": "Fitness Dumbbell Set", "category": "Sports", "price": 129.99,
     "description": "Adjustable dumbbell set for home workouts", "image": "https://images.unsplash.com/photo-1534258936925-c58bed479fcb?w=400&h=300&fit=crop"},
    {"id": 31, "name": "Running Smartwatch", "category": "Sports", "price": 179.99,
     "description": "GPS running watch with heart rate monitoring", "image": "https://picsum.photos/id/175/400/300"},
    {"id": 32, "name": "Hiking Backpack", "category": "Sports", "price": 89.99,
     "description": "50L hiking backpack with hydration compatible", "image": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400&h=300&fit=crop"},
    {"id": 33, "name": "Basketball Official", "category": "Sports", "price": 29.99,
     "description": "Official size basketball for indoor and outdoor", "image": "https://images.unsplash.com/photo-1546519638-68e109498ffc?w=400&h=300&fit=crop"},

    # Books & Education (7 products)
    {"id": 34, "name": "Programming Book Bundle", "category": "Books", "price": 49.99,
     "description": "Learn Python, JavaScript and Cloud Computing", "image": "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=400&h=300&fit=crop"},
    {"id": 35, "name": "Cookbook Collection", "category": "Books", "price": 39.99,
     "description": "Best-selling cookbook with 200+ recipes", "image": "https://images.unsplash.com/photo-1507048331197-7d4ac70811cf?w=400&h=300&fit=crop"},
    {"id": 36, "name": "Science Fiction Novel", "category": "Books", "price": 14.99,
     "description": "Award-winning science fiction bestseller", "image": "https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=400&h=300&fit=crop"},
    {"id": 37, "name": "Business Strategy Book", "category": "Books", "price": 24.99,
     "description": "Learn business strategies from top entrepreneurs", "image": "https://picsum.photos/id/24/400/300"},
    {"id": 38, "name": "Children's Storybook", "category": "Books", "price": 12.99,
     "description": "Colorful storybook for children ages 3-8", "image": "https://images.unsplash.com/photo-1629992101753-56d196c8aabb?w=400&h=300&fit=crop"},
    {"id": 39, "name": "Art History Textbook", "category": "Books", "price": 59.99,
     "description": "Comprehensive art history from ancient to modern", "image": "https://images.unsplash.com/photo-1568667256549-094345857637?w=400&h=300&fit=crop"},
    {"id": 40, "name": "Language Learning Set", "category": "Books", "price": 34.99,
     "description": "Complete language learning course with audio", "image": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=300&fit=crop"},

    # Home & Kitchen (10 products)
    {"id": 41, "name": "Coffee Maker Machine", "category": "Home", "price": 89.99,
     "description": "Programmable coffee maker with thermal carafe", "image": "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=400&h=300&fit=crop"},
    {"id": 42, "name": "Air Fryer XL", "category": "Home", "price": 129.99,
     "description": "Large capacity air fryer for healthy cooking", "image": "https://picsum.photos/id/225/400/300"},
    {"id": 43, "name": "Stand Mixer", "category": "Home", "price": 299.99,
     "description": "Professional stand mixer for baking enthusiasts", "image": "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=400&h=300&fit=crop"},
    {"id": 44, "name": "Smart Vacuum Cleaner", "category": "Home", "price": 249.99,
     "description": "Robot vacuum with smart mapping and app control", "image": "https://picsum.photos/id/1075/400/300"},
    {"id": 45, "name": "Ceramic Dinner Set", "category": "Home", "price": 79.99,
     "description": "16-piece ceramic dinner set for 4 people", "image": "https://picsum.photos/id/292/400/300"},
    {"id": 46, "name": "Memory Foam Pillow", "category": "Home", "price": 49.99,
     "description": "Ergonomic memory foam pillow for better sleep", "image": "https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?w=400&h=300&fit=crop"},
    {"id": 47, "name": "Desk Lamp LED", "category": "Home", "price": 34.99,
     "description": "Adjustable LED desk lamp with multiple brightness", "image": "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=400&h=300&fit=crop"},
    {"id": 48, "name": "Non-Stick Cookware Set", "category": "Home", "price": 149.99,
     "description": "10-piece non-stick cookware set with utensils", "image": "https://picsum.photos/id/338/400/300"},
    {"id": 49, "name": "Electric Kettle", "category": "Home", "price": 39.99,
     "description": "Stainless steel electric kettle with auto shut-off", "image": "https://picsum.photos/id/334/400/300"},
    {"id": 50, "name": "Blender Pro 1000W", "category": "Home", "price": 99.99,
     "description": "High-power blender for smoothies and food prep", "image": "https://images.unsplash.com/photo-1571330735066-03aaa9429d89?w=400&h=300&fit=crop"}
]




# ------------------------------------------------------------
# 3. Enhanced Agent System with Multiple Azure OpenAI Clients
# ------------------------------------------------------------
class SystemStatus(Enum):
    HEALTHY = "healthy"
    SEARCH_DEGRADED = "search_degraded"
    SEARCH_DOWN = "search_down"
    RECOVERING = "recovering"


class AlertLevel(Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    SUCCESS = "success"


class AgentRole(Enum):
    MONITOR = "monitor"
    TRIAGE = "triage"
    NOTIFIER = "notifier"
    FIXER = "fixer"
    ANALYZER = "analyzer"
    ROUTER = "router"
    SPEECH = "speech"


class MultiModelAgenticSystem:
    def __init__(self):
        logger.info("🤖 Initializing Multi-Model Agentic System")
        self.status = SystemStatus.HEALTHY
        self.incident_start_time = None
        self.current_incident = None
        self.banner_messages = []
        self.auto_resolution_enabled = True
        self.teams_webhook = os.getenv("TEAMS_WEBHOOK_URL", "")

        # Enhanced analytics
        self.agent_activities = []
        self.token_usage = {
            "monitor": 0,
            "triage": 0,
            "notifier": 0,
            "fixer": 0,
            "analyzer": 0,
            "router": 0,
            "speech": 0
        }
        self.incident_history = []
        self.performance_metrics = {
            "response_times": [],
            "success_rate": 100,
            "avg_resolution_time": 0
        }

        # Initialize multiple Azure OpenAI clients for different models
        self.clients = self._initialize_clients()

        # Initialize agents with different models
        self.agents = self._initialize_agents()

        # Search failure simulation
        self.search_failure_mode = False
        self.failure_count = 0
        self.last_incident_time = None

        # Banner management
        self.active_banners = {}

        # Performance tracking
        self.start_time = datetime.now()


    def _initialize_clients(self):
        """Initialize multiple Azure OpenAI clients for different models"""
        clients = {}

        try:
            # Main client for standard models
            clients["main"] = AzureOpenAI(
                api_key=os.getenv("AZURE_OPENAI_API_KEY"),
                azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
                api_version="2024-12-01-preview"
            )

            # Model Router client
            clients["router"] = AzureOpenAI(
                api_key=os.getenv("AZURE_OPENAI_API_KEY_ROUTER", os.getenv("AZURE_OPENAI_API_KEY")),
                azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT_ROUTER", os.getenv("AZURE_OPENAI_ENDPOINT")),
                api_version="2024-12-01-preview"
            )

            # Speech to Text client
            clients["speech"] = AzureOpenAI(
                api_key=os.getenv("AZURE_OPENAI_API_KEY_SPEECH", os.getenv("AZURE_OPENAI_API_KEY")),
                azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT_SPEECH", os.getenv("AZURE_OPENAI_ENDPOINT")),
                api_version="2025-03-01-preview"
            )

            logger.info("✅ Multiple Azure OpenAI clients initialized successfully")

        except Exception as e:
            logger.info(f"⚠️ Failed to initialize Azure OpenAI clients: {e}")
            clients = {}

        return clients

    def _initialize_agents(self):
        """Initialize different AI agents with specialized models using Agent Framework"""
        agents = {}

        if AGENT_FRAMEWORK_AVAILABLE and self.clients:
            try:
                # Monitor Agent - GPT-4o-mini for cost-efficient monitoring
                agents["monitor"] = ChatAgent(
                    AzureOpenAIChatClient(
                        model="gpt-4o-mini",
                        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
                        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
                        api_version="2024-02-01"
                    ),
                    name="SystemMonitor",
                    description="Monitors system health and detects anomalies"
                )

                # Triage Agent - GPT-4o for complex analysis
                agents["triage"] = ChatAgent(
                    AzureOpenAIChatClient(
                        model="gpt-4o",
                        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
                        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
                        api_version="2024-02-01"
                    ),
                    name="TriageSpecialist",
                    description="Analyzes incidents and identifies root causes"
                )

                # Notification Agent - GPT-4o-mini for message generation
                agents["notifier"] = ChatAgent(
                    AzureOpenAIChatClient(
                        model="gpt-4o-mini",
                        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
                        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
                        api_version="2024-02-01"
                    ),
                    name="NotificationManager",
                    description="Handles communications and alerts"
                )

                # Fix Agent - GPT-4o-2 for complex problem solving
                agents["fixer"] = ChatAgent(
                    AzureOpenAIChatClient(
                        model="gpt-4o-2",
                        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
                        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
                        api_version="2024-02-01"
                    ),
                    name="FixExecutor",
                    description="Implements solutions and repairs systems"
                )

                # Analysis Agent - GPT-4.1-mini for performance analysis
                agents["analyzer"] = ChatAgent(
                    AzureOpenAIChatClient(
                        model="gpt-4.1-mini",
                        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
                        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
                        api_version="2024-02-01"
                    ),
                    name="PerformanceAnalyzer",
                    description="Analyzes performance metrics and provides insights"
                )

                logger.info("✅ Microsoft Agent Framework agents initialized successfully")

            except Exception as e:
                logger.error(f"⚠️ Failed to initialize Agent Framework agents: {e}")
                agents = self._initialize_mock_agents()
        else:
            agents = self._initialize_mock_agents()

        return agents

    def _initialize_mock_agents(self):
        """Initialize mock agents when framework is not available"""
        logger.info("🔄 Using enhanced mock agents with multiple models")
        return {
            "monitor": {"name": "SystemMonitor", "model": "gpt-4o-mini", "description": "Monitors system health"},
            "triage": {"name": "TriageSpecialist", "model": "gpt-4o", "description": "Analyzes incidents"},
            "notifier": {"name": "NotificationManager", "model": "gpt-4o-mini",
                         "description": "Handles communications"},
            "fixer": {"name": "FixExecutor", "model": "gpt-4o-2", "description": "Implements solutions"},
            "analyzer": {"name": "PerformanceAnalyzer", "model": "gpt-4.1-mini", "description": "Analyzes performance"},
            "router": {"name": "ModelRouter", "model": "model-router",
                       "description": "Routes requests to optimal models"},
            "speech": {"name": "SpeechProcessor", "model": "gpt-4o-transcribe-diarize",
                       "description": "Processes audio inputs"}
        }

    def simulate_search_request(self, query: str) -> Dict[str, Any]:
        """Simulate search functionality with model routing and potential failures"""
        logger.info(f"🔍 Search query received: '{query}'")

        # Use model router for intelligent routing
        routed_model = self._route_query(query)
        logger.info(f"🔄 Model Router selected: {routed_model} for query: '{query}'")

        if self.search_failure_mode:
            self.failure_count += 1
            logger.info(f"🔴 Search failure #{self.failure_count} simulated")

            # Auto-detect failure if auto-resolution is enabled
            if self.auto_resolution_enabled and not self.current_incident:
                logger.info("🔄 Auto-detecting search failure (auto-resolution enabled)")
                self._detect_incident()

            # Simulate different types of failures
            failure_type = random.choice(["timeout", "error_503", "empty_results", "slow_response"])

            if failure_type == "timeout":
                raise TimeoutError("Search request timed out after 30s")
            elif failure_type == "error_503":
                raise Exception("503 Service Unavailable - Search backend not responding")
            elif failure_type == "empty_results":
                return {"results": [], "total": 0, "query": query, "error": "No results found"}
            elif failure_type == "slow_response":
                time.sleep(3)
                return {"results": [], "total": 0, "query": query, "warning": "Slow response"}
        else:
            # Normal search behavior with model-specific processing
            logger.info(f"🟢 Normal search for: '{query}' using {routed_model}")
            query_lower = query.lower()
            results = [p for p in PRODUCTS if query_lower in p["name"].lower() or
                       query_lower in p["category"].lower() or
                       query_lower in p["description"].lower()]

            # Simulate model-specific processing time
            processing_time = self._simulate_model_processing(routed_model, query)
            logger.info(f"⏳ {routed_model} processing time: {processing_time:.2f}s")
            time.sleep(processing_time)

            response = {
                "results": results,
                "total": len(results),
                "query": query,
                "model_used": routed_model,
                "processing_time": processing_time
            }
            logger.info(f"✅ Search completed. Found {len(results)} results using {routed_model}")

            # Log performance metrics
            self._log_performance_metric(processing_time, True)

            return response

    def _route_query(self, query: str) -> str:
        """Intelligently route queries to appropriate models"""
        query_lower = query.lower()

        # Simple routing logic - in production, this would use the model-router
        if len(query) < 20:
            return "gpt-4o-mini"  # Simple queries
        elif any(keyword in query_lower for keyword in ["analyze", "compare", "explain", "complex"]):
            return "gpt-4o"  # Complex reasoning
        elif any(keyword in query_lower for keyword in ["plan", "strategy", "comprehensive"]):
            return "gpt-4o-2"  # Advanced reasoning
        elif any(keyword in query_lower for keyword in ["technical", "performance", "metrics"]):
            return "gpt-4.1-mini"  # Technical analysis
        else:
            return "gpt-4o-mini"  # Default

    def _simulate_model_processing(self, model: str, query: str) -> float:
        """Simulate different processing times for different models"""
        base_times = {
            "gpt-4o-mini": 0.1,
            "gpt-4o": 0.3,
            "gpt-4o-2": 0.5,
            "gpt-4.1-mini": 0.2,
            "model-router": 0.05
        }

        base_time = base_times.get(model, 0.2)
        complexity_factor = len(query) / 100  # Longer queries take more time
        return base_time + (complexity_factor * 0.5) + random.random() * 0.3

    def process_audio_input(self, audio_data: str) -> Dict[str, Any]:
        """Simulate audio processing with speech-to-text model"""
        logger.info("🎤 Processing audio input with speech-to-text model")

        # Simulate speech recognition
        transcribed_text = self._simulate_speech_recognition(audio_data)

        # Use router to determine best model for processing transcribed text
        best_model = self._route_query(transcribed_text)

        response = {
            "transcribed_text": transcribed_text,
            "processing_model": "gpt-4o-transcribe-diarize",
            "analysis_model": best_model,
            "confidence": random.uniform(0.85, 0.98)
        }

        # Log token usage for speech processing
        self._simulate_token_usage("speech", 250)
        self._log_agent_activity("speech", f"Processed audio input: {transcribed_text[:50]}...", 250)

        return response

    def _simulate_speech_recognition(self, audio_data: str) -> str:
        """Simulate speech recognition with common search queries"""
        common_queries = [
            "I want to buy wireless headphones",
            "Show me smart watches for fitness",
            "Search for programming books",
            "Find gaming keyboards under 100 dollars",
            "Looking for organic cotton t-shirts"
        ]
        return random.choice(common_queries)

    def toggle_auto_resolution(self, enabled: bool):
        """Toggle auto-resolution feature"""
        self.auto_resolution_enabled = enabled
        status = "enabled" if enabled else "disabled"
        logger.info(f"🔄 Auto-resolution {status}")
        self.add_banner_message(f"Auto-resolution {status}", AlertLevel.INFO)
        self._log_agent_activity("system", f"Auto-resolution {status}", 0)

    def trigger_search_failure(self):
        """Manually trigger search failure for demo"""
        logger.info("🔴 MANUAL: Search failure triggered via admin button")
        self.search_failure_mode = True
        self.failure_start_time = datetime.now()
        self.status = SystemStatus.SEARCH_DOWN

        if self.auto_resolution_enabled:
            self._detect_incident()
        else:
            self.add_banner_message(
                "🔴 Search failure triggered. Auto-resolution is disabled - manual intervention required.",
                AlertLevel.ERROR,
                auto_close=False
            )

    def fix_search_issue(self):
        """Manually fix search issue for demo"""
        logger.info("🟢 MANUAL: Search issue fixed via admin button")
        self.search_failure_mode = False
        self.status = SystemStatus.HEALTHY
        self._resolve_incident_manual()

    def _detect_incident(self):
        """Monitor Agent detects the search failure incident"""
        incident_id = f"INC-{int(time.time())}"
        self.current_incident = {
            "id": incident_id,
            "type": "search_service_outage",
            "start_time": datetime.now().isoformat(),
            "severity": "P0",
            "description": "Search functionality completely unavailable",
            "detected_by": "Monitor Agent (gpt-4o-mini)"
        }

        # Log agent activity with actual model usage
        tokens = self._simulate_token_usage("monitor", 180)
        self._log_agent_activity("monitor", "Detected search service outage using continuous monitoring", tokens)

        # Add initial banner message
        self.add_banner_message(
            "🚨 Monitor Agent (gpt-4o-mini) detected search service issues. Activating AI response team...",
            AlertLevel.ERROR,
            auto_close=False
        )

        # Send enhanced Teams notification
        self._send_enhanced_teams_alert("INCIDENT_DETECTED")

        logger.info(f"🔴 [MONITOR AGENT - gpt-4o-mini] Incident detected: {incident_id}")

        # Start parallel agent processes with different models
        self._start_triage_process()
        self._start_notification_process()
        self._start_analysis_process()

    def _start_triage_process(self):
        """Triage Agent analyzes the issue using GPT-4o"""

        def triage_task():
            logger.info("🔧 [TRIAGE AGENT - gpt-4o] Starting root cause analysis...")
            time.sleep(2)

            # Simulate AI analysis with GPT-4o
            analysis_result = self._simulate_triage_analysis()
            tokens = self._simulate_token_usage("triage", 320)
            self._log_agent_activity("triage", f"Root cause analysis using GPT-4o: {analysis_result}", tokens)

            # Update banner with triage info
            self.add_banner_message(
                f"🔍 Triage Agent (gpt-4o) identified: {analysis_result}. Deploying fix...",
                AlertLevel.WARNING
            )

            logger.info(f"🔧 [TRIAGE AGENT - gpt-4o] Analysis complete: {analysis_result}")

            # Start fix process with GPT-4o-2
            self._start_fix_process()

        threading.Thread(target=triage_task, daemon=True).start()

    def _start_notification_process(self):
        """Notification Agent handles communications using GPT-4o-mini"""

        def notification_task():
            logger.info("📧 [NOTIFICATION AGENT - gpt-4o-mini] Starting notification process...")
            time.sleep(1)

            # Simulate notification generation
            notification_msg = self._simulate_notification_generation()
            tokens = self._simulate_token_usage("notifier", 150)
            self._log_agent_activity("notifier", "Generated stakeholder notifications using GPT-4o-mini", tokens)

            # Send enhanced Teams notification
            self._send_enhanced_teams_alert("TRIAGE_IN_PROGRESS")

            logger.info("📧 [NOTIFICATION AGENT - gpt-4o-mini] Notifications sent to stakeholders")

        threading.Thread(target=notification_task, daemon=True).start()

    def _start_analysis_process(self):
        """Analysis Agent performs deep analysis using GPT-4.1-mini"""

        def analysis_task():
            logger.info("📊 [ANALYSIS AGENT - gpt-4.1-mini] Starting performance analysis...")
            time.sleep(3)

            # Simulate performance analysis
            analysis_insights = self._simulate_performance_analysis()
            tokens = self._simulate_token_usage("analyzer", 280)
            self._log_agent_activity("analyzer", f"Performance analysis using GPT-4.1-mini: {analysis_insights}",
                                     tokens)

            # Update performance metrics
            self._update_performance_metrics()

            logger.info(f"📊 [ANALYSIS AGENT - gpt-4.1-mini] Analysis complete: {analysis_insights}")

        threading.Thread(target=analysis_task, daemon=True).start()

    def _start_fix_process(self):
        """Fix Agent implements the solution using GPT-4o-2"""

        def fix_task():
            logger.info("🛠️ [FIX AGENT - gpt-4o-2] Starting fix implementation...")
            time.sleep(3)

            # Simulate fix implementation with advanced reasoning
            fix_steps = self._simulate_fix_implementation()
            tokens = self._simulate_token_usage("fixer", 420)
            self._log_agent_activity("fixer", f"Implemented fix using GPT-4o-2: {fix_steps}", tokens)

            # Update banner with fix progress
            self.add_banner_message(
                "🛠️ Fix Agent (gpt-4o-2) is applying advanced database connection repairs...",
                AlertLevel.WARNING
            )

            time.sleep(2)

            # Complete the fix
            self._complete_fix()

        threading.Thread(target=fix_task, daemon=True).start()

    def _complete_fix(self):
        """Complete the fix and restore service"""
        self.search_failure_mode = False
        self.status = SystemStatus.HEALTHY

        # Calculate resolution time
        resolution_time = (datetime.now() - self.failure_start_time).total_seconds()

        # Log resolution with GPT-4o-2
        tokens = self._simulate_token_usage("fixer", 220)
        self._log_agent_activity("fixer",
                                 f"Successfully restored search service using GPT-4o-2 in {resolution_time:.1f}s",
                                 tokens)

        # Update banner with success
        self.add_banner_message(
            f"✅ Search functionality restored by Fix Agent (gpt-4o-2) in {resolution_time:.1f}s! All systems operational.",
            AlertLevel.SUCCESS
        )

        # Send resolution notification
        self._send_enhanced_teams_alert("INCIDENT_RESOLVED", resolution_time)

        # Add to incident history
        if self.current_incident:
            self.current_incident["resolved_time"] = datetime.now().isoformat()
            self.current_incident["resolution_time_seconds"] = resolution_time  # Store as number for calculations
            self.current_incident["resolution_time"] = f"{resolution_time:.1f}s"  # Store as string for display
            self.current_incident["resolution"] = "Automatic AI agent resolution with multiple models"
            self.current_incident["agents_involved"] = ["gpt-4o-mini", "gpt-4o", "gpt-4o-2", "gpt-4.1-mini"]
            self.incident_history.append(self.current_incident.copy())

        # Update performance metrics - FIXED: Use resolution_time_seconds for calculations
        if self.incident_history:
            total_resolution_time = sum(
                incident.get("resolution_time_seconds", 0)
                for incident in self.incident_history
                if incident.get("resolution_time_seconds") is not None
            )
            self.performance_metrics["avg_resolution_time"] = total_resolution_time / len(self.incident_history)
        else:
            self.performance_metrics["avg_resolution_time"] = 0

        logger.info("✅ [FIX AGENT - gpt-4o-2] Search service restored successfully!")

        # Clear incident after delay
        def clear_incident():
            time.sleep(8)
            self.current_incident = None
            self.add_banner_message(
                "🟢 All systems operating normally. Multiple AI agents collaborated to resolve the issue.",
                AlertLevel.INFO
            )
            logger.info("🟢 [SYSTEM] Incident fully resolved by collaborative AI agents")

        threading.Thread(target=clear_incident, daemon=True).start()

    def _resolve_incident_manual(self):
        """Manual resolution process"""
        if self.current_incident:
            self.current_incident["resolved_time"] = datetime.now().isoformat()
            self.current_incident["resolution"] = "Manual intervention"
            self.incident_history.append(self.current_incident.copy())

            self.add_banner_message(
                "✅ Search functionality restored via manual intervention.",
                AlertLevel.SUCCESS
            )

            self._send_enhanced_teams_alert("MANUAL_RESOLUTION")
            self._log_agent_activity("system", "Manual incident resolution", 0)

    def _update_performance_metrics(self):
        """Update system performance metrics"""
        total_incidents = len(self.incident_history)
        successful_resolutions = len([i for i in self.incident_history if i.get("resolved_time")])

        if total_incidents > 0:
            self.performance_metrics["success_rate"] = (successful_resolutions / total_incidents) * 100

        # Add recent response time
        if len(self.performance_metrics["response_times"]) > 50:
            self.performance_metrics["response_times"] = self.performance_metrics["response_times"][-50:]

    def _log_performance_metric(self, response_time: float, success: bool):
        """Log performance metrics for analytics"""
        self.performance_metrics["response_times"].append({
            "timestamp": datetime.now().isoformat(),
            "response_time": response_time,
            "success": success
        })

    # Simulation methods for agent activities
    def _simulate_triage_analysis(self):
        analyses = [
            "Database connection pool exhaustion - recommending connection reset and pool optimization",
            "Search index corruption detected - initiating index rebuild procedure",
            "Network latency issues identified - optimizing query routing and cache settings",
            "Cache invalidation problem - implementing distributed cache synchronization",
            "Load balancer misconfiguration - reconfiguring traffic distribution algorithms"
        ]
        return random.choice(analyses)

    def _simulate_notification_generation(self):
        messages = [
            "Stakeholders notified about service degradation with estimated resolution time",
            "Generated comprehensive incident report for engineering team review",
            "Sent real-time status updates to all affected system components"
        ]
        return random.choice(messages)

    def _simulate_performance_analysis(self):
        insights = [
            "Identified 40% increase in query response time - recommending query optimization",
            "Detected memory leak in search service - suggesting garbage collection tuning",
            "Found optimal cache configuration improving performance by 25%",
            "Identified database indexing improvements reducing query time by 60%"
        ]
        return random.choice(insights)

    def _simulate_fix_implementation(self):
        fixes = [
            "Restarted database connection pool with optimized settings and monitoring",
            "Rebuilt search index with improved tokenization and compression",
            "Optimized cache configuration with predictive loading algorithms",
            "Fixed load balancer settings with health-check integration and failover"
        ]
        return random.choice(fixes)

    def _simulate_token_usage(self, agent_type: str, base_tokens: int) -> int:
        """Simulate token usage with model-specific variance"""
        model_factors = {
            "monitor": 0.8,  # gpt-4o-mini - more efficient
            "triage": 1.2,  # gpt-4o - more comprehensive
            "notifier": 0.9,  # gpt-4o-mini - efficient
            "fixer": 1.5,  # gpt-4o-2 - most comprehensive
            "analyzer": 1.1,  # gpt-4.1-mini - technical
            "router": 0.7,  # model-router - lightweight
            "speech": 1.3  # speech-to-text - specialized
        }

        factor = model_factors.get(agent_type, 1.0)
        tokens = int(base_tokens * factor) + random.randint(-20, 50)
        self.token_usage[agent_type] += tokens
        return tokens

    def _log_agent_activity(self, agent_type: str, action: str, tokens: int):
        """Log agent activity for analytics"""
        activity = {
            "id": str(uuid.uuid4())[:8],
            "timestamp": datetime.now().isoformat(),
            "agent_type": agent_type,
            "agent_name": self.agents[agent_type]["name"] if agent_type in self.agents else "System",
            "model": self.agents[agent_type]["model"] if agent_type in self.agents else "N/A",
            "model_description": self.agents[agent_type].get("description", ""),
            "action": action,
            "tokens_used": tokens,
            "incident_id": self.current_incident["id"] if self.current_incident else None
        }
        self.agent_activities.append(activity)

        # Emit real-time update
        socketio.emit('agent_activity', activity)
        socketio.emit('system_metrics', self.get_system_metrics())

    def add_banner_message(self, message: str, level: AlertLevel, auto_close: bool = True):
        """Add a banner message with auto-close functionality"""
        banner_id = f"banner-{int(time.time())}-{random.randint(1000, 9999)}"
        banner_msg = {
            "id": banner_id,
            "message": message,
            "level": level.value,
            "timestamp": datetime.now().isoformat(),
            "auto_close": auto_close
        }

        self.banner_messages.append(banner_msg)
        self.active_banners[banner_id] = banner_msg

        # Keep only last 10 messages
        if len(self.banner_messages) > 10:
            self.banner_messages = self.banner_messages[-10:]

        # Broadcast via SocketIO
        socketio.emit('banner_update', banner_msg)
        logger.info(f"📢 [BANNER] {level.value.upper()}: {message}")

        # Auto-close if enabled
        if auto_close and level != AlertLevel.ERROR:
            def auto_close_banner():
                time.sleep(8)  # Close after 8 seconds
                if banner_id in self.active_banners:
                    self.remove_banner(banner_id)

            threading.Thread(target=auto_close_banner, daemon=True).start()

    def remove_banner(self, banner_id: str):
        """Remove a specific banner"""
        if banner_id in self.active_banners:
            del self.active_banners[banner_id]
            socketio.emit('banner_remove', {"id": banner_id})
            logger.info(f"🗑️ [BANNER] Removed banner: {banner_id}")

    def clear_all_banners(self):
        """Clear all banners"""
        self.active_banners.clear()
        socketio.emit('banners_clear', {})
        logger.info("🗑️ [BANNER] All banners cleared")

    def _send_enhanced_teams_alert(self, alert_type: str, resolution_time: float = None):
        """Send enhanced alert to Microsoft Teams with rich formatting"""
        alert_configs = {
            "INCIDENT_DETECTED": {
                "title": "🔴 P0 CRITICAL INCIDENT DETECTED",
                "color": "FF0000",
                "facts": [
                    ("Service", "Search Functionality"),
                    ("Severity", "P0 - Critical"),
                    ("Detected By", "Monitor Agent (gpt-4o-mini)"),
                    ("Status", "AI Agents Activated"),
                    ("Time", datetime.now().strftime('%H:%M:%S'))
                ]
            },
            "TRIAGE_IN_PROGRESS": {
                "title": "🔧 INCIDENT TRIAGE IN PROGRESS",
                "color": "FFA500",
                "facts": [
                    ("Analyzing", "Triage Agent (gpt-4o)"),
                    ("Status", "Root Cause Analysis"),
                    ("Notification", "Notification Agent (gpt-4o-mini)"),
                    ("Progress", "25% Complete")
                ]
            },
            "INCIDENT_RESOLVED": {
                "title": "✅ INCIDENT RESOLVED AUTOMATICALLY",
                "color": "00FF00",
                "facts": [
                    ("Resolved By", "Fix Agent (gpt-4o-2)"),
                    ("Resolution Time", f"{resolution_time:.1f} seconds" if resolution_time is not None else "N/A"),
                    ("Agents Involved", "4 AI Agents"),
                    ("Models Used", "gpt-4o-mini, gpt-4o, gpt-4o-2, gpt-4.1-mini"),
                    ("Success Rate", f"{self.performance_metrics['success_rate']:.1f}%")
                ]
            },
            "MANUAL_RESOLUTION": {
                "title": "✅ INCIDENT RESOLVED MANUALLY",
                "color": "00FF00",
                "facts": [
                    ("Resolution", "Manual Intervention"),
                    ("Status", "Service Restored"),
                    ("Recommendation", "Enable Auto-Resolution")
                ]
            }
        }

        config = alert_configs.get(alert_type)
        if not config:
            return

        # Build facts array safely
        facts_array = []
        for name, value in config["facts"]:
            # Handle any formatting issues in facts
            try:
                # If the value contains formatting that might fail, handle it
                if isinstance(value, str) and "{" in value and "}" in value:
                    # This is a format string, try to format it safely
                    try:
                        formatted_value = value.format(resolution_time=resolution_time)
                    except:
                        formatted_value = value  # Fallback to original if formatting fails
                else:
                    formatted_value = value
                facts_array.append({"name": name, "value": formatted_value})
            except Exception as e:
                logger.error(f"⚠️ Error formatting Teams fact {name}: {e}")
                facts_array.append({"name": name, "value": "N/A"})

        teams_message = {
            "@type": "MessageCard",
            "@context": "http://schema.org/extensions",
            "themeColor": config["color"],
            "summary": config["title"],
            "sections": [{
                "activityTitle": config["title"],
                "activitySubtitle": f"TechShop AI Agent System - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                "facts": facts_array,
                "markdown": True
            }],
            "potentialAction": [{
                "@type": "OpenUri",
                "name": "View Live Dashboard",
                "targets": [{
                    "os": "default",
                    "uri": "https://ignite-agent-framework.azurewebsites.net/"
                }]
            }, {
                "@type": "OpenUri",
                "name": "View Analytics",
                "targets": [{
                    "os": "default",
                    "uri": "https://ignite-agent-framework.azurewebsites.net/analytics"
                }]
            }]
        }

        logger.info(f"📧 [TEAMS] {config['title']}")

        if self.teams_webhook:
            try:
                response = requests.post(self.teams_webhook, json=teams_message)
                if response.status_code == 200:
                    logger.info(f"📧 [TEAMS] Enhanced message sent successfully")
                else:
                    logger.info(f"📧 [TEAMS] Failed to send message: {response.status_code}")
            except Exception as e:
                logger.error(f"📧 [TEAMS ERROR] {e}")
        else:
            logger.info(f"📧 [TEAMS MOCK] Webhook not configured - would send: {config['title']}")

    def get_system_metrics(self) -> Dict[str, Any]:
        """Get comprehensive system metrics for dashboard"""
        total_tokens = sum(self.token_usage.values())
        uptime = (datetime.now() - self.start_time).total_seconds()

        # Calculate model efficiency
        model_efficiency = {}
        for agent_type, tokens in self.token_usage.items():
            activities_count = len([a for a in self.agent_activities if a["agent_type"] == agent_type])
            efficiency = tokens / max(activities_count, 1)
            model_efficiency[agent_type] = {
                "tokens_per_action": efficiency,
                "total_tokens": tokens,
                "action_count": activities_count
            }

        return {
            "uptime": uptime,
            "total_incidents": len(self.incident_history),
            "success_rate": self.performance_metrics["success_rate"],
            "avg_resolution_time": self.performance_metrics["avg_resolution_time"],
            "total_tokens": total_tokens,
            "active_agents": len([a for a in self.agent_activities
                                  if datetime.fromisoformat(a["timestamp"]) > datetime.now() - timedelta(minutes=5)]),
            "model_efficiency": model_efficiency,
            "performance_metrics": self.performance_metrics,
            "agent_framework_available": AGENT_FRAMEWORK_AVAILABLE,
            "clients_available": len(self.clients) > 0
        }


# Global agentic system instance
agent_system = MultiModelAgenticSystem()


# ------------------------------------------------------------
# 4. Flask Routes
# ------------------------------------------------------------
@app.route('/')
def index():
    """Main page with featured products"""
    return render_template_string(index_template, products=PRODUCTS[:50])


@app.route('/search')
def search_page():
    """Search results page"""
    query = request.args.get('q', '')
    logger.info(f"🔍 Search page accessed with query: '{query}'")
    return render_template_string(search_template, query=query)


@app.route('/analytics')
def analytics_page():
    """Enhanced analytics dashboard"""
    return render_template_string(analytics_template)


@app.route('/api/search')
def api_search():
    """Search API endpoint with model routing"""
    query = request.args.get('q', '')

    logger.info(f"🎯 API Search called with query: '{query}'")

    if not query:
        logger.info("❌ API Search: No query provided")
        return jsonify({"error": "Query parameter 'q' is required"}), 400

    try:
        logger.info(f"🔄 API Search: Processing query '{query}'")
        results = agent_system.simulate_search_request(query)
        logger.info(
            f"✅ API Search: Successfully processed query '{query}', found {results['total']} results using {results.get('model_used', 'default')}")
        return jsonify(results)
    except Exception as e:
        error_msg = f"🔴 Search error: {str(e)}"
        logger.error(error_msg)

        # The agent system would detect this in real monitoring
        if not agent_system.search_failure_mode and agent_system.auto_resolution_enabled:
            logger.info("🔄 Auto-detecting search failure...")
            agent_system.trigger_search_failure()

        return jsonify({
            "error": "Search service temporarily unavailable",
            "message": "Our AI agents have been notified" if agent_system.auto_resolution_enabled else "Please try again later",
            "incident_id": agent_system.current_incident["id"] if agent_system.current_incident else None
        }), 503


@app.route('/api/audio/process', methods=['POST'])
def process_audio():
    """Process audio input with speech-to-text"""
    try:
        data = request.get_json()
        audio_data = data.get('audio_data', '')

        if not audio_data:
            return jsonify({"error": "Audio data is required"}), 400

        result = agent_system.process_audio_input(audio_data)
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": f"Audio processing failed: {str(e)}"}), 500


@app.route('/api/system/status')
def system_status():
    """Get current system status"""
    return jsonify({
        "status": agent_system.status.value,
        "search_operational": not agent_system.search_failure_mode,
        "auto_resolution_enabled": agent_system.auto_resolution_enabled,
        "current_incident": agent_system.current_incident,
        "banner_messages": agent_system.banner_messages[-5:],
        "timestamp": datetime.now().isoformat()
    })


@app.route('/api/analytics/data')
def analytics_data():
    """Get comprehensive analytics data for dashboard"""
    metrics = agent_system.get_system_metrics()

    # Get recent activities
    recent_activities = agent_system.agent_activities[-20:]

    # Calculate token usage by model
    model_usage = {}
    for activity in agent_system.agent_activities:
        model = activity["model"]
        if model not in model_usage:
            model_usage[model] = 0
        model_usage[model] += activity["tokens_used"]

    # Prepare chart data
    response_times = [rt["response_time"] for rt in agent_system.performance_metrics["response_times"][-10:]]
    time_labels = [f"T-{i}" for i in range(len(response_times), 0, -1)]

    return jsonify({
        "token_usage": agent_system.token_usage,
        "model_usage": model_usage,
        "recent_activities": recent_activities,
        "incident_history": agent_system.incident_history[-10:],
        "system_metrics": metrics,
        "chart_data": {
            "response_times": response_times,
            "time_labels": time_labels,
            "success_rate": metrics["success_rate"],
            "avg_resolution_time": metrics["avg_resolution_time"]
        },
        "agent_config": {
            "framework_available": AGENT_FRAMEWORK_AVAILABLE,
            "clients_available": len(agent_system.clients) > 0,
            "models_available": list(set([agent["model"] for agent in agent_system.agents.values()]))
        }
    })


@app.route('/api/admin/trigger-failure')
def trigger_failure():
    """Admin endpoint to trigger search failure"""
    logger.info("🎯 Admin: Triggering search failure")
    agent_system.trigger_search_failure()
    return jsonify({
        "message": "Search failure triggered",
        "auto_resolution": agent_system.auto_resolution_enabled,
        "incident_id": agent_system.current_incident["id"] if agent_system.current_incident else "None"
    })


@app.route('/api/admin/fix-issue')
def fix_issue():
    """Admin endpoint to manually fix search issue"""
    logger.info("🎯 Admin: Fixing search issue")
    agent_system.fix_search_issue()
    return jsonify({"message": "Search issue fixed manually"})


@app.route('/api/admin/toggle-auto-resolution', methods=['POST'])
def toggle_auto_resolution():
    """Toggle auto-resolution feature"""
    data = request.get_json()
    enabled = data.get('enabled', True)
    logger.info(f"🎯 Admin: Toggling auto-resolution to {enabled}")
    agent_system.toggle_auto_resolution(enabled)
    return jsonify({
        "message": f"Auto-resolution {'enabled' if enabled else 'disabled'}",
        "enabled": enabled
    })


@app.route('/api/admin/clear-banners')
def clear_banners():
    """Clear all banners"""
    logger.info("🎯 Admin: Clearing all banners")
    agent_system.clear_all_banners()
    return jsonify({"message": "All banners cleared"})


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})


# ------------------------------------------------------------
# 5. HTML Templates - Enhanced with Real-time Features
# ------------------------------------------------------------

# Enhanced index template with real-time metrics AND VOICE SEARCH
index_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TechShop - Multi-Model Agentic AI Demo</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f5f5f5; }

        .banner-container { position: fixed; top: 0; left: 0; right: 0; z-index: 1000; }
        .banner { padding: 15px 20px; margin: 0; border-bottom: 1px solid #ddd; display: flex; justify-content: space-between; align-items: center; }
        .banner.error { background: #fee; color: #c00; border-left: 4px solid #c00; }
        .banner.warning { background: #fff3cd; color: #856404; border-left: 4px solid #ffc107; }
        .banner.success { background: #d4edda; color: #155724; border-left: 4px solid #28a745; }
        .banner.info { background: #d1ecf1; color: #0c5460; border-left: 4px solid #17a2b8; }
        .banner-close { background: none; border: none; font-size: 1.2rem; cursor: pointer; padding: 0 5px; }

        .header { background: white; padding: 1rem 2rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-top: 0; }
        .nav { display: flex; justify-content: space-between; align-items: center; max-width: 1200px; margin: 0 auto; }
        .logo { font-size: 1.5rem; font-weight: bold; color: #0078d4; cursor: pointer; }
        .nav-links { display: flex; gap: 2rem; }
        .nav-links a { text-decoration: none; color: #333; font-weight: 500; }
        .nav-links a:hover { color: #0078d4; }
        .search-container { display: flex; gap: 10px; align-items: center; }
        .search-input { padding: 10px 15px; border: 2px solid #e1e5e9; border-radius: 6px; width: 400px; font-size: 1rem; }
        .search-btn { padding: 10px 20px; background: #0078d4; color: white; border: none; border-radius: 6px; cursor: pointer; }
        .voice-btn { padding: 10px 15px; background: #28a745; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 1.2rem; }
        .voice-btn.recording { background: #dc3545; animation: pulse 1.5s infinite; }
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }

        .control-panel { background: white; padding: 1.5rem; margin: 1rem auto; max-width: 1200px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
        .control-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.5rem; }
        .control-card { background: #f8f9fa; padding: 1.5rem; border-radius: 6px; border-left: 4px solid #0078d4; }

        .toggle-switch { position: relative; display: inline-block; width: 60px; height: 34px; margin-left: 1rem; }
        .toggle-switch input { opacity: 0; width: 0; height: 0; }
        .toggle-slider { position: absolute; cursor: pointer; top: 0; left: 0; right: 0; bottom: 0; background-color: #ccc; transition: .4s; border-radius: 34px; }
        .toggle-slider:before { position: absolute; content: ""; height: 26px; width: 26px; left: 4px; bottom: 4px; background-color: white; transition: .4s; border-radius: 50%; }
        input:checked + .toggle-slider { background-color: #28a745; }
        input:checked + .toggle-slider:before { transform: translateX(26px); }

        .admin-btn { padding: 10px 20px; margin: 5px; border: none; border-radius: 4px; cursor: pointer; font-size: 1rem; }
        .admin-btn.trigger { background: #dc3545; color: white; }
        .admin-btn.fix { background: #28a745; color: white; }
        .admin-btn.clear { background: #6c757d; color: white; }

        .status-indicator { display: inline-block; width: 12px; height: 12px; border-radius: 50%; margin-right: 8px; }
        .status-healthy { background: #28a745; }
        .status-down { background: #dc3545; }

        .hero { background: linear-gradient(135deg, #0078d4, #00bcf2); color: white; padding: 4rem 2rem; text-align: center; margin-top: 0; }
        .hero h1 { font-size: 3rem; margin-bottom: 1rem; }

        .products { max-width: 1200px; margin: 2rem auto; padding: 0 2rem; }
        .product-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 2rem; margin-top: 2rem; }
        .product-card { background: white; border-radius: 8px; padding: 1.5rem; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
        .product-image { width: 100%; height: 200px; background: linear-gradient(45deg, #0078d4, #00bcf2); display: flex; align-items: center; justify-content: center; border-radius: 4px; color: white; font-size: 2rem; }
        .product-name { font-size: 1.2rem; font-weight: bold; margin: 1rem 0 0.5rem; }
        .product-price { color: #0078d4; font-size: 1.3rem; font-weight: bold; margin: 0.5rem 0; }
        .product-description { color: #666; line-height: 1.5; }

        .toggle-label { display: flex; align-items: center; gap: 10px; }

        .real-time-metrics { background: white; padding: 1.5rem; margin: 1rem auto; max-width: 1200px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
        .metrics-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; }
        .metric-card { text-align: center; padding: 1rem; }
        .metric-value { font-size: 2rem; font-weight: bold; color: #0078d4; }
        .metric-label { color: #666; font-size: 0.9rem; }

        .voice-status { 
            background: #e8f4f8; 
            padding: 10px 15px; 
            border-radius: 6px; 
            margin: 10px 0; 
            border-left: 4px solid #0078d4;
            display: none;
        }
    </style>
</head>
<body>
    <div class="banner-container" id="bannerContainer"></div>

    <div class="header">
        <div class="nav">
            <div class="logo" onclick="window.location.href='/'">🛍️ TechShop</div>
            <div class="nav-links">
                <a href="/">Home</a>
                <a href="/analytics">Analytics</a>
            </div>
            <div class="search-container">
                <input type="text" class="search-input" id="searchInput" placeholder="Search products...">
                <button class="search-btn" onclick="performSearch()">Search</button>
                <button class="voice-btn" id="voiceBtn" onclick="toggleVoiceSearch()">🎤</button>
            </div>
        </div>
    </div>

    <div class="real-time-metrics">
        <h3>🤖 Live Agent System Metrics</h3>
        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-value" id="liveAgents">0</div>
                <div class="metric-label">Active Agents</div>
            </div>
            <div class="metric-card">
                <div class="metric-value" id="successRate">100%</div>
                <div class="metric-label">Success Rate</div>
            </div>
            <div class="metric-card">
                <div class="metric-value" id="avgResolution">0s</div>
                <div class="metric-label">Avg Resolution</div>
            </div>
            <div class="metric-card">
                <div class="metric-value" id="totalTokens">0</div>
                <div class="metric-label">Tokens Used</div>
            </div>
        </div>
    </div>

    <div class="control-panel">
        <h3>🎯 Multi-Model Agentic AI Control Center</h3>
        <div class="control-grid">
            <div class="control-card">
                <h4>🤖 Auto-Resolution System</h4>
                <p>Enable AI agents with multiple models to automatically detect and fix issues</p>
                <label class="toggle-label">
                    Auto-resolution:
                    <label class="toggle-switch">
                        <input type="checkbox" id="autoResolutionToggle" checked onchange="toggleAutoResolution(this.checked)">
                        <span class="toggle-slider"></span>
                    </label>
                </label>
                <div style="margin-top: 1rem; font-size: 0.9rem; color: #666;">
                    <strong>Available Models:</strong> gpt-4o-mini, gpt-4o, gpt-4o-2, gpt-4.1-mini, model-router, speech-to-text
                </div>
            </div>

            <div class="control-card">
                <h4>⚡ System Controls</h4>
                <button class="admin-btn trigger" onclick="triggerFailure()">🔴 Trigger Search Failure</button>
                <button class="admin-btn fix" onclick="fixIssue()">✅ Fix Search Issue</button>
                <button class="admin-btn clear" onclick="clearBanners()">🗑️ Clear Banners</button>
            </div>

            <div class="control-card">
                <h4>📊 System Status</h4>
                <div id="systemStatus">
                    <strong>Overall:</strong> <span id="overallStatus">Loading...</span><br>
                    <strong>Search:</strong> <span id="searchStatus">Loading...</span><br>
                    <strong>Auto-Resolution:</strong> <span id="autoResStatus">Loading...</span><br>
                    <strong>AI Framework:</strong> <span id="frameworkStatus">Loading...</span>
                </div>
            </div>
        </div>
    </div>

    <div class="hero">
        <h1>Multi-Model Agentic AI Demo</h1>
        <p>Watch specialized AI agents with different models work together to detect, analyze, and resolve issues automatically</p>
    </div>

    <div class="products">
        <h2>Featured Products</h2>
        <div class="product-grid" id="productGrid"></div>
    </div>

    <script>
        const socket = io();
        let currentBanners = [];
        let isRecording = false;
        let recognition = null;

        // Socket.IO for real-time updates
        socket.on('banner_update', function(banner) {
            addBanner(banner);
        });

        socket.on('banner_remove', function(data) {
            removeBanner(data.id);
        });

        socket.on('banners_clear', function() {
            clearAllBanners();
        });

        socket.on('agent_activity', function(activity) {
            console.log('🤖 Agent Activity:', activity);
            updateLiveMetrics();
        });

        socket.on('system_metrics', function(metrics) {
            updateLiveMetrics(metrics);
        });

        // Voice Search Functionality
        function initializeVoiceRecognition() {
            if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
                const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                recognition = new SpeechRecognition();
                recognition.continuous = false;
                recognition.interimResults = false;
                recognition.lang = 'en-US';

                recognition.onstart = function() {
                    console.log('🎤 Voice recognition started');
                    updateVoiceStatus('Listening... Speak now!', 'info');
                };

                recognition.onresult = function(event) {
                    const transcript = event.results[0][0].transcript;
                    console.log('🎤 Voice transcript:', transcript);
                    updateVoiceStatus(`Transcribed: "${transcript}"`, 'success');

                    // Set the search input and perform search
                    document.getElementById('searchInput').value = transcript;
                    performSearch();
                };

                recognition.onerror = function(event) {
                    console.error('🎤 Voice recognition error:', event.error);
                    updateVoiceStatus(`Error: ${event.error}`, 'error');
                    stopVoiceRecognition();
                };

                recognition.onend = function() {
                    console.log('🎤 Voice recognition ended');
                    stopVoiceRecognition();
                };

                return true;
            } else {
                console.warn('🎤 Speech recognition not supported in this browser');
                updateVoiceStatus('Speech recognition not supported in your browser', 'error');
                return false;
            }
        }

        function toggleVoiceSearch() {
            if (!isRecording) {
                startVoiceRecognition();
            } else {
                stopVoiceRecognition();
            }
        }

        function startVoiceRecognition() {
            if (initializeVoiceRecognition()) {
                try {
                    recognition.start();
                    isRecording = true;
                    document.getElementById('voiceBtn').classList.add('recording');
                    document.getElementById('voiceBtn').innerHTML = '⏹️';
                } catch (error) {
                    console.error('🎤 Failed to start voice recognition:', error);
                    updateVoiceStatus('Failed to start voice recognition', 'error');
                }
            }
        }

        function stopVoiceRecognition() {
            if (recognition && isRecording) {
                recognition.stop();
            }
            isRecording = false;
            document.getElementById('voiceBtn').classList.remove('recording');
            document.getElementById('voiceBtn').innerHTML = '🎤';
        }

        function updateVoiceStatus(message, type) {
            // Create or update voice status element
            let statusEl = document.getElementById('voiceStatus');
            if (!statusEl) {
                statusEl = document.createElement('div');
                statusEl.id = 'voiceStatus';
                statusEl.className = 'voice-status';
                document.querySelector('.search-container').appendChild(statusEl);
            }

            statusEl.textContent = message;
            statusEl.style.display = 'block';
            statusEl.style.borderLeftColor = 
                type === 'success' ? '#28a745' : 
                type === 'error' ? '#dc3545' : '#0078d4';

            // Auto-hide after 5 seconds
            setTimeout(() => {
                statusEl.style.display = 'none';
            }, 5000);
        }

        function addBanner(banner) {
            currentBanners = currentBanners.filter(b => b.message !== banner.message);
            currentBanners.push(banner);
            updateBannerDisplay();
        }

        function removeBanner(bannerId) {
            currentBanners = currentBanners.filter(b => b.id !== bannerId);
            updateBannerDisplay();
        }

        function clearAllBanners() {
            currentBanners = [];
            updateBannerDisplay();
        }

        function updateBannerDisplay() {
            const container = document.getElementById('bannerContainer');
            container.innerHTML = currentBanners.map(banner => 
                `<div class="banner ${banner.level}" id="banner-${banner.id}">
                    <span>${banner.message}</span>
                    <button class="banner-close" onclick="removeBanner('${banner.id}')">×</button>
                </div>`
            ).join('');
        }

        function performSearch() {
            const query = document.getElementById('searchInput').value.trim();
            if (query) {
                window.location.href = '/search?q=' + encodeURIComponent(query);
            }
        }

        function triggerFailure() {
            fetch('/api/admin/trigger-failure')
                .then(r => r.json())
                .then(data => {
                    console.log('Failure triggered:', data);
                    alert('Search failure triggered! Multiple AI agents with different models are now activated.');
                });
        }

        function fixIssue() {
            fetch('/api/admin/fix-issue')
                .then(r => r.json())
                .then(data => {
                    console.log('Issue fixed:', data);
                    alert('Search issue manually resolved.');
                });
        }

        function clearBanners() {
            fetch('/api/admin/clear-banners')
                .then(r => r.json())
                .then(data => {
                    console.log('Banners cleared:', data);
                });
        }

        function toggleAutoResolution(enabled) {
            fetch('/api/admin/toggle-auto-resolution', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ enabled: enabled })
            })
            .then(r => r.json())
            .then(data => {
                console.log('Auto-resolution toggled:', data);
            });
        }

        function updateSystemStatus() {
            fetch('/api/system/status')
                .then(r => r.json())
                .then(data => {
                    document.getElementById('overallStatus').innerHTML = 
                        '<span class="status-indicator ' + (data.status === 'healthy' ? 'status-healthy' : 'status-down') + '"></span>' + data.status;
                    document.getElementById('searchStatus').innerHTML = 
                        data.search_operational ? 
                        '<span class="status-indicator status-healthy"></span>Operational' : 
                        '<span class="status-indicator status-down"></span>Down';
                    document.getElementById('autoResStatus').innerHTML = 
                        data.auto_resolution_enabled ? 
                        '<span class="status-indicator status-healthy"></span>Enabled' : 
                        '<span class="status-indicator status-down"></span>Disabled';

                    // Update toggle state
                    document.getElementById('autoResolutionToggle').checked = data.auto_resolution_enabled;
                });
        }

        function updateLiveMetrics(metrics = null) {
            if (!metrics) {
                fetch('/api/analytics/data')
                    .then(r => r.json())
                    .then(data => {
                        updateMetricsDisplay(data.system_metrics);
                    });
            } else {
                updateMetricsDisplay(metrics);
            }
        }

        function updateMetricsDisplay(metrics) {
            document.getElementById('liveAgents').textContent = metrics.active_agents || 0;
            document.getElementById('successRate').textContent = metrics.success_rate ? metrics.success_rate.toFixed(1) + '%' : '100%';
            document.getElementById('avgResolution').textContent = metrics.avg_resolution_time ? metrics.avg_resolution_time.toFixed(1) + 's' : '0s';
            document.getElementById('totalTokens').textContent = metrics.total_tokens ? (metrics.total_tokens / 1000).toFixed(1) + 'K' : '0';

            // Update framework status
            document.getElementById('frameworkStatus').innerHTML = 
                metrics.agent_framework_available ? 
                '<span class="status-indicator status-healthy"></span>Available' : 
                '<span class="status-indicator status-down"></span>Mock Mode';
        }

        // Load featured products
        function loadFeaturedProducts() {
            const products = {{ products | tojson }};
            const grid = document.getElementById('productGrid');
            grid.innerHTML = products.map(product => `
                <div class="product-card">
                    <div class="product-image"><img src="${product.image}" height="200px" width="200px" /></div>
                    <div class="product-name">${product.name}</div>
                    <div class="product-price">$${product.price}</div>
                    <div class="product-description">${product.description}</div>
                </div>
            `).join('');
        }

        // Initialize
        document.getElementById('searchInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') performSearch();
        });

        loadFeaturedProducts();
        updateSystemStatus();
        updateLiveMetrics();
        setInterval(updateSystemStatus, 2000);
        setInterval(updateLiveMetrics, 3000);

        // Initial banner check
        fetch('/api/system/status')
            .then(r => r.json())
            .then(data => {
                currentBanners = data.banner_messages || [];
                updateBannerDisplay();
            });
    </script>
</body>
</html>
'''

# Enhanced search template with voice search
search_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Search Results - TechShop</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f5f5f5; }

        .header { background: white; padding: 1rem 2rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .nav { display: flex; justify-content: space-between; align-items: center; max-width: 1200px; margin: 0 auto; }
        .logo { font-size: 1.5rem; font-weight: bold; color: #0078d4; cursor: pointer; }
        .nav-links { display: flex; gap: 2rem; }
        .nav-links a { text-decoration: none; color: #333; font-weight: 500; }
        .nav-links a:hover { color: #0078d4; }
        .search-container { display: flex; gap: 10px; align-items: center; }
        .search-input { padding: 10px 15px; border: 2px solid #e1e5e9; border-radius: 6px; width: 400px; font-size: 1rem; }
        .search-btn { padding: 10px 20px; background: #0078d4; color: white; border: none; border-radius: 6px; cursor: pointer; }
        .voice-btn { padding: 10px 15px; background: #28a745; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 1.2rem; }
        .voice-btn.recording { background: #dc3545; animation: pulse 1.5s infinite; }
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }

        .search-results { max-width: 1200px; margin: 2rem auto; padding: 0 2rem; }
        .result-count { color: #666; margin-bottom: 1rem; font-size: 1.1rem; }
        .product-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 2rem; }
        .product-card { background: white; border-radius: 8px; padding: 1.5rem; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
        .product-image { width: 100%; height: 200px; background: linear-gradient(45deg, #0078d4, #00bcf2); display: flex; align-items: center; justify-content: center; border-radius: 4px; color: white; font-size: 2rem; }
        .product-name { font-size: 1.2rem; font-weight: bold; margin: 1rem 0 0.5rem; }
        .product-price { color: #0078d4; font-size: 1.3rem; font-weight: bold; margin: 0.5rem 0; }

        .loading { text-align: center; padding: 2rem; color: #666; font-size: 1.1rem; }
        .error-message { background: #fee; color: #c00; padding: 1rem; border-radius: 4px; margin: 1rem 0; }
        .admin-panel { background: white; padding: 1rem; margin: 2rem auto; max-width: 600px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); text-align: center; }
        .admin-btn { padding: 8px 16px; margin: 5px; border: none; border-radius: 4px; cursor: pointer; }
        .admin-btn.trigger { background: #dc3545; color: white; }
        .admin-btn.fix { background: #28a745; color: white; }

        .back-link { display: inline-block; margin-bottom: 1rem; color: #0078d4; text-decoration: none; }
        .back-link:hover { text-decoration: underline; }

        .model-info { background: #e8f4f8; padding: 0.5rem 1rem; border-radius: 4px; margin: 0.5rem 0; font-size: 0.9rem; color: #0078d4; }

        .voice-status { 
            background: #e8f4f8; 
            padding: 10px 15px; 
            border-radius: 6px; 
            margin: 10px 0; 
            border-left: 4px solid #0078d4;
            display: none;
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="nav">
            <div class="logo" onclick="window.location.href='/'">🛍️ TechShop</div>
            <div class="nav-links">
                <a href="/">Home</a>
                <a href="/analytics">Analytics</a>
            </div>
            <div class="search-container">
                <input type="text" class="search-input" id="searchInput" value="{{ query }}" placeholder="Search products...">
                <button class="search-btn" onclick="performSearch()">Search</button>
                <button class="voice-btn" id="voiceBtn" onclick="toggleVoiceSearch()">🎤</button>
            </div>
        </div>
    </div>

    <div class="search-results">
        <a href="/" class="back-link">← Back to Home</a>
        <h2>Search Results for "{{ query }}"</h2>
        <div class="result-count" id="resultCount">Searching...</div>
        <div id="modelInfo"></div>
        <div id="searchResults">
            <div class="loading">🔍 Searching products with AI model routing...</div>
        </div>
    </div>

    <div class="admin-panel">
        <button class="admin-btn trigger" onclick="triggerFailure()">🔴 Trigger Search Failure</button>
        <button class="admin-btn fix" onclick="fixIssue()">✅ Fix Search Issue</button>
    </div>

    <script>
        console.log('Search page loaded for query: "{{ query }}"');
        let isRecording = false;
        let recognition = null;

        // Voice Search Functionality
        function initializeVoiceRecognition() {
            if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
                const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                recognition = new SpeechRecognition();
                recognition.continuous = false;
                recognition.interimResults = false;
                recognition.lang = 'en-US';

                recognition.onstart = function() {
                    console.log('🎤 Voice recognition started');
                    updateVoiceStatus('Listening... Speak now!', 'info');
                };

                recognition.onresult = function(event) {
                    const transcript = event.results[0][0].transcript;
                    console.log('🎤 Voice transcript:', transcript);
                    updateVoiceStatus(`Transcribed: "${transcript}"`, 'success');

                    // Set the search input and perform search
                    document.getElementById('searchInput').value = transcript;
                    performSearch();
                };

                recognition.onerror = function(event) {
                    console.error('🎤 Voice recognition error:', event.error);
                    updateVoiceStatus(`Error: ${event.error}`, 'error');
                    stopVoiceRecognition();
                };

                recognition.onend = function() {
                    console.log('🎤 Voice recognition ended');
                    stopVoiceRecognition();
                };

                return true;
            } else {
                console.warn('🎤 Speech recognition not supported in this browser');
                updateVoiceStatus('Speech recognition not supported in your browser', 'error');
                return false;
            }
        }

        function toggleVoiceSearch() {
            if (!isRecording) {
                startVoiceRecognition();
            } else {
                stopVoiceRecognition();
            }
        }

        function startVoiceRecognition() {
            if (initializeVoiceRecognition()) {
                try {
                    recognition.start();
                    isRecording = true;
                    document.getElementById('voiceBtn').classList.add('recording');
                    document.getElementById('voiceBtn').innerHTML = '⏹️';
                } catch (error) {
                    console.error('🎤 Failed to start voice recognition:', error);
                    updateVoiceStatus('Failed to start voice recognition', 'error');
                }
            }
        }

        function stopVoiceRecognition() {
            if (recognition && isRecording) {
                recognition.stop();
            }
            isRecording = false;
            document.getElementById('voiceBtn').classList.remove('recording');
            document.getElementById('voiceBtn').innerHTML = '🎤';
        }

        function updateVoiceStatus(message, type) {
            let statusEl = document.getElementById('voiceStatus');
            if (!statusEl) {
                statusEl = document.createElement('div');
                statusEl.id = 'voiceStatus';
                statusEl.className = 'voice-status';
                document.querySelector('.search-container').appendChild(statusEl);
            }

            statusEl.textContent = message;
            statusEl.style.display = 'block';
            statusEl.style.borderLeftColor = 
                type === 'success' ? '#28a745' : 
                type === 'error' ? '#dc3545' : '#0078d4';

            setTimeout(() => {
                statusEl.style.display = 'none';
            }, 5000);
        }

        function performSearch() {
            const query = document.getElementById('searchInput').value.trim();
            if (query) {
                window.location.href = '/search?q=' + encodeURIComponent(query);
            }
        }

        function triggerFailure() {
            console.log('Triggering search failure...');
            fetch('/api/admin/trigger-failure')
                .then(r => r.json())
                .then(data => {
                    console.log('Failure triggered:', data);
                    alert('Search failure triggered! Multiple AI agents with different models are now activated.');
                    executeSearch(document.getElementById('searchInput').value);
                })
                .catch(error => {
                    console.error('Error triggering failure:', error);
                });
        }

        function fixIssue() {
            console.log('Fixing search issue...');
            fetch('/api/admin/fix-issue')
                .then(r => r.json())
                .then(data => {
                    console.log('Issue fixed:', data);
                    alert('Search issue manually resolved.');
                    executeSearch(document.getElementById('searchInput').value);
                })
                .catch(error => {
                    console.error('Error fixing issue:', error);
                });
        }

        function executeSearch(query) {
            console.log('Executing search for:', query);
            const resultsDiv = document.getElementById('searchResults');
            const countDiv = document.getElementById('resultCount');
            const modelInfoDiv = document.getElementById('modelInfo');

            resultsDiv.innerHTML = '<div class="loading">🔍 Searching products with AI model routing...</div>';
            modelInfoDiv.innerHTML = '';

            fetch('/api/search?q=' + encodeURIComponent(query))
                .then(response => {
                    console.log('Search response status:', response.status);
                    if (!response.ok) {
                        throw new Error('Search service unavailable - Status: ' + response.status);
                    }
                    return response.json();
                })
                .then(data => {
                    console.log('Search data received:', data);

                    // Display model information
                    if (data.model_used) {
                        modelInfoDiv.innerHTML = 
                            '<div class="model-info">' +
                            '🤖 AI Model Used: <strong>' + data.model_used + '</strong>' +
                            (data.processing_time ? ' | Processing Time: ' + data.processing_time.toFixed(2) + 's' : '') +
                            '</div>';
                    }

                    if (data.error) {
                        countDiv.innerHTML = 'Search Error';
                        resultsDiv.innerHTML = 
                            '<div class="error-message">' +
                            '<strong>Search Service Unavailable</strong><br>' +
                            (data.message || data.error) +
                            (data.incident_id ? '<br><small>Incident ID: ' + data.incident_id + '</small>' : '') +
                            '</div>';
                    } else {
                        countDiv.innerHTML = 'Found ' + data.total + ' results for "' + data.query + '"';

                        if (data.total === 0) {
                            resultsDiv.innerHTML = '<div class="loading">No products found matching your search.</div>';
                        } else {
                            resultsDiv.innerHTML = 
                                '<div class="product-grid">' +
                                data.results.map(product => 
                                    '<div class="product-card">' +
                                    '<div class="product-image"><img src="' + product.image + '" height="200px" width="200px" /></div>' +
                                    '<div class="product-name">' + product.name + '</div>' +
                                    '<div class="product-price">$' + product.price + '</div>' +
                                    '<div>' + product.description + '</div>' +
                                    '</div>'
                                ).join('') +
                                '</div>';
                        }
                    }
                })
                .catch(error => {
                    console.error('Search error:', error);
                    countDiv.innerHTML = 'Search Failed';
                    resultsDiv.innerHTML = 
                        '<div class="error-message">' +
                        '<strong>Search Service Error</strong><br>' +
                        error.message +
                        '<br><small>Our AI agents have been notified and are working on a fix.</small>' +
                        '</div>';
                });
        }

        // Initialize search
        document.getElementById('searchInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') performSearch();
        });

        // Execute search immediately when page loads
        executeSearch("{{ query }}");
    </script>
</body>
</html>
'''

# Enhanced analytics template with multiple charts (unchanged)
analytics_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Agent Analytics - TechShop</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f5f5f5; }

        .header { background: white; padding: 1rem 2rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .nav { display: flex; justify-content: space-between; align-items: center; max-width: 1400px; margin: 0 auto; }
        .logo { font-size: 1.5rem; font-weight: bold; color: #0078d4; cursor: pointer; }
        .nav-links { display: flex; gap: 2rem; }
        .nav-links a { text-decoration: none; color: #333; font-weight: 500; }
        .nav-links a:hover { color: #0078d4; }

        .dashboard { max-width: 1400px; margin: 2rem auto; padding: 0 2rem; }
        .dashboard-header { margin-bottom: 2rem; }

        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1.5rem; margin-bottom: 2rem; }
        .stat-card { background: white; padding: 1.5rem; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); text-align: center; }
        .stat-number { font-size: 2.5rem; font-weight: bold; color: #0078d4; margin-bottom: 0.5rem; }
        .stat-label { color: #666; font-size: 0.9rem; }

        .charts-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; margin-bottom: 2rem; }
        .chart-container { background: white; padding: 1.5rem; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
        .chart-title { margin-bottom: 1rem; color: #333; }

        .activities-table { background: white; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); overflow: hidden; }
        .table-header { background: #0078d4; color: white; padding: 1rem; font-weight: bold; }
        .table-content { max-height: 400px; overflow-y: auto; }
        table { width: 100%; border-collapse: collapse; }
        th, td { padding: 1rem; text-align: left; border-bottom: 1px solid #eee; }
        th { background: #f8f9fa; font-weight: 600; }
        tr:hover { background: #f8f9fa; }

        .agent-badge { display: inline-block; padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.8rem; font-weight: 500; }
        .badge-monitor { background: #e3f2fd; color: #1976d2; }
        .badge-triage { background: #fff3e0; color: #f57c00; }
        .badge-notifier { background: #e8f5e8; color: #388e3c; }
        .badge-fixer { background: #fce4ec; color: #c2185b; }
        .badge-analyzer { background: #f3e5f5; color: #7b1fa2; }
        .badge-router { background: #e1f5fe; color: #0288d1; }
        .badge-speech { background: #f3e5f5; color: #7b1fa2; }

        .system-info { background: white; padding: 1.5rem; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); margin-bottom: 2rem; }
        .info-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1rem; }
        .info-item { display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid #f0f0f0; }
    </style>
</head>
<body>
    <div class="header">
        <div class="nav">
            <div class="logo" onclick="window.location.href='/'">🛍️ TechShop</div>
            <div class="nav-links">
                <a href="/">Home</a>
                <a href="/analytics" style="color: #0078d4;">Analytics</a>
            </div>
        </div>
    </div>

    <div class="dashboard">
        <div class="dashboard-header">
            <h1>🤖 Multi-Model AI Agent Analytics Dashboard</h1>
            <p>Real-time monitoring of specialized AI agents, token usage, and system performance across multiple models</p>
        </div>

        <div class="system-info">
            <h3>System Configuration</h3>
            <div class="info-grid" id="systemConfig">
                <div class="info-item">
                    <span>Agent Framework:</span>
                    <span id="frameworkStatus">Checking...</span>
                </div>
                <div class="info-item">
                    <span>Azure Clients:</span>
                    <span id="clientsStatus">Checking...</span>
                </div>
                <div class="info-item">
                    <span>Available Models:</span>
                    <span id="modelsStatus">Checking...</span>
                </div>
                <div class="info-item">
                    <span>Uptime:</span>
                    <span id="uptimeStatus">Checking...</span>
                </div>
            </div>
        </div>

        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number" id="totalTokens">0</div>
                <div class="stat-label">Total Tokens Used</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" id="totalIncidents">0</div>
                <div class="stat-label">Incidents Resolved</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" id="successRate">100%</div>
                <div class="stat-label">Success Rate</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" id="avgResolution">0s</div>
                <div class="stat-label">Avg Resolution Time</div>
            </div>
        </div>

        <div class="charts-grid">
            <div class="chart-container">
                <h3 class="chart-title">Token Usage by Agent Type</h3>
                <canvas id="tokenUsageChart"></canvas>
            </div>
            <div class="chart-container">
                <h3 class="chart-title">Token Usage by Model</h3>
                <canvas id="modelUsageChart"></canvas>
            </div>
            <div class="chart-container">
                <h3 class="chart-title">Response Time Trends</h3>
                <canvas id="responseTimeChart"></canvas>
            </div>
            <div class="chart-container">
                <h3 class="chart-title">Agent Activity Distribution</h3>
                <canvas id="activityDistributionChart"></canvas>
            </div>
        </div>

        <div class="activities-table">
            <div class="table-header">Recent Agent Activities</div>
            <div class="table-content">
                <table>
                    <thead>
                        <tr>
                            <th>Time</th>
                            <th>Agent</th>
                            <th>Model</th>
                            <th>Action</th>
                            <th>Tokens</th>
                        </tr>
                    </thead>
                    <tbody id="activitiesTableBody">
                        <tr><td colspan="5" style="text-align: center;">Loading activities...</td></tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <script>
        let tokenUsageChart, modelUsageChart, responseTimeChart, activityDistributionChart;

        function getAgentBadgeClass(agentType) {
            const badgeClasses = {
                'monitor': 'badge-monitor',
                'triage': 'badge-triage', 
                'notifier': 'badge-notifier',
                'fixer': 'badge-fixer',
                'analyzer': 'badge-analyzer',
                'router': 'badge-router',
                'speech': 'badge-speech'
            };
            return badgeClasses[agentType] || 'badge-monitor';
        }

        function formatUptime(seconds) {
            const hours = Math.floor(seconds / 3600);
            const minutes = Math.floor((seconds % 3600) / 60);
            return `${hours}h ${minutes}m`;
        }

        function updateAnalytics() {
            fetch('/api/analytics/data')
                .then(r => r.json())
                .then(data => {
                    // Update system config
                    document.getElementById('frameworkStatus').textContent = 
                        data.agent_config.framework_available ? '✅ Available' : '⚠️ Mock Mode';
                    document.getElementById('clientsStatus').textContent = 
                        data.agent_config.clients_available ? '✅ Connected' : '⚠️ Limited';
                    document.getElementById('modelsStatus').textContent = 
                        data.agent_config.models_available.join(', ');
                    document.getElementById('uptimeStatus').textContent = 
                        formatUptime(data.system_metrics.uptime);

                    // Update stats
                    document.getElementById('totalTokens').textContent = 
                        (data.system_metrics.total_tokens / 1000).toFixed(1) + 'K';
                    document.getElementById('totalIncidents').textContent = data.system_metrics.total_incidents;
                    document.getElementById('successRate').textContent = data.system_metrics.success_rate.toFixed(1) + '%';
                    document.getElementById('avgResolution').textContent = 
                        data.system_metrics.avg_resolution_time ? data.system_metrics.avg_resolution_time.toFixed(1) + 's' : '0s';

                    // Update charts
                    updateTokenUsageChart(data.token_usage);
                    updateModelUsageChart(data.model_usage);
                    updateResponseTimeChart(data.chart_data);
                    updateActivityDistributionChart(data.recent_activities);

                    // Update activities table
                    updateActivitiesTable(data.recent_activities);
                });
        }

        function updateTokenUsageChart(tokenUsage) {
            const ctx = document.getElementById('tokenUsageChart').getContext('2d');
            const labels = Object.keys(tokenUsage).map(key => 
                key.charAt(0).toUpperCase() + key.slice(1) + ' Agent'
            );
            const data = Object.values(tokenUsage);
            const colors = ['#0078d4', '#ff8c00', '#107c10', '#e81123', '#7719aa', '#0288d1', '#7b1fa2'];

            if (tokenUsageChart) {
                tokenUsageChart.destroy();
            }

            tokenUsageChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Tokens Used',
                        data: data,
                        backgroundColor: colors,
                        borderColor: colors.map(c => c + 'CC'),
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: { display: false },
                        title: { display: true, text: 'Token Consumption by Agent Type' }
                    }
                }
            });
        }

        function updateModelUsageChart(modelUsage) {
            const ctx = document.getElementById('modelUsageChart').getContext('2d');
            const labels = Object.keys(modelUsage);
            const data = Object.values(modelUsage);
            const colors = ['#28a745', '#17a2b8', '#ffc107', '#dc3545', '#6f42c1', '#20c997', '#e83e8c'];

            if (modelUsageChart) {
                modelUsageChart.destroy();
            }

            modelUsageChart = new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: labels,
                    datasets: [{
                        data: data,
                        backgroundColor: colors,
                        borderColor: colors.map(c => c + 'CC'),
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: { position: 'bottom' }
                    }
                }
            });
        }

        function updateResponseTimeChart(chartData) {
            const ctx = document.getElementById('responseTimeChart').getContext('2d');

            if (responseTimeChart) {
                responseTimeChart.destroy();
            }

            responseTimeChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: chartData.time_labels,
                    datasets: [{
                        label: 'Response Time (seconds)',
                        data: chartData.response_times,
                        borderColor: '#0078d4',
                        backgroundColor: 'rgba(0, 120, 212, 0.1)',
                        borderWidth: 2,
                        fill: true,
                        tension: 0.4
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        title: { display: true, text: 'Search Response Time Trends' }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            title: { display: true, text: 'Seconds' }
                        }
                    }
                }
            });
        }

        function updateActivityDistributionChart(activities) {
            const ctx = document.getElementById('activityDistributionChart').getContext('2d');

            // Count activities by agent type
            const activityCount = {};
            activities.forEach(activity => {
                const agentType = activity.agent_type;
                activityCount[agentType] = (activityCount[agentType] || 0) + 1;
            });

            const labels = Object.keys(activityCount).map(key => 
                key.charAt(0).toUpperCase() + key.slice(1)
            );
            const data = Object.values(activityCount);
            const colors = ['#0078d4', '#ff8c00', '#107c10', '#e81123', '#7719aa', '#0288d1', '#7b1fa2'];

            if (activityDistributionChart) {
                activityDistributionChart.destroy();
            }

            activityDistributionChart = new Chart(ctx, {
                type: 'polarArea',
                data: {
                    labels: labels,
                    datasets: [{
                        data: data,
                        backgroundColor: colors,
                        borderColor: colors.map(c => c + 'CC'),
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: { position: 'right' }
                    }
                }
            });
        }

        function updateActivitiesTable(activities) {
            const tbody = document.getElementById('activitiesTableBody');
            tbody.innerHTML = activities.slice().reverse().map(activity => `
                <tr>
                    <td>${new Date(activity.timestamp).toLocaleTimeString()}</td>
                    <td>
                        <span class="agent-badge ${getAgentBadgeClass(activity.agent_type)}">
                            ${activity.agent_name}
                        </span>
                    </td>
                    <td><code>${activity.model}</code></td>
                    <td>${activity.action}</td>
                    <td>${activity.tokens_used.toLocaleString()}</td>
                </tr>
            `).join('') || '<tr><td colspan="5" style="text-align: center;">No activities yet</td></tr>';
        }

        // Initialize
        updateAnalytics();
        setInterval(updateAnalytics, 3000);
    </script>
</body>
</html>
'''



# ------------------------------------------------------------
# 6. Main Execution
# ------------------------------------------------------------
if __name__ == '__main__':
    setup_logging()
    logger.info("🚀 Starting Multi-Model Agentic AI Demo...")
    logger.info("🌐 Web application available at https://ignite-agent-framework.azurewebsites.net/")
    logger.info("📊 Enhanced analytics dashboard available at https://ignite-agent-framework.azurewebsites.net/analytics")
    logger.info("🔧 Advanced Features:")
    logger.info("   - Multiple Azure OpenAI clients for different models")
    logger.info("   - Microsoft Agent Framework integration")
    logger.info("   - Model routing with intelligent query distribution")
    logger.info("   - Speech-to-text processing capabilities")
    logger.info("   - Real-time metrics and advanced charts")
    logger.info("   - Enhanced Teams notifications with rich formatting")
    logger.info("   - Multi-agent collaboration with specialized models")
    logger.info(f"   - Agent Framework: {'✅ Available' if AGENT_FRAMEWORK_AVAILABLE else '⚠️ Using enhanced mock'}")
    logger.info(f"   - Azure Clients: {len(agent_system.clients)} configured")
    logger.info("\n🎮 Demo Instructions:")
    logger.info("   1. Search for products to see model routing in action")
    logger.info("   2. Trigger failures to watch multi-agent collaboration")
    logger.info("   3. Check analytics for live performance metrics")
    logger.info("   4. Watch Teams for enhanced notifications (if webhook configured)")
    logger.info("   5. Observe different AI models working together automatically")
    logger.info("   6. Use 🎤 voice search to test speech-to-text functionality")

    socketio.run(app, host='0.0.0.0', port=8080, debug=True, allow_unsafe_werkzeug=True)
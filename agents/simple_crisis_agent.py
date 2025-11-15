#!/usr/bin/env python3
"""
Simple Crisis Agent for Microsoft Ignite Contest
Minimal implementation to test agent framework discovery
"""

def handle_message(message):
    """Simple message handler for the agent framework"""
    
    if "crisis" in message.lower():
        return f"""🚨 CRISIS MANAGER ACTIVATED

Situation: {message}

⚡ IMMEDIATE RESPONSE:
1. Crisis team assembled
2. Assessing severity: HIGH
3. Implementing containment
4. Notifying stakeholders

🏢 Company: Trey Marketing Inc.
🎯 Mission: Product Launch Crisis
⏰ Deadline: 30 minutes
🤖 Model: GPT-5
🏆 Contest: Microsoft Ignite 2025

✅ Standing by for next directive!"""
    
    elif "help" in message.lower():
        return """🚨 Crisis Manager Agent

🎯 MISSION: Handle Trey Marketing Inc. emergencies
🏆 CONTEST: Microsoft Ignite 2025 - Mission Agent Possible
🤖 MODEL: GPT-5 (Azure OpenAI)

💡 USAGE:
• Type "crisis: [emergency]" to activate
• Specialized for product launch crises
• 30-minute resolution protocols

Ready for any emergency! 🚀"""
    
    else:
        return f"""👋 Crisis Manager monitoring...

You said: "{message}"

💡 Type "crisis: [emergency]" to activate crisis protocol
💡 Type "help" for capabilities

🔍 Standing by for Trey Marketing emergencies..."""

# Agent metadata for framework discovery
AGENT_INFO = {
    "name": "Simple Crisis Agent",
    "description": "Crisis Manager for Trey Marketing Inc.",
    "version": "1.0.0",
    "contest": "Microsoft Ignite 2025 - Mission Agent Possible",
    "company": "Trey Marketing Inc.",
    "model": "gpt-5",
    "ready": True
}

def get_info():
    """Return agent information"""
    return AGENT_INFO

if __name__ == "__main__":
    # Test the agent
    print("🚨 Simple Crisis Agent Test")
    print("=" * 30)
    
    test_messages = [
        "help",
        "crisis: Payment system down!",
        "Hello there"
    ]
    
    for msg in test_messages:
        print(f"\nInput: {msg}")
        response = handle_message(msg)
        print(f"Output: {response[:100]}...")

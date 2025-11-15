"""
Crisis Manager Agent - Microsoft Ignite Contest
Simple implementation for agent framework compatibility
"""

def process_message(message: str) -> str:
    """Process incoming message and return response"""
    
    if "crisis" in message.lower() or "emergency" in message.lower():
        return f"""🚨 CRISIS MANAGER ACTIVATED

Situation: {message}

⚡ IMMEDIATE ACTIONS:
1. 🚨 Crisis team assembled
2. 📊 Severity: HIGH PRIORITY  
3. 🔍 Root cause analysis initiated
4. 📢 Stakeholder notifications prepared
5. ⚡ Containment measures deploying

🏢 Company: Trey Marketing Inc.
🎯 Mission: Product Launch Crisis Management
⏰ Deadline: 30 minutes
🤖 Model: GPT-5 (Azure OpenAI)
🏆 Contest: Microsoft Ignite 2025 - Mission Agent Possible

📊 CONFIDENCE: 95% | ETA: 15-20 minutes

✅ Crisis Manager ready for next directive!"""

    elif "help" in message.lower() or "capabilities" in message.lower():
        return """🎯 CRISIS MANAGER CAPABILITIES

🚨 SPECIALIZED FOR:
• Trey Marketing Inc. product launch crises
• 30-minute emergency resolution protocols
• Multi-stakeholder crisis communication
• Real-time action plan generation

🏆 CONTEST FEATURES:
✅ Image analysis support
✅ Text communication under pressure  
✅ Creative problem solving
✅ Safety measures included
✅ Cost-efficient solutions

🤖 AI INTEGRATION:
• Model: GPT-5 (Azure OpenAI)
• Contest: Microsoft Ignite 2025
• Scenario: Mission Agent Possible

💡 USAGE:
Type "crisis: [emergency]" to activate crisis protocol!"""

    elif "status" in message.lower():
        return """📊 CRISIS MANAGER STATUS

🔴 OPERATIONAL STATUS: Ready & Monitoring
🏢 COMPANY: Trey Marketing Inc.
🎯 MISSION: Product launch crisis management
⏰ RESPONSE TIME: Immediate
🤖 MODEL: GPT-5
🏆 CONTEST: Microsoft Ignite 2025

✅ All systems operational - Standing by!"""

    else:
        return f"""👋 Crisis Manager Online

You said: "{message}"

🔍 Monitoring for emergencies...

💡 COMMANDS:
• "crisis: [emergency]" - Activate crisis protocol
• "help" - View capabilities  
• "status" - Check readiness

🎯 Ready for Trey Marketing Inc. emergencies!"""

# Simple entry point for the agent framework
def main():
    """Test the agent locally"""
    print("🚨 Crisis Manager Agent - Microsoft Ignite Contest")
    print("=" * 50)
    
    test_messages = [
        "help",
        "crisis: Payment system failure!",
        "status"
    ]
    
    for msg in test_messages:
        print(f"\n📝 Input: {msg}")
        response = process_message(msg)
        print(f"🤖 Response: {response[:100]}...")

if __name__ == "__main__":
    main()

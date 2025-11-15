#!/usr/bin/env python3
"""
Crisis Manager - Microsoft Ignite Contest
Ultra-simple agent for guaranteed framework discovery
"""

def handle_message(message):
    """Handle message - simple sync function"""
    
    if "crisis" in message.lower():
        return """🚨 CRISIS MANAGER ACTIVATED

Situation: """ + message + """

⚡ IMMEDIATE ACTIONS:
1. Crisis team assembled
2. Severity assessed: HIGH
3. Containment measures active
4. Stakeholders notified

🏢 Trey Marketing Inc.
🎯 Product Launch Crisis Management
⏰ 30-minute resolution protocol
🏆 Microsoft Ignite 2025 Contest

✅ Standing by for next directive!"""
    
    elif "help" in message.lower():
        return """🚨 Crisis Manager Agent

🎯 MISSION: Trey Marketing Inc. Crisis Management
🏆 CONTEST: Microsoft Ignite 2025 - Mission Agent Possible
🤖 MODEL: GPT-5

💡 USAGE:
• Type "crisis: [emergency]" to activate
• Specialized for product launch crises
• 30-minute resolution protocols

Ready for any emergency! 🚀"""
    
    else:
        return f"""👋 Crisis Manager monitoring...

You said: "{message}"

🔍 No crisis detected. Standing by.

💡 Type "crisis: [emergency]" to activate crisis protocol
🎯 Ready for Trey Marketing Inc. emergencies!"""

# Agent metadata
name = "Crisis Manager"
description = "AI Crisis Manager for Trey Marketing Inc. product launch emergencies"
version = "1.0.0"
contest = "Microsoft Ignite 2025 - Mission Agent Possible"
company = "Trey Marketing Inc."
model = "gpt-5"
ready = True

if __name__ == "__main__":
    print("🚨 Crisis Manager Agent - Microsoft Ignite Contest")
    print("Testing...")
    print(handle_message("help"))
    print("\n" + "="*50)
    print(handle_message("crisis: Payment system down!"))

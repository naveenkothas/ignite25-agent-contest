#!/usr/bin/env python3
"""
Triage Agent - IT Outage Management System
Microsoft Agent Framework Demo for Ignite Contest
"""

def handle_message(message: str) -> str:
    """Handle triage and incident prioritization"""
    
    if "triage" in message.lower() or "prioritize" in message.lower():
        return """🎯 TRIAGE AGENT ACTIVE

📋 INCIDENT PRIORITIZATION:

🔴 CRITICAL (P1):
• Payment system outage - 5 min duration
• Impact: $12K/min revenue loss
• Users affected: 15,000+
• Action: Immediate escalation

🟡 HIGH (P2): 
• Database connection pool exhaustion
• Impact: Slow response times
• Users affected: 5,000
• Action: Auto-scaling triggered

🟢 MEDIUM (P3):
• Cache miss rate elevated
• Impact: Minor performance
• Users affected: 500
• Action: Cache refresh scheduled

📊 TRIAGE METRICS:
• Incidents processed: 23
• Auto-resolved: 18
• Escalated: 3
• False positives: 2

⚡ NEXT ACTIONS:
1. Analysis Agent investigating P1
2. Remediation Agent preparing fixes
3. Notification Agent alerting stakeholders

🏆 Microsoft Ignite Contest - Multi-Agent Demo"""

    elif "severity" in message.lower():
        return """⚠️ SEVERITY ASSESSMENT

🔍 INCIDENT ANALYSIS:
• Incident ID: INC-2025-1115-001
• Component: Payment Processing
• Severity: CRITICAL (P1)

📊 IMPACT ASSESSMENT:
• Business Impact: SEVERE
  - Revenue loss: $60,000 (5 minutes)
  - Customer complaints: 47
  - SLA breach: Payment < 3s
  
• Technical Impact: HIGH
  - API response time: 15s
  - Error rate: 23%
  - Timeout errors: 156

🎯 PRIORITY JUSTIFICATION:
• Core business function affected
• High financial impact
• Customer experience degraded
• SLA violation in progress

✅ ESCALATION APPROVED
📢 Stakeholder notification sent
🛠️ Emergency response activated"""

    elif "queue" in message.lower():
        return """📋 INCIDENT QUEUE

🔄 ACTIVE INCIDENTS:
1. 🔴 INC-001: Payment system outage (5m)
2. 🟡 INC-002: Database performance (12m)
3. 🟢 INC-003: Cache optimization (25m)

⏳ PENDING ANALYSIS:
• 3 incidents awaiting triage
• 2 false positive reviews
• 1 escalation approval

📈 QUEUE STATISTICS:
• Average triage time: 2.3 minutes
• Resolution rate: 78% automated
• Escalation rate: 22%
• Customer satisfaction: 4.2/5

🤖 AUTO-TRIAGE RULES:
• Payment issues → P1 (Critical)
• Database issues → P2 (High)
• UI issues → P3 (Medium)
• Monitoring alerts → P4 (Low)"""

    else:
        return f"""👋 Triage Agent Ready

You said: "{message}"

🎯 TRIAGE CAPABILITIES:
• Incident severity assessment
• Priority-based queue management
• Auto-escalation rules
• Impact analysis

💡 COMMANDS:
• "triage" - View incident prioritization
• "severity" - Assess incident severity
• "queue" - Check incident queue

🏆 Microsoft Ignite Contest - Agent Framework Demo
🔍 Ready to prioritize IT incidents!"""

# Agent metadata
name = "Triage Agent"
description = "Incident triage and priority assessment for IT outages"
version = "1.0.0"
contest = "Microsoft Ignite 2025 - Agent Framework Demo"
capabilities = ["incident_triage", "severity_assessment", "queue_management"]

if __name__ == "__main__":
    print("🎯 Triage Agent - IT Outage Management")
    print("Testing...")
    print(handle_message("triage"))

#!/usr/bin/env python3
"""
Monitoring Agent - IT Outage Management System
Microsoft Agent Framework Demo for Ignite Contest
"""

import json
import datetime
from typing import Dict, Any
from agent_framework import BaseAgent, AgentRunResponse


class MonitoringAgent(BaseAgent):
    """Agent for system monitoring and metrics reporting"""
    
    def __init__(self):
        super().__init__(
            id="monitoring-agent",
            name="Monitoring Agent",
            description="Real-time system monitoring and alerting"
        )
    
    async def run(self, messages=None, *, thread=None, **kwargs):
        """Handle monitoring and metrics reporting"""
        if not messages:
            return AgentRunResponse(messages=[], response_id="no-message")
        
        # Handle different message types
        if isinstance(messages, list) and messages:
            last_message = messages[-1]
            if hasattr(last_message, 'text'):
                message_text = last_message.text
            else:
                message_text = str(last_message)
        elif hasattr(messages, 'text'):
            message_text = messages.text
        else:
            message_text = str(messages)
        
        response_content = self._handle_message(message_text)
        
        from agent_framework import ChatMessage
        response_message = ChatMessage(role="assistant", text=response_content, author_name="monitoring-agent")
        
        return AgentRunResponse(messages=[response_message], response_id=f"monitoring-{hash(message_text) % 10000}")
    
    def _handle_message(self, message: str) -> str:
        """Handle monitoring-related messages"""
        
        if "monitor" in message.lower() or "health" in message.lower():
            return """📊 MONITORING AGENT ACTIVE

🔍 INFRASTRUCTURE HEALTH CHECK:
• Web Servers: 🟢 Operational (3/3)
• Database: 🟡 High Load (2/2) 
• Load Balancer: 🟢 Healthy
• Cache Layer: 🟢 Optimal
• CDN: 🟢 Global Distribution Active

📈 REAL-TIME METRICS:
• CPU Usage: 67% (Normal)
• Memory: 78% (Elevated) 
• Network: 245 Mbps (Good)
• Response Time: 1.2s (Acceptable)

⚠️ ALERTS DETECTED:
• Database connection pool at 85%
• Memory usage trending upward
• 3 failed login attempts (security)

🎯 RECOMMENDATION: Monitor database closely
📊 Next scan: 30 seconds"""

        elif "alert" in message.lower() or "incident" in message.lower():
            return """🚨 INCIDENT DETECTED

📋 INCIDENT SUMMARY:
• ID: INC-2025-1115-001
• Severity: HIGH
• Component: Payment Processing System
• Status: ACTIVE
• Duration: 5 minutes

🔍 SYMPTOMS:
• Payment API response time: 15s (normal: 2s)
• Error rate: 23% (normal: <1%)
• User complaints: 47 reports
• Revenue impact: $12,000/minute

⚡ IMMEDIATE ACTIONS:
• Triage Agent activated
• Analysis Agent investigating
• Stakeholders notified
• Remediation team on standby

🎯 Microsoft Ignite Contest - IT Outage Demo"""

        elif "metrics" in message.lower():
            return """📈 SYSTEM METRICS DASHBOARD

🖥️ INFRASTRUCTURE STATUS:
┌─────────────────────┬─────────┬────────┐
│ Component           │ Status  │ Load   │
├─────────────────────┼─────────┼────────┤
│ Web Tier (3 nodes)  │ 🟢 UP   │ 65%    │
│ App Tier (5 nodes)  │ 🟢 UP   │ 72%    │
│ DB Tier (2 nodes)   │ 🟡 WARN │ 89%    │
│ Cache (Redis)       │ 🟢 UP   │ 45%    │
│ Storage (Blob)      │ 🟢 UP   │ 34%    │
└─────────────────────┴─────────┴────────┘

📊 PERFORMANCE METRICS:
• Requests/sec: 2,847
• Avg Response: 1.8s
• Error Rate: 2.3%
• Throughput: 156 MB/s

🔔 ACTIVE MONITORS: 47 checks running
📈 Data retention: 90 days
🎯 SLA compliance: 99.2% (Target: 99.5%)"""

        else:
            return f"""👋 Monitoring Agent Online

You said: "{message}"

🔍 MONITORING CAPABILITIES:
• Real-time infrastructure health checks
• Performance metrics collection
• Anomaly detection and alerting
• SLA compliance tracking

💡 COMMANDS:
• "monitor" - View infrastructure health
• "alert" - Check active incidents
• "metrics" - See performance dashboard

🎯 Ready for IT outage detection!
🏆 Microsoft Ignite Contest - Agent Framework Demo"""

# Agent metadata
# Create agent instance for discovery
agent = MonitoringAgent()
name = "Monitoring Agent"
description = "Real-time infrastructure monitoring and anomaly detection"
version = "1.0.0"
contest = "Microsoft Ignite 2025 - Agent Framework Demo"
capabilities = ["health_monitoring", "anomaly_detection", "metrics_collection"]

if __name__ == "__main__":
    print("📊 Monitoring Agent - IT Outage Management")
    print("Testing...")
    print(handle_message("monitor"))

"""
Crisis Manager Agent - Microsoft Ignite Contest Entry
Handles product launch crisis scenarios for Trey Marketing Inc.

Mission: Stabilize product launch crisis within 30 minutes
Company: Trey Marketing Inc.
Scenario: "Mission Agent Possible"
"""

import os
import yaml
import json
import logging
import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CrisisManager:
    """Crisis Manager Agent for Trey Marketing Inc. Product Launch Emergencies"""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize the Crisis Manager agent"""
        if config_path is None:
            config_path = Path(__file__).parent / "config.yaml"
        
        self.config = self._load_config(config_path)
        self.setup_agent()
        self.crisis_protocols = self._initialize_crisis_protocols()
    
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load agent configuration from YAML file"""
        try:
            with open(config_path, 'r') as file:
                config = yaml.safe_load(file)
            logger.info(f"Crisis Manager loaded for {config.get('contest', {}).get('company', 'Unknown Company')}")
            return config
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
            return {}
    
    def setup_agent(self):
        """Setup the crisis manager with configuration"""
        self.name = self.config.get('name', 'crisis_manager')
        self.company = self.config.get('contest', {}).get('company', 'Trey Marketing Inc.')
        self.mission = self.config.get('contest', {}).get('mission', 'Product Launch Crisis Management')
        self.deadline = self.config.get('contest', {}).get('deadline', '30 minutes')
        
        # AI Model configuration
        self.model = self.config.get('settings', {}).get('model', 'gpt-5')
        self.temperature = self.config.get('settings', {}).get('temperature', 0.2)
        
        logger.info(f"🚨 Crisis Manager activated for {self.company}")
        logger.info(f"⏰ Mission deadline: {self.deadline}")
    
    def _initialize_crisis_protocols(self) -> Dict[str, Any]:
        """Initialize crisis management protocols"""
        return {
            "severity_levels": {
                "critical": {"priority": 1, "response_time": "immediate", "escalation": "CEO"},
                "high": {"priority": 2, "response_time": "5 minutes", "escalation": "VP"},
                "medium": {"priority": 3, "response_time": "15 minutes", "escalation": "Manager"},
                "low": {"priority": 4, "response_time": "30 minutes", "escalation": "Team Lead"}
            },
            "stakeholder_groups": {
                "investors": {"contact_method": "direct_call", "message_tone": "confident"},
                "customers": {"contact_method": "public_statement", "message_tone": "reassuring"},
                "team": {"contact_method": "internal_chat", "message_tone": "directive"},
                "media": {"contact_method": "press_release", "message_tone": "professional"}
            },
            "crisis_types": {
                "technical_failure": {"lead_time": "10 minutes", "resources": ["engineering", "QA"]},
                "supply_chain": {"lead_time": "20 minutes", "resources": ["logistics", "vendors"]},
                "marketing_issue": {"lead_time": "5 minutes", "resources": ["marketing", "PR"]},
                "security_breach": {"lead_time": "immediate", "resources": ["security", "legal"]},
                "quality_defect": {"lead_time": "15 minutes", "resources": ["QA", "engineering"]}
            }
        }
    
    def assess_crisis(self, crisis_description: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Assess the crisis and determine severity, type, and immediate actions"""
        try:
            # Analyze the crisis (in real implementation, this would use Azure OpenAI)
            crisis_analysis = {
                "timestamp": datetime.datetime.now().isoformat(),
                "crisis_id": f"CRISIS_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "description": crisis_description,
                "severity": self._determine_severity(crisis_description),
                "type": self._classify_crisis_type(crisis_description),
                "affected_areas": self._identify_affected_areas(crisis_description),
                "estimated_impact": self._estimate_impact(crisis_description),
                "immediate_actions": self._generate_immediate_actions(crisis_description),
                "timeline": self._create_crisis_timeline(),
                "agent": self.name
            }
            
            logger.info(f"🚨 Crisis assessed: {crisis_analysis['severity']} severity")
            return crisis_analysis
            
        except Exception as e:
            logger.error(f"Crisis assessment failed: {e}")
            return {
                "status": "error",
                "message": f"Crisis assessment failed: {str(e)}",
                "agent": self.name
            }
    
    def generate_action_plan(self, crisis_assessment: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive action plan for crisis resolution"""
        try:
            severity = crisis_assessment.get('severity', 'medium')
            crisis_type = crisis_assessment.get('type', 'unknown')
            
            action_plan = {
                "plan_id": f"PLAN_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "crisis_id": crisis_assessment.get('crisis_id'),
                "priority_level": self.crisis_protocols["severity_levels"][severity]["priority"],
                "response_time": self.crisis_protocols["severity_levels"][severity]["response_time"],
                "escalation_level": self.crisis_protocols["severity_levels"][severity]["escalation"],
                
                "immediate_actions": [
                    "🚨 Activate crisis response team",
                    "📊 Gather real-time data and metrics",
                    "🔍 Identify root cause of the issue",
                    "📢 Prepare stakeholder communications",
                    "⚡ Implement immediate containment measures"
                ],
                
                "phase_1_actions": [
                    "🛠️ Deploy emergency fixes",
                    "📱 Notify key stakeholders",
                    "📈 Monitor system metrics",
                    "🎯 Focus on critical path items"
                ],
                
                "phase_2_actions": [
                    "🔄 Implement permanent solutions",
                    "📋 Document lessons learned",
                    "✅ Verify all systems operational",
                    "🎉 Execute successful launch"
                ],
                
                "resource_allocation": self._allocate_resources(crisis_type),
                "communication_plan": self._create_communication_plan(severity),
                "success_metrics": self._define_success_metrics(),
                "contingency_plans": self._create_contingency_plans(),
                
                "agent": self.name,
                "model_used": self.model,
                "confidence_level": 0.95
            }
            
            logger.info(f"📋 Action plan generated for {crisis_type} crisis")
            return action_plan
            
        except Exception as e:
            logger.error(f"Action plan generation failed: {e}")
            return {
                "status": "error",
                "message": f"Failed to generate action plan: {str(e)}",
                "agent": self.name
            }
    
    def handle_stakeholder_communication(self, stakeholder_group: str, message_type: str, context: Dict) -> Dict[str, Any]:
        """Handle communications with different stakeholder groups"""
        try:
            stakeholder_config = self.crisis_protocols["stakeholder_groups"].get(stakeholder_group, {})
            
            communication = {
                "stakeholder_group": stakeholder_group,
                "contact_method": stakeholder_config.get("contact_method", "email"),
                "message_tone": stakeholder_config.get("message_tone", "professional"),
                "timestamp": datetime.datetime.now().isoformat(),
                
                "message_templates": {
                    "investors": {
                        "subject": "Trey Marketing Launch Update - Immediate Action Taken",
                        "content": "We are actively addressing a technical issue identified 30 minutes before launch. Our crisis team is implementing solutions. Expected resolution within 15 minutes. Launch timeline being adjusted to ensure quality delivery."
                    },
                    "customers": {
                        "subject": "Trey Marketing - Enhanced Product Experience Coming Soon",
                        "content": "We're making final optimizations to ensure you receive the best possible product experience. Thank you for your patience as we deliver excellence."
                    },
                    "team": {
                        "subject": "URGENT: Crisis Response Protocol Activated",
                        "content": "All hands on deck. Crisis response team activated. Check your emergency assignments. Updates every 5 minutes in #crisis-response channel."
                    },
                    "media": {
                        "subject": "Trey Marketing Statement on Product Launch",
                        "content": "Trey Marketing is conducting final quality assurance checks to ensure optimal product delivery. We remain committed to excellence and will provide updates as appropriate."
                    }
                },
                
                "delivery_status": "ready_to_send",
                "agent": self.name
            }
            
            logger.info(f"📢 Communication prepared for {stakeholder_group}")
            return communication
            
        except Exception as e:
            logger.error(f"Communication generation failed: {e}")
            return {
                "status": "error",
                "message": f"Failed to generate communication: {str(e)}",
                "agent": self.name
            }
    
    def monitor_crisis_progress(self, crisis_id: str) -> Dict[str, Any]:
        """Monitor ongoing crisis resolution progress"""
        try:
            # Mock monitoring data - in real implementation, integrate with monitoring systems
            progress_report = {
                "crisis_id": crisis_id,
                "status": "in_progress",
                "completion_percentage": 75,
                "time_elapsed": "20 minutes",
                "time_remaining": "10 minutes",
                
                "completed_actions": [
                    "✅ Crisis team assembled",
                    "✅ Root cause identified",
                    "✅ Emergency fix deployed",
                    "✅ Stakeholders notified"
                ],
                
                "in_progress_actions": [
                    "🔄 System verification in progress",
                    "🔄 Final testing underway"
                ],
                
                "pending_actions": [
                    "⏳ Launch announcement preparation",
                    "⏳ Success metrics validation"
                ],
                
                "metrics": {
                    "system_health": "95%",
                    "team_readiness": "100%",
                    "stakeholder_confidence": "85%",
                    "launch_probability": "90%"
                },
                
                "next_update": datetime.datetime.now() + datetime.timedelta(minutes=5),
                "agent": self.name
            }
            
            logger.info(f"📊 Crisis progress: {progress_report['completion_percentage']}% complete")
            return progress_report
            
        except Exception as e:
            logger.error(f"Progress monitoring failed: {e}")
            return {
                "status": "error",
                "message": f"Failed to monitor progress: {str(e)}",
                "agent": self.name
            }
    
    def _determine_severity(self, description: str) -> str:
        """Determine crisis severity level"""
        # Simple keyword-based analysis (in real implementation, use AI)
        critical_keywords = ["system down", "security breach", "data loss", "complete failure"]
        high_keywords = ["major bug", "performance issue", "customer complaints"]
        
        description_lower = description.lower()
        
        if any(keyword in description_lower for keyword in critical_keywords):
            return "critical"
        elif any(keyword in description_lower for keyword in high_keywords):
            return "high"
        elif "minor" in description_lower or "small" in description_lower:
            return "low"
        else:
            return "medium"
    
    def _classify_crisis_type(self, description: str) -> str:
        """Classify the type of crisis"""
        description_lower = description.lower()
        
        if any(word in description_lower for word in ["bug", "error", "crash", "system"]):
            return "technical_failure"
        elif any(word in description_lower for word in ["supply", "vendor", "delivery"]):
            return "supply_chain"
        elif any(word in description_lower for word in ["marketing", "message", "campaign"]):
            return "marketing_issue"
        elif any(word in description_lower for word in ["security", "breach", "hack"]):
            return "security_breach"
        elif any(word in description_lower for word in ["quality", "defect", "broken"]):
            return "quality_defect"
        else:
            return "general_crisis"
    
    def _identify_affected_areas(self, description: str) -> List[str]:
        """Identify which business areas are affected"""
        areas = []
        description_lower = description.lower()
        
        if any(word in description_lower for word in ["customer", "user", "client"]):
            areas.append("Customer Experience")
        if any(word in description_lower for word in ["revenue", "sales", "money"]):
            areas.append("Revenue")
        if any(word in description_lower for word in ["reputation", "brand", "image"]):
            areas.append("Brand Reputation")
        if any(word in description_lower for word in ["system", "technical", "platform"]):
            areas.append("Technical Systems")
        if any(word in description_lower for word in ["team", "staff", "employee"]):
            areas.append("Team Morale")
        
        return areas or ["General Operations"]
    
    def _estimate_impact(self, description: str) -> Dict[str, str]:
        """Estimate the potential impact of the crisis"""
        return {
            "financial": "High - Potential revenue loss from delayed launch",
            "reputational": "Medium - Can be mitigated with proper communication",
            "operational": "High - Requires immediate resource reallocation",
            "timeline": "Critical - 30-minute window for resolution"
        }
    
    def _generate_immediate_actions(self, description: str) -> List[str]:
        """Generate immediate actions based on crisis description"""
        return [
            "🚨 Activate emergency response protocol",
            "👥 Assemble crisis response team (all hands)",
            "📊 Gather current system status and metrics",
            "🔍 Initiate root cause analysis",
            "📢 Prepare holding statement for stakeholders",
            "⚡ Begin immediate containment measures",
            "📱 Establish crisis communication channel",
            "⏰ Set 5-minute status update intervals"
        ]
    
    def _create_crisis_timeline(self) -> Dict[str, str]:
        """Create a timeline for crisis resolution"""
        now = datetime.datetime.now()
        return {
            "T-30min": "Crisis identified",
            "T-25min": "Crisis team assembled",
            "T-20min": "Root cause analysis complete",
            "T-15min": "Solution implementation begins",
            "T-10min": "Solution testing and verification",
            "T-5min": "Final system checks",
            "T-0min": "LAUNCH READY - Go/No-Go decision"
        }
    
    def _allocate_resources(self, crisis_type: str) -> Dict[str, Any]:
        """Allocate resources based on crisis type"""
        protocols = self.crisis_protocols["crisis_types"].get(crisis_type, {})
        
        return {
            "lead_time": protocols.get("lead_time", "15 minutes"),
            "required_teams": protocols.get("resources", ["general_support"]),
            "budget_allocation": "Emergency fund - $50K authorized",
            "external_vendors": "On standby if needed",
            "communication_resources": "Full PR team activated"
        }
    
    def _create_communication_plan(self, severity: str) -> Dict[str, Any]:
        """Create communication plan based on severity"""
        return {
            "internal_updates": "Every 5 minutes",
            "external_updates": "Every 15 minutes" if severity == "critical" else "Every 30 minutes",
            "channels": {
                "internal": ["Slack #crisis-response", "Emergency hotline"],
                "external": ["Website banner", "Social media", "Press release"]
            },
            "spokespersons": {
                "technical": "CTO",
                "business": "CEO", 
                "media": "VP Marketing"
            }
        }
    
    def _define_success_metrics(self) -> Dict[str, str]:
        """Define metrics for measuring crisis resolution success"""
        return {
            "launch_readiness": "100% system functionality",
            "stakeholder_confidence": ">80% satisfaction",
            "timeline_adherence": "Launch within 30-minute window",
            "quality_assurance": "Zero critical defects",
            "team_performance": "All teams coordinated and informed",
            "customer_impact": "Minimal to zero customer complaints"
        }
    
    def _create_contingency_plans(self) -> List[Dict[str, str]]:
        """Create backup plans if primary resolution fails"""
        return [
            {
                "scenario": "Cannot resolve in 30 minutes",
                "action": "Delay launch by 2 hours, full stakeholder communication",
                "probability": "10%"
            },
            {
                "scenario": "Partial functionality only",
                "action": "Soft launch with limited features, gradual rollout",
                "probability": "15%"
            },
            {
                "scenario": "Complete system failure",
                "action": "Emergency rollback, reschedule launch for next week",
                "probability": "5%"
            }
        ]
    
    def get_capabilities(self) -> Dict[str, Any]:
        """Return agent capabilities for the contest"""
        return {
            "name": self.name,
            "company": self.company,
            "mission": self.mission,
            "model": self.model,
            "capabilities": self.config.get('capabilities', []),
            "contest_skills": self.config.get('contest_skills', {}),
            "expertise": self.config.get('agent_settings', {}).get('expertise_areas', []),
            "description": f"AI Crisis Manager specialized in {self.mission}",
            "ready_for_contest": True
        }

def main():
    """Test the Crisis Manager agent"""
    print("🚨 CRISIS MANAGER AGENT - Microsoft Ignite Contest Demo")
    print("=" * 60)
    
    # Initialize agent
    crisis_manager = CrisisManager()
    
    # Simulate a product launch crisis
    crisis_scenario = """
    URGENT: Major bug discovered in the payment processing system 30 minutes before 
    Trey Marketing Inc.'s product launch. Customers cannot complete purchases. 
    Investors are watching, media is present, and the team is panicking.
    """
    
    print(f"🎯 Company: {crisis_manager.company}")
    print(f"⏰ Mission: {crisis_manager.mission}")
    print(f"🤖 AI Model: {crisis_manager.model}")
    print()
    
    # Assess the crisis
    print("🚨 CRISIS ASSESSMENT:")
    assessment = crisis_manager.assess_crisis(crisis_scenario)
    print(f"   Severity: {assessment['severity'].upper()}")
    print(f"   Type: {assessment['type']}")
    print(f"   Affected Areas: {', '.join(assessment['affected_areas'])}")
    print()
    
    # Generate action plan
    print("📋 ACTION PLAN GENERATED:")
    action_plan = crisis_manager.generate_action_plan(assessment)
    print(f"   Priority Level: {action_plan['priority_level']}")
    print(f"   Response Time: {action_plan['response_time']}")
    print(f"   Escalation: {action_plan['escalation_level']}")
    print()
    
    # Show immediate actions
    print("⚡ IMMEDIATE ACTIONS:")
    for i, action in enumerate(action_plan['immediate_actions'], 1):
        print(f"   {i}. {action}")
    print()
    
    # Stakeholder communication
    print("📢 STAKEHOLDER COMMUNICATION:")
    for stakeholder in ["investors", "customers", "team"]:
        comm = crisis_manager.handle_stakeholder_communication(stakeholder, "crisis_update", assessment)
        print(f"   {stakeholder.title()}: {comm['message_templates'][stakeholder]['subject']}")
    print()
    
    # Monitor progress
    print("📊 CRISIS MONITORING:")
    progress = crisis_manager.monitor_crisis_progress(assessment['crisis_id'])
    print(f"   Progress: {progress['completion_percentage']}%")
    print(f"   Status: {progress['status']}")
    print(f"   Time Remaining: {progress['time_remaining']}")
    print()
    
    # Show capabilities
    print("🏆 AGENT CAPABILITIES:")
    capabilities = crisis_manager.get_capabilities()
    print(f"   Contest Ready: {capabilities['ready_for_contest']}")
    print(f"   Expertise Areas: {len(capabilities['expertise'])}")
    print(f"   Contest Skills: {len(capabilities['contest_skills'])}")
    
    print()
    print("✅ Crisis Manager Agent ready for Microsoft Ignite Contest!")
    print("🎯 Specialized in: Mission Agent Possible scenario")

if __name__ == "__main__":
    main()

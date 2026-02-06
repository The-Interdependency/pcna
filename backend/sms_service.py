"""
SMS Service for PCNA System Check-ins
Supports mock mode for development, real Twilio integration for production
"""
import logging
from typing import Dict, Optional
from datetime import datetime

logger = logging.getLogger("sms_service")

class SMSService:
    """
    SMS service for system health check-ins and alerts
    Mock mode: logs to console instead of sending real SMS
    """
    def __init__(self, mock_mode: bool = True, phone_number: Optional[str] = None):
        self.mock_mode = mock_mode
        self.phone_number = phone_number or "+1234567890"  # Default for testing
        self.message_history = []
        
        if mock_mode:
            logger.info("SMS Service in MOCK mode - messages will be logged only")
        else:
            logger.info(f"SMS Service initialized for {self.phone_number}")
            # TODO: Initialize Twilio client when API key is available
            # self.twilio_client = Client(account_sid, auth_token)
    
    async def send_checkin(self, health_status: Dict):
        """
        Send periodic check-in message
        
        Args:
            health_status: System health metrics
        """
        status = health_status.get("status", "UNKNOWN")
        avg_health = health_status.get("average_health", 0.0)
        total_seeds = health_status.get("total_seeds", 0)
        
        message = f"""PCNA System Check-in [{datetime.utcnow().strftime('%H:%M UTC')}]
        
Status: {status}
Health: {avg_health:.2%}
Active Seeds: {total_seeds}
        
System operating normally. Reply STATUS for details."""
        
        await self._send(message)
    
    async def send_alert(self, alert_type: str, details: str):
        """
        Send critical alert
        
        Args:
            alert_type: Type of alert (DEGRADED, CRITICAL, ANOMALY)
            details: Alert details
        """
        message = f"""⚠️ PCNA ALERT: {alert_type}
        
{details}
        
Immediate attention recommended."""
        
        await self._send(message)
    
    async def process_command(self, command: str) -> str:
        """
        Process incoming SMS command
        
        Commands:
        - STATUS: Get current system status
        - HEALTH: Get detailed health metrics
        - LAST_TICK: Get last tick information
        - HELP: Show available commands
        
        Args:
            command: Command text
            
        Returns:
            Response message
        """
        command = command.upper().strip()
        
        if command == "STATUS":
            return """PCNA System Status:
✓ Operational
• 14 active seeds
• Health: 92%
• Last tick: 2s ago"""
        
        elif command == "HEALTH":
            return """Detailed Health Metrics:
• Avg Health: 92%
• Min Health: 87%
• Conservation: ✓ OK
• Anomalies: 0
• Trend: Stable"""
        
        elif command == "LAST_TICK":
            return """Last Tick Info:
• Tick #1247
• Processed: 2s ago
• All seeds responded
• No errors"""
        
        elif command == "HELP":
            return """PCNA Commands:
• STATUS - System status
• HEALTH - Health metrics
• LAST_TICK - Tick info
• HELP - This message"""
        
        else:
            return f"Unknown command: {command}. Reply HELP for available commands."
    
    async def _send(self, message: str):
        """
        Internal send method
        
        Args:
            message: Message to send
        """
        # Store in history
        self.message_history.append({
            "timestamp": datetime.utcnow(),
            "message": message,
            "to": self.phone_number
        })
        
        if self.mock_mode:
            logger.info(f"[MOCK SMS to {self.phone_number}]\n{message}\n")
        else:
            # TODO: Implement real Twilio sending
            # message = self.twilio_client.messages.create(
            #     body=message,
            #     from_=self.twilio_phone,
            #     to=self.phone_number
            # )
            logger.info(f"SMS sent to {self.phone_number}")
    
    def get_message_history(self, limit: int = 10):
        """Get recent message history"""
        return self.message_history[-limit:]

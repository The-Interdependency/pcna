"""
Researcher Outreach Module
Manages outreach to AI/ML researchers interested in PCNA and related topics
"""

import logging
from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr

logger = logging.getLogger("researcher_outreach")

class ResearcherProfile(BaseModel):
    """Researcher profile data model"""
    id: Optional[str] = None
    name: str
    email: Optional[EmailStr] = None
    institution: Optional[str] = None
    field: str = "AI/ML"
    interests: List[str] = []
    publications: List[str] = []
    last_contacted: Optional[datetime] = None
    response_status: Optional[str] = None  # pending, responded, no_response
    notes: Optional[str] = None

class OutreachManager:
    """
    Manages researcher database and outreach campaigns
    
    Features:
    - Researcher database management
    - Personalized outreach message generation (via LLM)
    - Tracking and follow-up
    - Campaign analytics
    """
    
    def __init__(self, db_connection, llm_orchestrator):
        """
        Initialize outreach manager
        
        Args:
            db_connection: MongoDB database connection
            llm_orchestrator: LLM orchestrator for message generation
        """
        self.db = db_connection
        self.llm = llm_orchestrator
        self.collection = self.db.researchers
        logger.info("Researcher outreach manager initialized")
    
    async def add_researcher(self, profile: ResearcherProfile) -> str:
        """
        Add researcher to database
        
        Args:
            profile: Researcher profile
            
        Returns:
            Researcher ID
        """
        profile_dict = profile.dict()
        profile_dict["created_at"] = datetime.utcnow()
        profile_dict["updated_at"] = datetime.utcnow()
        
        result = await self.collection.insert_one(profile_dict)
        researcher_id = str(result.inserted_id)
        
        logger.info(f"Added researcher: {profile.name} ({researcher_id})")
        return researcher_id
    
    async def find_researchers(self, 
                              field: Optional[str] = None,
                              interests: Optional[List[str]] = None) -> List[Dict]:
        """
        Find researchers matching criteria
        
        Args:
            field: Research field filter
            interests: Interest keywords filter
            
        Returns:
            List of matching researchers
        """
        query = {}
        
        if field:
            query["field"] = field
        
        if interests:
            query["interests"] = {"$in": interests}
        
        cursor = self.collection.find(query)
        researchers = await cursor.to_list(length=100)
        
        # Convert ObjectId to string
        for r in researchers:
            r["_id"] = str(r["_id"])
        
        logger.info(f"Found {len(researchers)} researchers matching criteria")
        return researchers
    
    async def generate_outreach_message(self, researcher: Dict) -> str:
        """
        Generate personalized outreach message using LLM
        
        Args:
            researcher: Researcher profile dictionary
            
        Returns:
            Personalized message text
        """
        prompt = f"""Generate a professional, trauma-informed outreach email to the following researcher.

Researcher Profile:
- Name: {researcher.get('name', 'Unknown')}
- Institution: {researcher.get('institution', 'Unknown')}
- Field: {researcher.get('field', 'AI/ML')}
- Interests: {', '.join(researcher.get('interests', []))}

Context about PCNA:
PCNA (Prime Circular Neural Architecture) is a deterministic, prime-indexed, circular graph architecture
for modular compute and diagnostics. It uses 7:3 heptagram routing for 49 compute seeds, 7 meta routers,
and 4 sentinels for independent monitoring.

Key features:
- Predictable routing and sparse communication
- Embedded observability
- Separation of computation and diagnostics
- Trauma-informed and transparent design
- Focus on harm reduction in AI systems

The email should:
1. Be respectful and concise (under 200 words)
2. Reference their specific research interests
3. Explain how PCNA might be relevant to their work
4. Invite collaboration or discussion
5. Include a clear call-to-action
6. Maintain a warm, professional tone
7. Be trauma-informed (transparent, non-manipulative)

Generate the email:"""
        
        message = await self.llm.chat(prompt, provider="anthropic")  # Claude is best for empathetic content
        
        logger.info(f"Generated outreach message for {researcher.get('name')}")
        return message
    
    async def send_outreach(self, researcher_id: str, message: str) -> Dict:
        """
        Send outreach message to researcher
        
        NOTE: This is a stub. In production, integrate with:
        - SendGrid for email
        - LinkedIn API for professional outreach
        - Twitter/X API for social media
        
        Args:
            researcher_id: Researcher database ID
            message: Message content
            
        Returns:
            Send status
        """
        # TODO: Implement actual sending logic
        logger.info(f"[STUB] Would send outreach to researcher {researcher_id}")
        logger.info(f"Message preview: {message[:100]}...")
        
        # Update researcher record
        await self.collection.update_one(
            {"_id": researcher_id},
            {
                "$set": {
                    "last_contacted": datetime.utcnow(),
                    "response_status": "pending",
                    "updated_at": datetime.utcnow()
                }
            }
        )
        
        return {
            "status": "sent",
            "researcher_id": researcher_id,
            "timestamp": datetime.utcnow().isoformat(),
            "message_length": len(message)
        }
    
    async def run_outreach_campaign(self, 
                                   target_field: str,
                                   target_interests: List[str],
                                   max_contacts: int = 10) -> Dict:
        """
        Run automated outreach campaign
        
        Args:
            target_field: Target research field
            target_interests: Target interests
            max_contacts: Maximum number of researchers to contact
            
        Returns:
            Campaign results
        """
        logger.info(f"Starting outreach campaign: {target_field}, {target_interests}")
        
        # Find eligible researchers
        researchers = await self.find_researchers(
            field=target_field,
            interests=target_interests
        )
        
        # Filter out recently contacted
        eligible = [
            r for r in researchers
            if not r.get("last_contacted") or 
            (datetime.utcnow() - r.get("last_contacted")).days > 30
        ][:max_contacts]
        
        results = {
            "total_found": len(researchers),
            "eligible": len(eligible),
            "contacted": 0,
            "messages": []
        }
        
        # Generate and send personalized messages
        for researcher in eligible:
            try:
                message = await self.generate_outreach_message(researcher)
                send_result = await self.send_outreach(researcher["_id"], message)
                
                results["contacted"] += 1
                results["messages"].append({
                    "researcher": researcher["name"],
                    "status": send_result["status"]
                })
                
            except Exception as e:
                logger.error(f"Error contacting {researcher.get('name')}: {e}")
                results["messages"].append({
                    "researcher": researcher["name"],
                    "status": "error",
                    "error": str(e)
                })
        
        logger.info(f"Campaign complete: {results['contacted']} researchers contacted")
        return results
    
    async def track_responses(self, researcher_id: str, response: str) -> Dict:
        """
        Track researcher response
        
        Args:
            researcher_id: Researcher database ID
            response: Response text or status
            
        Returns:
            Updated researcher record
        """
        await self.collection.update_one(
            {"_id": researcher_id},
            {
                "$set": {
                    "response_status": "responded",
                    "updated_at": datetime.utcnow()
                },
                "$push": {
                    "responses": {
                        "timestamp": datetime.utcnow(),
                        "content": response
                    }
                }
            }
        )
        
        logger.info(f"Recorded response from researcher {researcher_id}")
        
        return {"status": "recorded", "researcher_id": researcher_id}
    
    async def get_campaign_analytics(self) -> Dict:
        """
        Get analytics for outreach campaigns
        
        Returns:
            Analytics summary
        """
        total = await self.collection.count_documents({})
        contacted = await self.collection.count_documents({"last_contacted": {"$exists": True}})
        responded = await self.collection.count_documents({"response_status": "responded"})
        pending = await self.collection.count_documents({"response_status": "pending"})
        
        return {
            "total_researchers": total,
            "contacted": contacted,
            "responded": responded,
            "pending": pending,
            "response_rate": (responded / contacted * 100) if contacted > 0 else 0
        }

# Example usage
async def example_usage():
    """Example of how to use researcher outreach"""
    
    from motor.motor_asyncio import AsyncIOMotorClient
    from llm_abstraction import LLMOrchestrator
    
    # Initialize dependencies
    mongo_client = AsyncIOMotorClient("mongodb://localhost:27017/")
    db = mongo_client.pcna_db
    llm = LLMOrchestrator(api_key="your_api_key")
    
    # Create outreach manager
    outreach = OutreachManager(db, llm)
    
    # Add a researcher
    researcher = ResearcherProfile(
        name="Dr. Jane Smith",
        email="jane.smith@example.edu",
        institution="MIT",
        field="AI/ML",
        interests=["neural networks", "distributed systems", "AI ethics"]
    )
    researcher_id = await outreach.add_researcher(researcher)
    
    # Run campaign
    results = await outreach.run_outreach_campaign(
        target_field="AI/ML",
        target_interests=["neural networks", "distributed systems"],
        max_contacts=5
    )
    
    print(f"Campaign results: {results}")
    
    # Get analytics
    analytics = await outreach.get_campaign_analytics()
    print(f"Analytics: {analytics}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(example_usage())

"""
FastAPI Backend for PCNA Agent System
Integrates: PCNA topology, LLM abstraction, self-optimization, SMS, MongoDB
"""
import os
import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

# Import PCNA core components
import sys
sys.path.append('/app')
from core.topology import PCNATopology, SeedRole, Seed
from core.tensor_engine import TensorState, MarkovRecursion
import numpy as np

# Import custom modules
from llm_abstraction import LLMOrchestrator
from optimization_engine import SelfOptimizer
from sms_service import SMSService
from edcm_engine import EDCMAnalyzer

load_dotenv()

logger = logging.getLogger("pcna")
logging.basicConfig(level=logging.INFO)

# MongoDB client
mongo_client: Optional[AsyncIOMotorClient] = None
db = None

# Global instances
pcna_topology: Optional[PCNATopology] = None
llm_orchestrator: Optional[LLMOrchestrator] = None
self_optimizer: Optional[SelfOptimizer] = None
sms_service: Optional[SMSService] = None
edcm_analyzer: Optional[EDCMAnalyzer] = None
active_seeds: Dict[int, 'PCNASeed'] = {}

# WebSocket connections
active_connections: List[WebSocket] = []

class PCNASeed:
    """Individual PCNA seed instance"""
    def __init__(self, seed_id: int, role: SeedRole):
        self.seed_id = seed_id
        self.role = role
        self.state: Optional[TensorState] = None
        self.tick = 0
        self.health_score = 1.0
        
        if role == SeedRole.COMPUTE:
            # Initialize tensor state
            actor = np.array([seed_id])
            time = np.array([0])
            metric = np.ones((1,))
            context = np.array([0])
            self.state = TensorState(actor=actor, time=time, metric=metric, context=context)
            self.tensor_engine = MarkovRecursion()
            
    async def process_tick(self):
        """Process one tick"""
        self.tick += 1
        
        if self.role == SeedRole.COMPUTE:
            await self._compute_tick()
        elif self.role == SeedRole.SENTINEL:
            await self._sentinel_tick()
            
    async def _compute_tick(self):
        """Compute seed tick processing"""
        if self.state is None:
            return
            
        # Simulate computation
        injected = self.state.metric * 0.01
        resolved = self.state.metric * 0.009
        self.state = self.tensor_engine.update(self.state, injected, resolved)
        
        # Update health score
        mass = self.state.mass
        self.health_score = min(1.0, mass / 1.0) if mass > 0 else 0.0
        
    async def _sentinel_tick(self):
        """Sentinel monitoring tick"""
        # Monitor other seeds
        pass
        
    def to_dict(self) -> Dict:
        """Serialize seed state"""
        return {
            "seed_id": self.seed_id,
            "role": self.role.value,
            "tick": self.tick,
            "health_score": self.health_score,
            "mass": self.state.mass if self.state else 0.0,
            "spectral": {
                "magnitude": self.state.spectral_descriptor()[0] if self.state else 0.0,
                "phase": self.state.spectral_descriptor()[1] if self.state else 0.0,
            } if self.state else None
        }

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    global mongo_client, db, pcna_topology, llm_orchestrator, self_optimizer, sms_service, edcm_analyzer
    
    # Initialize MongoDB
    mongo_url = os.getenv("MONGO_URL", "mongodb://localhost:27017/")
    mongo_client = AsyncIOMotorClient(mongo_url)
    db = mongo_client.pcna_db
    logger.info("MongoDB connected")
    
    # Initialize PCNA topology
    pcna_topology = PCNATopology()
    logger.info(f"PCNA topology initialized: {len(pcna_topology.seeds)} seeds")
    
    # Initialize LLM orchestrator
    api_key = os.getenv("EMERGENT_LLM_KEY")
    llm_orchestrator = LLMOrchestrator(api_key=api_key)
    logger.info("LLM orchestrator initialized")
    
    # Initialize self-optimizer
    self_optimizer = SelfOptimizer(topology=pcna_topology)
    logger.info("Self-optimizer initialized")
    
    # Initialize SMS service
    sms_service = SMSService(mock_mode=os.getenv("SMS_MOCK_MODE", "true") == "true")
    logger.info("SMS service initialized")
    
    # Initialize EDCM analyzer
    edcm_analyzer = EDCMAnalyzer()
    logger.info("EDCM analyzer initialized")
    
    # Create initial seeds
    await initialize_seeds()
    
    # Start background tasks
    asyncio.create_task(tick_loop())
    asyncio.create_task(optimization_loop())
    asyncio.create_task(sms_checkin_loop())
    
    yield
    
    # Cleanup
    if mongo_client:
        mongo_client.close()
    logger.info("Shutdown complete")

app = FastAPI(title="PCNA Agent System", lifespan=lifespan)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def initialize_seeds():
    """Initialize key seeds"""
    global active_seeds
    
    # Create global router
    active_seeds[0] = PCNASeed(0, SeedRole.GLOBAL)
    
    # Create sentinels
    for i in range(1, 5):
        active_seeds[i] = PCNASeed(i, SeedRole.SENTINEL)
    
    # Create some compute seeds for demo
    for i in range(5, 15):
        seed = pcna_topology.seeds.get(i)
        if seed and seed.role == SeedRole.COMPUTE:
            active_seeds[i] = PCNASeed(i, SeedRole.COMPUTE)
    
    logger.info(f"Initialized {len(active_seeds)} seeds")

async def tick_loop():
    """Main tick loop"""
    while True:
        try:
            # Process all seeds
            for seed in active_seeds.values():
                await seed.process_tick()
            
            # Broadcast state to WebSocket clients
            await broadcast_state()
            
            await asyncio.sleep(1.0)
        except Exception as e:
            logger.error(f"Tick loop error: {e}")
            await asyncio.sleep(1.0)

async def optimization_loop():
    """Self-optimization loop"""
    while True:
        try:
            await asyncio.sleep(30)  # Run every 30 seconds
            
            if self_optimizer:
                optimization_result = await self_optimizer.optimize(active_seeds)
                if optimization_result.get("actions_taken"):
                    logger.info(f"Optimization: {optimization_result}")
                    
        except Exception as e:
            logger.error(f"Optimization loop error: {e}")
            await asyncio.sleep(30)

async def sms_checkin_loop():
    """SMS check-in loop"""
    while True:
        try:
            await asyncio.sleep(3600)  # Check every hour
            
            if sms_service:
                # Generate health report
                health_status = await get_system_health()
                await sms_service.send_checkin(health_status)
                
        except Exception as e:
            logger.error(f"SMS loop error: {e}")
            await asyncio.sleep(3600)

async def broadcast_state():
    """Broadcast system state to WebSocket clients"""
    if not active_connections:
        return
        
    state_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "seeds": {sid: seed.to_dict() for sid, seed in active_seeds.items()},
        "system_health": await get_system_health()
    }
    
    disconnected = []
    for connection in active_connections:
        try:
            await connection.send_json(state_data)
        except:
            disconnected.append(connection)
    
    for conn in disconnected:
        active_connections.remove(conn)

async def get_system_health() -> Dict:
    """Calculate system health metrics"""
    total_health = sum(seed.health_score for seed in active_seeds.values())
    avg_health = total_health / len(active_seeds) if active_seeds else 0.0
    
    return {
        "average_health": avg_health,
        "total_seeds": len(active_seeds),
        "status": "HEALTHY" if avg_health > 0.8 else "DEGRADED" if avg_health > 0.5 else "CRITICAL"
    }

# REST API Endpoints

@app.get("/api/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

@app.get("/api/topology")
async def get_topology():
    """Get PCNA topology"""
    if not pcna_topology:
        raise HTTPException(status_code=503, detail="Topology not initialized")
    return pcna_topology.to_dict()

@app.get("/api/seeds")
async def get_seeds():
    """Get all active seeds"""
    return {sid: seed.to_dict() for sid, seed in active_seeds.items()}

@app.get("/api/system-health")
async def system_health():
    """Get system health metrics"""
    return await get_system_health()

class LLMRequest(BaseModel):
    prompt: str
    provider: Optional[str] = "openai"
    model: Optional[str] = "gpt-5.2"

@app.post("/api/llm/chat")
async def llm_chat(request: LLMRequest):
    """Chat with LLM"""
    if not llm_orchestrator:
        raise HTTPException(status_code=503, detail="LLM orchestrator not initialized")
    
    try:
        response = await llm_orchestrator.chat(
            prompt=request.prompt,
            provider=request.provider,
            model=request.model
        )
        return {"response": response, "provider": request.provider, "model": request.model}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/edcm/analyze")
async def edcm_analyze():
    """Run EDCM analysis on system"""
    if not edcm_analyzer:
        raise HTTPException(status_code=503, detail="EDCM analyzer not initialized")
    
    seed_states = [seed.to_dict() for seed in active_seeds.values()]
    analysis = await edcm_analyzer.analyze(seed_states)
    
    # Store in MongoDB
    await db.edcm_reports.insert_one({
        "timestamp": datetime.utcnow(),
        "analysis": analysis
    })
    
    return analysis

@app.get("/api/edcm/artifacts")
async def get_edcm_artifacts(limit: int = 10):
    """Get EDCM artifacts for monetization"""
    cursor = db.edcm_reports.find().sort("timestamp", -1).limit(limit)
    artifacts = await cursor.to_list(length=limit)
    
    # Convert ObjectId to string
    for artifact in artifacts:
        artifact["_id"] = str(artifact["_id"])
        artifact["timestamp"] = artifact["timestamp"].isoformat()
    
    return {"artifacts": artifacts}

class SMSCommand(BaseModel):
    command: str

@app.post("/api/sms/command")
async def sms_command(cmd: SMSCommand):
    """Process SMS command"""
    if not sms_service:
        raise HTTPException(status_code=503, detail="SMS service not initialized")
    
    response = await sms_service.process_command(cmd.command)
    return {"response": response}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates"""
    await websocket.accept()
    active_connections.append(websocket)
    logger.info("WebSocket client connected")
    
    try:
        while True:
            # Keep connection alive
            await websocket.receive_text()
    except WebSocketDisconnect:
        active_connections.remove(websocket)
        logger.info("WebSocket client disconnected")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)

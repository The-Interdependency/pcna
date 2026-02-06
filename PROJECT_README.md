# PCNA Agent System

**Prime Circular Neural Architecture** - A self-optimizing, cloud-based AI agent system with trauma-informed, transparent, and harm reduction-focused design.

## 🌟 Features

### ✅ Implemented (Phase 1 MVP)

1. **📊 Web UI Dashboard**
   - Real-time PCNA topology visualization
   - System health monitoring with live metrics
   - Seed health tracking with spectral descriptors
   - EDCM analysis dashboard

2. **🤖 Self-Optimization Engine**
   - Automatic health monitoring
   - Anomaly detection
   - Mass conservation checking
   - Degraded seed flagging
   - Emergency rebalancing recommendations

3. **📱 SMS Check-in System** (Mock Mode)
   - Automated hourly health reports (simulated)
   - Critical alert system
   - Command interface (STATUS, HEALTH, LAST_TICK, HELP)
   - Ready for Twilio integration

4. **🧠 LLM Abstraction Layer** (Hot-Swappable)
   - OpenAI GPT-5.2 integration
   - Anthropic Claude 4 integration
   - Google Gemini integration
   - Automatic fallback cascade
   - Uses Emergent Universal Key

5. **📈 EDCM Analyzer**
   - Entropy calculation
   - Dissonance detection
   - Constraint strain analysis
   - Monetizable artifact generation
   - Insights and recommendations

### 🏗️ Architecture

```
PCNA System
├── Backend (FastAPI + Python)
│   ├── PCNA Core Engine
│   │   ├── Topology Management (53 seeds)
│   │   ├── Tensor State Engine
│   │   └── Markov Recursion
│   ├── LLM Orchestrator
│   ├── Self-Optimizer
│   ├── EDCM Analyzer
│   └── SMS Service
├── Frontend (React + Tailwind)
│   ├── System Health Dashboard
│   ├── Topology Visualization
│   ├── LLM Chat Interface
│   ├── EDCM Artifacts Viewer
│   └── SMS Console
└── Database (MongoDB)
    ├── EDCM Reports
    ├── System Metrics
    └── Message History
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- MongoDB
- Supervisor

### Installation

1. **Backend Setup**
```bash
cd /app/backend
pip install -r requirements.txt
```

2. **Frontend Setup**
```bash
cd /app/frontend
yarn install
```

3. **Start Services**
```bash
sudo supervisorctl restart all
```

4. **Access the System**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8001
- API Docs: http://localhost:8001/docs

## 📡 API Endpoints

### Health & Status
- `GET /api/health` - Health check
- `GET /api/system-health` - System health metrics
- `GET /api/topology` - PCNA topology structure
- `GET /api/seeds` - Active seeds status

### LLM Interface
- `POST /api/llm/chat` - Chat with LLM
  ```json
  {
    "prompt": "Your message",
    "provider": "openai|anthropic|gemini",
    "model": "gpt-5.2|claude-4-sonnet-20250514|gemini-2.5-pro"
  }
  ```

### EDCM Analysis
- `GET /api/edcm/analyze` - Run EDCM analysis
- `GET /api/edcm/artifacts` - Get monetizable artifacts

### SMS Commands
- `POST /api/sms/command` - Process SMS command
  ```json
  {
    "command": "STATUS|HEALTH|LAST_TICK|HELP"
  }
  ```

## 🎯 PCNA Topology

### Seed Structure (53 total)
- **1 Global Router** (ID: 0) - System coordination
- **4 Sentinels** (IDs: 1-4) - Diagnostics only
- **7 Meta Routers** (IDs: 5, 13, 21, 29, 37, 45, 53) - Cluster aggregation
- **49 Compute Seeds** - Primary computation

### Routing Patterns
- **7:3 Heptagram** - Compute seed connections (sparse communication)
- **7:2 Sentinel Scan** - Diagnostic monitoring pattern
- **Prime-indexed** - Avoids harmonic aliasing

## 🔐 Authentication

### Emergent Universal Key
The system uses Emergent's Universal LLM Key which works across:
- OpenAI (GPT-5.2, GPT-5.1, GPT-5, GPT-5-mini)
- Anthropic (Claude 4 Sonnet, Claude Opus, Claude Haiku)
- Google (Gemini 2.5 Pro, Gemini 3 Flash)

Key is configured in `/app/backend/.env`:
```env
EMERGENT_LLM_KEY=sk-emergent-7C50cAbD740Ea562b5
```

## 📊 EDCM (Entropy Dissonance Constraint Management)

EDCM analyzes system state and generates monetizable artifacts:

### Metrics
1. **Entropy** - System diversity and distribution
2. **Dissonance** - Deviation from expected patterns
3. **Constraint Strain** - Mass conservation violations

### Artifacts
- Insights: Human-readable system analysis
- Recommendations: Prioritized actionable items
- Monetization Value: High/Medium/Low classification

## 🔧 Configuration

### Backend (.env)
```env
EMERGENT_LLM_KEY=sk-emergent-7C50cAbD740Ea562b5
MONGO_URL=mongodb://localhost:27017/
SMS_MOCK_MODE=true
ENVIRONMENT=development
```

### Frontend (.env)
```env
REACT_APP_BACKEND_URL=http://localhost:8001
REACT_APP_WS_URL=ws://localhost:8001
```

## 📱 SMS Integration (Production)

To enable real SMS with Twilio:

1. Sign up at https://www.twilio.com
2. Get your credentials
3. Update `/app/backend/.env`:
```env
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=+1234567890
SMS_MOCK_MODE=false
```
4. Restart backend: `sudo supervisorctl restart backend`

## 🎨 UI Components

### System Health Dashboard
- Real-time health metrics
- Health trend charts
- Seed distribution
- EDCM analysis runner

### Topology Visualization
- Interactive circular topology
- Heptagram connection display
- Seed health indicators
- Detailed seed inspector

### LLM Chat Interface
- Multi-provider support
- Hot-swappable models
- Chat history
- Quick action templates

### EDCM Artifacts
- Artifact grid view
- Detailed report viewer
- Monetization value indicators
- Insight and recommendation display

### SMS Console
- Mock command simulator
- Message history
- Quick commands
- Production setup guide

## 🛠️ Development

### Backend Development
```bash
cd /app/backend
# Backend auto-reloads on file changes
tail -f /var/log/supervisor/backend.err.log
```

### Frontend Development
```bash
cd /app/frontend
# Frontend hot-reloads automatically
tail -f /var/log/supervisor/frontend.out.log
```

### Testing
```bash
# Test backend
curl http://localhost:8001/api/health

# Test LLM
curl -X POST http://localhost:8001/api/llm/chat \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Hello!", "provider":"openai", "model":"gpt-5.2"}'

# Test EDCM
curl http://localhost:8001/api/edcm/analyze
```

## 🌐 Future Features (Phase 2)

- [ ] Researcher outreach automation
- [ ] Moltbook (AI social media) integration
- [ ] Full Twilio SMS integration
- [ ] Advanced artifact monetization dashboard
- [ ] Multi-seed distributed deployment
- [ ] Google Cloud Platform deployment
- [ ] Interdependentway.org website integration
- [ ] Enhanced trauma-informed interaction framework

## 📝 Core Principles

### Trauma-Informed Design
- Transparent operations
- Explainable AI decisions
- Consent-based interactions
- Clear communication

### Harm Reduction
- Observable system state
- Graceful degradation
- Automatic health monitoring
- Emergency safeguards

### Interdependent Way
- AI-AI collaboration
- Human-AI interaction improvement
- Human-human relationship enhancement
- Competence through transparency

## 🤝 Contributing

This system is designed for:
- AI researchers interested in neural architectures
- Organizations working on trauma-informed AI
- Developers building distributed compute systems
- Anyone interested in transparent, ethical AI

## 📄 License

MIT License - see LICENSE file

## 🔗 Links

- **Interdependent Way**: https://interdependentway.org (coming soon)
- **EDCM Research**: See `/app/schemas/` for specifications
- **PCNA Whitepaper**: See `/app/README.md`

## 🆘 Support

For issues or questions:
1. Check logs: `/var/log/supervisor/`
2. Review API docs: `http://localhost:8001/docs`
3. Inspect system health dashboard
4. Use SMS console for diagnostics

---

**Built with ❤️ for the Interdependent Way Project**

*Creating better AI systems through trauma-informed design, transparency, and harm reduction.*

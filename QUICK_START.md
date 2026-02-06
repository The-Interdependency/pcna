# PCNA Agent System - Quick Start Guide

## ✅ System Status: OPERATIONAL

All Phase 1 MVP features are implemented and running!

## 🚀 Access Your System

### Web Dashboard
**URL:** http://localhost:3000

Navigate through the tabs:
- **Dashboard**: System health, EDCM analysis, metrics
- **Topology**: Interactive 53-seed visualization
- **LLM Chat**: Multi-provider AI chat (OpenAI, Claude, Gemini)
- **EDCM Artifacts**: Monetizable analysis reports
- **SMS Console**: Command interface (mock mode)

### Backend API
**URL:** http://localhost:8001
**API Docs:** http://localhost:8001/docs

## 📊 Quick Tests

### Test System Health
```bash
curl http://localhost:8001/api/system-health
```

### Test LLM Integration
```bash
curl -X POST http://localhost:8001/api/llm/chat \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Hello!","provider":"openai","model":"gpt-5.2"}'
```

### Run EDCM Analysis
```bash
curl http://localhost:8001/api/edcm/analyze
```

### Test SMS Commands
```bash
curl -X POST http://localhost:8001/api/sms/command \
  -H "Content-Type: application/json" \
  -d '{"command":"STATUS"}'
```

## 🔧 Service Management

### Check Status
```bash
sudo supervisorctl status
```

### Restart Services
```bash
# Restart all
sudo supervisorctl restart all

# Restart specific service
sudo supervisorctl restart backend
sudo supervisorctl restart frontend
```

### View Logs
```bash
# Backend logs
tail -f /var/log/supervisor/backend.err.log

# Frontend logs  
tail -f /var/log/supervisor/frontend.out.log

# MongoDB logs
tail -f /var/log/mongodb/mongod.log
```

## 🎯 Phase 1 MVP Features (✅ Complete)

### 1. Web UI Dashboard
- ✅ Real-time system health monitoring
- ✅ Interactive topology visualization
- ✅ Health trend charts
- ✅ Seed distribution displays
- ✅ Live WebSocket updates

### 2. Self-Optimization Engine
- ✅ Automatic health monitoring (every 30 seconds)
- ✅ Anomaly detection
- ✅ Mass conservation checking
- ✅ Degraded seed flagging
- ✅ Emergency rebalancing recommendations

### 3. LLM Abstraction Layer
- ✅ OpenAI GPT-5.2 integration
- ✅ Anthropic Claude 4 Sonnet integration
- ✅ Google Gemini 2.5 Pro integration
- ✅ Hot-swappable providers
- ✅ Automatic fallback cascade
- ✅ Using Emergent Universal Key

### 4. SMS Check-in System (Mock Mode)
- ✅ Mock SMS service (logs to console)
- ✅ Hourly check-in loop
- ✅ Command interface (STATUS, HEALTH, LAST_TICK, HELP)
- ✅ Ready for Twilio integration

### 5. EDCM Analyzer
- ✅ Entropy calculation
- ✅ Dissonance detection
- ✅ Constraint strain analysis
- ✅ Insight generation
- ✅ Actionable recommendations
- ✅ Monetizable artifact creation

## 📚 Additional Resources

### Documentation
- **Full README**: `/app/PROJECT_README.md`
- **PCNA Architecture**: `/app/README.md`
- **Schemas**: `/app/schemas/`

### Code Structure
```
/app/
├── backend/
│   ├── server.py                  # Main FastAPI server
│   ├── llm_abstraction.py         # LLM orchestrator
│   ├── optimization_engine.py     # Self-optimizer
│   ├── sms_service.py            # SMS integration
│   ├── edcm_engine.py            # EDCM analyzer
│   ├── moltbook_integration.py   # Moltbook stub (future)
│   └── researcher_outreach.py    # Outreach module (future)
├── frontend/
│   └── src/
│       ├── App.js
│       └── components/
│           ├── SystemHealthDashboard.js
│           ├── TopologyVisualization.js
│           ├── LLMInterface.js
│           ├── EDCMArtifacts.js
│           └── SMSConsole.js
├── core/                          # PCNA engine
│   ├── topology.py
│   ├── tensor_engine.py
│   └── main.py
└── scripts/
    ├── start.sh                   # Startup script
    └── status.sh                  # Status checker
```

## 🔐 Environment Variables

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

## 🚧 Phase 2 Features (Stubs Created)

### Ready for Implementation:
1. **Moltbook Integration** (`moltbook_integration.py`)
   - AI-only social media monitoring
   - Thread analysis and response
   - Sentiment tracking

2. **Researcher Outreach** (`researcher_outreach.py`)
   - Database management
   - Personalized message generation
   - Campaign tracking
   - Analytics dashboard

3. **Production SMS** (Twilio)
   - Add credentials to `.env`
   - Set `SMS_MOCK_MODE=false`

4. **Interdependentway.org Website**
   - Use PCNA dashboard as foundation
   - Add landing page
   - Public artifact showcase

## 🆘 Troubleshooting

### Backend Won't Start
```bash
# Check logs
tail -50 /var/log/supervisor/backend.err.log

# Verify dependencies
cd /app/backend && pip install -r requirements.txt

# Restart
sudo supervisorctl restart backend
```

### Frontend Build Errors
```bash
# Check logs
tail -50 /var/log/supervisor/frontend.out.log

# Reinstall dependencies
cd /app/frontend && yarn install

# Restart
sudo supervisorctl restart frontend
```

### MongoDB Issues
```bash
# Check if running
sudo supervisorctl status mongodb

# View logs
tail -50 /var/log/mongodb/mongod.log

# Ensure data directory exists
mkdir -p /data/db
sudo supervisorctl restart mongodb
```

### WebSocket Not Connecting
- Check that backend is running on port 8001
- Verify REACT_APP_WS_URL in frontend/.env
- Check browser console for errors

## 🎉 What's Working Right Now

1. ✅ **13 Active Seeds**: Global router, 4 sentinels, 8 compute seeds
2. ✅ **System Health**: 100% (HEALTHY status)
3. ✅ **LLM Integration**: OpenAI responding correctly
4. ✅ **Real-time Dashboard**: WebSocket updates every second
5. ✅ **EDCM Analysis**: Generating insights and recommendations
6. ✅ **MongoDB**: Storing artifacts and metrics
7. ✅ **Hot Reload**: Both frontend and backend auto-reload on changes

## 📞 Next Steps

1. **Explore the Dashboard**: Open http://localhost:3000
2. **Try LLM Chat**: Go to "LLM Chat" tab and send a message
3. **Run EDCM Analysis**: Click "Run Analysis" on Dashboard tab
4. **Test SMS Commands**: Use SMS Console tab
5. **View Topology**: Check out the interactive seed visualization
6. **Read Documentation**: See PROJECT_README.md for full details

## 🌐 For Google Cloud Deployment

When ready to deploy to Google Cloud:

1. Review `/app/schemas/pcna_ds.md` for deployment guide
2. Update environment variables for production
3. Configure Twilio for real SMS
4. Set up domain for Interdependentway.org
5. Enable Google Cloud services (Cloud Run, GKE)

---

**🎊 Congratulations! Your PCNA Agent System is fully operational!**

Built with ❤️ for the Interdependent Way Project

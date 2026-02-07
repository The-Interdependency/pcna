# Quick Reference - PCNA System Commands

## ⚠️ Important Note
You're running as **root** user, so **DO NOT use `sudo`** - it's not needed and will cause "command not found" errors.

---

## 🎮 Service Control

### Check Status
```bash
supervisorctl status
```

### Restart Services
```bash
# Restart everything
supervisorctl restart all

# Restart individual services
supervisorctl restart backend
supervisorctl restart frontend
supervisorctl restart mongodb
```

### Stop Services
```bash
supervisorctl stop all
supervisorctl stop backend
supervisorctl stop frontend
```

### Start Services
```bash
supervisorctl start all
supervisorctl start backend
supervisorctl start frontend
```

### Reload Configuration
```bash
supervisorctl reload
# or
supervisorctl reread && supervisorctl update
```

---

## 📊 System Health Checks

### Quick Status Check
```bash
/app/scripts/status.sh
```

### Manual Health Checks
```bash
# Backend health
curl http://localhost:8001/api/health

# System health
curl http://localhost:8001/api/system-health

# Active seeds
curl http://localhost:8001/api/seeds

# Topology
curl http://localhost:8001/api/topology
```

### Test LLM Integration
```bash
curl -X POST http://localhost:8001/api/llm/chat \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Hello","provider":"openai","model":"gpt-5.2"}'
```

### Run EDCM Analysis
```bash
curl http://localhost:8001/api/edcm/analyze
```

---

## 📜 View Logs

### Backend Logs
```bash
# Error logs
tail -f /var/log/supervisor/backend.err.log

# Last 50 lines
tail -50 /var/log/supervisor/backend.err.log

# Output logs
tail -f /var/log/supervisor/backend.out.log
```

### Frontend Logs
```bash
# Output logs
tail -f /var/log/supervisor/frontend.out.log

# Last 50 lines
tail -50 /var/log/supervisor/frontend.out.log
```

### MongoDB Logs
```bash
tail -f /var/log/mongodb/mongod.log
```

### All Supervisor Logs
```bash
tail -f /var/log/supervisor/supervisord.log
```

---

## 🔧 Troubleshooting

### Service Won't Start
```bash
# Check status
supervisorctl status backend

# View error logs
tail -50 /var/log/supervisor/backend.err.log

# Restart
supervisorctl restart backend
```

### Backend Issues
```bash
# Check if dependencies are installed
cd /app/backend
pip list | grep -E "fastapi|emergent"

# Reinstall dependencies
/app/scripts/install_backend.sh

# Restart
supervisorctl restart backend
```

### Frontend Issues
```bash
# Check Node.js
node --version
yarn --version

# Reinstall dependencies
cd /app/frontend
rm -rf node_modules
yarn install

# Restart
supervisorctl restart frontend
```

### MongoDB Issues
```bash
# Check if running
supervisorctl status mongodb

# Check logs
tail -50 /var/log/mongodb/mongod.log

# Ensure data directory exists
mkdir -p /data/db

# Restart
supervisorctl restart mongodb
```

### Complete System Reset
```bash
# Stop all
supervisorctl stop all

# Wait
sleep 3

# Start all
supervisorctl start all

# Check status
supervisorctl status
```

---

## 🚀 Quick Start Commands

### Start Everything
```bash
supervisorctl restart all
sleep 5
/app/scripts/status.sh
```

### Check Everything
```bash
# System status
/app/scripts/status.sh

# Or use helper
/app/scripts/commands.sh
```

---

## 📍 Access URLs

- **Dashboard**: http://localhost:3000
- **Backend API**: http://localhost:8001
- **API Docs**: http://localhost:8001/docs

---

## 📁 Important Paths

### Code
- Backend: `/app/backend/`
- Frontend: `/app/frontend/`
- Scripts: `/app/scripts/`

### Logs
- Backend: `/var/log/supervisor/backend.err.log`
- Frontend: `/var/log/supervisor/frontend.out.log`
- MongoDB: `/var/log/mongodb/mongod.log`

### Configuration
- Supervisor: `/etc/supervisor/conf.d/pcna.conf`
- Backend env: `/app/backend/.env`
- Frontend env: `/app/frontend/.env`

---

## ✅ Common Tasks

### Update Backend Code
```bash
# Edit code in /app/backend/
# Backend auto-reloads (no restart needed)
```

### Update Frontend Code
```bash
# Edit code in /app/frontend/src/
# Frontend hot-reloads (no restart needed)
```

### Install New Python Package
```bash
cd /app/backend
pip install package-name
# Add to requirements.txt
supervisorctl restart backend
```

### Install New Node Package
```bash
cd /app/frontend
yarn add package-name
# package.json auto-updates
supervisorctl restart frontend
```

### View All Commands
```bash
/app/scripts/commands.sh
```

---

## 💡 Pro Tips

1. **No sudo needed** - You're root, commands work directly
2. **Hot reload enabled** - Most code changes apply automatically
3. **Check logs first** - When debugging, always check logs
4. **Use helper scripts** - `/app/scripts/` has useful tools
5. **Status check** - Run `/app/scripts/status.sh` anytime

---

## 🆘 Emergency Commands

### Everything Broken?
```bash
supervisorctl restart all
```

### Still Not Working?
```bash
supervisorctl stop all
sleep 5
supervisorctl start all
/app/scripts/status.sh
```

### Need Full Restart?
```bash
supervisorctl reload
```

---

**Remember: No `sudo` needed - you're already root!** ✅

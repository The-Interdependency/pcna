# Installation Guide - PCNA Agent System

## ✅ Issue Resolved: emergentintegrations Installation Error

### Problem
The error occurred because `emergentintegrations` is a custom library that requires a special installation URL.

### Solution
The library must be installed separately with the Emergent package index:

```bash
pip install emergentintegrations --extra-index-url https://d33sy5i8bnduwe.cloudfront.net/simple/
```

---

## 📦 Complete Installation Steps

### Method 1: Automated Installation (Recommended)

Use the provided installation script:

```bash
# Backend installation
/app/scripts/install_backend.sh

# Frontend installation
cd /app/frontend && yarn install
```

### Method 2: Manual Installation

#### Backend

```bash
cd /app/backend

# Install standard dependencies
pip install -r requirements.txt

# Install emergentintegrations (special)
pip install emergentintegrations --extra-index-url https://d33sy5i8bnduwe.cloudfront.net/simple/

# Verify
python -c "import emergentintegrations; print('Success!')"
```

#### Frontend

```bash
cd /app/frontend

# Install dependencies
yarn install

# Verify
yarn --version
```

---

## 🔄 If You Need to Reinstall

### Complete Clean Reinstall

```bash
# Stop services
sudo supervisorctl stop all

# Backend
cd /app/backend
pip uninstall -y emergentintegrations
pip install -r requirements.txt
pip install emergentintegrations --extra-index-url https://d33sy5i8bnduwe.cloudfront.net/simple/

# Frontend
cd /app/frontend
rm -rf node_modules yarn.lock
yarn install

# Restart services
sudo supervisorctl restart all
```

---

## 📋 Dependencies List

### Backend (Python)
- **FastAPI** - Web framework
- **Uvicorn** - ASGI server
- **Motor** - Async MongoDB driver
- **PyMongo** - MongoDB driver
- **NumPy** - Tensor operations
- **Pydantic** - Data validation
- **aiohttp** - Async HTTP client
- **python-dotenv** - Environment variables
- **structlog** - Structured logging
- **emergentintegrations** ⚠️ (requires special index URL)

### Frontend (Node.js)
- **React** 18.2.0
- **Tailwind CSS** 3.4.0
- **Axios** - HTTP client
- **Recharts** - Data visualization
- **D3** - Advanced visualizations

---

## ⚙️ Environment Configuration

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
DANGEROUSLY_DISABLE_HOST_CHECK=true
WDS_SOCKET_PORT=0
```

---

## 🚀 Starting the System

### After Installation

```bash
# Start all services
sudo supervisorctl restart all

# Check status
sudo supervisorctl status

# Expected output:
# backend     RUNNING
# frontend    RUNNING
# mongodb     RUNNING
```

### Verify Installation

```bash
# Test backend
curl http://localhost:8001/api/health

# Test LLM
curl -X POST http://localhost:8001/api/llm/chat \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Hello","provider":"openai","model":"gpt-5.2"}'

# Check frontend
curl http://localhost:3000 | grep "PCNA"
```

---

## 🐛 Troubleshooting

### emergentintegrations Not Found
```bash
# Install with correct URL
pip install emergentintegrations --extra-index-url https://d33sy5i8bnduwe.cloudfront.net/simple/
```

### Motor/PyMongo Version Conflict
```bash
# Upgrade motor
pip install --upgrade 'motor>=3.7.0' 'pymongo>=4.6.0,<5.0'
```

### Frontend Won't Compile
```bash
# Clear cache and reinstall
cd /app/frontend
rm -rf node_modules yarn.lock .cache
yarn install
```

### Services Won't Start
```bash
# Check logs
tail -f /var/log/supervisor/backend.err.log
tail -f /var/log/supervisor/frontend.out.log

# Restart supervisor
sudo supervisorctl reload
```

---

## 📍 Important Paths

### Code
- Backend: `/app/backend/`
- Frontend: `/app/frontend/`
- Core PCNA: `/app/core/`
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

## ✅ Post-Installation Checklist

- [ ] Backend dependencies installed (including emergentintegrations)
- [ ] Frontend dependencies installed (yarn)
- [ ] MongoDB running
- [ ] Backend service running (port 8001)
- [ ] Frontend service running (port 3000)
- [ ] Backend health check passes
- [ ] LLM integration working
- [ ] Dashboard accessible

---

## 🆘 Need Help?

### Quick Status Check
```bash
/app/scripts/status.sh
```

### Complete Restart
```bash
sudo supervisorctl restart all
sleep 5
/app/scripts/status.sh
```

### Check Individual Service
```bash
# Backend
sudo supervisorctl status backend
tail -20 /var/log/supervisor/backend.err.log

# Frontend
sudo supervisorctl status frontend
tail -20 /var/log/supervisor/frontend.out.log
```

---

## 🎉 Success!

Once all checks pass, access your system:

- **Dashboard**: http://localhost:3000
- **API**: http://localhost:8001
- **Docs**: http://localhost:8001/docs

The system is now fully operational! 🚀

---

*Installation issue resolved - emergentintegrations now installs correctly*

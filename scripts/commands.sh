#!/bin/bash

# PCNA System Management Commands
# Use these commands to control your system

echo "🎛️  PCNA System Control Commands"
echo "=================================="
echo ""

# Check Status
echo "📊 CHECK STATUS:"
echo "  supervisorctl status"
echo ""

# Restart Commands
echo "🔄 RESTART SERVICES:"
echo "  supervisorctl restart all          # Restart everything"
echo "  supervisorctl restart backend      # Restart backend only"
echo "  supervisorctl restart frontend     # Restart frontend only"
echo "  supervisorctl restart mongodb      # Restart MongoDB only"
echo ""

# Stop Commands
echo "🛑 STOP SERVICES:"
echo "  supervisorctl stop all"
echo "  supervisorctl stop backend"
echo "  supervisorctl stop frontend"
echo ""

# Start Commands
echo "▶️  START SERVICES:"
echo "  supervisorctl start all"
echo "  supervisorctl start backend"
echo "  supervisorctl start frontend"
echo ""

# Reload Configuration
echo "🔧 RELOAD CONFIGURATION:"
echo "  supervisorctl reload"
echo "  supervisorctl reread && supervisorctl update"
echo ""

# View Logs
echo "📜 VIEW LOGS:"
echo "  tail -f /var/log/supervisor/backend.err.log"
echo "  tail -f /var/log/supervisor/frontend.out.log"
echo "  tail -f /var/log/mongodb/mongod.log"
echo ""

# Quick Tests
echo "🧪 QUICK TESTS:"
echo "  curl http://localhost:8001/api/health"
echo "  curl http://localhost:8001/api/system-health"
echo "  /app/scripts/status.sh"
echo ""

# Current Status
echo "📍 CURRENT STATUS:"
supervisorctl status

echo ""
echo "💡 TIP: You're running as root, so 'sudo' is not needed!"

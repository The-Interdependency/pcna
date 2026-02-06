#!/bin/bash

# PCNA Agent System - Startup Script
# This script initializes and starts all services

set -e

echo "🚀 Starting PCNA Agent System..."
echo "================================"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if MongoDB is installed
echo -e "${BLUE}Checking MongoDB...${NC}"
if ! command -v mongod &> /dev/null; then
    echo -e "${YELLOW}MongoDB not found. Installing...${NC}"
    apt-get update
    apt-get install -y mongodb
fi

# Ensure MongoDB data directory exists
mkdir -p /data/db /var/log/mongodb

# Check backend dependencies
echo -e "${BLUE}Checking backend dependencies...${NC}"
cd /app/backend
if [ ! -d "/root/.venv" ] || ! pip list | grep -q "fastapi"; then
    echo -e "${YELLOW}Installing backend dependencies...${NC}"
    pip install -r requirements.txt
fi

# Check frontend dependencies
echo -e "${BLUE}Checking frontend dependencies...${NC}"
cd /app/frontend
if [ ! -d "node_modules" ]; then
    echo -e "${YELLOW}Installing frontend dependencies...${NC}"
    yarn install
fi

# Start services with supervisor
echo -e "${BLUE}Starting services...${NC}"
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl restart all

# Wait for services to start
echo -e "${YELLOW}Waiting for services to initialize...${NC}"
sleep 5

# Check service status
echo -e "${BLUE}Service Status:${NC}"
sudo supervisorctl status

# Test backend health
echo -e "\n${BLUE}Testing backend health...${NC}"
if curl -s http://localhost:8001/api/health | grep -q "healthy"; then
    echo -e "${GREEN}✓ Backend is healthy${NC}"
else
    echo -e "${RED}✗ Backend health check failed${NC}"
fi

# Test system health
echo -e "${BLUE}Testing system health...${NC}"
HEALTH=$(curl -s http://localhost:8001/api/system-health)
echo -e "${GREEN}$HEALTH${NC}"

echo -e "\n${GREEN}================================${NC}"
echo -e "${GREEN}🎉 PCNA Agent System Started!${NC}"
echo -e "${GREEN}================================${NC}"
echo ""
echo -e "📊 Dashboard: ${BLUE}http://localhost:3000${NC}"
echo -e "🔌 Backend API: ${BLUE}http://localhost:8001${NC}"
echo -e "📚 API Docs: ${BLUE}http://localhost:8001/docs${NC}"
echo ""
echo -e "Logs:"
echo -e "  Backend: tail -f /var/log/supervisor/backend.err.log"
echo -e "  Frontend: tail -f /var/log/supervisor/frontend.out.log"
echo -e "  MongoDB: tail -f /var/log/mongodb/mongod.log"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop monitoring. Services will continue running.${NC}"
echo ""

# Monitor logs
tail -f /var/log/supervisor/backend.err.log

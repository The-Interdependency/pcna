#!/bin/bash

# PCNA System Status Check

echo "🔍 PCNA Agent System Status"
echo "============================"
echo ""

# Service Status
echo "📊 Service Status:"
supervisorctl status
echo ""

# Backend Health
echo "🏥 Backend Health:"
curl -s http://localhost:8001/api/health | python3 -m json.tool
echo ""

# System Health
echo "💚 System Health:"
curl -s http://localhost:8001/api/system-health | python3 -m json.tool
echo ""

# Active Seeds
echo "🌱 Active Seeds:"
curl -s http://localhost:8001/api/seeds | python3 -c "import sys, json; data=json.load(sys.stdin); print(f'Total: {len(data)} seeds')"
echo ""

# LLM Status
echo "🤖 LLM Test:"
curl -s -X POST http://localhost:8001/api/llm/chat \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Say OK","provider":"openai","model":"gpt-5.2"}' | python3 -m json.tool
echo ""

echo "✅ Status check complete!"

#!/bin/bash

# Backend Installation Script
# Installs all Python dependencies including emergentintegrations

set -e

echo "🔧 Installing Backend Dependencies..."
echo "====================================="

cd /app/backend

# Install standard dependencies
echo "📦 Installing standard packages..."
pip install -r requirements.txt

# Install emergentintegrations with special index
echo "🔑 Installing emergentintegrations library..."
pip install emergentintegrations --extra-index-url https://d33sy5i8bnduwe.cloudfront.net/simple/

# Verify installation
echo ""
echo "✅ Verifying installation..."
python -c "import fastapi; print('✓ FastAPI installed')"
python -c "import motor; print('✓ Motor (MongoDB) installed')"
python -c "import emergentintegrations; print('✓ EmergentIntegrations installed')"

echo ""
echo "🎉 Backend dependencies installed successfully!"
echo ""
echo "To start the backend:"
echo "  sudo supervisorctl restart backend"

#!/bin/bash
# ============================================
# Stop Script - Mac/Linux
# ============================================

echo ""
echo "Stopping the AI Metadata Application..."
echo ""

if ! command -v docker-compose &> /dev/null; then
    docker-compose() { docker compose "$@"; }
fi

docker-compose down

echo ""
echo "Application stopped successfully."
echo ""
echo "To start again, run: ./start.sh"
echo ""

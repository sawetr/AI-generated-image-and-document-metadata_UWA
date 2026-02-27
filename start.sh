#!/bin/bash
# ============================================
# Quick Start Script - Mac/Linux
# AI Image & Document Metadata Application
# ============================================

echo ""
echo "============================================"
echo "AI Metadata Application - Quick Start"
echo "============================================"
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "ERROR: Docker is not installed."
    echo ""
    echo "Please install Docker Desktop from:"
    echo "https://www.docker.com/products/docker-desktop"
    echo ""
    exit 1
fi

# Make docker-compose available if only docker compose (newer versions) exists
if ! command -v docker-compose &> /dev/null; then
    docker-compose() { docker compose "$@"; }
fi

echo "[1/4] Stopping any existing containers..."
docker-compose down

echo ""
echo "[2/4] Building the application (this may take a few minutes)..."
docker-compose build

echo ""
echo "[3/4] Starting MongoDB and the application..."
docker-compose up -d

echo ""
echo "[4/4] Waiting for services to be ready..."
sleep 10

echo ""
echo "============================================"
echo "READY!"
echo "============================================"
echo ""
echo "Open your browser and go to:"
echo "http://127.0.0.1:5000"
echo ""
echo "To stop the application, run: ./stop.sh"
echo ""
echo "To view logs, run: docker-compose logs -f"
echo ""

#!/bin/bash
# Script pour builder et lancer Xpra LTS
# À exécuter dans Git Bash

set -e

echo "========================================="
echo "Building Xpra LTS Image"
echo "========================================="
echo ""

# Build avec --no-cache pour forcer le téléchargement du nouveau repo
echo "Building image (cela peut prendre 10-15 minutes)..."
docker compose -f docker-compose.xpra.yml build --no-cache

echo ""
echo "========================================="
echo "Build Complete!"
echo "========================================="
echo ""

# Start le container
echo "Starting Xpra container..."
docker compose -f docker-compose.xpra.yml up -d

echo ""
echo "Waiting for Xpra to start (60 seconds)..."
sleep 60

echo ""
echo "========================================="
echo "Checking Xpra Version"
echo "========================================="
docker exec -it remote-ide-xpra xpra --version | head -n1

echo ""
echo "========================================="
echo "Xpra LTS is Ready!"
echo "========================================="
echo ""
echo "Access URL: http://localhost:8080"
echo ""
echo "To check logs:"
echo "  docker logs -f remote-ide-xpra"
echo ""
echo "To check stats:"
echo "  docker stats remote-ide-xpra"
echo ""
echo "To stop:"
echo "  docker compose -f docker-compose.xpra.yml down"
echo ""
echo "Opening browser..."
start http://localhost:8080

echo ""
echo "Done! 🚀"


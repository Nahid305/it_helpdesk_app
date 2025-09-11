#!/bin/bash

# Local Docker Test Script
# This script builds and tests the Docker container locally

echo "🐳 Building Docker image locally..."
docker build -t it-helpdesk:test .

echo "🧪 Testing Docker container..."
echo "Starting container on port 8501..."
docker run -d --name it-helpdesk-test -p 8501:8501 \
  -e GROK_API_KEY="test-key" \
  -e JWT_SECRET_KEY="test-secret-key" \
  it-helpdesk:test

echo "⏳ Waiting for container to start..."
sleep 10

echo "🔍 Checking container health..."
if curl -f http://localhost:8501/_stcore/health 2>/dev/null; then
    echo "✅ Container is healthy!"
    echo "🌐 Access the app at: http://localhost:8501"
else
    echo "❌ Container health check failed"
    echo "📋 Container logs:"
    docker logs it-helpdesk-test
fi

echo ""
echo "🛑 To stop the test container:"
echo "docker stop it-helpdesk-test && docker rm it-helpdesk-test"

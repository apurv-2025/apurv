# =============================================================================
# FILE: scripts/setup.sh
# =============================================================================
#!/bin/bash

set -e

echo "🚀 Setting up Enhanced EDI Claims Processing System"

# Check prerequisites
echo "📋 Checking prerequisites..."

if ! command -v docker &> /dev/null; then
    echo "❌ Docker is required but not installed"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is required but not installed"
    exit 1
fi

echo "✅ Prerequisites met"

# Setup environment
echo "🔧 Setting up environment..."

if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your configuration before continuing"
    echo "   Required: OPENAI_API_KEY or ANTHROPIC_API_KEY or CUSTOM_MODEL_ENDPOINT"
    exit 1
fi

# Load environment variables
source .env

# Validate required settings
if [ -z "$OPENAI_API_KEY" ] && [ -z "$ANTHROPIC_API_KEY" ] && [ -z "$CUSTOM_MODEL_ENDPOINT" ]; then
    echo "❌ No AI model configuration found. Please set one of:"
    echo "   - OPENAI_API_KEY for OpenAI models"
    echo "   - ANTHROPIC_API_KEY for Anthropic models"
    echo "   - CUSTOM_MODEL_ENDPOINT for custom models"
    exit 1
fi

echo "✅ Environment configuration validated"

# Build and deploy
echo "🐳 Building and deploying services..."

# Stop any existing containers
docker-compose down

# Build images
echo "Building Docker images..."
docker-compose build

# Start services
echo "Starting services..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to initialize..."
sleep 30

# Health checks
echo "🏥 Running health checks..."

# Check backend
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Backend service is healthy"
else
    echo "❌ Backend service is not responding"
    docker-compose logs backend
    exit 1
fi

# Check agent
if curl -f http://localhost:8000/api/agent/health > /dev/null 2>&1; then
    echo "✅ AI Agent is healthy"
    
    # Get agent details
    AGENT_HEALTH=$(curl -s http://localhost:8000/api/agent/health)
    MODEL_PROVIDER=$(echo $AGENT_HEALTH | grep -o '"model_provider":"[^"]*"' | cut -d'"' -f4)
    TOOLS_COUNT=$(echo $AGENT_HEALTH | grep -o '"tools_count":[0-9]*' | cut -d':' -f2)
    
    echo "   Model Provider: $MODEL_PROVIDER"
    echo "   Available Tools: $TOOLS_COUNT"
else
    echo "⚠️  AI Agent is not responding (check your API keys)"
    docker-compose logs backend
fi

# Check frontend
if curl -f http://localhost:3000 > /dev/null 2>&1; then
    echo "✅ Frontend is healthy"
else
    echo "❌ Frontend is not responding"
    docker-compose logs frontend
fi

# Setup complete
echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "📊 Access your application:"
echo "   Frontend:        http://localhost:3000"
echo "   Backend API:     http://localhost:8000"
echo "   API Documentation: http://localhost:8000/docs"
echo "   Agent API:       http://localhost:8000/api/agent"
echo ""
echo "🤖 Test the AI Agent:"
echo "   curl -X POST http://localhost:8000/api/agent/chat \\"
echo "     -H 'Content-Type: application/json' \\"
echo "     -d '{\"message\": \"Hello, what can you help me with?\", \"user_id\": \"test\"}'"
echo ""
echo "📚 Documentation:"
echo "   See docs/README.md for detailed usage instructions"
echo ""
echo "🛠️ Development:"
echo "   Run 'make help' for available commands"
echo "   Use 'docker-compose logs -f' to view logs"

# =============================================================================
# FILE: scripts/test.sh
# =============================================================================
#!/bin/bash

set -e

echo "🧪 Running comprehensive test suite"

# Backend tests
echo "🐍 Running backend tests..."
docker-compose exec backend python -m pytest app/tests/ -v --cov=app --cov-report=html

# Agent-specific tests
echo "🤖 Running agent tests..."
docker-compose exec backend python -m pytest app/tests/test_agent.py -v

# Load tests
echo "⚡ Running load tests..."
python scripts/load_test.py --concurrent=5 --requests=50

# Frontend tests (if available)
if [ -d "frontend/src/__tests__" ]; then
    echo "⚛️  Running frontend tests..."
    cd frontend && npm test -- --coverage --watchAll=false
    cd ..
fi

# Health checks
echo "🏥 Running health checks..."
curl -f http://localhost:8000/health
curl -f http://localhost:8000/api/agent/health
curl -f http://localhost:3000

echo "✅ All tests passed!"

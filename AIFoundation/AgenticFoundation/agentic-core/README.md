# Agentic Core - Reusable AI Agent Framework

## 🚀 **Overview**

Agentic Core is a modular, reusable AI agent framework that provides intelligent automation capabilities for any application. It includes frontend components, backend services, and database schemas that can be easily integrated into existing projects.

## ✨ **Features**

### **🤖 AI Agent Capabilities**
- **Natural Language Processing**: Chat with AI agents using plain English
- **Task Automation**: Automated task execution and workflow management
- **Intelligent Analysis**: AI-powered data analysis and insights
- **Multi-Model Support**: Support for Claude, GPT, and custom models
- **Real-time Processing**: Live task monitoring and status updates

### **🎨 Frontend Components**
- **Modern Chat Interface**: Claude.ai/ChatGPT-style chat components
- **Floating Widget**: Always-available chat widget
- **Dashboard**: Real-time metrics and performance monitoring
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Customizable UI**: Easy theming and branding

### **⚙️ Backend Services**
- **Agent Manager**: Centralized agent orchestration
- **Task Processing**: Asynchronous task execution
- **Tool Integration**: Extensible tool system
- **API Endpoints**: RESTful API for all operations
- **Health Monitoring**: System health and performance tracking

### **🗄️ Database Layer**
- **Conversation Storage**: Persistent chat history
- **Task Management**: Task tracking and status
- **User Management**: User sessions and preferences
- **Analytics**: Usage metrics and performance data

## 📦 **Installation**

### **Quick Start**
```bash
# Clone the repository
git clone <repository-url>
cd agentic-core

# Install dependencies
npm install

# Set up environment
cp .env.example .env
# Edit .env with your configuration

# Start the application
npm run dev
```

### **As a Package**
```bash
# Install as npm package
npm install @agentic/core

# Or using yarn
yarn add @agentic/core
```

## 🏗️ **Architecture**

```
agentic-core/
├── frontend/           # React components and UI
├── backend/            # FastAPI services and API
├── database/           # Database schemas and migrations
├── shared/             # Shared types and utilities
├── tools/              # Extensible tool system
├── examples/           # Integration examples
└── docs/              # Documentation
```

## 🔧 **Configuration**

### **Environment Variables**
```bash
# AI Model Configuration
AI_MODEL_PROVIDER=openai|anthropic|custom
AI_MODEL_NAME=gpt-4|claude-3-sonnet|custom
AI_API_KEY=your_api_key_here

# Database Configuration
DATABASE_URL=postgresql://user:pass@localhost/agentic
REDIS_URL=redis://localhost:6379

# Application Configuration
APP_NAME=Agentic Core
APP_VERSION=1.0.0
DEBUG=true
```

### **Model Configuration**
```yaml
# config/models.yaml
models:
  - name: "GPT-4"
    provider: "openai"
    model: "gpt-4"
    max_tokens: 4000
    temperature: 0.7
    
  - name: "Claude Sonnet"
    provider: "anthropic"
    model: "claude-3-sonnet-20240229"
    max_tokens: 4000
    temperature: 0.7
    
  - name: "Custom Model"
    provider: "custom"
    endpoint: "https://api.custom.com/v1/chat"
    headers:
      Authorization: "Bearer your_token"
```

## 🎯 **Usage Examples**

### **Frontend Integration**

#### **Basic Chat Component**
```jsx
import { AgentChat } from '@agentic/core/frontend';

function App() {
  return (
    <div className="h-screen">
      <AgentChat 
        apiUrl="http://localhost:8000"
        userId="user_123"
        model="gpt-4"
      />
    </div>
  );
}
```

#### **Floating Widget**
```jsx
import { FloatingChatWidget } from '@agentic/core/frontend';

function App() {
  return (
    <div>
      {/* Your app content */}
      <FloatingChatWidget 
        apiUrl="http://localhost:8000"
        position="bottom-right"
        theme="light"
      />
    </div>
  );
}
```

#### **Custom Chat Interface**
```jsx
import { useAgenticChat } from '@agentic/core/frontend';

function CustomChat() {
  const { messages, sendMessage, isLoading } = useAgenticChat({
    apiUrl: 'http://localhost:8000',
    userId: 'user_123',
    model: 'gpt-4'
  });

  return (
    <div>
      {messages.map(message => (
        <div key={message.id}>{message.content}</div>
      ))}
      <button onClick={() => sendMessage('Hello!')}>
        Send Message
      </button>
    </div>
  );
}
```

### **Backend Integration**

#### **FastAPI Integration**
```python
from agentic_core import AgenticAPI, AgentManager

# Initialize the API
app = FastAPI()
agentic_api = AgenticAPI(app)

# Add custom routes
@app.post("/custom/analyze")
async def analyze_data(data: dict):
    agent_manager = AgentManager()
    result = await agent_manager.process_task({
        "type": "analyze",
        "data": data,
        "user_id": "user_123"
    })
    return result
```

#### **Custom Tool Integration**
```python
from agentic_core.tools import BaseTool

class CustomAnalysisTool(BaseTool):
    name = "custom_analysis"
    description = "Perform custom data analysis"
    
    async def execute(self, data: dict) -> dict:
        # Your custom analysis logic
        result = self.analyze_data(data)
        return {
            "status": "success",
            "result": result,
            "confidence": 0.95
        }

# Register the tool
agent_manager = AgentManager()
agent_manager.register_tool(CustomAnalysisTool())
```

#### **Database Integration**
```python
from agentic_core.database import DatabaseManager, Conversation, Task

# Initialize database
db = DatabaseManager()

# Save conversation
conversation = Conversation(
    user_id="user_123",
    messages=[{"role": "user", "content": "Hello"}],
    model="gpt-4"
)
await db.save_conversation(conversation)

# Get conversation history
history = await db.get_conversation_history("user_123")
```

### **Database Schema**

#### **PostgreSQL Tables**
```sql
-- Conversations table
CREATE TABLE conversations (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    title VARCHAR(500),
    model VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Messages table
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER REFERENCES conversations(id),
    role VARCHAR(50) NOT NULL,
    content TEXT NOT NULL,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tasks table
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    task_type VARCHAR(100) NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    data JSONB,
    result JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP
);

-- Tools table
CREATE TABLE tools (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    config JSONB,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🔌 **Integration Patterns**

### **Pattern 1: Standalone Service**
```bash
# Run as a separate service
docker run -d \
  -p 8000:8000 \
  -e AI_API_KEY=your_key \
  -e DATABASE_URL=postgresql://... \
  agentic/core:latest
```

### **Pattern 2: Embedded Library**
```python
# Embed in existing Python application
from agentic_core import AgenticCore

agentic = AgenticCore(
    model_provider="openai",
    api_key="your_key",
    database_url="postgresql://..."
)

# Use in your application
result = await agentic.chat("Hello, how can you help me?")
```

### **Pattern 3: Microservice**
```yaml
# docker-compose.yml
version: '3.8'
services:
  agentic:
    image: agentic/core:latest
    ports:
      - "8000:8000"
    environment:
      - AI_API_KEY=${AI_API_KEY}
      - DATABASE_URL=${DATABASE_URL}
    volumes:
      - ./config:/app/config
```

## 🎨 **Customization**

### **Theming**
```css
/* Custom theme variables */
:root {
  --agentic-primary: #3B82F6;
  --agentic-secondary: #6B7280;
  --agentic-success: #10B981;
  --agentic-error: #EF4444;
  --agentic-warning: #F59E0B;
}
```

### **Custom Tools**
```python
# Define custom tools
class CustomTool(BaseTool):
    name = "custom_tool"
    description = "Custom functionality"
    
    async def execute(self, params: dict) -> dict:
        # Implementation
        return {"result": "success"}
```

### **Custom Models**
```python
# Custom model provider
class CustomModelProvider(BaseModelProvider):
    async def generate(self, prompt: str, config: dict) -> str:
        # Custom model implementation
        return "Generated response"
```

## 📊 **Monitoring & Analytics**

### **Health Checks**
```bash
# Check service health
curl http://localhost:8000/health

# Response:
{
  "status": "healthy",
  "version": "1.0.0",
  "uptime": "2h 30m",
  "active_tasks": 5,
  "model_status": "connected"
}
```

### **Metrics**
```python
# Get performance metrics
from agentic_core.metrics import MetricsCollector

metrics = MetricsCollector()
performance = await metrics.get_performance_metrics()
```

## 🔒 **Security**

### **Authentication**
```python
# JWT Authentication
from agentic_core.auth import JWTAuth

auth = JWTAuth(secret_key="your_secret")
app.add_middleware(auth.middleware)
```

### **Rate Limiting**
```python
# Rate limiting
from agentic_core.security import RateLimiter

limiter = RateLimiter(max_requests=100, window=3600)
app.add_middleware(limiter.middleware)
```

## 🚀 **Deployment**

### **Docker Deployment**
```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### **Kubernetes Deployment**
```yaml
# k8s-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: agentic-core
spec:
  replicas: 3
  selector:
    matchLabels:
      app: agentic-core
  template:
    metadata:
      labels:
        app: agentic-core
    spec:
      containers:
      - name: agentic
        image: agentic/core:latest
        ports:
        - containerPort: 8000
        env:
        - name: AI_API_KEY
          valueFrom:
            secretKeyRef:
              name: agentic-secrets
              key: ai-api-key
```

## 📚 **Documentation**

- [API Reference](./docs/api.md)
- [Component Library](./docs/components.md)
- [Tool Development](./docs/tools.md)
- [Deployment Guide](./docs/deployment.md)
- [Troubleshooting](./docs/troubleshooting.md)

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 **License**

MIT License - see [LICENSE](LICENSE) file for details.

## 🆘 **Support**

- **Documentation**: [docs.agentic.core](https://docs.agentic.core)
- **Issues**: [GitHub Issues](https://github.com/agentic/core/issues)
- **Discussions**: [GitHub Discussions](https://github.com/agentic/core/discussions)
- **Email**: support@agentic.core 
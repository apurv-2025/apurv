import React, { useState } from 'react';
import {
  AgentChat,
  EnhancedAgentChat,
  FloatingChatWidget,
  useAgenticChat,
  createAgenticChat,
  AgenticService
} from '@agentic/core-frontend';

// Example 1: Basic Chat Component
function BasicChatExample() {
  return (
    <div className="h-screen">
      <AgentChat 
        apiUrl="http://localhost:8000"
        userId="user_123"
        model="gpt-4"
        theme="light"
      />
    </div>
  );
}

// Example 2: Enhanced Chat with Sidebar
function EnhancedChatExample() {
  return (
    <div className="h-screen">
      <EnhancedAgentChat 
        apiUrl="http://localhost:8000"
        userId="user_123"
        model="gpt-4"
        enableHistory={true}
        enableMetrics={true}
      />
    </div>
  );
}

// Example 3: Floating Chat Widget
function FloatingWidgetExample() {
  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">
          My Application
        </h1>
        
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h2 className="text-xl font-semibold mb-4">Welcome to My App</h2>
          <p className="text-gray-600">
            This is your main application content. The AI assistant is available
            via the floating chat widget in the bottom-right corner.
          </p>
        </div>
        
        {/* Your app content goes here */}
        <div className="mt-8 grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h3 className="text-lg font-semibold mb-2">Feature 1</h3>
            <p className="text-gray-600">Description of feature 1</p>
          </div>
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h3 className="text-lg font-semibold mb-2">Feature 2</h3>
            <p className="text-gray-600">Description of feature 2</p>
          </div>
        </div>
      </div>
      
      {/* Floating Chat Widget */}
      <FloatingChatWidget 
        apiUrl="http://localhost:8000"
        position="bottom-right"
        theme="light"
        userId="user_123"
      />
    </div>
  );
}

// Example 4: Custom Chat Hook
function CustomChatExample() {
  const { messages, sendMessage, isLoading, error } = useAgenticChat({
    apiUrl: 'http://localhost:8000',
    userId: 'user_123',
    model: 'gpt-4'
  });

  const [inputMessage, setInputMessage] = useState('');

  const handleSend = () => {
    if (inputMessage.trim()) {
      sendMessage(inputMessage);
      setInputMessage('');
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-6">
      <h1 className="text-2xl font-bold mb-6">Custom Chat Interface</h1>
      
      {/* Messages */}
      <div className="bg-white rounded-lg shadow-lg p-4 mb-4 h-96 overflow-y-auto">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`mb-4 p-3 rounded-lg ${
              message.role === 'user'
                ? 'bg-blue-100 ml-12'
                : 'bg-gray-100 mr-12'
            }`}
          >
            <p className="text-sm font-medium mb-1">
              {message.role === 'user' ? 'You' : 'AI Assistant'}
            </p>
            <p className="text-gray-800">{message.content}</p>
          </div>
        ))}
        
        {isLoading && (
          <div className="text-center text-gray-500">
            AI is thinking...
          </div>
        )}
        
        {error && (
          <div className="text-center text-red-500">
            Error: {error.message}
          </div>
        )}
      </div>
      
      {/* Input */}
      <div className="flex gap-2">
        <input
          type="text"
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleSend()}
          placeholder="Type your message..."
          className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          disabled={isLoading}
        />
        <button
          onClick={handleSend}
          disabled={isLoading || !inputMessage.trim()}
          className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Send
        </button>
      </div>
    </div>
  );
}

// Example 5: Agentic Service Integration
function ServiceIntegrationExample() {
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);

  const agenticService = new AgenticService({
    apiUrl: 'http://localhost:8000',
    userId: 'user_123'
  });

  const handleTask = async () => {
    setLoading(true);
    try {
      const result = await agenticService.processTask({
        taskType: 'analyze',
        description: 'Analyze the current market trends',
        context: { industry: 'technology' }
      });
      setResponse(result);
    } catch (error) {
      console.error('Task failed:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-6">
      <h1 className="text-2xl font-bold mb-6">Service Integration</h1>
      
      <button
        onClick={handleTask}
        disabled={loading}
        className="px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50"
      >
        {loading ? 'Processing...' : 'Run Analysis Task'}
      </button>
      
      {response && (
        <div className="mt-6 bg-white rounded-lg shadow-lg p-4">
          <h3 className="text-lg font-semibold mb-2">Task Result</h3>
          <pre className="text-sm text-gray-800 whitespace-pre-wrap">
            {JSON.stringify(response, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
}

// Example 6: Dynamic Configuration
function DynamicConfigExample() {
  const [config, setConfig] = useState({
    apiUrl: 'http://localhost:8000',
    model: 'gpt-4',
    theme: 'light',
    enableHistory: true
  });

  const agenticChat = createAgenticChat(config);

  return (
    <div className="h-screen">
      <div className="p-4 bg-gray-100 border-b">
        <h2 className="text-lg font-semibold mb-2">Configuration</h2>
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium mb-1">Model</label>
            <select
              value={config.model}
              onChange={(e) => setConfig({ ...config, model: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg"
            >
              <option value="gpt-4">GPT-4</option>
              <option value="gpt-3.5-turbo">GPT-3.5 Turbo</option>
              <option value="claude-3-sonnet">Claude 3 Sonnet</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Theme</label>
            <select
              value={config.theme}
              onChange={(e) => setConfig({ ...config, theme: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg"
            >
              <option value="light">Light</option>
              <option value="dark">Dark</option>
            </select>
          </div>
        </div>
      </div>
      
      <agenticChat.EnhancedAgentChat />
    </div>
  );
}

// Example 7: Plugin Integration
function PluginExample() {
  const [plugins, setPlugins] = useState([]);

  // Example plugin
  const customPlugin = {
    name: 'custom-tool',
    component: ({ onExecute }) => (
      <button
        onClick={() => onExecute('custom-action')}
        className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700"
      >
        Custom Action
      </button>
    ),
    config: { enabled: true }
  };

  const addPlugin = () => {
    setPlugins([...plugins, customPlugin]);
  };

  return (
    <div className="h-screen">
      <div className="p-4 bg-gray-100 border-b">
        <button
          onClick={addPlugin}
          className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
        >
          Add Plugin
        </button>
      </div>
      
      <EnhancedAgentChat 
        apiUrl="http://localhost:8000"
        userId="user_123"
        plugins={plugins}
      />
    </div>
  );
}

// Main App Component
function App() {
  const [currentExample, setCurrentExample] = useState('basic');

  const examples = {
    basic: { component: BasicChatExample, title: 'Basic Chat' },
    enhanced: { component: EnhancedChatExample, title: 'Enhanced Chat' },
    floating: { component: FloatingWidgetExample, title: 'Floating Widget' },
    custom: { component: CustomChatExample, title: 'Custom Hook' },
    service: { component: ServiceIntegrationExample, title: 'Service Integration' },
    config: { component: DynamicConfigExample, title: 'Dynamic Config' },
    plugin: { component: PluginExample, title: 'Plugin System' }
  };

  const CurrentComponent = examples[currentExample].component;

  return (
    <div>
      {/* Navigation */}
      <nav className="bg-white shadow-lg border-b">
        <div className="max-w-7xl mx-auto px-4">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-bold text-gray-900">
                Agentic Core Examples
              </h1>
            </div>
            <div className="flex items-center space-x-4">
              {Object.entries(examples).map(([key, { title }]) => (
                <button
                  key={key}
                  onClick={() => setCurrentExample(key)}
                  className={`px-3 py-2 rounded-lg text-sm font-medium ${
                    currentExample === key
                      ? 'bg-blue-600 text-white'
                      : 'text-gray-600 hover:text-gray-900'
                  }`}
                >
                  {title}
                </button>
              ))}
            </div>
          </div>
        </div>
      </nav>

      {/* Current Example */}
      <CurrentComponent />
    </div>
  );
}

export default App; 
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Bot, MessageCircle, Zap, BookOpen, Settings, Activity } from 'lucide-react';

const AIAssistantPage = () => {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [userId] = useState(`user_${Math.random().toString(36).substr(2, 9)}`);
  const [examples, setExamples] = useState([]);
  const [tools, setTools] = useState([]);
  const [aiHealth, setAiHealth] = useState(null);

  const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8002';

  useEffect(() => {
    loadExamples();
    loadTools();
    checkAIHealth();
    // Add welcome message
    setMessages([
      {
        id: 1,
        role: 'assistant',
        content: 'Hello! I\'m your AI assistant for Prior Authorization. I can help you with creating authorization requests, checking status, generating EDI documents, looking up patients, and finding healthcare codes. How can I help you today?',
        timestamp: new Date().toISOString()
      }
    ]);
  }, []);

  const loadExamples = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/v1/agent/examples`);
      if (response.data.success) {
        setExamples(response.data.examples);
      }
    } catch (error) {
      console.error('Error loading examples:', error);
    }
  };

  const loadTools = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/v1/agent/tools`);
      if (response.data.success) {
        setTools(response.data.tools);
      }
    } catch (error) {
      console.error('Error loading tools:', error);
    }
  };

  const checkAIHealth = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/v1/agent/health`);
      setAiHealth(response.data);
    } catch (error) {
      console.error('Error checking AI health:', error);
      setAiHealth({ status: 'unhealthy', error: error.message });
    }
  };

  const sendMessage = async () => {
    if (!inputMessage.trim() || isLoading) return;

    const userMessage = {
      id: Date.now(),
      role: 'user',
      content: inputMessage,
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      const response = await axios.post(`${API_BASE_URL}/api/v1/agent/chat`, {
        message: inputMessage,
        user_id: userId
      });

      if (response.data.success) {
        const assistantMessage = {
          id: Date.now() + 1,
          role: 'assistant',
          content: response.data.response,
          timestamp: response.data.timestamp
        };
        setMessages(prev => [...prev, assistantMessage]);
      } else {
        const errorMessage = {
          id: Date.now() + 1,
          role: 'assistant',
          content: response.data.error || 'Sorry, I encountered an error. Please try again.',
          timestamp: new Date().toISOString()
        };
        setMessages(prev => [...prev, errorMessage]);
      }
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = {
        id: Date.now() + 1,
        role: 'assistant',
        content: 'Sorry, I\'m having trouble connecting right now. Please try again later.',
        timestamp: new Date().toISOString()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const useExample = (example) => {
    setInputMessage(example);
  };

  const clearConversation = () => {
    setMessages([
      {
        id: Date.now(),
        role: 'assistant',
        content: 'Hello! I\'m your AI assistant for Prior Authorization. I can help you with creating authorization requests, checking status, generating EDI documents, looking up patients, and finding healthcare codes. How can I help you today?',
        timestamp: new Date().toISOString()
      }
    ]);
  };

  return (
    <div className="max-w-6xl mx-auto">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center space-x-3 mb-4">
          <div className="p-3 bg-blue-100 rounded-lg">
            <Bot className="h-8 w-8 text-blue-600" />
          </div>
          <div>
            <h1 className="text-3xl font-bold text-gray-900">AI Assistant</h1>
            <p className="text-gray-600">Intelligent help for Prior Authorization workflows</p>
          </div>
        </div>
        
        {/* AI Health Status */}
        {aiHealth && (
          <div className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${
            aiHealth.status === 'healthy' 
              ? 'bg-green-100 text-green-800' 
              : aiHealth.status === 'degraded'
              ? 'bg-yellow-100 text-yellow-800'
              : 'bg-red-100 text-red-800'
          }`}>
            <Activity className="h-4 w-4 mr-2" />
            AI Status: {aiHealth.status}
          </div>
        )}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Chat Interface */}
        <div className="lg:col-span-2">
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 h-[600px] flex flex-col">
            {/* Chat Header */}
            <div className="bg-blue-600 text-white p-4 rounded-t-lg flex justify-between items-center">
              <div className="flex items-center space-x-2">
                <MessageCircle className="h-5 w-5" />
                <span className="font-semibold">Chat with AI Assistant</span>
              </div>
              <button
                onClick={clearConversation}
                className="text-white hover:text-gray-200 transition-colors text-sm"
              >
                Clear Chat
              </button>
            </div>

            {/* Messages */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
              {messages.map((message) => (
                <div
                  key={message.id}
                  className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div
                    className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                      message.role === 'user'
                        ? 'bg-blue-600 text-white'
                        : 'bg-gray-100 text-gray-800'
                    }`}
                  >
                    <p className="text-sm whitespace-pre-wrap">{message.content}</p>
                    <p className="text-xs opacity-70 mt-1">
                      {new Date(message.timestamp).toLocaleTimeString()}
                    </p>
                  </div>
                </div>
              ))}
              {isLoading && (
                <div className="flex justify-start">
                  <div className="bg-gray-100 text-gray-800 px-4 py-2 rounded-lg">
                    <div className="flex space-x-1">
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                    </div>
                  </div>
                </div>
              )}
            </div>

            {/* Input */}
            <div className="p-4 border-t border-gray-200">
              <div className="flex space-x-2">
                <textarea
                  value={inputMessage}
                  onChange={(e) => setInputMessage(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder="Type your message..."
                  className="flex-1 border border-gray-300 rounded-lg px-3 py-2 text-sm resize-none focus:outline-none focus:ring-2 focus:ring-blue-500"
                  rows="2"
                  disabled={isLoading}
                />
                <button
                  onClick={sendMessage}
                  disabled={!inputMessage.trim() || isLoading}
                  className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white px-4 py-2 rounded-lg transition-colors flex items-center"
                >
                  <Zap className="w-4 h-4" />
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Examples */}
          {examples.length > 0 && (
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <div className="flex items-center space-x-2 mb-4">
                <BookOpen className="h-5 w-5 text-blue-600" />
                <h3 className="font-semibold text-gray-900">Try These Examples</h3>
              </div>
              <div className="space-y-3">
                {examples.slice(0, 3).map((category, index) => (
                  <div key={index}>
                    <h4 className="text-sm font-medium text-gray-700 mb-2">{category.category}</h4>
                    {category.examples.slice(0, 1).map((example, exampleIndex) => (
                      <button
                        key={exampleIndex}
                        onClick={() => useExample(example.user)}
                        className="text-sm text-blue-600 hover:text-blue-800 block text-left w-full p-2 rounded hover:bg-blue-50 transition-colors"
                      >
                        "{example.user}"
                      </button>
                    ))}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Available Tools */}
          {tools.length > 0 && (
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <div className="flex items-center space-x-2 mb-4">
                <Settings className="h-5 w-5 text-blue-600" />
                <h3 className="font-semibold text-gray-900">Available Tools</h3>
              </div>
              <div className="space-y-2">
                {tools.map((tool, index) => (
                  <div key={index} className="text-sm">
                    <div className="font-medium text-gray-700">{tool.name}</div>
                    <div className="text-gray-500">{tool.description}</div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Quick Actions */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h3 className="font-semibold text-gray-900 mb-4">Quick Actions</h3>
            <div className="space-y-2">
              <button
                onClick={() => useExample("I need to create a prior authorization request")}
                className="w-full text-left p-2 rounded hover:bg-gray-50 transition-colors text-sm"
              >
                Create Prior Authorization
              </button>
              <button
                onClick={() => useExample("Check the status of my authorization request")}
                className="w-full text-left p-2 rounded hover:bg-gray-50 transition-colors text-sm"
              >
                Check Authorization Status
              </button>
              <button
                onClick={() => useExample("Generate an EDI 278 document")}
                className="w-full text-left p-2 rounded hover:bg-gray-50 transition-colors text-sm"
              >
                Generate EDI Document
              </button>
              <button
                onClick={() => useExample("Look up patient information")}
                className="w-full text-left p-2 rounded hover:bg-gray-50 transition-colors text-sm"
              >
                Lookup Patient
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AIAssistantPage; 
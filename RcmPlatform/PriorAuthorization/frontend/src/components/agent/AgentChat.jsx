import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, Clock, CheckCircle, AlertCircle, Shield, FileText, CheckCircle2, AlertTriangle, MessageSquare } from 'lucide-react';
import axios from 'axios';

const AgentChat = () => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'assistant',
      content: "Hello! I'm your AI Prior Authorization Assistant. I can help you with creating authorization requests, checking status, generating EDI documents, looking up patients, and finding healthcare codes. What would you like to do today?",
      timestamp: new Date(),
      suggestions: [
        "Create prior authorization request",
        "Check authorization status",
        "Generate EDI document",
        "Look up patient information"
      ]
    }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [userId] = useState(`user_${Math.random().toString(36).substr(2, 9)}`);
  const messagesEndRef = useRef(null);

  const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8002';

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async () => {
    if (!inputMessage.trim() || isLoading) return;

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: inputMessage,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      const response = await axios.post(`${API_BASE_URL}/api/v1/agent/chat`, {
        message: inputMessage,
        user_id: userId,
        context: {}
      });

      const assistantMessage = {
        id: Date.now() + 1,
        type: 'assistant',
        content: response.data.response || response.data.error || "I'm sorry, I couldn't process your request.",
        timestamp: new Date(),
        suggestions: generateSuggestions(inputMessage.toLowerCase()),
        isError: !response.data.success
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = {
        id: Date.now() + 1,
        type: 'assistant',
        content: "I'm sorry, I'm having trouble connecting right now. Please try again in a moment.",
        timestamp: new Date(),
        isError: true
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const generateSuggestions = (message) => {
    if (message.includes('create') || message.includes('authorization') || message.includes('request')) {
      return [
        "Check authorization status",
        "Generate EDI 278 document",
        "Look up patient information",
        "Find healthcare codes"
      ];
    } else if (message.includes('status') || message.includes('check')) {
      return [
        "Create prior authorization request",
        "Generate EDI document",
        "Look up patient information",
        "Find healthcare codes"
      ];
    } else if (message.includes('edi') || message.includes('document') || message.includes('generate')) {
      return [
        "Create prior authorization request",
        "Check authorization status",
        "Look up patient information",
        "Find healthcare codes"
      ];
    } else if (message.includes('patient') || message.includes('lookup') || message.includes('find')) {
      return [
        "Create prior authorization request",
        "Check authorization status",
        "Generate EDI document",
        "Find healthcare codes"
      ];
    } else if (message.includes('code') || message.includes('cpt') || message.includes('icd')) {
      return [
        "Create prior authorization request",
        "Check authorization status",
        "Generate EDI document",
        "Look up patient information"
      ];
    }
    
    return [
      "Create prior authorization request",
      "Check authorization status",
      "Generate EDI document",
      "Look up patient information"
    ];
  };

  const handleSuggestionClick = (suggestion) => {
    setInputMessage(suggestion);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const formatTime = (timestamp) => {
    return timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  const getMessageIcon = (type, isError = false) => {
    if (isError) {
      return <AlertTriangle className="h-5 w-5 text-red-600" />;
    }
    
    switch (type) {
      case 'user':
        return <User className="h-5 w-5 text-blue-600" />;
      case 'assistant':
        return <Bot className="h-5 w-5 text-green-600" />;
      default:
        return <MessageSquare className="h-5 w-5 text-gray-600" />;
    }
  };

  const getMessageBubbleClass = (type, isError = false) => {
    if (type === 'user') {
      return 'bg-blue-600 text-white';
    }
    
    if (isError) {
      return 'bg-red-50 border border-red-200 text-red-800';
    }
    
    return 'bg-gray-100 text-gray-900';
  };

  return (
    <div className="bg-white rounded-lg shadow-sm border h-[600px] flex flex-col">
      {/* Chat Header */}
      <div className="flex items-center justify-between p-4 border-b bg-gray-50 rounded-t-lg">
        <div className="flex items-center space-x-3">
          <Bot className="h-6 w-6 text-blue-600" />
          <div>
            <h3 className="font-semibold text-gray-900">AI Prior Authorization Assistant</h3>
            <p className="text-sm text-gray-500">Powered by Agentic Core</p>
          </div>
        </div>
        <div className="flex items-center space-x-2">
          <div className="w-2 h-2 bg-green-500 rounded-full"></div>
          <span className="text-sm text-gray-500">Online</span>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((message) => (
          <div key={message.id} className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`flex items-start space-x-2 max-w-xs lg:max-w-md ${message.type === 'user' ? 'flex-row-reverse space-x-reverse' : ''}`}>
              <div className="flex-shrink-0">
                {getMessageIcon(message.type, message.isError)}
              </div>
              <div className={`rounded-lg px-4 py-2 ${getMessageBubbleClass(message.type, message.isError)}`}>
                <p className="text-sm whitespace-pre-wrap">{message.content}</p>
                <div className={`flex items-center space-x-1 mt-1 text-xs ${message.type === 'user' ? 'text-blue-100' : 'text-gray-500'}`}>
                  <Clock className="h-3 w-3" />
                  <span>{formatTime(message.timestamp)}</span>
                </div>
              </div>
            </div>
          </div>
        ))}
        
        {isLoading && (
          <div className="flex justify-start">
            <div className="flex items-start space-x-2 max-w-xs lg:max-w-md">
              <Bot className="h-5 w-5 text-green-600 flex-shrink-0" />
              <div className="bg-gray-100 rounded-lg px-4 py-2">
                <div className="flex space-x-1">
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Suggestions */}
        {messages.length > 0 && !isLoading && messages[messages.length - 1].type === 'assistant' && messages[messages.length - 1].suggestions && (
          <div className="flex justify-start">
            <div className="flex flex-wrap gap-2 max-w-xs lg:max-w-md">
              {messages[messages.length - 1].suggestions.map((suggestion, index) => (
                <button
                  key={index}
                  onClick={() => handleSuggestionClick(suggestion)}
                  className="bg-blue-50 hover:bg-blue-100 text-blue-700 text-xs px-3 py-1 rounded-full border border-blue-200 transition-colors"
                >
                  {suggestion}
                </button>
              ))}
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="border-t p-4 bg-gray-50 rounded-b-lg">
        <div className="flex space-x-2">
          <div className="flex-1">
            <textarea
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask me about prior authorization requests, status checks, EDI generation, patient lookup, or healthcare codes..."
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
              rows="2"
              disabled={isLoading}
            />
          </div>
          <button
            onClick={handleSendMessage}
            disabled={!inputMessage.trim() || isLoading}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            <Send className="h-4 w-4" />
          </button>
        </div>
        
        {/* Quick Actions */}
        <div className="mt-3 flex flex-wrap gap-2">
          <button
            onClick={() => handleSuggestionClick("Create a prior authorization request for patient PAT123456")}
            className="flex items-center space-x-1 bg-green-50 hover:bg-green-100 text-green-700 text-xs px-2 py-1 rounded border border-green-200 transition-colors"
          >
            <Shield className="h-3 w-3" />
            <span>Create Auth</span>
          </button>
          <button
            onClick={() => handleSuggestionClick("Check the status of authorization request AUTH123456")}
            className="flex items-center space-x-1 bg-purple-50 hover:bg-purple-100 text-purple-700 text-xs px-2 py-1 rounded border border-purple-200 transition-colors"
          >
            <CheckCircle2 className="h-3 w-3" />
            <span>Check Status</span>
          </button>
          <button
            onClick={() => handleSuggestionClick("Generate an EDI 278 document for authorization request")}
            className="flex items-center space-x-1 bg-orange-50 hover:bg-orange-100 text-orange-700 text-xs px-2 py-1 rounded border border-orange-200 transition-colors"
          >
            <FileText className="h-3 w-3" />
            <span>Generate EDI</span>
          </button>
          <button
            onClick={() => handleSuggestionClick("Look up patient information for PAT123456")}
            className="flex items-center space-x-1 bg-blue-50 hover:bg-blue-100 text-blue-700 text-xs px-2 py-1 rounded border border-blue-200 transition-colors"
          >
            <User className="h-3 w-3" />
            <span>Lookup Patient</span>
          </button>
        </div>
      </div>
    </div>
  );
};

export default AgentChat; 
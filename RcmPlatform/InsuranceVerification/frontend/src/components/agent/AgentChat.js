import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, Clock, CheckCircle, AlertCircle, Shield, FileText, CheckCircle2, AlertTriangle } from 'lucide-react';

const AgentChat = () => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'assistant',
      content: "Hello! I'm your AI Insurance Assistant. I can help you with insurance verification, eligibility checks, document analysis, and EDI processing. What would you like to do today?",
      timestamp: new Date(),
      suggestions: [
        "Verify insurance coverage",
        "Check patient eligibility",
        "Extract insurance info from documents",
        "Analyze EDI transactions"
      ]
    }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

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
      const response = await fetch('/api/v1/agent/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: inputMessage,
          user_id: 'user-123', // In real app, get from auth context
          context: {}
        })
      });

      const data = await response.json();
      
      const assistantMessage = {
        id: Date.now() + 1,
        type: 'assistant',
        content: data.response,
        timestamp: new Date(),
        suggestions: generateSuggestions(inputMessage.toLowerCase())
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
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
    if (message.includes('verify') || message.includes('coverage')) {
      return [
        "Check eligibility for specific services",
        "Verify multiple service types",
        "Get coverage details"
      ];
    } else if (message.includes('eligibility') || message.includes('check')) {
      return [
        "Verify insurance coverage",
        "Check multiple service types",
        "Get benefit details"
      ];
    } else if (message.includes('extract') || message.includes('document')) {
      return [
        "Upload insurance card",
        "Process multiple documents",
        "Extract member information"
      ];
    } else if (message.includes('edi') || message.includes('transaction')) {
      return [
        "Analyze 270 transaction",
        "Validate EDI format",
        "Process 271 response"
      ];
    }
    
    return [
      "Verify insurance coverage",
      "Check patient eligibility",
      "Extract insurance info from documents",
      "Analyze EDI transactions"
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
    if (type === 'user') {
      return <User className="h-5 w-5 text-blue-600" />;
    }
    
    if (isError) {
      return <AlertTriangle className="h-5 w-5 text-red-600" />;
    }
    
    return <Bot className="h-5 w-5 text-green-600" />;
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
            <h3 className="font-semibold text-gray-900">AI Insurance Assistant</h3>
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
                <p className="text-sm">{message.content}</p>
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
              placeholder="Ask me about insurance verification, eligibility checks, document analysis, or EDI processing..."
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
            onClick={() => handleSuggestionClick("Verify insurance coverage for member 123456789")}
            className="flex items-center space-x-1 bg-green-50 hover:bg-green-100 text-green-700 text-xs px-2 py-1 rounded border border-green-200 transition-colors"
          >
            <Shield className="h-3 w-3" />
            <span>Verify Coverage</span>
          </button>
          <button
            onClick={() => handleSuggestionClick("Check eligibility for service type 30")}
            className="flex items-center space-x-1 bg-purple-50 hover:bg-purple-100 text-purple-700 text-xs px-2 py-1 rounded border border-purple-200 transition-colors"
          >
            <CheckCircle2 className="h-3 w-3" />
            <span>Check Eligibility</span>
          </button>
          <button
            onClick={() => handleSuggestionClick("Extract insurance information from uploaded document")}
            className="flex items-center space-x-1 bg-orange-50 hover:bg-orange-100 text-orange-700 text-xs px-2 py-1 rounded border border-orange-200 transition-colors"
          >
            <FileText className="h-3 w-3" />
            <span>Extract Info</span>
          </button>
        </div>
      </div>
    </div>
  );
};

export default AgentChat; 
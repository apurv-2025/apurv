import React, { useState, useRef, useEffect } from 'react';
import { 
  Send, 
  Bot, 
  User, 
  Loader2, 
  Sparkles, 
  Copy, 
  Check, 
  RefreshCw,
  MessageSquare,
  BarChart3,
  FileText,
  AlertCircle,
  ChevronDown,
  ChevronUp,
  MoreHorizontal,
  ThumbsUp,
  ThumbsDown,
  Settings,
  Trash2,
  Download,
  Upload,
  History,
  Plus,
  Search,
  Filter,
  BookOpen,
  Zap,
  Shield,
  Globe,
  X,
  CheckCircle
} from 'lucide-react';

const AgentChat = () => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'agent',
      content: "Hello! I'm your AI assistant for charge capture. I can help you capture charges, validate codes, find templates, and analyze patterns. What would you like to do today?",
      timestamp: new Date(),
      status: 'sent',
      isTyping: false,
      model: 'Apurv RCM 1.0'
    }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [userId] = useState('user_' + Math.random().toString(36).substr(2, 9));
  const [copiedMessageId, setCopiedMessageId] = useState(null);
  const [expandedMessages, setExpandedMessages] = useState(new Set());
  const [messageFeedback, setMessageFeedback] = useState({});
  const [showSidebar, setShowSidebar] = useState(false);
  const [selectedModel, setSelectedModel] = useState('Apurv RCM 1.0');
  const [conversationHistory, setConversationHistory] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [showSettings, setShowSettings] = useState(false);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
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
      timestamp: new Date(),
      status: 'sent'
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    // Add typing indicator
    const typingMessage = {
      id: Date.now() + 1,
      type: 'agent',
      content: '',
      timestamp: new Date(),
      status: 'typing',
      isTyping: true
    };

    setMessages(prev => [...prev, typingMessage]);

    try {
      const response = await fetch('/api/v1/agent/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: inputMessage,
          conversation_id: null
        }),
      });

      const data = await response.json();

      // Remove typing indicator and add actual response
      setMessages(prev => prev.filter(msg => !msg.isTyping));

      const agentMessage = {
        id: Date.now() + 2,
        type: 'agent',
        content: data.response || 'I apologize, but I couldn\'t process your request. Please try again.',
        timestamp: new Date(),
        status: 'sent',
        taskId: data.conversation_id,
        metadata: {
          model: 'Apurv RCM 1.0',
          processingTime: '2.3s',
          toolsUsed: data.tools_used || []
        }
      };

      setMessages(prev => [...prev, agentMessage]);
    } catch (error) {
      console.error('Error sending message:', error);

      // Remove typing indicator
      setMessages(prev => prev.filter(msg => !msg.isTyping));

      const errorMessage = {
        id: Date.now() + 2,
        type: 'agent',
        content: 'I\'m sorry, I encountered an error while processing your request. Please try again.',
        timestamp: new Date(),
        status: 'error'
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const copyMessage = async (messageId, content) => {
    try {
      await navigator.clipboard.writeText(content);
      setCopiedMessageId(messageId);
      setTimeout(() => setCopiedMessageId(null), 2000);
    } catch (error) {
      console.error('Failed to copy message:', error);
    }
  };

  const toggleMessageExpansion = (messageId) => {
    setExpandedMessages(prev => {
      const newSet = new Set(prev);
      if (newSet.has(messageId)) {
        newSet.delete(messageId);
      } else {
        newSet.add(messageId);
      }
      return newSet;
    });
  };

  const handleMessageFeedback = (messageId, feedback) => {
    setMessageFeedback(prev => ({
      ...prev,
      [messageId]: feedback
    }));
  };

  const retryMessage = (messageId) => {
    const message = messages.find(m => m.id === messageId);
    if (message && message.type === 'user') {
      setInputMessage(message.content);
      setMessages(prev => prev.filter(m => m.id !== messageId));
    }
  };

  const clearConversation = () => {
    setMessages([
      {
        id: Date.now(),
        type: 'agent',
        content: "Hello! I'm your AI assistant for charge capture. I can help you capture charges, validate codes, find templates, and analyze patterns. What would you like to do today?",
        timestamp: new Date(),
        status: 'sent',
        isTyping: false,
        model: 'Apurv RCM 1.0'
      }
    ]);
  };

  const quickActions = [
    {
      label: 'Capture Charge',
      description: 'Create a new charge with AI assistance',
      action: () => setInputMessage("Help me capture a new charge"),
      icon: Plus,
      color: 'text-blue-600'
    },
    {
      label: 'Validate Codes',
      description: 'Check CPT/ICD combinations',
      action: () => setInputMessage("Validate this CPT code: 99213 with ICD Z00.00"),
      icon: CheckCircle,
      color: 'text-green-600'
    },
    {
      label: 'Get Templates',
      description: 'Find charge templates by specialty',
      action: () => setInputMessage("Show me templates for cardiology"),
      icon: FileText,
      color: 'text-purple-600'
    },
    {
      label: 'Analyze Charges',
      description: 'Get insights and recommendations',
      action: () => setInputMessage("Analyze my charges for the last 30 days"),
      icon: BarChart3,
      color: 'text-orange-600'
    }
  ];

  const renderMessage = (message) => {
    const isExpanded = expandedMessages.has(message.id);
    const isCopied = copiedMessageId === message.id;
    const feedback = messageFeedback[message.id];

    return (
      <div
        key={message.id}
        className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'} mb-6`}
      >
        <div className={`max-w-3xl ${message.type === 'user' ? 'order-2' : 'order-1'}`}>
          <div
            className={`px-4 py-3 rounded-2xl border ${
              message.type === 'user'
                ? 'bg-blue-600 text-white border-blue-600'
                : message.status === 'error'
                ? 'bg-red-50 text-red-800 border-red-200'
                : 'bg-gray-50 text-gray-900 border-gray-200'
            }`}
          >
            <div className="flex items-start space-x-3">
              {message.type === 'agent' && (
                <div className="flex-shrink-0">
                  <Bot className={`w-5 h-5 mt-0.5 ${
                    message.status === 'error' ? 'text-red-600' : 'text-blue-600'
                  }`} />
                </div>
              )}
              {message.type === 'user' && (
                <div className="flex-shrink-0">
                  <User className="w-5 h-5 mt-0.5 text-white" />
                </div>
              )}
              <div className="flex-1 min-w-0">
                <div className="whitespace-pre-wrap text-sm leading-relaxed">
                  {message.content}
                </div>
                
                {/* Message Metadata */}
                {message.metadata && (
                  <div className="mt-2 pt-2 border-t border-gray-200">
                    <div className="flex items-center justify-between text-xs text-gray-500">
                      <div className="flex items-center space-x-2">
                        <span>{message.metadata.model}</span>
                        {message.metadata.processingTime && (
                          <>
                            <span>•</span>
                            <span>{message.metadata.processingTime}</span>
                          </>
                        )}
                      </div>
                      {message.metadata.toolsUsed && message.metadata.toolsUsed.length > 0 && (
                        <div className="flex items-center space-x-1">
                          <span>Tools:</span>
                          {message.metadata.toolsUsed.map((tool, index) => (
                            <span key={index} className="bg-blue-100 text-blue-700 px-1.5 py-0.5 rounded text-xs">
                              {tool}
                            </span>
                          ))}
                        </div>
                      )}
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Message Actions */}
          <div className={`flex items-center space-x-2 mt-2 ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}>
            {message.type === 'agent' && (
              <>
                <button
                  onClick={() => copyMessage(message.id, message.content)}
                  className="p-1 text-gray-400 hover:text-gray-600 rounded"
                  title="Copy message"
                >
                  {isCopied ? <Check className="w-4 h-4" /> : <Copy className="w-4 h-4" />}
                </button>
                
                <button
                  onClick={() => handleMessageFeedback(message.id, 'positive')}
                  className={`p-1 rounded ${
                    feedback === 'positive' 
                      ? 'text-green-600 bg-green-50' 
                      : 'text-gray-400 hover:text-green-600'
                  }`}
                  title="Good response"
                >
                  <ThumbsUp className="w-4 h-4" />
                </button>
                
                <button
                  onClick={() => handleMessageFeedback(message.id, 'negative')}
                  className={`p-1 rounded ${
                    feedback === 'negative' 
                      ? 'text-red-600 bg-red-50' 
                      : 'text-gray-400 hover:text-red-600'
                  }`}
                  title="Bad response"
                >
                  <ThumbsDown className="w-4 h-4" />
                </button>
              </>
            )}

            {message.status === 'error' && (
              <button
                onClick={() => retryMessage(message.id)}
                className="p-1 text-red-400 hover:text-red-600 rounded"
                title="Retry"
              >
                <RefreshCw className="w-4 h-4" />
              </button>
            )}
          </div>

          {/* Timestamp */}
          <div className={`text-xs text-gray-500 mt-1 ${
            message.type === 'user' ? 'text-right' : 'text-left'
          }`}>
            {message.timestamp.toLocaleTimeString([], {
              hour: '2-digit',
              minute: '2-digit'
            })}
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="flex flex-col h-full bg-white rounded-lg shadow-sm border">
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b bg-gradient-to-r from-blue-50 to-indigo-50">
        <div className="flex items-center space-x-3">
          <div className="p-2 bg-blue-100 rounded-lg">
            <Bot className="w-5 h-5 text-blue-600" />
          </div>
          <div>
            <h3 className="font-semibold text-gray-900">AI Charge Capture Assistant</h3>
            <p className="text-sm text-gray-600">Powered by Apurv RCM 1.0</p>
          </div>
        </div>
        <div className="flex items-center space-x-2">
          <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
          <span className="text-sm text-gray-600">Online</span>
          <button
            onClick={clearConversation}
            className="p-2 text-gray-400 hover:text-gray-600 rounded-lg hover:bg-gray-100"
            title="Clear conversation"
          >
            <Trash2 className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-6">
        {messages.length === 1 && (
          <div className="text-center py-8">
            <div className="max-w-2xl mx-auto">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {quickActions.map((action, index) => {
                  const Icon = action.icon;
                  return (
                    <button
                      key={index}
                      onClick={action.action}
                      className="p-4 text-left bg-white border border-gray-200 rounded-lg hover:bg-gray-50 hover:border-gray-300 transition-colors"
                    >
                      <div className="flex items-center space-x-3">
                        <Icon className={`w-5 h-5 ${action.color}`} />
                        <div>
                          <div className="font-medium text-gray-900">{action.label}</div>
                          <div className="text-sm text-gray-500">{action.description}</div>
                        </div>
                      </div>
                    </button>
                  );
                })}
              </div>
            </div>
          </div>
        )}

        {messages.map(renderMessage)}

        {isLoading && !messages.some(msg => msg.isTyping) && (
          <div className="flex justify-start">
            <div className="bg-gray-50 text-gray-900 max-w-2xl px-4 py-3 rounded-2xl border border-gray-200">
              <div className="flex items-center space-x-3">
                <Bot className="w-5 h-5 text-blue-600" />
                <div className="flex items-center space-x-2">
                  <Loader2 className="w-4 h-4 animate-spin text-blue-600" />
                  <span className="text-sm">Processing your request...</span>
                </div>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="p-4 border-t bg-gray-50">
        <div className="flex space-x-3">
          <div className="flex-1 relative">
            <textarea
              ref={inputRef}
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask me about charge capture, validation, templates, or analysis..."
              className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none text-sm"
              rows="1"
              disabled={isLoading}
              style={{ minHeight: '44px', maxHeight: '120px' }}
            />
          </div>
          <button
            onClick={handleSendMessage}
            disabled={!inputMessage.trim() || isLoading}
            className="px-4 py-3 bg-blue-600 text-white rounded-xl hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {isLoading ? (
              <Loader2 className="w-5 h-5 animate-spin" />
            ) : (
              <Send className="w-5 h-5" />
            )}
          </button>
        </div>
        <div className="mt-2 flex items-center justify-between">
          <p className="text-xs text-gray-500">
            Press Enter to send, Shift+Enter for new line
          </p>
          <div className="flex items-center space-x-1">
            <Sparkles className="w-3 h-3 text-blue-600" />
            <span className="text-xs text-gray-500">AI Powered</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AgentChat; 
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
  ThumbsDown
} from 'lucide-react';
import { agentService } from '../../services/agentService';

const AgentChat = () => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'agent',
      content: 'Hello! I\'m your AI assistant for claims processing. I can help you analyze claims, process rejections, generate reports, and answer questions about your claims data. How can I help you today?',
      timestamp: new Date(),
      status: 'sent',
      isTyping: false
    }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [userId] = useState('user_' + Math.random().toString(36).substr(2, 9));
  const [copiedMessageId, setCopiedMessageId] = useState(null);
  const [expandedMessages, setExpandedMessages] = useState(new Set());
  const [messageFeedback, setMessageFeedback] = useState({});
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
      const response = await agentService.chat(inputMessage, userId);

      // Remove typing indicator and add actual response
      setMessages(prev => prev.filter(msg => !msg.isTyping));

      const agentMessage = {
        id: Date.now() + 2,
        type: 'agent',
        content: response.response || 'I apologize, but I couldn\'t process your request. Please try again.',
        timestamp: new Date(),
        status: 'sent',
        taskId: response.task_id,
        metadata: {
          model: 'Claude Sonnet 4',
          processingTime: response.processing_time || '2.3s'
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

  const handleFeedback = (messageId, feedback) => {
    setMessageFeedback(prev => ({
      ...prev,
      [messageId]: feedback
    }));
    // Here you would typically send feedback to the backend
    console.log(`Feedback for message ${messageId}: ${feedback}`);
  };

  const retryMessage = async (messageId) => {
    const message = messages.find(msg => msg.id === messageId);
    if (message && message.type === 'user') {
      setInputMessage(message.content);
      inputRef.current?.focus();
    }
  };

  const quickActions = [
    {
      label: 'Analyze Claims',
      action: 'Can you analyze my recent claims for any issues?',
      icon: BarChart3,
      description: 'Check for validation issues'
    },
    {
      label: 'Generate Report',
      action: 'Generate a financial summary report for this month',
      icon: FileText,
      description: 'Create financial summary'
    },
    {
      label: 'Check Rejections',
      action: 'Show me claims that were rejected recently',
      icon: AlertCircle,
      description: 'Review rejected claims'
    },
    {
      label: 'Help',
      action: 'What can you help me with?',
      icon: MessageSquare,
      description: 'Learn about capabilities'
    }
  ];

  const handleQuickAction = (action) => {
    setInputMessage(action);
    inputRef.current?.focus();
  };

  const formatMessage = (content) => {
    // Handle line breaks, code blocks, and basic formatting
    const lines = content.split('\n');
    return lines.map((line, index) => {
      // Check if line looks like code (contains special characters or is indented)
      const isCode = line.trim().startsWith('•') ||
                    line.trim().startsWith('-') ||
                    line.includes('```') ||
                    line.match(/^\s*[A-Z][a-z]+:/);

      return (
        <React.Fragment key={index}>
          <span className={isCode ? 'font-mono text-sm bg-gray-100 px-1 rounded' : ''}>
            {line}
          </span>
          {index < lines.length - 1 && <br />}
        </React.Fragment>
      );
    });
  };

  const renderMessage = (message) => {
    const isExpanded = expandedMessages.has(message.id);
    const feedback = messageFeedback[message.id];

    return (
      <div
        key={message.id}
        className={`group relative ${
          message.type === 'user' ? 'flex justify-end' : 'flex justify-start'
        }`}
      >
        <div
          className={`max-w-2xl px-4 py-3 rounded-2xl ${
            message.type === 'user'
              ? 'bg-blue-600 text-white'
              : message.status === 'error'
              ? 'bg-red-50 text-red-800 border border-red-200'
              : 'bg-gray-50 text-gray-900 border border-gray-200'
          } ${message.isTyping ? 'animate-pulse' : ''}`}
        >
          <div className="flex items-start space-x-3">
            {message.type === 'agent' && !message.isTyping && (
              <div className="flex-shrink-0 mt-1">
                <Bot className="w-5 h-5 text-blue-600" />
              </div>
            )}

            <div className="flex-1 min-w-0">
              {message.isTyping ? (
                <div className="flex items-center space-x-2">
                  <div className="flex space-x-1">
                    <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                    <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                  </div>
                  <span className="text-sm text-gray-600">AI is typing...</span>
                </div>
              ) : (
                <>
                  <div className="text-sm leading-relaxed">
                    {formatMessage(message.content)}
                  </div>

                  {message.metadata && (
                    <div className="mt-2 text-xs text-gray-500 flex items-center space-x-2">
                      <span>{message.metadata.model}</span>
                      <span>•</span>
                      <span>{message.metadata.processingTime}</span>
                    </div>
                  )}
                </>
              )}
            </div>

            {message.type === 'user' && (
              <div className="flex-shrink-0 mt-1">
                <User className="w-5 h-5 text-blue-100" />
              </div>
            )}
          </div>

          {/* Message Actions */}
          {!message.isTyping && (
            <div className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity">
              <div className="flex items-center space-x-1">
                {message.type === 'agent' && (
                  <>
                    <button
                      onClick={() => copyMessage(message.id, message.content)}
                      className="p-1 text-gray-400 hover:text-gray-600 rounded"
                      title="Copy message"
                    >
                      {copiedMessageId === message.id ? (
                        <Check className="w-4 h-4 text-green-600" />
                      ) : (
                        <Copy className="w-4 h-4" />
                      )}
                    </button>

                    <button
                      onClick={() => handleFeedback(message.id, 'thumbs_up')}
                      className={`p-1 rounded ${
                        feedback === 'thumbs_up'
                          ? 'text-green-600'
                          : 'text-gray-400 hover:text-gray-600'
                      }`}
                      title="Helpful"
                    >
                      <ThumbsUp className="w-4 h-4" />
                    </button>

                    <button
                      onClick={() => handleFeedback(message.id, 'thumbs_down')}
                      className={`p-1 rounded ${
                        feedback === 'thumbs_down'
                          ? 'text-red-600'
                          : 'text-gray-400 hover:text-gray-600'
                      }`}
                      title="Not helpful"
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
            </div>
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
            <h3 className="font-semibold text-gray-900">AI Claims Assistant</h3>
            <p className="text-sm text-gray-600">Powered by Apurv RCM 1.0</p>
          </div>
        </div>
        <div className="flex items-center space-x-2">
          <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
          <span className="text-sm text-gray-600">Online</span>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-6">
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

      {/* Quick Actions */}
      {messages.length === 1 && (
        <div className="px-4 py-3 border-t bg-gray-50">
          <p className="text-sm text-gray-600 mb-3">Quick actions:</p>
          <div className="grid grid-cols-2 gap-2">
            {quickActions.map((action, index) => {
              const Icon = action.icon;
              return (
                <button
                  key={index}
                  onClick={() => handleQuickAction(action.action)}
                  className="flex items-center space-x-2 p-3 text-left bg-white border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 hover:border-gray-400 transition-colors"
                >
                  <Icon className="w-4 h-4 text-blue-600" />
                  <div>
                    <div className="font-medium text-sm">{action.label}</div>
                    <div className="text-xs text-gray-500">{action.description}</div>
                  </div>
                </button>
              );
            })}
          </div>
        </div>
      )}

      {/* Input */}
      <div className="p-4 border-t bg-gray-50">
        <div className="flex space-x-3">
          <div className="flex-1 relative">
            <textarea
              ref={inputRef}
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask me about claims, rejections, reports, or anything else..."
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
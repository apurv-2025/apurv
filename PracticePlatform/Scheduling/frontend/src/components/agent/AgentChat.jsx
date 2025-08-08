// =============================================================================
// FILE: frontend/src/components/agent/AgentChat.jsx
// =============================================================================
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
  Calendar,
  Clock,
  Users,
  Activity
} from 'lucide-react';
import { toast } from 'react-toastify';
import { agentService } from '../../services/agentService';

const AgentChat = () => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'agent',
      content: 'Hello! I\'m your AI assistant for scheduling. I can help you schedule appointments, find availability, analyze schedules, generate reports, and answer questions about your scheduling system. How can I help you today?',
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
        content: response.message || 'I apologize, but I couldn\'t process your request. Please try again.',
        timestamp: new Date(),
        status: 'sent',
        taskId: response.task_id,
        metadata: {
          model: 'Scheduling Agent',
          processingTime: response.processing_time || '2.3s',
          confidenceScore: response.confidence_score || 0.8,
          suggestions: response.suggestions || [],
          nextActions: response.next_actions || []
        },
        result: response.result
      };

      setMessages(prev => [...prev, agentMessage]);
    } catch (error) {
      console.error('Error sending message:', error);

      // Remove typing indicator
      setMessages(prev => prev.filter(msg => !msg.isTyping));

      // Add error message
      const errorMessage = {
        id: Date.now() + 2,
        type: 'agent',
        content: 'I apologize, but I encountered an error while processing your request. Please try again.',
        timestamp: new Date(),
        status: 'error',
        error: error.message
      };

      setMessages(prev => [...prev, errorMessage]);
      toast.error('Failed to send message. Please try again.');
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
      toast.success('Message copied to clipboard');
    } catch (error) {
      toast.error('Failed to copy message');
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
    toast.success(`Feedback submitted: ${feedback}`);
  };

  const retryMessage = async (messageId) => {
    const message = messages.find(msg => msg.id === messageId);
    if (!message || message.type !== 'user') return;

    // Remove the error message and retry
    setMessages(prev => prev.filter(msg => msg.id !== messageId + 1));
    setInputMessage(message.content);
    setIsLoading(true);

    try {
      const response = await agentService.chat(message.content, userId);

      const agentMessage = {
        id: Date.now(),
        type: 'agent',
        content: response.message || 'I apologize, but I couldn\'t process your request. Please try again.',
        timestamp: new Date(),
        status: 'sent',
        taskId: response.task_id,
        metadata: {
          model: 'Scheduling Agent',
          processingTime: response.processing_time || '2.3s',
          confidenceScore: response.confidence_score || 0.8,
          suggestions: response.suggestions || [],
          nextActions: response.next_actions || []
        },
        result: response.result
      };

      setMessages(prev => [...prev, agentMessage]);
    } catch (error) {
      console.error('Error retrying message:', error);
      toast.error('Failed to retry message');
    } finally {
      setIsLoading(false);
    }
  };

  const handleQuickAction = (action) => {
    const actionMessages = {
      'schedule': 'I can help you schedule an appointment. Please provide the patient name, practitioner name, preferred date and time.',
      'availability': 'I can help you find available time slots. Please specify the practitioner and date.',
      'analyze': 'I can analyze your schedule patterns and provide insights. Would you like me to analyze the last 7 days?',
      'report': 'I can generate various reports. What type of report would you like (daily, weekly, monthly)?',
      'optimize': 'I can help optimize your schedule. What type of optimization are you looking for?'
    };

    setInputMessage(actionMessages[action] || action);
  };

  const formatMessage = (content) => {
    // Simple formatting for better readability
    return content
      .split('\n')
      .map((line, index) => (
        <span key={index}>
          {line}
          {index < content.split('\n').length - 1 && <br />}
        </span>
      ));
  };

  const renderMessage = (message) => {
    const isExpanded = expandedMessages.has(message.id);
    const hasFeedback = messageFeedback[message.id];

    return (
      <div
        key={message.id}
        className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'} mb-4`}
      >
        <div
          className={`max-w-[80%] rounded-lg p-4 ${
            message.type === 'user'
              ? 'bg-blue-600 text-white'
              : message.status === 'error'
              ? 'bg-red-100 text-red-800 border border-red-200'
              : 'bg-gray-100 text-gray-800'
          }`}
        >
          {/* Message Header */}
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center space-x-2">
              {message.type === 'user' ? (
                <User className="h-4 w-4" />
              ) : (
                <Bot className="h-4 w-4" />
              )}
              <span className="text-sm font-medium">
                {message.type === 'user' ? 'You' : 'Scheduling Assistant'}
              </span>
              {message.metadata && (
                <span className="text-xs opacity-75">
                  {message.metadata.processingTime}
                </span>
              )}
            </div>
            <div className="flex items-center space-x-1">
              {message.type === 'agent' && message.status === 'error' && (
                <button
                  onClick={() => retryMessage(message.id - 1)}
                  className="p-1 hover:bg-gray-200 rounded"
                  title="Retry"
                >
                  <RefreshCw className="h-3 w-3" />
                </button>
              )}
              <button
                onClick={() => copyMessage(message.id, message.content)}
                className="p-1 hover:bg-gray-200 rounded"
                title="Copy message"
              >
                {copiedMessageId === message.id ? (
                  <Check className="h-3 w-3" />
                ) : (
                  <Copy className="h-3 w-3" />
                )}
              </button>
              {message.metadata && (message.metadata.suggestions?.length > 0 || message.metadata.nextActions?.length > 0) && (
                <button
                  onClick={() => toggleMessageExpansion(message.id)}
                  className="p-1 hover:bg-gray-200 rounded"
                  title={isExpanded ? 'Collapse' : 'Expand'}
                >
                  {isExpanded ? (
                    <ChevronUp className="h-3 w-3" />
                  ) : (
                    <ChevronDown className="h-3 w-3" />
                  )}
                </button>
              )}
            </div>
          </div>

          {/* Message Content */}
          <div className="text-sm">
            {message.isTyping ? (
              <div className="flex items-center space-x-2">
                <Loader2 className="h-4 w-4 animate-spin" />
                <span>Thinking...</span>
              </div>
            ) : (
              formatMessage(message.content)
            )}
          </div>

          {/* Expanded Content */}
          {isExpanded && message.metadata && (
            <div className="mt-3 pt-3 border-t border-gray-200">
              {/* Suggestions */}
              {message.metadata.suggestions?.length > 0 && (
                <div className="mb-3">
                  <h4 className="text-xs font-semibold text-gray-600 mb-1">Suggestions:</h4>
                  <ul className="text-xs space-y-1">
                    {message.metadata.suggestions.map((suggestion, index) => (
                      <li key={index} className="flex items-center space-x-1">
                        <Sparkles className="h-3 w-3 text-yellow-500" />
                        <span>{suggestion}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Next Actions */}
              {message.metadata.nextActions?.length > 0 && (
                <div className="mb-3">
                  <h4 className="text-xs font-semibold text-gray-600 mb-1">Next Actions:</h4>
                  <ul className="text-xs space-y-1">
                    {message.metadata.nextActions.map((action, index) => (
                      <li key={index} className="flex items-center space-x-1">
                        <Activity className="h-3 w-3 text-blue-500" />
                        <span>{action}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Confidence Score */}
              {message.metadata.confidenceScore && (
                <div className="text-xs text-gray-500">
                  Confidence: {(message.metadata.confidenceScore * 100).toFixed(1)}%
                </div>
              )}
            </div>
          )}

          {/* Message Footer */}
          <div className="flex items-center justify-between mt-2 pt-2 border-t border-gray-200">
            <span className="text-xs opacity-75">
              {message.timestamp.toLocaleTimeString()}
            </span>
            {message.type === 'agent' && !hasFeedback && (
              <div className="flex items-center space-x-1">
                <button
                  onClick={() => handleFeedback(message.id, 'helpful')}
                  className="p-1 hover:bg-gray-200 rounded"
                  title="Helpful"
                >
                  <ThumbsUp className="h-3 w-3" />
                </button>
                <button
                  onClick={() => handleFeedback(message.id, 'not_helpful')}
                  className="p-1 hover:bg-gray-200 rounded"
                  title="Not helpful"
                >
                  <ThumbsDown className="h-3 w-3" />
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="flex flex-col h-full bg-white rounded-lg shadow-lg">
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-gray-200">
        <div className="flex items-center space-x-3">
          <div className="p-2 bg-blue-100 rounded-lg">
            <Bot className="h-6 w-6 text-blue-600" />
          </div>
          <div>
            <h2 className="text-lg font-semibold text-gray-900">Scheduling Assistant</h2>
            <p className="text-sm text-gray-600">AI-powered scheduling help</p>
          </div>
        </div>
        <div className="flex items-center space-x-2">
          <button
            onClick={() => window.location.reload()}
            className="p-2 hover:bg-gray-100 rounded-lg"
            title="Refresh"
          >
            <RefreshCw className="h-4 w-4" />
          </button>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="p-4 border-b border-gray-200">
        <div className="flex flex-wrap gap-2">
          {[
            { icon: Calendar, label: 'Schedule', action: 'schedule' },
            { icon: Clock, label: 'Availability', action: 'availability' },
            { icon: BarChart3, label: 'Analyze', action: 'analyze' },
            { icon: FileText, label: 'Report', action: 'report' },
            { icon: Activity, label: 'Optimize', action: 'optimize' }
          ].map(({ icon: Icon, label, action }) => (
            <button
              key={action}
              onClick={() => handleQuickAction(action)}
              className="flex items-center space-x-2 px-3 py-2 bg-gray-100 hover:bg-gray-200 rounded-lg text-sm transition-colors"
            >
              <Icon className="h-4 w-4" />
              <span>{label}</span>
            </button>
          ))}
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map(renderMessage)}
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="p-4 border-t border-gray-200">
        <div className="flex space-x-2">
          <div className="flex-1 relative">
            <textarea
              ref={inputRef}
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask me about scheduling, appointments, availability, reports..."
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
              rows="2"
              disabled={isLoading}
            />
          </div>
          <button
            onClick={handleSendMessage}
            disabled={!inputMessage.trim() || isLoading}
            className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {isLoading ? (
              <Loader2 className="h-5 w-5 animate-spin" />
            ) : (
              <Send className="h-5 w-5" />
            )}
          </button>
        </div>
        <div className="mt-2 text-xs text-gray-500">
          Press Enter to send, Shift+Enter for new line
        </div>
      </div>
    </div>
  );
};

export default AgentChat; 
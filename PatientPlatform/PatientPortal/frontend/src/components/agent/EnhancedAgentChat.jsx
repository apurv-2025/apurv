import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, Clock, CheckCircle, AlertCircle, Sparkles, Calendar, Pill, FileText, User as UserIcon, Bell, Heart, Zap, Settings, MessageSquare } from 'lucide-react';
import SurveyModal from '../SurveyModal';

const EnhancedAgentChat = () => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      role: 'assistant',
      content: 'Hello! I\'m your enhanced AI health assistant. I can help you with appointments, medications, lab results, health summaries, and more. What would you like to do today?',
      timestamp: new Date(),
      status: 'sent',
      type: 'text',
      suggestions: [
        'Schedule an appointment',
        'Check my medications',
        'View lab results',
        'Generate health summary'
      ]
    }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [selectedTool, setSelectedTool] = useState(null);
  const [showToolPanel, setShowToolPanel] = useState(false);
  const [showSurveyModal, setShowSurveyModal] = useState(false);
  const [conversationId, setConversationId] = useState(null);
  const [messageCount, setMessageCount] = useState(1);
  const messagesEndRef = useRef(null);

  const tools = [
    {
      id: 'schedule_appointment',
      name: 'Schedule Appointment',
      description: 'Book appointments with doctors',
      icon: Calendar,
      color: 'blue',
      examples: ['Schedule annual physical', 'Book specialist consultation', 'Find urgent care']
    },
    {
      id: 'check_medications',
      name: 'Medication Check',
      description: 'Review medications and refills',
      icon: Pill,
      color: 'purple',
      examples: ['Check refill status', 'Review medication list', 'Set up reminders']
    },
    {
      id: 'lab_results',
      name: 'Lab Results',
      description: 'Analyze and explain lab results',
      icon: FileText,
      color: 'green',
      examples: ['Explain blood work', 'Review test results', 'Get health insights']
    },
    {
      id: 'find_doctor',
      name: 'Find Doctor',
      description: 'Search for specialists',
      icon: UserIcon,
      color: 'orange',
      examples: ['Find cardiologist', 'Search by location', 'Check availability']
    },
    {
      id: 'health_summary',
      name: 'Health Summary',
      description: 'Generate comprehensive health report',
      icon: Heart,
      color: 'red',
      examples: ['Create health summary', 'Get wellness report', 'Review health trends']
    },
    {
      id: 'medication_reminder',
      name: 'Set Reminders',
      description: 'Configure medication reminders',
      icon: Bell,
      color: 'yellow',
      examples: ['Set daily reminder', 'Configure alerts', 'Manage notifications']
    }
  ];

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    // Generate conversation ID on component mount
    setConversationId(`conv_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`);
  }, []);

  useEffect(() => {
    // Check if we should show survey after certain number of messages
    if (messageCount >= 5 && messageCount % 5 === 0) {
      // Don't show survey immediately, wait a bit
      setTimeout(() => {
        setShowSurveyModal(true);
      }, 2000);
    }
  }, [messageCount]);

  const handleSendMessage = async () => {
    if (!inputMessage.trim() || isLoading) return;

    const userMessage = {
      id: Date.now(),
      role: 'user',
      content: inputMessage,
      timestamp: new Date(),
      status: 'sent',
      type: 'text'
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);
    setMessageCount(prev => prev + 1);

    // Simulate AI response with enhanced features
    setTimeout(() => {
      const aiResponse = generateEnhancedResponse(inputMessage);
      setMessages(prev => [...prev, aiResponse]);
      setIsLoading(false);
      setMessageCount(prev => prev + 1);
    }, 1000 + Math.random() * 2000);
  };

  const generateEnhancedResponse = (userMessage) => {
    const lowerMessage = userMessage.toLowerCase();
    
    if (lowerMessage.includes('appointment') || lowerMessage.includes('schedule')) {
      return {
        id: Date.now() + 1,
        role: 'assistant',
        content: "I can help you schedule an appointment! I have access to real-time availability and can suggest the best times based on your preferences. What type of visit do you need?",
        timestamp: new Date(),
        status: 'sent',
        type: 'text',
        suggestions: ['Annual physical', 'Specialist consultation', 'Urgent care', 'Follow-up visit'],
        tool: 'schedule_appointment',
        data: {
          available_slots: [
            { date: '2024-02-15', time: '10:00 AM', doctor: 'Dr. Smith' },
            { date: '2024-02-16', time: '2:00 PM', doctor: 'Dr. Johnson' },
            { date: '2024-02-17', time: '9:00 AM', doctor: 'Dr. Williams' }
          ]
        }
      };
    } else if (lowerMessage.includes('medication') || lowerMessage.includes('meds') || lowerMessage.includes('pill')) {
      return {
        id: Date.now() + 1,
        role: 'assistant',
        content: "I can help you manage your medications! Let me check your current prescription status and refill information.",
        timestamp: new Date(),
        status: 'sent',
        type: 'text',
        suggestions: ['Check refills', 'Review side effects', 'Set reminders', 'Request refill'],
        tool: 'check_medications',
        data: {
          medications: [
            { name: 'Lisinopril', refills: 2, next_refill: '2024-02-20' },
            { name: 'Metformin', refills: 0, next_refill: '2024-02-10' }
          ]
        }
      };
    } else if (lowerMessage.includes('lab') || lowerMessage.includes('test') || lowerMessage.includes('result')) {
      return {
        id: Date.now() + 1,
        role: 'assistant',
        content: "I can help you understand your lab results! I'll analyze the data and provide personalized insights and recommendations.",
        timestamp: new Date(),
        status: 'sent',
        type: 'text',
        suggestions: ['Explain blood work', 'Review trends', 'Get recommendations', 'Compare results'],
        tool: 'lab_results',
        data: {
          recent_tests: ['Complete Blood Count', 'Metabolic Panel', 'Lipid Panel'],
          status: 'All values within normal range'
        }
      };
    } else if (lowerMessage.includes('doctor') || lowerMessage.includes('physician') || lowerMessage.includes('specialist')) {
      return {
        id: Date.now() + 1,
        role: 'assistant',
        content: "I can help you find the right doctor! I'll search based on your needs, location, and insurance coverage.",
        timestamp: new Date(),
        status: 'sent',
        type: 'text',
        suggestions: ['Search by specialty', 'Find by location', 'Check ratings', 'View availability'],
        tool: 'find_doctor',
        data: {
          specialties: ['Cardiology', 'Dermatology', 'Orthopedics', 'Neurology'],
          locations: ['Main Medical Center', 'Downtown Clinic', 'Northside Office']
        }
      };
    } else if (lowerMessage.includes('health') || lowerMessage.includes('summary') || lowerMessage.includes('report')) {
      return {
        id: Date.now() + 1,
        role: 'assistant',
        content: "I can generate a comprehensive health summary for you! This will include your recent appointments, medications, lab results, and personalized recommendations.",
        timestamp: new Date(),
        status: 'sent',
        type: 'text',
        suggestions: ['Generate summary', 'Include trends', 'Add recommendations', 'Export report'],
        tool: 'health_summary',
        data: {
          summary_type: 'comprehensive',
          includes: ['Appointments', 'Medications', 'Lab Results', 'Recommendations']
        }
      };
    } else if (lowerMessage.includes('reminder') || lowerMessage.includes('alert')) {
      return {
        id: Date.now() + 1,
        role: 'assistant',
        content: "I can help you set up smart reminders for your medications, appointments, and health checks!",
        timestamp: new Date(),
        status: 'sent',
        type: 'text',
        suggestions: ['Set medication reminder', 'Appointment alerts', 'Health check reminders', 'Custom notifications'],
        tool: 'medication_reminder',
        data: {
          reminder_types: ['Medication', 'Appointment', 'Health Check', 'Custom'],
          frequency_options: ['Daily', 'Weekly', 'Monthly', 'Custom']
        }
      };
    } else {
      return {
        id: Date.now() + 1,
        role: 'assistant',
        content: "I understand you're asking about that. Let me help you with that. Could you provide more specific details so I can give you the most accurate assistance?",
        timestamp: new Date(),
        status: 'sent',
        type: 'text',
        suggestions: [
          'Schedule an appointment',
          'Check my medications',
          'View lab results',
          'Find a doctor'
        ]
      };
    }
  };

  const handleSuggestionClick = (suggestion) => {
    setInputMessage(suggestion);
  };

  const handleToolClick = (tool) => {
    setSelectedTool(tool);
    setShowToolPanel(true);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const handleSurveyComplete = () => {
    // Add a thank you message to the chat
    const thankYouMessage = {
      id: Date.now(),
      role: 'assistant',
      content: "Thank you for your feedback! Your responses help us improve our AI assistant to better serve you. Is there anything else I can help you with?",
      timestamp: new Date(),
      status: 'sent',
      type: 'text',
      suggestions: [
        'Schedule an appointment',
        'Check my medications',
        'View lab results',
        'Generate health summary'
      ]
    };
    setMessages(prev => [...prev, thankYouMessage]);
  };

  const formatTime = (timestamp) => {
    return timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  const getColorClasses = (color) => {
    const colors = {
      blue: 'bg-blue-100 text-blue-800 border-blue-200',
      purple: 'bg-purple-100 text-purple-800 border-purple-200',
      green: 'bg-green-100 text-green-800 border-green-200',
      orange: 'bg-orange-100 text-orange-800 border-orange-200',
      red: 'bg-red-100 text-red-800 border-red-200',
      yellow: 'bg-yellow-100 text-yellow-800 border-yellow-200'
    };
    return colors[color] || colors.blue;
  };

  return (
    <div className="flex flex-col h-full bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 p-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-gradient-to-r from-primary-600 to-primary-700 rounded-full flex items-center justify-center">
              <Bot className="w-6 h-6 text-white" />
            </div>
            <div>
              <h2 className="text-lg font-semibold text-gray-900">AI Health Assistant</h2>
              <p className="text-sm text-gray-500">Powered by advanced AI</p>
            </div>
          </div>
          <div className="flex items-center space-x-2">
            <div className="flex items-center space-x-1 text-sm text-gray-500">
              <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
              <span>Online</span>
            </div>
            <button
              onClick={() => setShowToolPanel(!showToolPanel)}
              className="p-2 text-gray-400 hover:text-gray-600 transition-colors"
            >
              <Settings className="w-5 h-5" />
            </button>
          </div>
        </div>
      </div>

      {/* Tool Panel */}
      {showToolPanel && (
        <div className="bg-white border-b border-gray-200 p-4">
          <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
            {tools.map((tool) => (
              <button
                key={tool.id}
                onClick={() => handleToolClick(tool)}
                className="p-4 border border-gray-200 rounded-lg hover:border-primary-300 hover:bg-primary-50 transition-colors text-left"
              >
                <div className="flex items-center space-x-3">
                  <tool.icon className={`w-6 h-6 text-${tool.color}-600`} />
                  <div>
                    <h3 className="font-medium text-gray-900">{tool.name}</h3>
                    <p className="text-sm text-gray-500">{tool.description}</p>
                  </div>
                </div>
              </button>
            ))}
          </div>
        </div>
      )}

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
                  ? 'bg-primary-600 text-white'
                  : 'bg-white border border-gray-200'
              }`}
            >
              <div className="flex items-start space-x-2">
                {message.role === 'assistant' && (
                  <Bot className="w-5 h-5 text-primary-600 mt-0.5 flex-shrink-0" />
                )}
                <div className="flex-1">
                  <p className="text-sm">{message.content}</p>
                  {message.suggestions && (
                    <div className="mt-3 space-y-2">
                      {message.suggestions.map((suggestion, index) => (
                        <button
                          key={index}
                          onClick={() => handleSuggestionClick(suggestion)}
                          className="block w-full text-left px-3 py-2 text-xs bg-gray-100 hover:bg-gray-200 rounded transition-colors"
                        >
                          {suggestion}
                        </button>
                      ))}
                    </div>
                  )}
                  {message.data && (
                    <div className="mt-3 p-3 bg-gray-50 rounded-lg">
                      <pre className="text-xs text-gray-600 whitespace-pre-wrap">
                        {JSON.stringify(message.data, null, 2)}
                      </pre>
                    </div>
                  )}
                </div>
                {message.role === 'user' && (
                  <User className="w-5 h-5 text-white mt-0.5 flex-shrink-0" />
                )}
              </div>
              <div className="flex items-center justify-between mt-2">
                <span className="text-xs opacity-70">
                  {formatTime(message.timestamp)}
                </span>
                {message.status && (
                  <span className="text-xs opacity-70">
                    {message.status === 'sent' && <CheckCircle className="w-3 h-3" />}
                    {message.status === 'sending' && <Clock className="w-3 h-3 animate-spin" />}
                  </span>
                )}
              </div>
            </div>
          </div>
        ))}
        
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-white border border-gray-200 rounded-lg px-4 py-2">
              <div className="flex items-center space-x-2">
                <Bot className="w-5 h-5 text-primary-600" />
                <div className="flex space-x-1">
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                </div>
              </div>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="bg-white border-t border-gray-200 p-4">
        <div className="flex space-x-3">
          <div className="flex-1">
            <textarea
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Type your message..."
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent resize-none"
              rows={1}
            />
          </div>
          <button
            onClick={handleSendMessage}
            disabled={!inputMessage.trim() || isLoading}
            className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            <Send className="w-5 h-5" />
          </button>
        </div>
        
        {/* Quick Actions */}
        <div className="mt-3 flex flex-wrap gap-2">
          <button
            onClick={() => setShowSurveyModal(true)}
            className="flex items-center space-x-2 px-3 py-1 text-sm bg-blue-100 text-blue-700 rounded-full hover:bg-blue-200 transition-colors"
          >
            <MessageSquare className="w-4 h-4" />
            <span>Feedback</span>
          </button>
        </div>
      </div>

      {/* Survey Modal */}
      <SurveyModal
        isOpen={showSurveyModal}
        onClose={() => setShowSurveyModal(false)}
        surveyType="ai_chat"
        conversationId={conversationId}
        onComplete={handleSurveyComplete}
      />
    </div>
  );
};

export default EnhancedAgentChat; 
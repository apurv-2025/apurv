import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, Clock, CheckCircle, AlertCircle, Sparkles, Calendar, Pill, FileText, User as UserIcon, Bell, Heart, Zap, Settings } from 'lucide-react';

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

    // Simulate AI response with enhanced features
    setTimeout(() => {
      const aiResponse = generateEnhancedResponse(inputMessage);
      setMessages(prev => [...prev, aiResponse]);
      setIsLoading(false);
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
        suggestions: ['Medication reminders', 'Appointment alerts', 'Health check reminders', 'Custom notifications'],
        tool: 'medication_reminder',
        data: {
          reminder_types: ['Daily', 'Weekly', 'Monthly', 'Custom'],
          notification_methods: ['Email', 'SMS', 'Push notification']
        }
      };
    } else {
      return {
        id: Date.now() + 1,
        role: 'assistant',
        content: "I'm here to help with all your health needs! I can assist with appointments, medications, lab results, finding doctors, and more. What would you like to do?",
        timestamp: new Date(),
        status: 'sent',
        type: 'text',
        suggestions: ['Schedule appointment', 'Check medications', 'View lab results', 'Find doctor'],
        show_tools: true
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

  const formatTime = (timestamp) => {
    return timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  const getColorClasses = (color) => {
    const colors = {
      blue: 'bg-blue-100 text-blue-700 border-blue-200',
      purple: 'bg-purple-100 text-purple-700 border-purple-200',
      green: 'bg-green-100 text-green-700 border-green-200',
      orange: 'bg-orange-100 text-orange-700 border-orange-200',
      red: 'bg-red-100 text-red-700 border-red-200',
      yellow: 'bg-yellow-100 text-yellow-700 border-yellow-200'
    };
    return colors[color] || colors.blue;
  };

  return (
    <div className="flex h-full">
      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col">
        {/* Chat Header */}
        <div className="flex items-center justify-between p-4 border-b border-gray-200">
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-gradient-to-r from-green-500 to-blue-600 rounded-lg">
              <Bot className="w-5 h-5 text-white" />
            </div>
            <div>
              <h3 className="font-semibold text-gray-900">Enhanced AI Health Assistant</h3>
              <p className="text-sm text-gray-500">Powered by advanced AI • Real-time assistance</p>
            </div>
          </div>
          <div className="flex items-center space-x-2">
            <Sparkles className="w-4 h-4 text-green-600" />
            <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
            <span className="text-sm text-gray-500">Enhanced Mode</span>
          </div>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-xs lg:max-w-md px-4 py-3 rounded-lg ${
                  message.role === 'user'
                    ? 'bg-green-500 text-white'
                    : 'bg-gray-50 text-gray-900 border border-gray-200'
                }`}
              >
                <div className="flex items-start space-x-2">
                  {message.role === 'assistant' && (
                    <Bot className="w-4 h-4 text-green-600 mt-0.5 flex-shrink-0" />
                  )}
                  <div className="flex-1">
                    <p className="text-sm">{message.content}</p>
                    
                    {/* Suggestions */}
                    {message.suggestions && message.role === 'assistant' && (
                      <div className="mt-3 space-y-2">
                        <p className="text-xs text-gray-500 font-medium">Quick Actions:</p>
                        <div className="flex flex-wrap gap-1">
                          {message.suggestions.map((suggestion, index) => (
                            <button
                              key={index}
                              onClick={() => handleSuggestionClick(suggestion)}
                              className="px-2 py-1 text-xs bg-white border border-gray-200 rounded-full hover:bg-gray-50 transition-colors"
                            >
                              {suggestion}
                            </button>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Tool Data Display */}
                    {message.data && message.role === 'assistant' && (
                      <div className="mt-3 p-2 bg-blue-50 rounded border border-blue-200">
                        <p className="text-xs text-blue-700 font-medium mb-1">Available Data:</p>
                        <div className="text-xs text-blue-600">
                          {message.tool === 'schedule_appointment' && (
                            <div>
                              <p>Available slots: {message.data.available_slots.length}</p>
                              <p>Next available: {message.data.available_slots[0]?.date}</p>
                            </div>
                          )}
                          {message.tool === 'check_medications' && (
                            <div>
                              <p>Medications: {message.data.medications.length}</p>
                              <p>Needs refill: {message.data.medications.filter(m => m.refills === 0).length}</p>
                            </div>
                          )}
                          {message.tool === 'lab_results' && (
                            <div>
                              <p>Recent tests: {message.data.recent_tests.length}</p>
                              <p>Status: {message.data.status}</p>
                            </div>
                          )}
                        </div>
                      </div>
                    )}

                    <div className="flex items-center justify-between mt-2">
                      <span className="text-xs opacity-70">
                        {formatTime(message.timestamp)}
                      </span>
                      {message.status === 'sent' && (
                        <CheckCircle className="w-3 h-3 text-green-500" />
                      )}
                      {message.status === 'sending' && (
                        <Clock className="w-3 h-3 text-gray-400" />
                      )}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          ))}
          
          {isLoading && (
            <div className="flex justify-start">
              <div className="bg-gray-50 text-gray-900 max-w-xs lg:max-w-md px-4 py-3 rounded-lg border border-gray-200">
                <div className="flex items-center space-x-2">
                  <Bot className="w-4 h-4 text-green-600" />
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
        <div className="p-4 border-t border-gray-200">
          <div className="flex space-x-2">
            <div className="flex-1">
              <textarea
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Type your message or ask about your health..."
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent resize-none"
                rows="1"
                disabled={isLoading}
              />
            </div>
            <button
              onClick={handleSendMessage}
              disabled={!inputMessage.trim() || isLoading}
              className="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              <Send className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      {/* Tools Panel */}
      {showToolPanel && (
        <div className="w-80 border-l border-gray-200 bg-gray-50">
          <div className="p-4 border-b border-gray-200">
            <div className="flex items-center justify-between">
              <h3 className="font-semibold text-gray-900">AI Tools</h3>
              <button
                onClick={() => setShowToolPanel(false)}
                className="text-gray-400 hover:text-gray-600"
              >
                ×
              </button>
            </div>
          </div>
          <div className="p-4 space-y-3">
            {tools.map((tool) => {
              const Icon = tool.icon;
              return (
                <div
                  key={tool.id}
                  className={`p-3 rounded-lg border cursor-pointer transition-colors ${getColorClasses(tool.color)}`}
                  onClick={() => handleToolClick(tool)}
                >
                  <div className="flex items-center space-x-3">
                    <Icon className="w-5 h-5" />
                    <div>
                      <h4 className="font-medium">{tool.name}</h4>
                      <p className="text-xs opacity-80">{tool.description}</p>
                    </div>
                  </div>
                  <div className="mt-2">
                    <p className="text-xs font-medium mb-1">Examples:</p>
                    <div className="space-y-1">
                      {tool.examples.map((example, index) => (
                        <button
                          key={index}
                          onClick={(e) => {
                            e.stopPropagation();
                            setInputMessage(example);
                          }}
                          className="block text-xs hover:underline"
                        >
                          • {example}
                        </button>
                      ))}
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
};

export default EnhancedAgentChat; 
import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, Clock, CheckCircle, AlertCircle } from 'lucide-react';

const AgentChat = () => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      role: 'assistant',
      content: 'Hello! I\'m your AI health assistant. I can help you with appointments, medications, lab results, and more. How can I assist you today?',
      timestamp: new Date(),
      status: 'sent'
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
      role: 'user',
      content: inputMessage,
      timestamp: new Date(),
      status: 'sent'
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    // Simulate AI response
    setTimeout(() => {
      const aiResponse = {
        id: Date.now() + 1,
        role: 'assistant',
        content: generateMockResponse(inputMessage),
        timestamp: new Date(),
        status: 'sent'
      };
      setMessages(prev => [...prev, aiResponse]);
      setIsLoading(false);
    }, 1000 + Math.random() * 2000);
  };

  const generateMockResponse = (userMessage) => {
    const lowerMessage = userMessage.toLowerCase();
    
    if (lowerMessage.includes('appointment') || lowerMessage.includes('schedule')) {
      return "I can help you schedule an appointment! What type of visit do you need? I can assist with annual physicals, specialist consultations, or urgent care visits.";
    } else if (lowerMessage.includes('medication') || lowerMessage.includes('meds') || lowerMessage.includes('pill')) {
      return "I can help you check your medications, refill status, and set up reminders. Would you like me to review your current medication list or help you set up a reminder?";
    } else if (lowerMessage.includes('lab') || lowerMessage.includes('test') || lowerMessage.includes('result')) {
      return "I can help you understand your lab results! I can explain what each test means and provide personalized insights. Which lab results would you like me to review?";
    } else if (lowerMessage.includes('doctor') || lowerMessage.includes('physician') || lowerMessage.includes('specialist')) {
      return "I can help you find and book appointments with doctors. What specialty are you looking for? I can search based on location, availability, and your insurance.";
    } else if (lowerMessage.includes('health') || lowerMessage.includes('summary') || lowerMessage.includes('report')) {
      return "I can generate a comprehensive health summary for you, including your recent appointments, medications, lab results, and personalized recommendations. Would you like me to create one?";
    } else if (lowerMessage.includes('reminder') || lowerMessage.includes('alert')) {
      return "I can help you set up medication reminders, appointment notifications, and health check reminders. What type of reminder would you like to set up?";
    } else {
      return "I understand you're asking about your health. I'm here to help with appointments, medications, lab results, finding doctors, and more. Could you please be more specific about what you need assistance with?";
    }
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

  return (
    <div className="flex flex-col h-full">
      {/* Chat Header */}
      <div className="flex items-center justify-between p-4 border-b border-gray-200">
        <div className="flex items-center space-x-3">
          <div className="p-2 bg-green-100 rounded-lg">
            <Bot className="w-5 h-5 text-green-600" />
          </div>
          <div>
            <h3 className="font-semibold text-gray-900">AI Health Assistant</h3>
            <p className="text-sm text-gray-500">Online • Ready to help</p>
          </div>
        </div>
        <div className="flex items-center space-x-2">
          <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
          <span className="text-sm text-gray-500">Active</span>
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
              className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                message.role === 'user'
                  ? 'bg-green-500 text-white'
                  : 'bg-gray-100 text-gray-900'
              }`}
            >
              <div className="flex items-start space-x-2">
                {message.role === 'assistant' && (
                  <Bot className="w-4 h-4 text-green-600 mt-0.5 flex-shrink-0" />
                )}
                <div className="flex-1">
                  <p className="text-sm">{message.content}</p>
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
            <div className="bg-gray-100 text-gray-900 max-w-xs lg:max-w-md px-4 py-2 rounded-lg">
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
              placeholder="Type your message here..."
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
        
        {/* Quick Actions */}
        <div className="mt-3 flex flex-wrap gap-2">
          <button
            onClick={() => setInputMessage("I need to schedule an appointment")}
            className="px-3 py-1 text-xs bg-blue-100 text-blue-700 rounded-full hover:bg-blue-200 transition-colors"
          >
            Schedule Appointment
          </button>
          <button
            onClick={() => setInputMessage("Check my medications")}
            className="px-3 py-1 text-xs bg-purple-100 text-purple-700 rounded-full hover:bg-purple-200 transition-colors"
          >
            Check Medications
          </button>
          <button
            onClick={() => setInputMessage("Show my lab results")}
            className="px-3 py-1 text-xs bg-green-100 text-green-700 rounded-full hover:bg-green-200 transition-colors"
          >
            Lab Results
          </button>
          <button
            onClick={() => setInputMessage("Find a doctor")}
            className="px-3 py-1 text-xs bg-orange-100 text-orange-700 rounded-full hover:bg-orange-200 transition-colors"
          >
            Find Doctor
          </button>
        </div>
      </div>
    </div>
  );
};

export default AgentChat; 
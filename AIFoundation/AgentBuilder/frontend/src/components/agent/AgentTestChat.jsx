import React, { useRef, useEffect } from 'react';
import { Send, Loader, Bot } from 'lucide-react';

const AgentTestChat = ({ 
  testMessage, 
  setTestMessage, 
  testConversation, 
  isTestingAgent, 
  sendTestMessage 
}) => {
  const chatEndRef = useRef(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [testConversation]);

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 flex flex-col h-96">
      <div className="p-4 border-b border-gray-200">
        <h3 className="text-lg font-semibold text-gray-900">Test Conversation</h3>
        <p className="text-sm text-gray-600">Test your agent's responses in real-time</p>
      </div>
      
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {testConversation.length === 0 ? (
          <div className="text-center text-gray-500 mt-8">
            <Bot className="w-12 h-12 mx-auto mb-4 text-gray-300" />
            <p>Start a conversation to test your agent</p>
          </div>
        ) : (
          testConversation.map((message, index) => (
            <div key={index} className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                message.type === 'user' 
                  ? 'bg-blue-600 text-white' 
                  : 'bg-gray-100 text-gray-900'
              }`}>
                <p className="text-sm">{message.content}</p>
                {message.type === 'agent' && (
                  <div className="mt-2 text-xs opacity-75">
                    <div>Confidence: {(message.confidence * 100).toFixed(1)}%</div>
                    <div>Response time: {message.processingTime.toFixed(0)}ms</div>
                  </div>
                )}
              </div>
            </div>
          ))
        )}
        {isTestingAgent && (
          <div className="flex justify-start">
            <div className="bg-gray-100 text-gray-900 px-4 py-2 rounded-lg">
              <div className="flex items-center space-x-2">
                <Loader className="w-4 h-4 animate-spin" />
                <span className="text-sm">Agent is thinking...</span>
              </div>
            </div>
          </div>
        )}
        <div ref={chatEndRef} />
      </div>
      
      <div className="p-4 border-t border-gray-200">
        <div className="flex space-x-2">
          <input
            type="text"
            value={testMessage}
            onChange={(e) => setTestMessage(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && sendTestMessage()}
            placeholder="Type your message..."
            className="flex-1 border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            disabled={isTestingAgent}
          />
          <button
            onClick={sendTestMessage}
            disabled={!testMessage.trim() || isTestingAgent}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
          >
            <Send className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
};

export default AgentTestChat; 
import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, Loader2, Settings, History, Download, Copy, ThumbsUp, ThumbsDown, RotateCcw } from 'lucide-react';

interface EnhancedAgentChatProps {
  apiUrl?: string;
  userId?: string;
  model?: string;
  theme?: 'light' | 'dark';
  showSidebar?: boolean;
  showQuickActions?: boolean;
}

interface Message {
  id: string;
  type: 'user' | 'agent';
  content: string;
  timestamp: Date;
  metadata?: Record<string, any>;
}

const EnhancedAgentChat: React.FC<EnhancedAgentChatProps> = ({
  apiUrl = 'http://localhost:8000',
  userId = 'default_user',
  model = 'gpt-4',
  theme = 'light',
  showSidebar = true,
  showQuickActions = true
}) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [selectedModel, setSelectedModel] = useState(model);
  const [sidebarOpen, setSidebarOpen] = useState(showSidebar);
  const [copiedMessageId, setCopiedMessageId] = useState<string | null>(null);
  const [messageFeedback, setMessageFeedback] = useState<Record<string, 'like' | 'dislike' | null>>({});
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async () => {
    if (!inputMessage.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      type: 'user',
      content: inputMessage,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      const response = await fetch(`${apiUrl}/api/agent/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: inputMessage,
          user_id: userId,
          context: { model: selectedModel }
        })
      });

      const data = await response.json();
      
      const agentMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'agent',
        content: data.response || 'Sorry, I could not process your request.',
        timestamp: new Date(),
        metadata: data.result
      };

      setMessages(prev => [...prev, agentMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'agent',
        content: 'Sorry, there was an error processing your request.',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const copyMessage = async (messageId: string, content: string) => {
    try {
      await navigator.clipboard.writeText(content);
      setCopiedMessageId(messageId);
      setTimeout(() => setCopiedMessageId(null), 2000);
    } catch (error) {
      console.error('Failed to copy message:', error);
    }
  };

  const handleFeedback = (messageId: string, feedback: 'like' | 'dislike') => {
    setMessageFeedback(prev => ({ ...prev, [messageId]: feedback }));
    // Here you would typically send feedback to the backend
    console.log(`Feedback for message ${messageId}: ${feedback}`);
  };

  const retryMessage = async (messageId: string) => {
    const messageIndex = messages.findIndex(m => m.id === messageId);
    if (messageIndex > 0) {
      const previousMessage = messages[messageIndex - 1];
      if (previousMessage.type === 'user') {
        setInputMessage(previousMessage.content);
        // Remove the failed message and retry
        setMessages(prev => prev.filter(m => m.id !== messageId));
        await handleSendMessage();
      }
    }
  };

  const exportConversation = () => {
    const conversationData = {
      messages,
      metadata: {
        userId,
        model: selectedModel,
        exportedAt: new Date().toISOString()
      }
    };
    
    const blob = new Blob([JSON.stringify(conversationData, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `conversation-${new Date().toISOString().split('T')[0]}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const quickActions = [
    { label: 'Analyze Claim', action: 'analyze_claim' },
    { label: 'Process Rejection', action: 'process_rejection' },
    { label: 'Generate Report', action: 'generate_report' },
    { label: 'Search Claims', action: 'search_claims' }
  ];

  const handleQuickAction = async (action: string) => {
    const actionMessages = {
      analyze_claim: 'Please provide the claim ID you would like me to analyze.',
      process_rejection: 'Please provide the rejection details you would like me to process.',
      generate_report: 'What type of report would you like me to generate?',
      search_claims: 'What criteria would you like me to search for?'
    };
    
    setInputMessage(actionMessages[action as keyof typeof actionMessages] || '');
  };

  return (
    <div className={`h-full flex ${theme === 'dark' ? 'bg-gray-900 text-white' : 'bg-white'}`}>
      {/* Sidebar */}
      {sidebarOpen && (
        <div className={`w-64 border-r ${theme === 'dark' ? 'border-gray-700 bg-gray-800' : 'border-gray-200 bg-gray-50'}`}>
          <div className="p-4">
            <h3 className="font-semibold mb-4">Settings</h3>
            
            <div className="mb-4">
              <label className="block text-sm font-medium mb-2">Model</label>
              <select
                value={selectedModel}
                onChange={(e) => setSelectedModel(e.target.value)}
                className={`w-full p-2 border rounded-lg ${
                  theme === 'dark' 
                    ? 'bg-gray-700 border-gray-600 text-white' 
                    : 'bg-white border-gray-300'
                }`}
              >
                <option value="gpt-4">GPT-4</option>
                <option value="gpt-3.5-turbo">GPT-3.5 Turbo</option>
                <option value="claude-3-sonnet">Claude 3 Sonnet</option>
                <option value="claude-3-haiku">Claude 3 Haiku</option>
              </select>
            </div>

            <div className="mb-4">
              <label className="block text-sm font-medium mb-2">User ID</label>
              <input
                type="text"
                value={userId}
                readOnly
                className={`w-full p-2 border rounded-lg ${
                  theme === 'dark' 
                    ? 'bg-gray-700 border-gray-600 text-white' 
                    : 'bg-gray-100 border-gray-300'
                }`}
              />
            </div>

            <button
              onClick={exportConversation}
              className={`w-full p-2 rounded-lg flex items-center justify-center space-x-2 ${
                theme === 'dark' 
                  ? 'bg-blue-600 hover:bg-blue-700' 
                  : 'bg-blue-600 hover:bg-blue-700 text-white'
              }`}
            >
              <Download className="h-4 w-4" />
              <span>Export Chat</span>
            </button>
          </div>
        </div>
      )}

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <div className={`p-4 border-b ${theme === 'dark' ? 'border-gray-700' : 'border-gray-200'}`}>
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <Bot className="h-6 w-6 text-blue-600" />
              <div>
                <h2 className="font-semibold">AI Assistant</h2>
                <p className="text-sm text-gray-500">Powered by {selectedModel}</p>
              </div>
            </div>
            <div className="flex items-center space-x-2">
              <button
                onClick={() => setSidebarOpen(!sidebarOpen)}
                className={`p-2 rounded-lg ${
                  theme === 'dark' 
                    ? 'hover:bg-gray-700' 
                    : 'hover:bg-gray-100'
                }`}
              >
                <Settings className="h-5 w-5" />
              </button>
            </div>
          </div>
        </div>

        {/* Quick Actions */}
        {showQuickActions && (
          <div className={`p-4 border-b ${theme === 'dark' ? 'border-gray-700' : 'border-gray-200'}`}>
            <div className="flex flex-wrap gap-2">
              {quickActions.map((action) => (
                <button
                  key={action.action}
                  onClick={() => handleQuickAction(action.action)}
                  className={`px-3 py-1 text-sm rounded-full ${
                    theme === 'dark'
                      ? 'bg-gray-700 hover:bg-gray-600'
                      : 'bg-gray-100 hover:bg-gray-200'
                  }`}
                >
                  {action.label}
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
              className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div className={`max-w-xs lg:max-w-md ${message.type === 'user' ? 'order-2' : 'order-1'}`}>
                <div
                  className={`px-4 py-2 rounded-lg ${
                    message.type === 'user'
                      ? 'bg-blue-600 text-white'
                      : theme === 'dark' ? 'bg-gray-700' : 'bg-gray-100'
                  }`}
                >
                  <p className="text-sm whitespace-pre-wrap">{message.content}</p>
                </div>
                
                {/* Message Actions */}
                {message.type === 'agent' && (
                  <div className="flex items-center space-x-2 mt-2">
                    <button
                      onClick={() => copyMessage(message.id, message.content)}
                      className={`p-1 rounded ${
                        theme === 'dark' ? 'hover:bg-gray-700' : 'hover:bg-gray-100'
                      }`}
                      title="Copy message"
                    >
                      {copiedMessageId === message.id ? (
                        <span className="text-green-500 text-xs">Copied!</span>
                      ) : (
                        <Copy className="h-3 w-3" />
                      )}
                    </button>
                    
                    <button
                      onClick={() => handleFeedback(message.id, 'like')}
                      className={`p-1 rounded ${
                        messageFeedback[message.id] === 'like' 
                          ? 'text-green-500' 
                          : theme === 'dark' ? 'hover:bg-gray-700' : 'hover:bg-gray-100'
                      }`}
                      title="Like"
                    >
                      <ThumbsUp className="h-3 w-3" />
                    </button>
                    
                    <button
                      onClick={() => handleFeedback(message.id, 'dislike')}
                      className={`p-1 rounded ${
                        messageFeedback[message.id] === 'dislike' 
                          ? 'text-red-500' 
                          : theme === 'dark' ? 'hover:bg-gray-700' : 'hover:bg-gray-100'
                      }`}
                      title="Dislike"
                    >
                      <ThumbsDown className="h-3 w-3" />
                    </button>
                    
                    <button
                      onClick={() => retryMessage(message.id)}
                      className={`p-1 rounded ${
                        theme === 'dark' ? 'hover:bg-gray-700' : 'hover:bg-gray-100'
                      }`}
                      title="Retry"
                    >
                      <RotateCcw className="h-3 w-3" />
                    </button>
                  </div>
                )}
              </div>
            </div>
          ))}
          
          {isLoading && (
            <div className="flex justify-start">
              <div className={`px-4 py-2 rounded-lg ${theme === 'dark' ? 'bg-gray-700' : 'bg-gray-100'}`}>
                <Loader2 className="animate-spin h-4 w-4" />
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
        
        {/* Input */}
        <div className={`p-4 border-t ${theme === 'dark' ? 'border-gray-700' : 'border-gray-200'}`}>
          <div className="flex space-x-2">
            <input
              type="text"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
              placeholder="Type your message..."
              className={`flex-1 px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                theme === 'dark' ? 'bg-gray-800 border-gray-600' : 'bg-white border-gray-300'
              }`}
              disabled={isLoading}
            />
            <button
              onClick={handleSendMessage}
              disabled={isLoading || !inputMessage.trim()}
              className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <Send className="h-4 w-4" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default EnhancedAgentChat; 
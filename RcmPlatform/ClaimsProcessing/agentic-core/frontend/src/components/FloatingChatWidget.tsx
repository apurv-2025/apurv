import React, { useState, useRef, useEffect } from 'react';
import { MessageCircle, X, Send, Loader2, Copy, ThumbsUp, ThumbsDown, RotateCcw, Minimize2 } from 'lucide-react';

interface FloatingChatWidgetProps {
  apiUrl?: string;
  userId?: string;
  model?: string;
  theme?: 'light' | 'dark';
  position?: 'bottom-right' | 'bottom-left' | 'top-right' | 'top-left';
  initialMessage?: string;
}

interface Message {
  id: string;
  type: 'user' | 'agent';
  content: string;
  timestamp: Date;
}

const FloatingChatWidget: React.FC<FloatingChatWidgetProps> = ({
  apiUrl = 'http://localhost:8000',
  userId = 'default_user',
  model = 'gpt-4',
  theme = 'light',
  position = 'bottom-right',
  initialMessage = 'Hello! How can I help you today?'
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const [isMinimized, setIsMinimized] = useState(false);
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      type: 'agent',
      content: initialMessage,
      timestamp: new Date()
    }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
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
          context: { model }
        })
      });

      const data = await response.json();
      
      const agentMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'agent',
        content: data.response || 'Sorry, I could not process your request.',
        timestamp: new Date()
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
    console.log(`Feedback for message ${messageId}: ${feedback}`);
  };

  const retryMessage = async (messageId: string) => {
    const messageIndex = messages.findIndex(m => m.id === messageId);
    if (messageIndex > 0) {
      const previousMessage = messages[messageIndex - 1];
      if (previousMessage.type === 'user') {
        setInputMessage(previousMessage.content);
        setMessages(prev => prev.filter(m => m.id !== messageId));
        await handleSendMessage();
      }
    }
  };

  const getPositionClasses = () => {
    switch (position) {
      case 'bottom-left':
        return 'bottom-4 left-4';
      case 'top-right':
        return 'top-4 right-4';
      case 'top-left':
        return 'top-4 left-4';
      default:
        return 'bottom-4 right-4';
    }
  };

  if (!isOpen) {
    return (
      <div className={`fixed ${getPositionClasses()} z-50`}>
        <button
          onClick={() => setIsOpen(true)}
          className={`p-4 rounded-full shadow-lg ${
            theme === 'dark' 
              ? 'bg-blue-600 hover:bg-blue-700 text-white' 
              : 'bg-blue-600 hover:bg-blue-700 text-white'
          }`}
        >
          <MessageCircle className="h-6 w-6" />
        </button>
      </div>
    );
  }

  return (
    <div className={`fixed ${getPositionClasses()} z-50`}>
      <div className={`w-80 h-96 rounded-lg shadow-xl flex flex-col ${
        theme === 'dark' ? 'bg-gray-800 text-white' : 'bg-white'
      }`}>
        {/* Header */}
        <div className={`p-4 border-b ${theme === 'dark' ? 'border-gray-700' : 'border-gray-200'}`}>
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <MessageCircle className="h-5 w-5 text-blue-600" />
              <span className="font-semibold">AI Assistant</span>
            </div>
            <div className="flex items-center space-x-1">
              <button
                onClick={() => setIsMinimized(!isMinimized)}
                className={`p-1 rounded ${
                  theme === 'dark' ? 'hover:bg-gray-700' : 'hover:bg-gray-100'
                }`}
              >
                <Minimize2 className="h-4 w-4" />
              </button>
              <button
                onClick={() => setIsOpen(false)}
                className={`p-1 rounded ${
                  theme === 'dark' ? 'hover:bg-gray-700' : 'hover:bg-gray-100'
                }`}
              >
                <X className="h-4 w-4" />
              </button>
            </div>
          </div>
        </div>

        {!isMinimized && (
          <>
            {/* Messages */}
            <div className="flex-1 overflow-y-auto p-4 space-y-3">
              {messages.map((message) => (
                <div
                  key={message.id}
                  className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div className={`max-w-xs ${message.type === 'user' ? 'order-2' : 'order-1'}`}>
                    <div
                      className={`px-3 py-2 rounded-lg text-sm ${
                        message.type === 'user'
                          ? 'bg-blue-600 text-white'
                          : theme === 'dark' ? 'bg-gray-700' : 'bg-gray-100'
                      }`}
                    >
                      <p className="whitespace-pre-wrap">{message.content}</p>
                    </div>
                    
                    {/* Message Actions */}
                    {message.type === 'agent' && (
                      <div className="flex items-center space-x-1 mt-1">
                        <button
                          onClick={() => copyMessage(message.id, message.content)}
                          className={`p-1 rounded ${
                            theme === 'dark' ? 'hover:bg-gray-700' : 'hover:bg-gray-100'
                          }`}
                          title="Copy"
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
                  <div className={`px-3 py-2 rounded-lg ${theme === 'dark' ? 'bg-gray-700' : 'bg-gray-100'}`}>
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
                  className={`flex-1 px-3 py-2 border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                    theme === 'dark' ? 'bg-gray-700 border-gray-600' : 'bg-white border-gray-300'
                  }`}
                  disabled={isLoading}
                />
                <button
                  onClick={handleSendMessage}
                  disabled={isLoading || !inputMessage.trim()}
                  className="px-3 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <Send className="h-4 w-4" />
                </button>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default FloatingChatWidget; 
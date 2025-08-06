import React, { useState, useEffect } from 'react';
import { Mail, Calendar, User, Eye, Check } from 'lucide-react';
import { useAPI } from '../hooks/useAPI';

const Messages = () => {
  const { get, put } = useAPI();
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchMessages();
  }, []);

  const fetchMessages = async () => {
    try {
      const data = await get('/messages');
      setMessages(data);
    } catch (error) {
      console.error('Error fetching messages:', error);
    } finally {
      setLoading(false);
    }
  };

  const markAsRead = async (messageId) => {
    try {
      await put(`/messages/${messageId}/read`);
      // Update local state
      setMessages(messages.map(msg => 
        msg.id === messageId ? { ...msg, is_read: true } : msg
      ));
    } catch (error) {
      console.error('Error marking message as read:', error);
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffTime = Math.abs(now - date);
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    
    if (diffDays === 1) {
      return 'Yesterday';
    } else if (diffDays < 7) {
      return `${diffDays} days ago`;
    } else {
      return date.toLocaleDateString();
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  const unreadCount = messages.filter(msg => !msg.is_read).length;

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-gray-800">Messages</h2>
        {unreadCount > 0 && (
          <span className="bg-red-500 text-white px-3 py-1 rounded-full text-sm font-medium">
            {unreadCount} unread
          </span>
        )}
      </div>

      <div className="bg-white rounded-lg shadow overflow-hidden">
        <div className="p-6 border-b border-gray-200">
          <h3 className="text-lg font-semibold text-gray-800">Inbox</h3>
        </div>
        
        {messages.length === 0 ? (
          <div className="p-6 text-center text-gray-500">
            <Mail className="w-12 h-12 mx-auto mb-4 text-gray-300" />
            <p>No messages</p>
          </div>
        ) : (
          <div className="divide-y divide-gray-200">
            {messages.map((message) => (
              <div 
                key={message.id} 
                className={`p-6 hover:bg-gray-50 transition-colors ${!message.is_read ? 'bg-blue-50' : ''}`}
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-4">
                    <div className={`w-12 h-12 rounded-full flex items-center justify-center ${
                      message.is_read ? 'bg-gray-100' : 'bg-blue-100'
                    }`}>
                      <Mail className={`w-6 h-6 ${message.is_read ? 'text-gray-600' : 'text-blue-600'}`} />
                    </div>
                    <div className="flex-1">
                      <div className="flex items-center space-x-2">
                        <h4 className="text-lg font-medium text-gray-800">{message.subject}</h4>
                        {!message.is_read && (
                          <span className="w-2 h-2 bg-blue-600 rounded-full"></span>
                        )}
                      </div>
                      <div className="flex items-center space-x-4 text-sm text-gray-600 mt-1">
                        <span className="flex items-center space-x-1">
                          <User className="w-4 h-4" />
                          <span>Dr. {message.sender.first_name} {message.sender.last_name}</span>
                        </span>
                        <span>•</span>
                        <span className="flex items-center space-x-1">
                          <Calendar className="w-4 h-4" />
                          <span>{formatDate(message.created_at)}</span>
                        </span>
                      </div>
                      <p className="text-sm text-gray-600 mt-2 line-clamp-2">{message.content}</p>
                    </div>
                  </div>
                  <div className="flex items-center space-x-2">
                    {!message.is_read && (
                      <button
                        onClick={() => markAsRead(message.id)}
                        className="p-2 text-gray-400 hover:text-green-600 hover:bg-green-50 rounded-lg transition-colors"
                        title="Mark as read"
                      >
                        <Check className="w-4 h-4" />
                      </button>
                    )}
                    <button className="p-2 text-gray-400 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors">
                      <Eye className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Message Tips */}
      <div className="bg-orange-50 rounded-lg p-6">
        <div className="flex items-start space-x-3">
          <Mail className="w-6 h-6 text-orange-600 mt-1" />
          <div>
            <h4 className="text-lg font-semibold text-orange-800 mb-2">Message Guidelines</h4>
            <ul className="text-sm text-orange-700 space-y-1">
              <li>• Messages are typically responded to within 24-48 hours</li>
              <li>• For urgent medical concerns, please call your doctor's office</li>
              <li>• Include relevant details when asking questions</li>
              <li>• Check your messages regularly for updates</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Messages; 
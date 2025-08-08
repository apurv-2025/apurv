// =============================================================================
// FILE: frontend/src/pages/AgentChat.jsx
// =============================================================================
import React from 'react';
import AgentChatComponent from '../components/agent/AgentChat';

const AgentChat = () => {
  return (
    <div className="h-screen p-6 bg-gray-50">
      <div className="h-full">
        <AgentChatComponent />
      </div>
    </div>
  );
};

export default AgentChat; 
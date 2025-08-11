export interface AgenticConfig {
  apiUrl: string;
  userId: string;
  model: string;
  theme: 'light' | 'dark';
  position?: 'bottom-right' | 'bottom-left' | 'top-right' | 'top-left';
  showQuickActions?: boolean;
  enableHistory?: boolean;
  enableMetrics?: boolean;
}

export interface ChatMessage {
  id: number;
  type: 'user' | 'agent';
  content: string;
  timestamp: Date;
  metadata?: Record<string, any>;
}

export interface Conversation {
  id: string;
  title: string;
  messages: ChatMessage[];
  createdAt: Date;
  updatedAt: Date;
}

export interface Task {
  id: string;
  type: string;
  status: 'pending' | 'processing' | 'completed' | 'failed';
  data: Record<string, any>;
  result?: Record<string, any>;
  createdAt: Date;
  completedAt?: Date;
}

export interface Tool {
  name: string;
  description: string;
  parameters: Record<string, any>;
  enabled: boolean;
}

export interface User {
  id: string;
  name: string;
  email: string;
  preferences: Record<string, any>;
}

export interface ModelConfig {
  name: string;
  provider: string;
  maxTokens: number;
  temperature: number;
  enabled: boolean;
}

export interface AgentResponse {
  taskId: string;
  taskType: string;
  status: string;
  response: string;
  result?: Record<string, any>;
  createdAt: Date;
  completedAt?: Date;
}

export interface AgentRequest {
  taskType: string;
  userId: string;
  taskDescription: string;
  context?: Record<string, any>;
}

export type TaskType = 'chat' | 'analyze_claim' | 'analyze_rejection' | 'generate_report' | 'search_claims';

export type AgentStatus = 'idle' | 'processing' | 'error' | 'completed'; 
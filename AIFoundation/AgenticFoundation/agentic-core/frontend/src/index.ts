/**
 * Agentic Core Frontend - Reusable AI Agent Components
 * 
 * This package provides React components for building AI agent interfaces
 * that can be easily integrated into any application.
 */

// Core Components
import AgentChat from './components/AgentChat';
export { default as AgentChat } from './components/AgentChat';

// Types
export type {
  AgenticConfig,
  ChatMessage as ChatMessageType,
  Conversation,
  Task,
  Tool,
  User,
  ModelConfig,
  AgentResponse,
  AgentRequest,
  TaskType,
  AgentStatus,
} from './types';

// Constants
export { DEFAULT_CONFIG, SUPPORTED_MODELS, QUICK_ACTIONS } from './constants';

// Version info
export const VERSION = '1.0.0';
export const AUTHOR = 'Agentic Core Team';

// Default configuration
export const DEFAULT_AGENTIC_CONFIG = {
  apiUrl: 'http://localhost:8000',
  model: 'gpt-4',
  theme: 'light',
  position: 'bottom-right',
  showQuickActions: true,
  enableHistory: true,
  enableMetrics: true,
} as const;

// Quick setup function
export function createAgenticChat(config: Partial<typeof DEFAULT_AGENTIC_CONFIG> = {}) {
  const finalConfig = { ...DEFAULT_AGENTIC_CONFIG, ...config };
  
  return {
    AgentChat: () => import('./components/AgentChat').then(m => m.default),
    config: finalConfig,
  };
}

// Plugin system
export class AgenticPlugin {
  constructor(
    public name: string,
    public component: React.ComponentType<any>,
    public config: Record<string, any> = {}
  ) {}
}

export class AgenticPluginManager {
  private plugins: Map<string, AgenticPlugin> = new Map();

  register(plugin: AgenticPlugin) {
    this.plugins.set(plugin.name, plugin);
  }

  get(name: string): AgenticPlugin | undefined {
    return this.plugins.get(name);
  }

  getAll(): AgenticPlugin[] {
    return Array.from(this.plugins.values());
  }

  remove(name: string): boolean {
    return this.plugins.delete(name);
  }
}

// Global plugin manager instance
export const pluginManager = new AgenticPluginManager();

// Error handling
export class AgenticError extends Error {
  constructor(
    message: string,
    public code: string,
    public details?: Record<string, any>
  ) {
    super(message);
    this.name = 'AgenticError';
  }
}

// Logging
export const logger = {
  info: (message: string, ...args: any[]) => console.log(`[Agentic] ${message}`, ...args),
  warn: (message: string, ...args: any[]) => console.warn(`[Agentic] ${message}`, ...args),
  error: (message: string, ...args: any[]) => console.error(`[Agentic] ${message}`, ...args),
  debug: (message: string, ...args: any[]) => console.debug(`[Agentic] ${message}`, ...args),
};

// Performance monitoring
export const performance = {
  mark: (name: string) => {
    if (typeof window !== 'undefined' && window.performance) {
      window.performance.mark(name);
    }
  },
  measure: (name: string, startMark: string, endMark: string) => {
    if (typeof window !== 'undefined' && window.performance) {
      try {
        window.performance.measure(name, startMark, endMark);
      } catch (error) {
        logger.warn(`Failed to measure performance: ${name}`, error);
      }
    }
  },
  getEntries: () => {
    if (typeof window !== 'undefined' && window.performance) {
      return window.performance.getEntries();
    }
    return [];
  },
};

// Analytics
export const analytics = {
  track: (event: string, properties?: Record<string, any>) => {
    logger.info(`Analytics: ${event}`, properties);
    // Integrate with your analytics provider here
  },
  identify: (userId: string, traits?: Record<string, any>) => {
    logger.info(`Analytics: Identify ${userId}`, traits);
    // Integrate with your analytics provider here
  },
  page: (page: string, properties?: Record<string, any>) => {
    logger.info(`Analytics: Page ${page}`, properties);
    // Integrate with your analytics provider here
  },
};

// Export everything as default for convenience
export default {
  // Components
  AgentChat,
  
  // Utilities
  createAgenticChat,
  
  // Plugin system
  AgenticPlugin,
  pluginManager,
  
  // Error handling
  AgenticError,
  
  // Logging
  logger,
  
  // Performance
  performance,
  
  // Analytics
  analytics,
  
  // Constants
  VERSION,
  AUTHOR,
  DEFAULT_AGENTIC_CONFIG,
}; 
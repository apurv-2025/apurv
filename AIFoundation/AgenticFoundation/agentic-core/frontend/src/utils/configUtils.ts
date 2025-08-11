/**
 * Configuration utilities for Agentic Core
 */

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

export interface ModelConfig {
  name: string;
  value: string;
  provider: string;
  maxTokens?: number;
  temperature?: number;
}

export interface ToolConfig {
  name: string;
  enabled: boolean;
  config?: Record<string, any>;
}

/**
 * Create a default Agentic configuration
 */
export function createAgenticConfig(overrides: Partial<AgenticConfig> = {}): AgenticConfig {
  return {
    apiUrl: 'http://localhost:8000',
    userId: 'default_user',
    model: 'gpt-4',
    theme: 'light',
    position: 'bottom-right',
    showQuickActions: true,
    enableHistory: true,
    enableMetrics: true,
    ...overrides
  };
}

/**
 * Validate configuration
 */
export function validateConfig(config: AgenticConfig): { valid: boolean; errors: string[] } {
  const errors: string[] = [];
  
  if (!config.apiUrl) {
    errors.push('API URL is required');
  }
  
  if (!config.userId) {
    errors.push('User ID is required');
  }
  
  if (!config.model) {
    errors.push('Model is required');
  }
  
  if (!['light', 'dark'].includes(config.theme)) {
    errors.push('Theme must be either "light" or "dark"');
  }
  
  if (config.position && !['bottom-right', 'bottom-left', 'top-right', 'top-left'].includes(config.position)) {
    errors.push('Position must be one of: bottom-right, bottom-left, top-right, top-left');
  }
  
  return {
    valid: errors.length === 0,
    errors
  };
}

/**
 * Get supported models
 */
export function getSupportedModels(): ModelConfig[] {
  return [
    { name: 'GPT-4', value: 'gpt-4', provider: 'openai', maxTokens: 8192, temperature: 0.7 },
    { name: 'GPT-3.5 Turbo', value: 'gpt-3.5-turbo', provider: 'openai', maxTokens: 4096, temperature: 0.7 },
    { name: 'Claude 3 Sonnet', value: 'claude-3-sonnet', provider: 'anthropic', maxTokens: 200000, temperature: 0.7 },
    { name: 'Claude 3 Haiku', value: 'claude-3-haiku', provider: 'anthropic', maxTokens: 200000, temperature: 0.7 }
  ];
}

/**
 * Get default tools configuration
 */
export function getDefaultToolsConfig(): ToolConfig[] {
  return [
    { name: 'search', enabled: true },
    { name: 'calculator', enabled: true },
    { name: 'datetime', enabled: true },
    { name: 'weather', enabled: true },
    { name: 'file_read', enabled: false }
  ];
}

/**
 * Merge configurations
 */
export function mergeConfigs(base: AgenticConfig, overrides: Partial<AgenticConfig>): AgenticConfig {
  return {
    ...base,
    ...overrides
  };
}

/**
 * Load configuration from localStorage
 */
export function loadConfigFromStorage(key: string = 'agentic-config'): AgenticConfig | null {
  try {
    const stored = localStorage.getItem(key);
    if (stored) {
      const config = JSON.parse(stored);
      const validation = validateConfig(config);
      if (validation.valid) {
        return config;
      } else {
        console.warn('Invalid stored config:', validation.errors);
        return null;
      }
    }
  } catch (error) {
    console.error('Error loading config from storage:', error);
  }
  return null;
}

/**
 * Save configuration to localStorage
 */
export function saveConfigToStorage(config: AgenticConfig, key: string = 'agentic-config'): boolean {
  try {
    const validation = validateConfig(config);
    if (validation.valid) {
      localStorage.setItem(key, JSON.stringify(config));
      return true;
    } else {
      console.error('Cannot save invalid config:', validation.errors);
      return false;
    }
  } catch (error) {
    console.error('Error saving config to storage:', error);
    return false;
  }
}

/**
 * Get environment-specific configuration
 */
export function getEnvironmentConfig(): Partial<AgenticConfig> {
  const env = process.env.NODE_ENV || 'development';
  
  switch (env) {
    case 'production':
      return {
        apiUrl: process.env.REACT_APP_API_URL || 'https://api.agentic-core.com',
        enableMetrics: true,
        enableHistory: true
      };
    case 'staging':
      return {
        apiUrl: process.env.REACT_APP_API_URL || 'https://staging-api.agentic-core.com',
        enableMetrics: true,
        enableHistory: true
      };
    default:
      return {
        apiUrl: process.env.REACT_APP_API_URL || 'http://localhost:8000',
        enableMetrics: false,
        enableHistory: true
      };
  }
}

/**
 * Create configuration from environment variables
 */
export function createConfigFromEnv(): AgenticConfig {
  const envConfig = getEnvironmentConfig();
  
  return createAgenticConfig({
    apiUrl: envConfig.apiUrl,
    userId: process.env.REACT_APP_USER_ID || 'default_user',
    model: process.env.REACT_APP_MODEL || 'gpt-4',
    theme: (process.env.REACT_APP_THEME as 'light' | 'dark') || 'light',
    position: (process.env.REACT_APP_POSITION as any) || 'bottom-right',
    showQuickActions: process.env.REACT_APP_SHOW_QUICK_ACTIONS !== 'false',
    enableHistory: envConfig.enableHistory !== false,
    enableMetrics: envConfig.enableMetrics !== false
  });
}

/**
 * Get configuration for specific use case
 */
export function getUseCaseConfig(useCase: string): Partial<AgenticConfig> {
  switch (useCase) {
    case 'claims-processing':
      return {
        showQuickActions: true,
        enableHistory: true,
        enableMetrics: true,
        position: 'bottom-right'
      };
    case 'customer-support':
      return {
        showQuickActions: false,
        enableHistory: true,
        enableMetrics: true,
        position: 'bottom-right'
      };
    case 'development':
      return {
        showQuickActions: true,
        enableHistory: true,
        enableMetrics: false,
        position: 'bottom-right'
      };
    default:
      return {};
  }
} 
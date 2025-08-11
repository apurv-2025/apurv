/**
 * Validation utilities for Agentic Core
 */

export interface ValidationResult {
  valid: boolean;
  errors: string[];
  warnings: string[];
}

/**
 * Validate a message before sending
 */
export function validateMessage(message: string): ValidationResult {
  const errors: string[] = [];
  const warnings: string[] = [];
  
  if (!message || message.trim().length === 0) {
    errors.push('Message cannot be empty');
  }
  
  if (message.length > 4000) {
    errors.push('Message is too long (maximum 4000 characters)');
  }
  
  if (message.length > 2000) {
    warnings.push('Message is quite long, consider breaking it into smaller parts');
  }
  
  // Check for potentially harmful content
  const harmfulPatterns = [
    /<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi,
    /javascript:/gi,
    /on\w+\s*=/gi,
    /<iframe\b[^<]*(?:(?!<\/iframe>)<[^<]*)*<\/iframe>/gi
  ];
  
  for (const pattern of harmfulPatterns) {
    if (pattern.test(message)) {
      errors.push('Message contains potentially harmful content');
      break;
    }
  }
  
  return {
    valid: errors.length === 0,
    errors,
    warnings
  };
}

/**
 * Validate user ID
 */
export function validateUserId(userId: string): ValidationResult {
  const errors: string[] = [];
  const warnings: string[] = [];
  
  if (!userId || userId.trim().length === 0) {
    errors.push('User ID cannot be empty');
  }
  
  if (userId.length > 100) {
    errors.push('User ID is too long (maximum 100 characters)');
  }
  
  if (!/^[a-zA-Z0-9_-]+$/.test(userId)) {
    warnings.push('User ID contains special characters, consider using only alphanumeric characters, hyphens, and underscores');
  }
  
  return {
    valid: errors.length === 0,
    errors,
    warnings
  };
}

/**
 * Validate API URL
 */
export function validateApiUrl(url: string): ValidationResult {
  const errors: string[] = [];
  const warnings: string[] = [];
  
  if (!url || url.trim().length === 0) {
    errors.push('API URL cannot be empty');
  }
  
  try {
    const urlObj = new URL(url);
    if (!['http:', 'https:'].includes(urlObj.protocol)) {
      errors.push('API URL must use HTTP or HTTPS protocol');
    }
  } catch {
    errors.push('API URL is not valid');
  }
  
  if (url.includes('localhost') || url.includes('127.0.0.1')) {
    warnings.push('Using localhost URL - make sure the API server is running');
  }
  
  return {
    valid: errors.length === 0,
    errors,
    warnings
  };
}

/**
 * Validate model name
 */
export function validateModel(model: string): ValidationResult {
  const errors: string[] = [];
  const warnings: string[] = [];
  
  if (!model || model.trim().length === 0) {
    errors.push('Model name cannot be empty');
  }
  
  const supportedModels = [
    'gpt-4',
    'gpt-3.5-turbo',
    'claude-3-sonnet',
    'claude-3-haiku',
    'mock-model'
  ];
  
  if (!supportedModels.includes(model)) {
    warnings.push(`Model "${model}" may not be supported by the current API`);
  }
  
  return {
    valid: errors.length === 0,
    errors,
    warnings
  };
}

/**
 * Validate configuration object
 */
export function validateConfig(config: Record<string, any>): ValidationResult {
  const errors: string[] = [];
  const warnings: string[] = [];
  
  // Check required fields
  const requiredFields = ['apiUrl', 'userId', 'model'];
  for (const field of requiredFields) {
    if (!config[field]) {
      errors.push(`Required field "${field}" is missing`);
    }
  }
  
  // Validate individual fields
  if (config.apiUrl) {
    const urlValidation = validateApiUrl(config.apiUrl);
    errors.push(...urlValidation.errors);
    warnings.push(...urlValidation.warnings);
  }
  
  if (config.userId) {
    const userIdValidation = validateUserId(config.userId);
    errors.push(...userIdValidation.errors);
    warnings.push(...userIdValidation.warnings);
  }
  
  if (config.model) {
    const modelValidation = validateModel(config.model);
    errors.push(...modelValidation.errors);
    warnings.push(...modelValidation.warnings);
  }
  
  // Validate theme
  if (config.theme && !['light', 'dark'].includes(config.theme)) {
    errors.push('Theme must be either "light" or "dark"');
  }
  
  // Validate position
  if (config.position && !['bottom-right', 'bottom-left', 'top-right', 'top-left'].includes(config.position)) {
    errors.push('Position must be one of: bottom-right, bottom-left, top-right, top-left');
  }
  
  return {
    valid: errors.length === 0,
    errors,
    warnings
  };
}

/**
 * Validate task data
 */
export function validateTaskData(taskData: Record<string, any>): ValidationResult {
  const errors: string[] = [];
  const warnings: string[] = [];
  
  if (!taskData.taskType) {
    errors.push('Task type is required');
  }
  
  if (!taskData.taskDescription) {
    errors.push('Task description is required');
  }
  
  if (taskData.taskDescription && taskData.taskDescription.length > 1000) {
    errors.push('Task description is too long (maximum 1000 characters)');
  }
  
  if (taskData.context && typeof taskData.context !== 'object') {
    errors.push('Context must be an object');
  }
  
  return {
    valid: errors.length === 0,
    errors,
    warnings
  };
}

/**
 * Sanitize input for safe processing
 */
export function sanitizeInput(input: string): string {
  return input
    .trim()
    .replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '')
    .replace(/<iframe\b[^<]*(?:(?!<\/iframe>)<[^<]*)*<\/iframe>/gi, '')
    .replace(/javascript:/gi, '')
    .replace(/on\w+\s*=/gi, '');
}

/**
 * Validate email format
 */
export function validateEmail(email: string): ValidationResult {
  const errors: string[] = [];
  const warnings: string[] = [];
  
  if (!email || email.trim().length === 0) {
    errors.push('Email cannot be empty');
  }
  
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(email)) {
    errors.push('Email format is not valid');
  }
  
  if (email.length > 254) {
    errors.push('Email is too long');
  }
  
  return {
    valid: errors.length === 0,
    errors,
    warnings
  };
}

/**
 * Validate file upload
 */
export function validateFileUpload(file: File, maxSize: number = 10 * 1024 * 1024, allowedTypes: string[] = ['txt', 'pdf', 'doc', 'docx', 'csv', 'json']): ValidationResult {
  const errors: string[] = [];
  const warnings: string[] = [];
  
  if (!file) {
    errors.push('File is required');
  }
  
  if (file && file.size > maxSize) {
    errors.push(`File size exceeds maximum allowed size of ${Math.round(maxSize / 1024 / 1024)}MB`);
  }
  
  if (file) {
    const extension = file.name.split('.').pop()?.toLowerCase();
    if (extension && !allowedTypes.includes(extension)) {
      errors.push(`File type "${extension}" is not allowed. Allowed types: ${allowedTypes.join(', ')}`);
    }
  }
  
  return {
    valid: errors.length === 0,
    errors,
    warnings
  };
} 
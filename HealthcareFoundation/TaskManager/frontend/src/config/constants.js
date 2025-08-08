// src/config/constants.js
export const PRIORITY_LEVELS = {
  NONE: 'none',
  LOW: 'low',
  MEDIUM: 'medium',
  HIGH: 'high',
  URGENT: 'urgent'
};

export const TASK_STATUS = {
  TODO: 'todo',
  IN_PROGRESS: 'in_progress',
  COMPLETED: 'completed',
  CANCELLED: 'cancelled'
};

export const PRIORITY_COLORS = {
  [PRIORITY_LEVELS.NONE]: 'priority-none',
  [PRIORITY_LEVELS.LOW]: 'priority-low',
  [PRIORITY_LEVELS.MEDIUM]: 'priority-medium',
  [PRIORITY_LEVELS.HIGH]: 'priority-high',
  [PRIORITY_LEVELS.URGENT]: 'priority-urgent'
};

export const STATUS_COLORS = {
  [TASK_STATUS.TODO]: 'status-todo',
  [TASK_STATUS.IN_PROGRESS]: 'status-in-progress',
  [TASK_STATUS.COMPLETED]: 'status-completed',
  [TASK_STATUS.CANCELLED]: 'status-cancelled'
};

export const DATE_FORMATS = {
  DISPLAY: 'MMM dd, yyyy',
  INPUT: 'yyyy-MM-dd',
  TIME: 'HH:mm',
  DATETIME: 'MMM dd, yyyy HH:mm'
};

export const FILE_CONSTRAINTS = {
  MAX_SIZE: 50 * 1024 * 1024, // 50MB
  MAX_COUNT: 20,
  ALLOWED_TYPES: [
    'image/jpeg',
    'image/png',
    'image/gif',
    'application/pdf',
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'text/plain'
  ]
};

// frontend/src/utils/constants.js
export const APPOINTMENT_STATUSES = {
  SCHEDULED: 'scheduled',
  COMPLETED: 'completed',
  CANCELLED: 'cancelled',
  RESCHEDULED: 'rescheduled'
};

export const LAB_RESULT_STATUSES = {
  NORMAL: 'Normal',
  ABNORMAL: 'Abnormal',
  CRITICAL: 'Critical',
  PENDING: 'Pending'
};

export const MESSAGE_STATUS = {
  READ: true,
  UNREAD: false
};

export const API_ENDPOINTS = {
  AUTH: {
    LOGIN: '/auth/login',
    REGISTER: '/auth/register',
    ME: '/users/me'
  },
  APPOINTMENTS: '/appointments',
  MEDICATIONS: '/medications',
  LAB_RESULTS: '/lab-results',
  MESSAGES: '/messages'
};

export const API_BASE_URL = 'http://127.0.0.1:8000';

export const NOTE_TYPES = {
  SOAP: 'SOAP',
  DAP: 'DAP', 
  BIRP: 'BIRP',
  PAIP: 'PAIP'
};

export const USER_ROLES = {
  ADMIN: 'admin',
  THERAPIST: 'therapist',
  CLINICIAN: 'clinician'
};

export const DEMO_CREDENTIALS = {
  email: 'admin@clinic.com',
  password: 'admin123'
};



export const NOTE_FILTERS = {
  SEARCH_QUERY: 'search_query',
  NOTE_TYPE: 'note_type',
  IS_DRAFT: 'is_draft',
  IS_SIGNED: 'is_signed',
  DATE_FROM: 'date_from',
  DATE_TO: 'date_to',
  PATIENT_ID: 'patient_id',
  PAGE: 'page',
  PAGE_SIZE: 'page_size'
};

export const SORT_FIELDS = {
  SESSION_DATE: 'session_date',
  PATIENT_NAME: 'patient_name',
  NOTE_TYPE: 'note_type',
  CREATED_AT: 'created_at'
};

export const VIEW_MODES = {
  LIST: 'list',
  GRID: 'grid'
};

export const AUDIT_ACTIONS = {
  CREATE: 'create',
  UPDATE: 'update',
  READ: 'read',
  SIGN: 'sign',
  UNLOCK: 'unlock',
  DELETE: 'delete'
};

export const NOTIFICATION_TYPES = {
  SUCCESS: 'success',
  ERROR: 'error',
  WARNING: 'warning',
  INFO: 'info'
};

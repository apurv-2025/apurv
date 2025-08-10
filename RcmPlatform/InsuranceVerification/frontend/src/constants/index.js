// File: src/constants/index.js
export const API_ENDPOINTS = {
  UPLOAD_CARD: '/api/upload-insurance-card',
  ELIGIBILITY_INQUIRY: '/api/eligibility-inquiry',
  ELIGIBILITY_RESPONSE: '/api/eligibility-response',
  INSURANCE_CARDS: '/api/insurance-cards',
  HEALTH_CHECK: '/'
};

export const SERVICE_TYPES = [
  { value: '30', label: 'Health Benefit Plan Coverage' },
  { value: '1', label: 'Medical Care' },
  { value: '88', label: 'Pharmacy' },
  { value: '98', label: 'Professional Services' },
  { value: '2', label: 'Surgical' },
  { value: '3', label: 'Consultation' },
  { value: '4', label: 'Diagnostic X-Ray' },
  { value: '5', label: 'Diagnostic Lab' },
  { value: '6', label: 'Radiation Therapy' },
  { value: '7', label: 'Anesthesia' },
  { value: '8', label: 'Surgical Assistance' },
  { value: '9', label: 'Other Medical' },
  { value: '10', label: 'Blood Charges' }
];

export const REQUEST_STATUS = {
  SUBMITTED: 'submitted',
  PROCESSING: 'processing',
  COMPLETED: 'completed',
  ERROR: 'error'
};

export const FILE_TYPES = {
  ALLOWED_TYPES: ['image/jpeg', 'image/png', 'image/tiff', 'application/pdf'],
  MAX_SIZE: 10 * 1024 * 1024, // 10MB
  EXTENSIONS: ['.jpg', '.jpeg', '.png', '.tiff', '.tif', '.pdf']
};

export const TOAST_DURATION = {
  SHORT: 3000,
  MEDIUM: 5000,
  LONG: 8000
};

// Status configurations
export const STATUS_CONFIG = {
  validated: { color: 'bg-green-100 text-green-800', icon: 'CheckCircle' },
  sent: { color: 'bg-blue-100 text-blue-800', icon: 'Clock' },
  paid: { color: 'bg-emerald-100 text-emerald-800', icon: 'DollarSign' },
  rejected: { color: 'bg-red-100 text-red-800', icon: 'XCircle' },
  queued: { color: 'bg-yellow-100 text-yellow-800', icon: 'Clock' },
  default: { color: 'bg-gray-100 text-gray-800', icon: 'Activity' }
};

// Claim type configurations
export const CLAIM_TYPE_CONFIG = {
  '837D': { color: 'bg-purple-100 text-purple-800', icon: 'Heart', label: 'Dental' },
  '837P': { color: 'bg-blue-100 text-blue-800', icon: 'Stethoscope', label: 'Professional' },
  '837I': { color: 'bg-orange-100 text-orange-800', icon: 'Building', label: 'Institutional' },
  default: { color: 'bg-gray-100 text-gray-800', icon: 'FileText', label: 'Unknown' }
};

// Available payers
export const PAYERS = [
  { id: '1', name: 'Delta Dental' },
  { id: '2', name: 'Blue Cross Blue Shield' },
  { id: '3', name: 'Medicare' },
  { id: '4', name: 'Cigna' },
  { id: '5', name: 'MetLife' }
];

// Navigation tabs
export const NAVIGATION_TABS = [
  { id: 'dashboard', label: 'Dashboard', icon: 'Activity' },
  { id: 'claims', label: 'Claims', icon: 'FileText' },
  { id: 'upload', label: 'Upload', icon: 'Upload' },
  { id: 'analytics', label: 'Analytics', icon: 'BarChart3' },
  { id: 'agent', label: 'AI Assistant', icon: 'Bot' }
];

// File upload settings
export const UPLOAD_CONFIG = {
  maxFileSize: 10 * 1024 * 1024, // 10MB
  acceptedExtensions: ['.edi', '.txt', '.x12'],
  acceptedMimeTypes: 'text/plain,application/x-edi,application/x-x12'
};

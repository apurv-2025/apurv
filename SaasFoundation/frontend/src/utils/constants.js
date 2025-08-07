// src/utils/constants.js (Complete version)
export const API_ENDPOINTS = {
  AUTH: {
    LOGIN: '/api/v1/auth/login',
    LOGOUT: '/api/v1/auth/logout',
    
    REGISTER: '/api/v1/auth/register',
    VERIFY_EMAIL: '/api/v1/auth/verify',
    
    RESEND_VERIFICATION: '/api/v1/auth/resend-verification',
    REFRESH: '/api/v1/auth/refresh',


    DELETE_ACCOUNT: '/api/v1/user/delete-account',
    FORGOT_PASSWORD: '/api/v1/user/forgot-password',
    RESET_PASSWORD: '/api/v1/user/reset-password',
    CHANGE_PASSWORD: '/api/v1/user/change-password',
  
    PROFILE: '/api/v1/user/profile',
  
    ENABLE_2FA: '/api/v1/user/2fa/enable',
    DISABLE_2FA: '/api/v1/user/2fa/disable',
    VERIFY_2FA: '/api/v1/user/2fa/verify'
    
  },
  USER: {
    PROFILE: '/api/v1/user/profile',
    PREFERENCES: '/api/v1/user/preferences',
    PASSWORD: '/api/v1/user/change-password',
    EXPORT: '/api/v1/user/export',
    DELETE: '/api/v1/user/account'
  },
  
  SUBSCRIPTIONS: {
    CURRENT: '/api/v1/subscriptions/current',
    CREATE: '/api/v1/subscriptions/subscriptions',
    UPDATE: `/api/v1/subscriptions`,
    CANCEL: `/api/v1/subscriptions`
  },
  PRICING: {
    PLANS: '/api/v1/pricing/plans',
    DETAIL: '/api/v1/pricing/plans/${id}/details'
  },
  ORGANIZATIONS: {
    CURRENT: '/api/v1/organizations/current',
    MEMBERS: '/api/v1/organizations/current/members',
    INVITATIONS: '/api/v1/organizations/current/invitations',
    INVITE: '/api/v1/organizations/current/invite',
    UPDATE: '/api/v1/organizations/current'
  },
  INVITATIONS: {
    DETAILS: (token) => `/api/v1/organizations/invitations/${token}`,
    ACCEPT: (token) => `/api/v1/organizations/invitations/${token}/accept`,
    RESEND: (id) => `/api/v1/organizations/current/invitations/${id}/resend`,
    CANCEL: (id) => `/api/v1/organizations/current/invitations/${id}`
  },
  INVOICES: {
    LIST: '/api/v1/invoices',
    DETAILS: (id) => `/api/v1/invoices/${id}`,
    PAY: (id) => `/api/v1/invoices/${id}/pay`,
    DOWNLOAD: (id) => `/api/v1/invoices/${id}/download`
  },
  PAYMENT_METHODS: {
    LIST: '/api/v1/payment-methods',
    CREATE: '/api/v1/payment-methods',
    UPDATE: (id) => `/api/v1/payment-methods/${id}`,
    DELETE: (id) => `/api/v1/payment-methods/${id}`,
    SET_DEFAULT: (id) => `/api/v1/payment-methods/${id}/default`
  }
};

export const ROLES = {
  // Management Roles
  OWNER: 'owner',
  ADMIN: 'admin',
  REVENUE_CYCLE_MANAGER: 'Revenue Cycle Manager',
  COMPLIANCE_OFFICER: 'Compliance Officer',
  RCM_ANALYST: 'RCM Analyst',
  RCM_SYSTEMS_ANALYST: 'RCM Systems Analyst',
  PRACTICE_MANAGER: 'Practice Manager',
  
  // Specialist Roles
  INSURANCE_VERIFICATION_SPECIALIST: 'Insurance Verification Specialist',
  PRE_AUTHORIZATION_SPECIALIST: 'Pre-Authorization Specialist',
  FINANCIAL_COUNSELOR: 'Financial Counselor',
  REGISTRATION_CLERK: 'Registration Clerk',
  MEDICAL_CODER: 'Medical Coder',
  CLINICAL_DOCUMENTATION_SPECIALIST: 'Clinical Documentation Specialist',
  CHARGE_ENTRY_SPECIALIST: 'Charge Entry Specialist',
  BILLING_SPECIALIST: 'Billing Specialist / Medical Biller',
  ACCOUNTS_RECEIVABLE_SPECIALIST: 'Accounts Receivable (A/R) Specialist',
  PAYMENT_POSTER: 'Payment Poster',
  DENIALS_MANAGEMENT_SPECIALIST: 'Denials Management Specialist',
  PATIENT_COLLECTIONS_REPRESENTATIVE: 'Patient Collections Representative',
  SCHEDULER: 'Scheduler',
  HEALTH_INFORMATION_TECHNICIAN: 'Health Information Technician',
  
  // Legacy role for backward compatibility
  MEMBER: 'member'
};

// Management roles that have administrative privileges
export const MANAGEMENT_ROLES = [
  ROLES.OWNER,
  ROLES.ADMIN,
  ROLES.REVENUE_CYCLE_MANAGER,
  ROLES.COMPLIANCE_OFFICER,
  ROLES.RCM_ANALYST,
  ROLES.RCM_SYSTEMS_ANALYST,
  ROLES.PRACTICE_MANAGER
];

// Helper function to check if a role has management privileges
export const isManagementRole = (role) => {
  return MANAGEMENT_ROLES.includes(role);
};

export const SUBSCRIPTION_STATUS = {
  ACTIVE: 'active',
  CANCELLED: 'cancelled',
  PENDING: 'pending',
  PAST_DUE: 'past_due',
  TRIALING: 'trialing',
  INCOMPLETE: 'incomplete'
};

export const BILLING_CYCLES = {
  MONTHLY: 'monthly',
  YEARLY: 'yearly'
};

export const PLAN_NAMES = {
  FREE: 'free',
  STARTER: 'starter',
  PROFESSIONAL: 'professional',
  ENTERPRISE: 'enterprise'
};

export const INVOICE_STATUS = {
  DRAFT: 'draft',
  OPEN: 'open',
  PAID: 'paid',
  UNCOLLECTIBLE: 'uncollectible',
  VOID: 'void'
};

export const NOTIFICATION_TYPES = {
  SUCCESS: 'success',
  ERROR: 'error',
  WARNING: 'warning',
  INFO: 'info'
};

export const BREAKPOINTS = {
  SM: 640,
  MD: 768,
  LG: 1024,
  XL: 1280,
  '2XL': 1536
};

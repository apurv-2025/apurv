// src/components/team/RoleSelect.jsx
import React from 'react';
import Select from '../ui/Select';
import { cn } from '../../utils/helpers';
import { ROLES, MANAGEMENT_ROLES, isManagementRole } from '../../utils/constants';

const RoleSelect = ({ 
  value, 
  onChange, 
  currentUserRole, 
  disabled = false,
  size = 'md',
  includeDescriptions = false,
  className 
}) => {
  // Define available roles based on current user's role
  const getAvailableRoles = () => {
    const allRoles = [
      // Management Roles
      { 
        value: ROLES.OWNER, 
        label: 'Owner',
        description: 'Full access including billing and organization management',
        category: 'Management'
      },
      { 
        value: ROLES.ADMIN, 
        label: 'Admin',
        description: 'Can manage team members and settings',
        category: 'Management'
      },
      { 
        value: ROLES.REVENUE_CYCLE_MANAGER, 
        label: 'Revenue Cycle Manager',
        description: 'Manages revenue cycle operations and team',
        category: 'Management'
      },
      { 
        value: ROLES.COMPLIANCE_OFFICER, 
        label: 'Compliance Officer',
        description: 'Ensures regulatory compliance and policies',
        category: 'Management'
      },
      { 
        value: ROLES.RCM_ANALYST, 
        label: 'RCM Analyst',
        description: 'Analyzes revenue cycle data and performance',
        category: 'Management'
      },
      { 
        value: ROLES.RCM_SYSTEMS_ANALYST, 
        label: 'RCM Systems Analyst',
        description: 'Manages RCM systems and technical processes',
        category: 'Management'
      },
      { 
        value: ROLES.PRACTICE_MANAGER, 
        label: 'Practice Manager',
        description: 'Manages practice operations and staff',
        category: 'Management'
      },
      
      // Specialist Roles
      { 
        value: ROLES.INSURANCE_VERIFICATION_SPECIALIST, 
        label: 'Insurance Verification Specialist',
        description: 'Verifies insurance coverage and benefits',
        category: 'Specialist'
      },
      { 
        value: ROLES.PRE_AUTHORIZATION_SPECIALIST, 
        label: 'Pre-Authorization Specialist',
        description: 'Obtains pre-authorizations for procedures',
        category: 'Specialist'
      },
      { 
        value: ROLES.FINANCIAL_COUNSELOR, 
        label: 'Financial Counselor',
        description: 'Provides financial guidance to patients',
        category: 'Specialist'
      },
      { 
        value: ROLES.REGISTRATION_CLERK, 
        label: 'Registration Clerk',
        description: 'Handles patient registration and check-in',
        category: 'Specialist'
      },
      { 
        value: ROLES.MEDICAL_CODER, 
        label: 'Medical Coder',
        description: 'Assigns medical codes for billing',
        category: 'Specialist'
      },
      { 
        value: ROLES.CLINICAL_DOCUMENTATION_SPECIALIST, 
        label: 'Clinical Documentation Specialist',
        description: 'Ensures accurate clinical documentation',
        category: 'Specialist'
      },
      { 
        value: ROLES.CHARGE_ENTRY_SPECIALIST, 
        label: 'Charge Entry Specialist',
        description: 'Enters charges for services provided',
        category: 'Specialist'
      },
      { 
        value: ROLES.BILLING_SPECIALIST, 
        label: 'Billing Specialist / Medical Biller',
        description: 'Processes medical bills and claims',
        category: 'Specialist'
      },
      { 
        value: ROLES.ACCOUNTS_RECEIVABLE_SPECIALIST, 
        label: 'Accounts Receivable (A/R) Specialist',
        description: 'Manages accounts receivable and collections',
        category: 'Specialist'
      },
      { 
        value: ROLES.PAYMENT_POSTER, 
        label: 'Payment Poster',
        description: 'Posts payments and adjustments',
        category: 'Specialist'
      },
      { 
        value: ROLES.DENIALS_MANAGEMENT_SPECIALIST, 
        label: 'Denials Management Specialist',
        description: 'Manages claim denials and appeals',
        category: 'Specialist'
      },
      { 
        value: ROLES.PATIENT_COLLECTIONS_REPRESENTATIVE, 
        label: 'Patient Collections Representative',
        description: 'Handles patient payment collections',
        category: 'Specialist'
      },
      { 
        value: ROLES.SCHEDULER, 
        label: 'Scheduler',
        description: 'Manages patient appointments and scheduling',
        category: 'Specialist'
      },
      { 
        value: ROLES.HEALTH_INFORMATION_TECHNICIAN, 
        label: 'Health Information Technician',
        description: 'Manages health records and information systems',
        category: 'Specialist'
      },
      
      // Legacy role
      { 
        value: ROLES.MEMBER, 
        label: 'Member',
        description: 'Can access and use platform features',
        category: 'Legacy'
      }
    ];

    // Filter roles based on current user's permissions
    let availableRoles = [];
    
    // Only owners can assign owner role
    if (currentUserRole === ROLES.OWNER) {
      availableRoles = allRoles; // Owners can assign any role
    } else if (isManagementRole(currentUserRole)) {
      // Management roles can assign specialist and member roles, but not owner
      availableRoles = allRoles.filter(role => role.value !== ROLES.OWNER);
    } else {
      // Regular members can only assign member role
      availableRoles = allRoles.filter(role => role.value === ROLES.MEMBER);
    }

    return availableRoles;
  };

  const availableRoles = getAvailableRoles();

  const sizeClasses = {
    sm: 'text-sm py-1 px-2',
    md: 'text-sm py-2 px-3',
    lg: 'text-base py-2 px-4'
  };

  return (
    <div className={className}>
      <Select
        value={value}
        onChange={onChange}
        disabled={disabled}
        className={cn(sizeClasses[size])}
      >
        <option value="">Select a role...</option>
        {availableRoles.map(role => (
          <option key={role.value} value={role.value}>
            {role.label}
            {includeDescriptions && ` - ${role.description}`}
          </option>
        ))}
      </Select>
    </div>
  );
};

// Role Badge Component
const RoleBadge = ({ role, className }) => {
  const getRoleConfig = (role) => {
    // Management Roles
    if (role === ROLES.OWNER) {
      return { emoji: '👑', variant: 'warning', label: 'Owner' };
    }
    if (role === ROLES.ADMIN) {
      return { emoji: '🛡️', variant: 'info', label: 'Admin' };
    }
    if (role === ROLES.REVENUE_CYCLE_MANAGER) {
      return { emoji: '📊', variant: 'info', label: 'Revenue Cycle Manager' };
    }
    if (role === ROLES.COMPLIANCE_OFFICER) {
      return { emoji: '⚖️', variant: 'info', label: 'Compliance Officer' };
    }
    if (role === ROLES.RCM_ANALYST) {
      return { emoji: '📈', variant: 'info', label: 'RCM Analyst' };
    }
    if (role === ROLES.RCM_SYSTEMS_ANALYST) {
      return { emoji: '💻', variant: 'info', label: 'RCM Systems Analyst' };
    }
    if (role === ROLES.PRACTICE_MANAGER) {
      return { emoji: '🏢', variant: 'info', label: 'Practice Manager' };
    }
    
    // Specialist Roles
    if (role === ROLES.INSURANCE_VERIFICATION_SPECIALIST) {
      return { emoji: '🏥', variant: 'success', label: 'Insurance Verification Specialist' };
    }
    if (role === ROLES.PRE_AUTHORIZATION_SPECIALIST) {
      return { emoji: '✅', variant: 'success', label: 'Pre-Authorization Specialist' };
    }
    if (role === ROLES.FINANCIAL_COUNSELOR) {
      return { emoji: '💰', variant: 'success', label: 'Financial Counselor' };
    }
    if (role === ROLES.REGISTRATION_CLERK) {
      return { emoji: '📝', variant: 'success', label: 'Registration Clerk' };
    }
    if (role === ROLES.MEDICAL_CODER) {
      return { emoji: '🏷️', variant: 'success', label: 'Medical Coder' };
    }
    if (role === ROLES.CLINICAL_DOCUMENTATION_SPECIALIST) {
      return { emoji: '📋', variant: 'success', label: 'Clinical Documentation Specialist' };
    }
    if (role === ROLES.CHARGE_ENTRY_SPECIALIST) {
      return { emoji: '💳', variant: 'success', label: 'Charge Entry Specialist' };
    }
    if (role === ROLES.BILLING_SPECIALIST) {
      return { emoji: '🧾', variant: 'success', label: 'Billing Specialist' };
    }
    if (role === ROLES.ACCOUNTS_RECEIVABLE_SPECIALIST) {
      return { emoji: '📊', variant: 'success', label: 'A/R Specialist' };
    }
    if (role === ROLES.PAYMENT_POSTER) {
      return { emoji: '📥', variant: 'success', label: 'Payment Poster' };
    }
    if (role === ROLES.DENIALS_MANAGEMENT_SPECIALIST) {
      return { emoji: '🚫', variant: 'success', label: 'Denials Management Specialist' };
    }
    if (role === ROLES.PATIENT_COLLECTIONS_REPRESENTATIVE) {
      return { emoji: '📞', variant: 'success', label: 'Patient Collections Representative' };
    }
    if (role === ROLES.SCHEDULER) {
      return { emoji: '📅', variant: 'success', label: 'Scheduler' };
    }
    if (role === ROLES.HEALTH_INFORMATION_TECHNICIAN) {
      return { emoji: '📋', variant: 'success', label: 'Health Information Technician' };
    }
    
    // Legacy role
    if (role === ROLES.MEMBER) {
      return { emoji: '👤', variant: 'secondary', label: 'Member' };
    }
    
    // Default fallback
    return {
      emoji: '👤',
      variant: 'secondary',
      label: role?.charAt(0).toUpperCase() + role?.slice(1) || 'Unknown'
    };
  };

  const config = getRoleConfig(role);

  return (
    <span className={cn("inline-flex items-center", className)}>
      <span className="mr-1">{config.emoji}</span>
      <span className={cn(
        "px-2 py-1 text-xs font-medium rounded-full",
        config.variant === 'warning' && "bg-yellow-100 text-yellow-800",
        config.variant === 'info' && "bg-blue-100 text-blue-800",
        config.variant === 'success' && "bg-green-100 text-green-800",
        config.variant === 'secondary' && "bg-gray-100 text-gray-800"
      )}>
        {config.label.toUpperCase()}
      </span>
    </span>
  );
};

export default RoleSelect;
export { RoleBadge };

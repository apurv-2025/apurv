// src/components/team/RoleSelect.jsx
import React from 'react';
import Select from '../ui/Select';
import { cn } from '../../utils/helpers';

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
    const baseRoles = [
      { 
        value: 'member', 
        label: 'Member',
        description: 'Can access and use platform features'
      },
      { 
        value: 'admin', 
        label: 'Admin',
        description: 'Can manage team members and settings'
      }
    ];

    // Only owners can assign owner role
    if (currentUserRole === 'owner') {
      baseRoles.push({
        value: 'owner',
        label: 'Owner',
        description: 'Full access including billing and organization management'
      });
    }

    return baseRoles;
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
    switch (role) {
      case 'owner':
        return {
          emoji: '👑',
          variant: 'warning',
          label: 'Owner'
        };
      case 'admin':
        return {
          emoji: '🛡️',
          variant: 'info',
          label: 'Admin'
        };
      case 'member':
        return {
          emoji: '👤',
          variant: 'secondary',
          label: 'Member'
        };
      default:
        return {
          emoji: '👤',
          variant: 'secondary',
          label: role?.charAt(0).toUpperCase() + role?.slice(1) || 'Unknown'
        };
    }
  };

  const config = getRoleConfig(role);

  return (
    <span className={cn("inline-flex items-center", className)}>
      <span className="mr-1">{config.emoji}</span>
      <span className={cn(
        "px-2 py-1 text-xs font-medium rounded-full",
        config.variant === 'warning' && "bg-yellow-100 text-yellow-800",
        config.variant === 'info' && "bg-blue-100 text-blue-800",
        config.variant === 'secondary' && "bg-gray-100 text-gray-800"
      )}>
        {config.label.toUpperCase()}
      </span>
    </span>
  );
};

export default RoleSelect;
export { RoleBadge };

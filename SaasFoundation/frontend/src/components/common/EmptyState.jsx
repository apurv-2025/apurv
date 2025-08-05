import React from 'react';
import { Button } from '../ui';

const EmptyState = ({
  icon: Icon,
  title,
  description,
  actionLabel,
  onAction,
  className = '',
  variant = 'default'
}) => {
  const getVariantStyles = () => {
    switch (variant) {
      case 'minimal':
        return 'py-8';
      case 'large':
        return 'py-16';
      default:
        return 'py-12';
    }
  };

  const getIconSize = () => {
    switch (variant) {
      case 'minimal':
        return 'w-8 h-8';
      case 'large':
        return 'w-16 h-16';
      default:
        return 'w-12 h-12';
    }
  };

  return (
    <div className={`flex flex-col items-center justify-center text-center ${getVariantStyles()} ${className}`}>
      {Icon && (
        <div className="mb-4">
          <Icon className={`${getIconSize()} text-gray-400 mx-auto`} />
        </div>
      )}
      
      {title && (
        <h3 className="text-lg font-semibold text-gray-900 mb-2">
          {title}
        </h3>
      )}
      
      {description && (
        <p className="text-gray-500 mb-6 max-w-md">
          {description}
        </p>
      )}
      
      {actionLabel && onAction && (
        <Button 
          onClick={onAction}
          variant="primary"
          className="mt-2"
        >
          {actionLabel}
        </Button>
      )}
    </div>
  );
};

// Common empty state configurations for different contexts
export const EmptyStates = {
  // Dashboard related
  noData: {
    title: "No data available",
    description: "There's no data to display at the moment. Check back later or refresh the page."
  },
  
  // Team management
  noTeamMembers: {
    title: "No team members yet",
    description: "Start building your team by inviting members to collaborate on your projects.",
    actionLabel: "Invite Members"
  },
  
  // Subscription/Billing
  noInvoices: {
    title: "No invoices found",
    description: "You don't have any invoices yet. Invoices will appear here after your first billing cycle."
  },
  
  // General search/filter results
  noResults: {
    title: "No results found",
    description: "Try adjusting your search criteria or filters to find what you're looking for."
  },
  
  // Activity/Usage
  noActivity: {
    title: "No recent activity",
    description: "Your recent activity will appear here once you start using the platform."
  },
  
  // Invitations
  noInvitations: {
    title: "No pending invitations",
    description: "You don't have any pending team invitations at the moment."
  }
};

export default EmptyState;

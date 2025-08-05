// src/components/dashboard/QuickActions.jsx
import React from 'react';
import { Link } from 'react-router-dom';
import DashboardCard from './DashboardCard';
import { 
  CreditCardIcon, 
  ChartBarIcon, 
  Cog6ToothIcon, 
  ChatBubbleLeftRightIcon 
} from '@heroicons/react/24/outline';

const QuickActions = () => {
  const actions = [
    {
      to: '/subscription',
      icon: CreditCardIcon,
      label: 'Manage Subscription',
      emoji: '💳'
    },
    {
      to: '/assistants',
      icon: CreditCardIcon,
      label: 'Manage AI Assistants',
      emoji: '💳'
    },
    {
      href: '#',
      icon: ChatBubbleLeftRightIcon,
      label: 'Applications',
      emoji: '💳'
    },  
    {
      to: '/apar',
      icon: CreditCardIcon,
      label: 'Manage Practice Finance',
      emoji: '💳'
    },
    {
      to: '/apar',
      icon: CreditCardIcon,
      label: 'Manage Practice Marketing',
      emoji: '💳'
    },
    {
      href: '#',
      icon: ChatBubbleLeftRightIcon,
      label: 'Analytics',
      emoji: '💬'
    },  
    {
      href: '#',
      icon: ChatBubbleLeftRightIcon,
      label: 'Integrations',
      emoji: '💬'
    },  
    {
      href: '#',
      icon: ChatBubbleLeftRightIcon,
      label: 'Support',
      emoji: '💬'
    }
  ];

  return (
    <DashboardCard title="Quick Actions">
      <div className="grid grid-cols-2 gap-4">
        {actions.map((action, index) => {
          const ActionComponent = action.to ? Link : 'button';
          return (
            <ActionComponent
              key={index}
              to={action.to}
              href={action.href}
              className="flex flex-col items-center p-4 bg-gray-50 hover:bg-gray-100 border border-gray-200 rounded-lg transition-all duration-200 hover:scale-105 cursor-pointer"
            >
              <span className="text-2xl mb-2">{action.emoji}</span>
              <span className="text-sm font-medium text-center">{action.label}</span>
            </ActionComponent>
          );
        })}
      </div>
    </DashboardCard>
  );
};

export default QuickActions;

// src/components/ui/Badge.jsx
import React from 'react';
import { cn } from '../../utils/helpers';

const Badge = ({ className, variant = 'default', ...props }) => {
  const variants = {
    default: "bg-gray-900 text-gray-50 hover:bg-gray-900/80",
    secondary: "bg-gray-100 text-gray-900 hover:bg-gray-100/80",
    success: "bg-green-100 text-green-800",
    warning: "bg-yellow-100 text-yellow-800",
    danger: "bg-red-100 text-red-800",
    verified: "bg-green-100 text-green-800",
    unverified: "bg-yellow-100 text-yellow-800"
  };

  return (
    <div
      className={cn(
        "inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2",
        variants[variant],
        className
      )}
      {...props}
    />
  );
};

export default Badge;

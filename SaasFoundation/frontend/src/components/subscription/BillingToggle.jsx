// src/components/subscription/BillingToggle.jsx
import React from 'react';
import { cn } from '../../utils/helpers';

const BillingToggle = ({ billingCycle, onBillingCycleChange }) => {
  return (
    <div className="flex justify-center mb-8">
      <div className="bg-gray-100 p-1 rounded-lg flex">
        <button
          className={cn(
            "px-4 py-2 rounded-md text-sm font-medium transition-all",
            billingCycle === 'monthly' 
              ? "bg-white text-gray-900 shadow-sm" 
              : "text-gray-600 hover:text-gray-900"
          )}
          onClick={() => onBillingCycleChange('monthly')}
        >
          Monthly
        </button>
        <button
          className={cn(
            "px-4 py-2 rounded-md text-sm font-medium transition-all relative",
            billingCycle === 'yearly' 
              ? "bg-white text-gray-900 shadow-sm" 
              : "text-gray-600 hover:text-gray-900"
          )}
          onClick={() => onBillingCycleChange('yearly')}
        >
          Yearly
          <span className="absolute -top-2 -right-2 bg-green-500 text-white text-xs px-1.5 py-0.5 rounded-full">
            Save 20%
          </span>
        </button>
      </div>
    </div>
  );
};

export default BillingToggle;

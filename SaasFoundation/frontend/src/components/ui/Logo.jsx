import React from 'react';

const Logo = ({ size = 'default', className = '' }) => {
  const sizeClasses = {
    small: 'text-lg',
    default: 'text-2xl',
    large: 'text-3xl',
    xlarge: 'text-4xl'
  };

  return (
    <div className={`text-center ${className}`}>
      <div className={`font-bold text-gray-900 ${sizeClasses[size]}`}>
        <div className="leading-tight">
          <span className="block">Agentic</span>
          <span className="block">Practice</span>
        </div>
      </div>
    </div>
  );
};

export default Logo;

// File: src/components/common/Card.js - Reusable Card Component
import React from 'react';

const Card = ({ children, className = '', title = null, subtitle = null }) => {
  return (
    <div className={`bg-white rounded-lg shadow p-6 ${className}`}>
      {(title || subtitle) && (
        <div className="mb-4">
          {title && <h3 className="text-lg font-medium text-gray-900">{title}</h3>}
          {subtitle && <p className="text-sm text-gray-600 mt-1">{subtitle}</p>}
        </div>
      )}
      {children}
    </div>
  );
};

export default Card;

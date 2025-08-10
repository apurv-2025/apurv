// File: src/components/common/Card.js
import React from 'react';

const Card = ({ children, className = '', title = null }) => {
  return (
    <div className={`bg-white rounded-lg shadow p-6 ${className}`}>
      {title && (
        <h3 className="text-lg font-medium text-gray-900 mb-4">
          {title}
        </h3>
      )}
      {children}
    </div>
  );
};

export default Card;

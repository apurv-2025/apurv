import React from 'react';

const CloudVendorSelector = ({ cloudVendors, selectedVendor, onVendorSelect }) => {
  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Select Cloud Vendor</h3>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {cloudVendors.map((vendor) => (
          <div
            key={vendor.id}
            onClick={() => onVendorSelect(vendor.id)}
            className={`p-4 border rounded-lg cursor-pointer transition-all ${
              selectedVendor === vendor.id 
                ? 'border-blue-300 bg-blue-50' 
                : 'border-gray-200 hover:border-blue-200'
            }`}
          >
            <div className="text-center">
              <div className="text-4xl mb-2">{vendor.logo}</div>
              <h4 className="font-medium text-gray-900">{vendor.name}</h4>
              <div className="mt-2 flex flex-wrap gap-1 justify-center">
                {vendor.features.slice(0, 2).map(feature => (
                  <span key={feature} className="text-xs bg-gray-100 px-2 py-1 rounded">
                    {feature}
                  </span>
                ))}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default CloudVendorSelector; 
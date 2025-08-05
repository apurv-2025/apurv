import React from 'react';
import { CheckCircle } from 'lucide-react';

const DataSourceSelector = ({ 
  dataSourceOptions, 
  selectedDataSources, 
  handleDataSourceToggle 
}) => {
  const getConnectionStatus = (status) => {
    switch (status) {
      case 'connected': return 'text-green-600 bg-green-100';
      case 'available': return 'text-gray-600 bg-gray-100';
      case 'error': return 'text-red-600 bg-red-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Available Data Sources</h3>
      <p className="text-gray-600 mb-6">Select data sources to import training data from your connected systems.</p>
      
      {dataSourceOptions.map((category) => (
        <div key={category.category} className="mb-8">
          <h4 className="font-medium text-gray-900 mb-4">{category.category}</h4>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {category.sources.map((source) => {
              const IconComponent = source.icon;
              const isSelected = selectedDataSources.includes(source.id);
              const isConnected = source.status === 'connected';
              
              return (
                <div
                  key={source.id}
                  onClick={() => isConnected && handleDataSourceToggle(source.id)}
                  className={`p-4 border rounded-lg transition-all cursor-pointer ${
                    isSelected 
                      ? 'border-blue-300 bg-blue-50' 
                      : isConnected 
                        ? 'border-gray-200 hover:border-blue-200' 
                        : 'border-gray-200 opacity-50 cursor-not-allowed'
                  }`}
                >
                  <div className="flex items-center space-x-3">
                    <div className={`p-2 rounded-lg ${
                      isConnected ? 'bg-green-100' : 'bg-gray-100'
                    }`}>
                      <IconComponent className={`w-5 h-5 ${
                        isConnected ? 'text-green-600' : 'text-gray-400'
                      }`} />
                    </div>
                    <div className="flex-1">
                      <h5 className="font-medium text-gray-900">{source.name}</h5>
                      <div className="flex items-center space-x-2 mt-1">
                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${getConnectionStatus(source.status)}`}>
                          {source.status}
                        </span>
                        {isSelected && (
                          <CheckCircle className="w-4 h-4 text-blue-600" />
                        )}
                      </div>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      ))}

      {selectedDataSources.length > 0 && (
        <div className="mt-6 p-4 bg-blue-50 rounded-lg">
          <h4 className="font-medium text-blue-900 mb-2">Selected Data Sources ({selectedDataSources.length})</h4>
          <div className="flex flex-wrap gap-2">
            {selectedDataSources.map((sourceId) => {
              const source = dataSourceOptions
                .flatMap(cat => cat.sources)
                .find(s => s.id === sourceId);
              return (
                <span key={sourceId} className="bg-blue-100 text-blue-800 px-2 py-1 rounded text-sm">
                  {source?.name}
                </span>
              );
            })}
          </div>
          <button className="mt-4 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors">
            Import Data from Selected Sources
          </button>
        </div>
      )}
    </div>
  );
};

export default DataSourceSelector; 
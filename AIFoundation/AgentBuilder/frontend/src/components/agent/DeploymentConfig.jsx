import React from 'react';

const DeploymentConfig = ({ 
  selectedVendor, 
  deploymentConfig, 
  setDeploymentConfig 
}) => {
  if (!selectedVendor) return null;

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Deployment Configuration</h3>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Region Selection */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Region</label>
          <select
            value={deploymentConfig.region}
            onChange={(e) => setDeploymentConfig({ ...deploymentConfig, region: e.target.value })}
            className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="">Select region...</option>
            {selectedVendor.regions.map(region => (
              <option key={region.id} value={region.id}>
                {region.name} ({region.latency})
              </option>
            ))}
          </select>
        </div>

        {/* Instance Type */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Instance Type</label>
          <select
            value={deploymentConfig.instanceType}
            onChange={(e) => setDeploymentConfig({ ...deploymentConfig, instanceType: e.target.value })}
            className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="">Select instance...</option>
            {selectedVendor.instanceTypes.map(instance => (
              <option key={instance.id} value={instance.id}>
                {instance.name} - {instance.cpu}, {instance.memory} ({instance.cost})
              </option>
            ))}
          </select>
        </div>

        {/* Scaling */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Scaling</label>
          <select
            value={deploymentConfig.scaling}
            onChange={(e) => setDeploymentConfig({ ...deploymentConfig, scaling: e.target.value })}
            className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="auto">Auto Scaling</option>
            <option value="manual">Manual Scaling</option>
            <option value="fixed">Fixed Instances</option>
          </select>
        </div>

        {/* Environment */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Environment</label>
          <select
            value={deploymentConfig.environment}
            onChange={(e) => setDeploymentConfig({ ...deploymentConfig, environment: e.target.value })}
            className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="staging">Staging</option>
            <option value="production">Production</option>
          </select>
        </div>
      </div>

      {/* Cost Estimate */}
      {deploymentConfig.instanceType && (
        <div className="mt-6 p-4 bg-blue-50 rounded-lg">
          <h4 className="font-medium text-blue-900 mb-2">Estimated Monthly Cost</h4>
          <div className="text-2xl font-bold text-blue-600">
            {selectedVendor.instanceTypes.find(i => i.id === deploymentConfig.instanceType)?.cost || 'N/A'}
          </div>
          <p className="text-sm text-blue-700 mt-1">
            Includes compute, storage, and basic monitoring
          </p>
        </div>
      )}
    </div>
  );
};

export default DeploymentConfig; 
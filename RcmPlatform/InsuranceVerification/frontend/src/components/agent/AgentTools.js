import React, { useState } from 'react';
import { Shield, FileText, CheckCircle, AlertTriangle, Upload, Search, Settings, Bot } from 'lucide-react';

const AgentTools = () => {
  const [activeTool, setActiveTool] = useState('verify');
  const [formData, setFormData] = useState({
    member_id: '',
    provider_npi: '',
    service_type: '30',
    file_path: '',
    file_type: 'image',
    edi_content: '',
    transaction_type: '270'
  });
  const [results, setResults] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const tools = [
    {
      id: 'verify',
      name: 'Insurance Verification',
      icon: Shield,
      description: 'Verify insurance coverage and eligibility',
      color: 'text-blue-600',
      bgColor: 'bg-blue-50'
    },
    {
      id: 'extract',
      name: 'Document Extraction',
      icon: FileText,
      description: 'Extract insurance information from documents',
      color: 'text-green-600',
      bgColor: 'bg-green-50'
    },
    {
      id: 'eligibility',
      name: 'Eligibility Check',
      icon: CheckCircle,
      description: 'Check patient eligibility for services',
      color: 'text-purple-600',
      bgColor: 'bg-purple-50'
    },
    {
      id: 'edi',
      name: 'EDI Analysis',
      icon: AlertTriangle,
      description: 'Analyze EDI 270/271 transactions',
      color: 'text-orange-600',
      bgColor: 'bg-orange-50'
    }
  ];

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      let endpoint = '';
      let payload = {};

      switch (activeTool) {
        case 'verify':
          endpoint = '/api/v1/agent/verify-insurance';
          payload = {
            member_id: formData.member_id,
            provider_npi: formData.provider_npi,
            service_type: formData.service_type
          };
          break;
        case 'extract':
          endpoint = '/api/v1/agent/extract-insurance-info';
          payload = {
            file_path: formData.file_path,
            file_type: formData.file_type
          };
          break;
        case 'eligibility':
          endpoint = '/api/v1/agent/check-eligibility';
          payload = {
            member_id: formData.member_id,
            service_type: formData.service_type,
            provider_npi: formData.provider_npi
          };
          break;
        case 'edi':
          endpoint = '/api/v1/agent/analyze-edi';
          payload = {
            edi_content: formData.edi_content,
            transaction_type: formData.transaction_type
          };
          break;
      }

      const response = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      const data = await response.json();
      setResults(data);
    } catch (error) {
      setResults({ error: 'Failed to process request' });
    } finally {
      setIsLoading(false);
    }
  };

  const renderForm = () => {
    switch (activeTool) {
      case 'verify':
        return (
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">Member ID</label>
              <input
                type="text"
                value={formData.member_id}
                onChange={(e) => setFormData({...formData, member_id: e.target.value})}
                className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-blue-500 focus:border-blue-500"
                placeholder="Enter member ID"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Provider NPI</label>
              <input
                type="text"
                value={formData.provider_npi}
                onChange={(e) => setFormData({...formData, provider_npi: e.target.value})}
                className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-blue-500 focus:border-blue-500"
                placeholder="Enter provider NPI"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Service Type</label>
              <select
                value={formData.service_type}
                onChange={(e) => setFormData({...formData, service_type: e.target.value})}
                className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="30">Office Visit</option>
                <option value="35">Hospital</option>
                <option value="40">Emergency</option>
                <option value="50">Urgent Care</option>
              </select>
            </div>
          </div>
        );

      case 'extract':
        return (
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">File Path</label>
              <input
                type="text"
                value={formData.file_path}
                onChange={(e) => setFormData({...formData, file_path: e.target.value})}
                className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-green-500 focus:border-green-500"
                placeholder="Enter file path"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">File Type</label>
              <select
                value={formData.file_type}
                onChange={(e) => setFormData({...formData, file_type: e.target.value})}
                className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-green-500 focus:border-green-500"
              >
                <option value="image">Image</option>
                <option value="pdf">PDF</option>
                <option value="document">Document</option>
              </select>
            </div>
          </div>
        );

      case 'eligibility':
        return (
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">Member ID</label>
              <input
                type="text"
                value={formData.member_id}
                onChange={(e) => setFormData({...formData, member_id: e.target.value})}
                className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-purple-500 focus:border-purple-500"
                placeholder="Enter member ID"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Service Type</label>
              <select
                value={formData.service_type}
                onChange={(e) => setFormData({...formData, service_type: e.target.value})}
                className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-purple-500 focus:border-purple-500"
              >
                <option value="30">Office Visit</option>
                <option value="35">Hospital</option>
                <option value="40">Emergency</option>
                <option value="50">Urgent Care</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Provider NPI (Optional)</label>
              <input
                type="text"
                value={formData.provider_npi}
                onChange={(e) => setFormData({...formData, provider_npi: e.target.value})}
                className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-purple-500 focus:border-purple-500"
                placeholder="Enter provider NPI"
              />
            </div>
          </div>
        );

      case 'edi':
        return (
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">EDI Content</label>
              <textarea
                value={formData.edi_content}
                onChange={(e) => setFormData({...formData, edi_content: e.target.value})}
                rows="6"
                className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-orange-500 focus:border-orange-500"
                placeholder="Paste EDI transaction content here..."
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Transaction Type</label>
              <select
                value={formData.transaction_type}
                onChange={(e) => setFormData({...formData, transaction_type: e.target.value})}
                className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-orange-500 focus:border-orange-500"
              >
                <option value="270">270 - Eligibility Request</option>
                <option value="271">271 - Eligibility Response</option>
              </select>
            </div>
          </div>
        );

      default:
        return null;
    }
  };

  const renderResults = () => {
    if (!results) return null;

    if (results.error) {
      return (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <div className="flex items-center space-x-2">
            <AlertTriangle className="h-5 w-5 text-red-600" />
            <span className="text-red-800 font-medium">Error</span>
          </div>
          <p className="text-red-700 mt-2">{results.error}</p>
        </div>
      );
    }

    return (
      <div className="bg-green-50 border border-green-200 rounded-lg p-4">
        <div className="flex items-center space-x-2 mb-3">
          <CheckCircle className="h-5 w-5 text-green-600" />
          <span className="text-green-800 font-medium">Success</span>
        </div>
        <pre className="text-sm text-green-700 overflow-auto">
          {JSON.stringify(results, null, 2)}
        </pre>
      </div>
    );
  };

  return (
    <div className="space-y-6">
      {/* Tool Selection */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {tools.map((tool) => {
          const Icon = tool.icon;
          return (
            <button
              key={tool.id}
              onClick={() => setActiveTool(tool.id)}
              className={`p-4 rounded-lg border-2 transition-all ${
                activeTool === tool.id
                  ? `${tool.bgColor} border-blue-500`
                  : 'bg-white border-gray-200 hover:border-gray-300'
              }`}
            >
              <div className="flex items-center space-x-3">
                <Icon className={`h-6 w-6 ${tool.color}`} />
                <div className="text-left">
                  <h3 className="font-medium text-gray-900">{tool.name}</h3>
                  <p className="text-sm text-gray-500">{tool.description}</p>
                </div>
              </div>
            </button>
          );
        })}
      </div>

      {/* Tool Form */}
      <div className="bg-white rounded-lg shadow-sm border p-6">
        <div className="flex items-center space-x-3 mb-6">
          {tools.find(t => t.id === activeTool)?.icon && 
            React.createElement(tools.find(t => t.id === activeTool).icon, { 
              className: `h-6 w-6 ${tools.find(t => t.id === activeTool).color}` 
            })
          }
          <h2 className="text-lg font-semibold text-gray-900">
            {tools.find(t => t.id === activeTool)?.name}
          </h2>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          {renderForm()}
          
          <div className="flex justify-end">
            <button
              type="submit"
              disabled={isLoading}
              className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              {isLoading ? (
                <div className="flex items-center space-x-2">
                  <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                  <span>Processing...</span>
                </div>
              ) : (
                <div className="flex items-center space-x-2">
                  <Search className="h-4 w-4" />
                  <span>Process</span>
                </div>
              )}
            </button>
          </div>
        </form>

        {/* Results */}
        {renderResults()}
      </div>
    </div>
  );
};

export default AgentTools; 
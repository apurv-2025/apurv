import React, { useState } from 'react';
import { Shield, FileText, CheckCircle, AlertTriangle, Upload, Search, Settings, Bot, User, Code, Calendar } from 'lucide-react';
import axios from 'axios';

const AgentTools = () => {
  const [activeTool, setActiveTool] = useState('create');
  const [formData, setFormData] = useState({
    patient_id: '',
    provider_npi: '',
    procedure_codes: '',
    diagnosis_codes: '',
    service_date: '',
    medical_necessity: '',
    request_id: '',
    edi_type: '278',
    member_id: '',
    code_type: 'procedure',
    search_term: ''
  });
  const [results, setResults] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8002';

  const tools = [
    {
      id: 'create',
      name: 'Create Authorization',
      icon: Shield,
      description: 'Create a new prior authorization request',
      color: 'text-blue-600',
      bgColor: 'bg-blue-50'
    },
    {
      id: 'status',
      name: 'Check Status',
      icon: CheckCircle,
      description: 'Check authorization request status',
      color: 'text-green-600',
      bgColor: 'bg-green-50'
    },
    {
      id: 'edi',
      name: 'Generate EDI',
      icon: FileText,
      description: 'Generate EDI 278/275 documents',
      color: 'text-purple-600',
      bgColor: 'bg-purple-50'
    },
    {
      id: 'patient',
      name: 'Patient Lookup',
      icon: User,
      description: 'Look up patient information',
      color: 'text-orange-600',
      bgColor: 'bg-orange-50'
    },
    {
      id: 'codes',
      name: 'Code Lookup',
      icon: Code,
      description: 'Find healthcare codes',
      color: 'text-indigo-600',
      bgColor: 'bg-indigo-50'
    }
  ];

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      let endpoint = '';
      let payload = {};

      switch (activeTool) {
        case 'create':
          endpoint = `${API_BASE_URL}/api/v1/agent/create-prior-auth`;
          payload = {
            patient_id: formData.patient_id,
            provider_npi: formData.provider_npi,
            procedure_codes: formData.procedure_codes ? formData.procedure_codes.split(',').map(code => ({ code: code.trim() })) : [],
            diagnosis_codes: formData.diagnosis_codes ? formData.diagnosis_codes.split(',').map(code => ({ code: code.trim() })) : [],
            service_date: formData.service_date,
            medical_necessity: formData.medical_necessity
          };
          break;
        case 'status':
          endpoint = `${API_BASE_URL}/api/v1/agent/check-status`;
          payload = {
            request_id: formData.request_id
          };
          break;
        case 'edi':
          endpoint = `${API_BASE_URL}/api/v1/agent/generate-edi`;
          payload = {
            edi_type: formData.edi_type,
            patient_id: formData.patient_id,
            request_id: formData.request_id,
            provider_npi: formData.provider_npi,
            service_date: formData.service_date
          };
          break;
        case 'patient':
          endpoint = `${API_BASE_URL}/api/v1/agent/lookup-patient`;
          payload = {
            patient_id: formData.patient_id || undefined,
            member_id: formData.member_id || undefined
          };
          break;
        case 'codes':
          endpoint = `${API_BASE_URL}/api/v1/agent/lookup-codes`;
          payload = {
            code_type: formData.code_type,
            search_term: formData.search_term || undefined,
            code: formData.search_term || undefined
          };
          break;
      }

      const response = await axios.post(endpoint, payload);
      setResults(response.data);
    } catch (error) {
      console.error('Error executing tool:', error);
      setResults({
        success: false,
        error: error.response?.data?.detail || error.message
      });
    } finally {
      setIsLoading(false);
    }
  };

  const renderForm = () => {
    switch (activeTool) {
      case 'create':
        return (
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Patient ID *</label>
                <input
                  type="text"
                  value={formData.patient_id}
                  onChange={(e) => setFormData({...formData, patient_id: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="PAT123456"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Provider NPI *</label>
                <input
                  type="text"
                  value={formData.provider_npi}
                  onChange={(e) => setFormData({...formData, provider_npi: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="1234567890"
                  required
                />
              </div>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Procedure Codes</label>
                <input
                  type="text"
                  value={formData.procedure_codes}
                  onChange={(e) => setFormData({...formData, procedure_codes: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="99213, 99214 (comma separated)"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Diagnosis Codes</label>
                <input
                  type="text"
                  value={formData.diagnosis_codes}
                  onChange={(e) => setFormData({...formData, diagnosis_codes: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="E11.9, I10 (comma separated)"
                />
              </div>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Service Date</label>
                <input
                  type="date"
                  value={formData.service_date}
                  onChange={(e) => setFormData({...formData, service_date: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Medical Necessity</label>
              <textarea
                value={formData.medical_necessity}
                onChange={(e) => setFormData({...formData, medical_necessity: e.target.value})}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                rows="3"
                placeholder="Describe the medical necessity for this authorization request..."
              />
            </div>
          </form>
        );

      case 'status':
        return (
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Request ID *</label>
              <input
                type="text"
                value={formData.request_id}
                onChange={(e) => setFormData({...formData, request_id: e.target.value})}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="AUTH123456"
                required
              />
            </div>
          </form>
        );

      case 'edi':
        return (
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">EDI Type *</label>
                <select
                  value={formData.edi_type}
                  onChange={(e) => setFormData({...formData, edi_type: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  required
                >
                  <option value="278">278 - Authorization Request</option>
                  <option value="275">275 - Patient Information</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Patient ID *</label>
                <input
                  type="text"
                  value={formData.patient_id}
                  onChange={(e) => setFormData({...formData, patient_id: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="PAT123456"
                  required
                />
              </div>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Request ID</label>
                <input
                  type="text"
                  value={formData.request_id}
                  onChange={(e) => setFormData({...formData, request_id: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="AUTH123456"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Provider NPI</label>
                <input
                  type="text"
                  value={formData.provider_npi}
                  onChange={(e) => setFormData({...formData, provider_npi: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="1234567890"
                />
              </div>
            </div>
          </form>
        );

      case 'patient':
        return (
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Patient ID</label>
                <input
                  type="text"
                  value={formData.patient_id}
                  onChange={(e) => setFormData({...formData, patient_id: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="PAT123456"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Member ID</label>
                <input
                  type="text"
                  value={formData.member_id}
                  onChange={(e) => setFormData({...formData, member_id: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="MEM123456"
                />
              </div>
            </div>
            <p className="text-sm text-gray-500">Provide either Patient ID or Member ID to lookup patient information.</p>
          </form>
        );

      case 'codes':
        return (
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Code Type *</label>
                <select
                  value={formData.code_type}
                  onChange={(e) => setFormData({...formData, code_type: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  required
                >
                  <option value="procedure">Procedure Codes (CPT)</option>
                  <option value="diagnosis">Diagnosis Codes (ICD-10)</option>
                  <option value="service_type">Service Type Codes</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Search Term / Code</label>
                <input
                  type="text"
                  value={formData.search_term}
                  onChange={(e) => setFormData({...formData, search_term: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="office visit, 99213, diabetes..."
                  required
                />
              </div>
            </div>
          </form>
        );

      default:
        return null;
    }
  };

  const renderResults = () => {
    if (!results) return null;

    return (
      <div className="mt-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Results</h3>
        <div className={`p-4 rounded-lg border ${
          results.success ? 'bg-green-50 border-green-200' : 'bg-red-50 border-red-200'
        }`}>
          {results.success ? (
            <div>
              <div className="flex items-center space-x-2 mb-2">
                <CheckCircle className="h-5 w-5 text-green-600" />
                <span className="font-medium text-green-800">Success</span>
              </div>
              <pre className="text-sm text-green-700 whitespace-pre-wrap overflow-x-auto">
                {JSON.stringify(results.data || results, null, 2)}
              </pre>
            </div>
          ) : (
            <div>
              <div className="flex items-center space-x-2 mb-2">
                <AlertTriangle className="h-5 w-5 text-red-600" />
                <span className="font-medium text-red-800">Error</span>
              </div>
              <p className="text-sm text-red-700">{results.error}</p>
            </div>
          )}
        </div>
      </div>
    );
  };

  return (
    <div className="space-y-6">
      {/* Tool Selection */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
        {tools.map((tool) => {
          const Icon = tool.icon;
          return (
            <button
              key={tool.id}
              onClick={() => setActiveTool(tool.id)}
              className={`p-4 rounded-lg border-2 transition-all ${
                activeTool === tool.id
                  ? 'border-blue-500 bg-blue-50'
                  : 'border-gray-200 bg-white hover:border-gray-300'
              }`}
            >
              <div className="flex items-center space-x-3">
                <Icon className={`h-6 w-6 ${tool.color}`} />
                <div className="text-left">
                  <h3 className="font-medium text-gray-900">{tool.name}</h3>
                  <p className="text-xs text-gray-500">{tool.description}</p>
                </div>
              </div>
            </button>
          );
        })}
      </div>

      {/* Tool Form */}
      <div className="bg-white rounded-lg shadow-sm border p-6">
        <div className="flex items-center space-x-3 mb-6">
          {(() => {
            const Icon = tools.find(t => t.id === activeTool)?.icon || Settings;
            return <Icon className="h-6 w-6 text-blue-600" />;
          })()}
          <div>
            <h2 className="text-lg font-semibold text-gray-900">
              {tools.find(t => t.id === activeTool)?.name}
            </h2>
            <p className="text-sm text-gray-500">
              {tools.find(t => t.id === activeTool)?.description}
            </p>
          </div>
        </div>

        {renderForm()}

        <div className="mt-6 flex justify-end">
          <button
            onClick={handleSubmit}
            disabled={isLoading}
            className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center space-x-2"
          >
            {isLoading ? (
              <>
                <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                <span>Processing...</span>
              </>
            ) : (
              <>
                <Bot className="h-4 w-4" />
                <span>Execute Tool</span>
              </>
            )}
          </button>
        </div>
      </div>

      {renderResults()}
    </div>
  );
};

export default AgentTools; 
import React, { useState } from 'react';
import {
  Plus, CheckCircle, FileText, BarChart3,
  Loader2, AlertCircle, Check, X,
  DollarSign, Calendar, User, Stethoscope,
  Search, Settings, Bot, Sparkles
} from 'lucide-react';

const AgentTools = () => {
  const [activeTool, setActiveTool] = useState('capture');
  const [isLoading, setIsLoading] = useState(false);
  const [results, setResults] = useState({});

  // Form states
  const [captureForm, setCaptureForm] = useState({
    encounter_id: '',
    patient_id: '',
    provider_id: '',
    cpt_code: '',
    icd_code: '',
    charge_amount: '',
    modifiers: '',
    notes: ''
  });

  const [validationForm, setValidationForm] = useState({
    cpt_code: '',
    icd_code: '',
    modifiers: '',
    charge_amount: '',
    specialty: ''
  });

  const [templateForm, setTemplateForm] = useState({
    specialty: '',
    procedure_type: '',
    search_query: ''
  });

  const [analysisForm, setAnalysisForm] = useState({
    provider_id: '',
    date_range: '30',
    specialty: '',
    analysis_type: 'performance'
  });

  const tools = [
    {
      id: 'capture',
      name: 'Capture Charge',
      description: 'Create a new charge with AI assistance',
      icon: Plus,
      color: 'text-blue-600',
      bgColor: 'bg-blue-50'
    },
    {
      id: 'validate',
      name: 'Validate Charge',
      description: 'Validate CPT/ICD codes and compliance',
      icon: CheckCircle,
      color: 'text-green-600',
      bgColor: 'bg-green-50'
    },
    {
      id: 'templates',
      name: 'Get Templates',
      description: 'Find charge templates by specialty',
      icon: FileText,
      color: 'text-purple-600',
      bgColor: 'bg-purple-50'
    },
    {
      id: 'analysis',
      name: 'Analyze Charges',
      description: 'Get insights and recommendations',
      icon: BarChart3,
      color: 'text-orange-600',
      bgColor: 'bg-orange-50'
    }
  ];

  const handleCaptureCharge = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    try {
      const response = await fetch('/api/v1/agent/capture-charge', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(captureForm)
      });
      const data = await response.json();
      setResults({ capture: data });
    } catch (error) {
      setResults({ capture: { success: false, error: 'Failed to capture charge' } });
    } finally {
      setIsLoading(false);
    }
  };

  const handleValidateCharge = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    try {
      const response = await fetch('/api/v1/agent/validate-charge', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(validationForm)
      });
      const data = await response.json();
      setResults({ validate: data });
    } catch (error) {
      setResults({ validate: { success: false, error: 'Failed to validate charge' } });
    } finally {
      setIsLoading(false);
    }
  };

  const handleGetTemplates = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    try {
      const response = await fetch('/api/v1/agent/get-templates', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(templateForm)
      });
      const data = await response.json();
      setResults({ templates: data });
    } catch (error) {
      setResults({ templates: { success: false, error: 'Failed to get templates' } });
    } finally {
      setIsLoading(false);
    }
  };

  const handleAnalyzeCharges = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    try {
      const response = await fetch('/api/v1/agent/analyze-charges', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(analysisForm)
      });
      const data = await response.json();
      setResults({ analysis: data });
    } catch (error) {
      setResults({ analysis: { success: false, error: 'Failed to analyze charges' } });
    } finally {
      setIsLoading(false);
    }
  };

  const renderCaptureForm = () => (
    <form onSubmit={handleCaptureCharge} className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Encounter ID
          </label>
          <input
            type="text"
            value={captureForm.encounter_id}
            onChange={(e) => setCaptureForm({...captureForm, encounter_id: e.target.value})}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="Enter encounter ID"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Patient ID
          </label>
          <input
            type="text"
            value={captureForm.patient_id}
            onChange={(e) => setCaptureForm({...captureForm, patient_id: e.target.value})}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="Enter patient ID"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Provider ID
          </label>
          <input
            type="text"
            value={captureForm.provider_id}
            onChange={(e) => setCaptureForm({...captureForm, provider_id: e.target.value})}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="Enter provider ID"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            CPT Code
          </label>
          <input
            type="text"
            value={captureForm.cpt_code}
            onChange={(e) => setCaptureForm({...captureForm, cpt_code: e.target.value})}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="e.g., 99213"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            ICD Code
          </label>
          <input
            type="text"
            value={captureForm.icd_code}
            onChange={(e) => setCaptureForm({...captureForm, icd_code: e.target.value})}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="e.g., Z00.00"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Charge Amount
          </label>
          <input
            type="number"
            step="0.01"
            value={captureForm.charge_amount}
            onChange={(e) => setCaptureForm({...captureForm, charge_amount: e.target.value})}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="0.00"
          />
        </div>
      </div>
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Modifiers
        </label>
        <input
          type="text"
          value={captureForm.modifiers}
          onChange={(e) => setCaptureForm({...captureForm, modifiers: e.target.value})}
          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          placeholder="e.g., 25, 59"
        />
      </div>
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Notes
        </label>
        <textarea
          value={captureForm.notes}
          onChange={(e) => setCaptureForm({...captureForm, notes: e.target.value})}
          rows="3"
          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          placeholder="Additional notes..."
        />
      </div>
      <div className="flex justify-end">
        <button
          type="submit"
          disabled={isLoading}
          className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center space-x-2"
        >
          {isLoading ? (
            <>
              <Loader2 className="w-4 h-4 animate-spin" />
              <span>Processing...</span>
            </>
          ) : (
            <>
              <Plus className="w-4 h-4" />
              <span>Capture Charge</span>
            </>
          )}
        </button>
      </div>
    </form>
  );

  const renderValidationForm = () => (
    <form onSubmit={handleValidateCharge} className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            CPT Code
          </label>
          <input
            type="text"
            value={validationForm.cpt_code}
            onChange={(e) => setValidationForm({...validationForm, cpt_code: e.target.value})}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="e.g., 99213"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            ICD Code
          </label>
          <input
            type="text"
            value={validationForm.icd_code}
            onChange={(e) => setValidationForm({...validationForm, icd_code: e.target.value})}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="e.g., Z00.00"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Modifiers
          </label>
          <input
            type="text"
            value={validationForm.modifiers}
            onChange={(e) => setValidationForm({...validationForm, modifiers: e.target.value})}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="e.g., 25, 59"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Charge Amount
          </label>
          <input
            type="number"
            step="0.01"
            value={validationForm.charge_amount}
            onChange={(e) => setValidationForm({...validationForm, charge_amount: e.target.value})}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="0.00"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Specialty
          </label>
          <select
            value={validationForm.specialty}
            onChange={(e) => setValidationForm({...validationForm, specialty: e.target.value})}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="">Select specialty</option>
            <option value="cardiology">Cardiology</option>
            <option value="orthopedics">Orthopedics</option>
            <option value="primary_care">Primary Care</option>
            <option value="dermatology">Dermatology</option>
            <option value="neurology">Neurology</option>
          </select>
        </div>
      </div>
      <div className="flex justify-end">
        <button
          type="submit"
          disabled={isLoading}
          className="px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 focus:ring-2 focus:ring-green-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center space-x-2"
        >
          {isLoading ? (
            <>
              <Loader2 className="w-4 h-4 animate-spin" />
              <span>Validating...</span>
            </>
          ) : (
            <>
              <CheckCircle className="w-4 h-4" />
              <span>Validate Charge</span>
            </>
          )}
        </button>
      </div>
    </form>
  );

  const renderTemplateForm = () => (
    <form onSubmit={handleGetTemplates} className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Specialty
          </label>
          <select
            value={templateForm.specialty}
            onChange={(e) => setTemplateForm({...templateForm, specialty: e.target.value})}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="">Select specialty</option>
            <option value="cardiology">Cardiology</option>
            <option value="orthopedics">Orthopedics</option>
            <option value="primary_care">Primary Care</option>
            <option value="dermatology">Dermatology</option>
            <option value="neurology">Neurology</option>
          </select>
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Procedure Type
          </label>
          <input
            type="text"
            value={templateForm.procedure_type}
            onChange={(e) => setTemplateForm({...templateForm, procedure_type: e.target.value})}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="e.g., office visit, procedure"
          />
        </div>
      </div>
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Search Query
        </label>
        <input
          type="text"
          value={templateForm.search_query}
          onChange={(e) => setTemplateForm({...templateForm, search_query: e.target.value})}
          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          placeholder="Search for specific templates..."
        />
      </div>
      <div className="flex justify-end">
        <button
          type="submit"
          disabled={isLoading}
          className="px-6 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 focus:ring-2 focus:ring-purple-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center space-x-2"
        >
          {isLoading ? (
            <>
              <Loader2 className="w-4 h-4 animate-spin" />
              <span>Searching...</span>
            </>
          ) : (
            <>
              <FileText className="w-4 h-4" />
              <span>Get Templates</span>
            </>
          )}
        </button>
      </div>
    </form>
  );

  const renderAnalysisForm = () => (
    <form onSubmit={handleAnalyzeCharges} className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Provider ID
          </label>
          <input
            type="text"
            value={analysisForm.provider_id}
            onChange={(e) => setAnalysisForm({...analysisForm, provider_id: e.target.value})}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="Enter provider ID"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Date Range (days)
          </label>
          <select
            value={analysisForm.date_range}
            onChange={(e) => setAnalysisForm({...analysisForm, date_range: e.target.value})}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="7">Last 7 days</option>
            <option value="30">Last 30 days</option>
            <option value="90">Last 90 days</option>
            <option value="365">Last year</option>
          </select>
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Specialty
          </label>
          <select
            value={analysisForm.specialty}
            onChange={(e) => setAnalysisForm({...analysisForm, specialty: e.target.value})}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="">All specialties</option>
            <option value="cardiology">Cardiology</option>
            <option value="orthopedics">Orthopedics</option>
            <option value="primary_care">Primary Care</option>
            <option value="dermatology">Dermatology</option>
            <option value="neurology">Neurology</option>
          </select>
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Analysis Type
          </label>
          <select
            value={analysisForm.analysis_type}
            onChange={(e) => setAnalysisForm({...analysisForm, analysis_type: e.target.value})}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="performance">Performance Analysis</option>
            <option value="revenue">Revenue Analysis</option>
            <option value="compliance">Compliance Analysis</option>
            <option value="patterns">Pattern Analysis</option>
          </select>
        </div>
      </div>
      <div className="flex justify-end">
        <button
          type="submit"
          disabled={isLoading}
          className="px-6 py-2 bg-orange-600 text-white rounded-lg hover:bg-orange-700 focus:ring-2 focus:ring-orange-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center space-x-2"
        >
          {isLoading ? (
            <>
              <Loader2 className="w-4 h-4 animate-spin" />
              <span>Analyzing...</span>
            </>
          ) : (
            <>
              <BarChart3 className="w-4 h-4" />
              <span>Analyze Charges</span>
            </>
          )}
        </button>
      </div>
    </form>
  );

  const renderResults = () => {
    const result = results[activeTool];
    if (!result) return null;

    return (
      <div className="mt-8 p-6 bg-gray-50 rounded-lg border">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Results</h3>
        {result.success ? (
          <div className="space-y-4">
            {result.data && (
              <div className="bg-white p-4 rounded-lg border">
                <pre className="text-sm text-gray-700 whitespace-pre-wrap">
                  {JSON.stringify(result.data, null, 2)}
                </pre>
              </div>
            )}
            {result.message && (
              <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                <div className="flex items-center">
                  <Check className="h-5 w-5 text-green-600 mr-2" />
                  <span className="text-green-800">{result.message}</span>
                </div>
              </div>
            )}
          </div>
        ) : (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4">
            <div className="flex items-center">
              <X className="h-5 w-5 text-red-600 mr-2" />
              <span className="text-red-800">{result.error || 'An error occurred'}</span>
            </div>
          </div>
        )}
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

        {activeTool === 'capture' && renderCaptureForm()}
        {activeTool === 'validate' && renderValidationForm()}
        {activeTool === 'templates' && renderTemplateForm()}
        {activeTool === 'analysis' && renderAnalysisForm()}
        
        {renderResults()}
      </div>
    </div>
  );
};

export default AgentTools; 
import React, { useState, useEffect } from 'react';
import { Search, Plus, Save, AlertTriangle, CheckCircle, Clock, Filter, Download, Edit, Trash2, Bot, Sparkles, MessageSquare, Settings } from 'lucide-react';
import AgentChat from './components/AgentChat';
import AgentTools from './components/AgentTools';

// Mock API functions - replace with actual API calls
const api = {
  searchCodes: async (query, type) => {
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 300));
    
    const mockCPTCodes = [
      { code: '99213', description: 'Office visit, established patient, low complexity' },
      { code: '99214', description: 'Office visit, established patient, moderate complexity' },
      { code: '99215', description: 'Office visit, established patient, high complexity' },
      { code: '99201', description: 'Office visit, new patient, straightforward' },
      { code: '99202', description: 'Office visit, new patient, low complexity' },
      { code: '93306', description: 'Echocardiogram, complete' },
      { code: '93015', description: 'Cardiovascular stress test' }
    ];
    
    const mockICDCodes = [
      { code: 'Z00.00', description: 'Encounter for general adult medical examination' },
      { code: 'M79.3', description: 'Panniculitis, unspecified' },
      { code: 'I10', description: 'Essential hypertension' },
      { code: 'E11.9', description: 'Type 2 diabetes mellitus without complications' },
      { code: 'J06.9', description: 'Acute upper respiratory infection, unspecified' },
      { code: 'I25.9', description: 'Chronic ischemic heart disease, unspecified' },
      { code: 'R06.02', description: 'Shortness of breath' }
    ];
    
    const codes = type === 'cpt' ? mockCPTCodes : mockICDCodes;
    return codes.filter(code => 
      code.code.toLowerCase().includes(query.toLowerCase()) ||
      code.description.toLowerCase().includes(query.toLowerCase())
    );
  },
  
  getTemplates: async (specialty) => {
    await new Promise(resolve => setTimeout(resolve, 200));
    return [
      {
        id: '1',
        name: 'Common Office Visits',
        codes: [
          { cpt: '99213', icd: 'Z00.00', description: 'Routine checkup' },
          { cpt: '99214', icd: 'I10', description: 'Hypertension follow-up' }
        ]
      },
      {
        id: '2',
        name: 'Diabetes Management',
        codes: [
          { cpt: '99214', icd: 'E11.9', description: 'Diabetes without complications' },
          { cpt: '99215', icd: 'E11.40', description: 'Diabetes with neuropathy' }
        ]
      },
      {
        id: '3',
        name: 'Cardiology Consults',
        codes: [
          { cpt: '93306', icd: 'I25.9', description: 'Echo for CAD' },
          { cpt: '93015', icd: 'R06.02', description: 'Stress test for SOB' }
        ]
      }
    ];
  },
  
  validateCharge: async (chargeData) => {
    await new Promise(resolve => setTimeout(resolve, 100));
    const errors = [];
    const warnings = [];
    
    if (!chargeData.cptCode) errors.push({ field: 'cptCode', message: 'CPT code is required' });
    if (!chargeData.icdCode) errors.push({ field: 'icdCode', message: 'ICD code is required' });
    
    // Mock validation rules
    if (chargeData.cptCode === '99215' && chargeData.icdCode === 'Z00.00') {
      warnings.push({ field: 'combination', message: 'High complexity visit for routine exam may be questioned' });
    }
    
    if (chargeData.cptCode === '93306' && !chargeData.icdCode?.startsWith('I')) {
      warnings.push({ field: 'combination', message: 'Echo typically requires cardiac diagnosis' });
    }
    
    return {
      isValid: errors.length === 0,
      errors,
      warnings
    };
  },
  
  saveCharge: async (chargeData) => {
    await new Promise(resolve => setTimeout(resolve, 500));
    return { 
      id: Math.random().toString(36), 
      ...chargeData, 
      status: 'draft', 
      createdAt: new Date() 
    };
  },

  getCharges: async (filters = {}) => {
    await new Promise(resolve => setTimeout(resolve, 300));
    
    // Mock charge data
    const mockCharges = [
      {
        id: '1',
        patientName: 'John Doe',
        patientMrn: 'MRN-001',
        encounterDate: '2024-08-12',
        cptCode: '99213',
        cptDescription: 'Office visit, established patient, low complexity',
        icdCode: 'I10',
        icdDescription: 'Essential hypertension',
        status: 'draft',
        capturedAt: '2024-08-12T10:30:00Z',
        amount: 150.00,
        providerName: 'Dr. Smith',
        units: 1,
        quantity: 1
      },
      {
        id: '2',
        patientName: 'Jane Smith',
        patientMrn: 'MRN-002',
        encounterDate: '2024-08-12',
        cptCode: '99214',
        cptDescription: 'Office visit, established patient, moderate complexity',
        icdCode: 'E11.9',
        icdDescription: 'Type 2 diabetes mellitus without complications',
        status: 'submitted',
        capturedAt: '2024-08-12T11:15:00Z',
        amount: 200.00,
        providerName: 'Dr. Johnson',
        units: 1,
        quantity: 1
      },
      {
        id: '3',
        patientName: 'Robert Wilson',
        patientMrn: 'MRN-003',
        encounterDate: '2024-08-11',
        cptCode: '93306',
        cptDescription: 'Echocardiogram, complete',
        icdCode: 'I25.9',
        icdDescription: 'Chronic ischemic heart disease, unspecified',
        status: 'billed',
        capturedAt: '2024-08-11T14:20:00Z',
        amount: 400.00,
        providerName: 'Dr. Davis',
        units: 1,
        quantity: 1
      }
    ];

    // Apply filters
    let filteredCharges = [...mockCharges];
    
    if (filters.status) {
      filteredCharges = filteredCharges.filter(charge => charge.status === filters.status);
    }
    
    if (filters.dateFrom) {
      filteredCharges = filteredCharges.filter(charge => charge.encounterDate >= filters.dateFrom);
    }
    
    if (filters.dateTo) {
      filteredCharges = filteredCharges.filter(charge => charge.encounterDate <= filters.dateTo);
    }

    return {
      charges: filteredCharges,
      totalCount: filteredCharges.length,
      page: 1,
      pageSize: 20,
      totalPages: 1
    };
  }
};

// Code search component
const CodeSearch = ({ type, value, onChange, placeholder, onSelect }) => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [showResults, setShowResults] = useState(false);

  useEffect(() => {
    if (query.length > 2) {
      setIsLoading(true);
      api.searchCodes(query, type).then(codes => {
        setResults(codes);
        setIsLoading(false);
        setShowResults(true);
      });
    } else {
      setResults([]);
      setShowResults(false);
    }
  }, [query, type]);

  const handleSelect = (code) => {
    onSelect(code);
    setQuery('');
    setShowResults(false);
  };

  return (
    <div className="relative">
      <div className="relative">
        <Search className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
        <input
          type="text"
          placeholder={placeholder}
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
        />
      </div>
      
      {showResults && (
        <div className="absolute z-10 w-full mt-1 bg-white border border-gray-300 rounded-lg shadow-lg max-h-60 overflow-y-auto">
          {isLoading ? (
            <div className="p-4 text-center text-gray-500">Searching...</div>
          ) : results.length > 0 ? (
            results.map((code, index) => (
              <div
                key={index}
                onClick={() => handleSelect(code)}
                className="p-3 hover:bg-gray-50 cursor-pointer border-b border-gray-100 last:border-b-0"
              >
                <div className="font-medium text-gray-900">{code.code}</div>
                <div className="text-sm text-gray-600">{code.description}</div>
              </div>
            ))
          ) : (
            <div className="p-4 text-center text-gray-500">No codes found</div>
          )}
        </div>
      )}
      
      {value && (
        <div className="mt-2 p-2 bg-blue-50 border border-blue-200 rounded">
          <div className="font-medium text-blue-900">{value.code}</div>
          <div className="text-sm text-blue-700">{value.description}</div>
        </div>
      )}
    </div>
  );
};

// Template selector component
const TemplateSelector = ({ specialty, onSelectTemplate }) => {
  const [templates, setTemplates] = useState([]);
  const [selectedTemplate, setSelectedTemplate] = useState('');

  useEffect(() => {
    if (specialty) {
      api.getTemplates(specialty).then(setTemplates);
    }
  }, [specialty]);

  const handleTemplateChange = (templateId) => {
    setSelectedTemplate(templateId);
    const template = templates.find(t => t.id === templateId);
    if (template) {
      onSelectTemplate(template);
    }
  };

  if (templates.length === 0) return null;

  return (
    <div className="mb-6">
      <label className="block text-sm font-medium text-gray-700 mb-2">
        Quick Templates
      </label>
      <select
        value={selectedTemplate}
        onChange={(e) => handleTemplateChange(e.target.value)}
        className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
      >
        <option value="">Select a template...</option>
        {templates.map(template => (
          <option key={template.id} value={template.id}>
            {template.name}
          </option>
        ))}
      </select>
    </div>
  );
};

// Validation alerts component
const ValidationAlerts = ({ validation }) => {
  if (!validation || (validation.errors.length === 0 && validation.warnings.length === 0)) {
    return null;
  }

  return (
    <div className="space-y-2">
      {validation.errors.map((error, index) => (
        <div key={index} className="flex items-center p-3 bg-red-50 border border-red-200 rounded-lg">
          <AlertTriangle className="h-4 w-4 text-red-500 mr-2" />
          <span className="text-red-700 text-sm">{error.message}</span>
        </div>
      ))}
      
      {validation.warnings.map((warning, index) => (
        <div key={index} className="flex items-center p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
          <AlertTriangle className="h-4 w-4 text-yellow-500 mr-2" />
          <span className="text-yellow-700 text-sm">{warning.message}</span>
        </div>
      ))}
    </div>
  );
};

// Main Charge Capture component
const ChargeCaptureInterface = () => {
  const [chargeData, setChargeData] = useState({
    cptCode: null,
    icdCode: null,
    modifiers: [],
    units: 1,
    quantity: 1,
    notes: ''
  });
  
  const [validation, setValidation] = useState(null);
  const [isValidating, setIsValidating] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [saveSuccess, setSaveSuccess] = useState(false);
  
  // Mock patient and encounter data
  const [currentPatient] = useState({
    id: '123',
    name: 'John Doe',
    mrn: 'MRN-001',
    dob: '1985-03-15'
  });
  
  const [currentEncounter] = useState({
    id: '456',
    date: '2024-08-12',
    type: 'Office Visit',
    provider: 'Dr. Smith'
  });

  const [specialty] = useState('Internal Medicine');

  // Auto-validate when charge data changes
  useEffect(() => {
    if (chargeData.cptCode || chargeData.icdCode) {
      setIsValidating(true);
      api.validateCharge(chargeData).then(result => {
        setValidation(result);
        setIsValidating(false);
      });
    }
  }, [chargeData]);

  const handleCodeSelect = (code, type) => {
    setChargeData(prev => ({
      ...prev,
      [type === 'cpt' ? 'cptCode' : 'icdCode']: code
    }));
  };

  const handleTemplateSelect = (template) => {
    if (template.codes.length > 0) {
      const templateCode = template.codes[0];
      setChargeData(prev => ({
        ...prev,
        cptCode: { code: templateCode.cpt, description: templateCode.description },
        icdCode: { code: templateCode.icd, description: templateCode.description }
      }));
    }
  };

  const handleSave = async () => {
    if (!validation?.isValid) return;
    
    setIsSaving(true);
    try {
      await api.saveCharge({
        ...chargeData,
        patientId: currentPatient.id,
        encounterId: currentEncounter.id
      });
      setSaveSuccess(true);
      setTimeout(() => setSaveSuccess(false), 3000);
    } catch (error) {
      console.error('Save failed:', error);
    } finally {
      setIsSaving(false);
    }
  };

  const canSave = validation?.isValid && chargeData.cptCode && chargeData.icdCode;

  return (
    <div className="max-w-4xl mx-auto p-6 bg-white">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900 mb-2">Charge Capture</h1>
        <div className="flex items-center space-x-4 text-sm text-gray-600">
          <span>Patient: <strong>{currentPatient.name}</strong></span>
          <span>MRN: <strong>{currentPatient.mrn}</strong></span>
          <span>Encounter: <strong>{currentEncounter.date}</strong></span>
          <span>Provider: <strong>{currentEncounter.provider}</strong></span>
        </div>
      </div>

      {/* Success Message */}
      {saveSuccess && (
        <div className="mb-6 flex items-center p-4 bg-green-50 border border-green-200 rounded-lg">
          <CheckCircle className="h-5 w-5 text-green-500 mr-2" />
          <span className="text-green-700">Charge saved successfully!</span>
        </div>
      )}

      {/* Template Selector */}
      <TemplateSelector 
        specialty={specialty}
        onSelectTemplate={handleTemplateSelect}
      />

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Left Column - Code Selection */}
        <div className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              CPT Code *
            </label>
            <CodeSearch
              type="cpt"
              value={chargeData.cptCode}
              placeholder="Search CPT codes..."
              onSelect={(code) => handleCodeSelect(code, 'cpt')}
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              ICD Code *
            </label>
            <CodeSearch
              type="icd"
              value={chargeData.icdCode}
              placeholder="Search ICD codes..."
              onSelect={(code) => handleCodeSelect(code, 'icd')}
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Units
              </label>
              <input
                type="number"
                min="1"
                value={chargeData.units}
                onChange={(e) => setChargeData(prev => ({ ...prev, units: parseInt(e.target.value) || 1 }))}
                className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Quantity
              </label>
              <input
                type="number"
                min="1"
                value={chargeData.quantity}
                onChange={(e) => setChargeData(prev => ({ ...prev, quantity: parseInt(e.target.value) || 1 }))}
                className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Notes (Optional)
            </label>
            <textarea
              value={chargeData.notes}
              onChange={(e) => setChargeData(prev => ({ ...prev, notes: e.target.value }))}
              rows={3}
              className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              placeholder="Add any additional notes about this charge..."
            />
          </div>
        </div>

        {/* Right Column - Validation & Actions */}
        <div className="space-y-6">
          {/* Validation Status */}
          <div className="bg-gray-50 rounded-lg p-4">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Validation Status</h3>
            
            {isValidating ? (
              <div className="flex items-center text-gray-600">
                <Clock className="h-4 w-4 mr-2 animate-spin" />
                <span>Validating...</span>
              </div>
            ) : validation ? (
              <div className="space-y-3">
                <div className="flex items-center">
                  {validation.isValid ? (
                    <>
                      <CheckCircle className="h-5 w-5 text-green-500 mr-2" />
                      <span className="text-green-700 font-medium">Valid charge</span>
                    </>
                  ) : (
                    <>
                      <AlertTriangle className="h-5 w-5 text-red-500 mr-2" />
                      <span className="text-red-700 font-medium">Validation issues found</span>
                    </>
                  )}
                </div>
                <ValidationAlerts validation={validation} />
              </div>
            ) : (
              <div className="text-gray-500">Enter codes to validate</div>
            )}
          </div>

          {/* Charge Summary */}
          {(chargeData.cptCode || chargeData.icdCode) && (
            <div className="bg-blue-50 rounded-lg p-4">
              <h3 className="text-lg font-medium text-gray-900 mb-4">Charge Summary</h3>
              <div className="space-y-2 text-sm">
                {chargeData.cptCode && (
                  <div>
                    <span className="font-medium">CPT:</span> {chargeData.cptCode.code} - {chargeData.cptCode.description}
                  </div>
                )}
                {chargeData.icdCode && (
                  <div>
                    <span className="font-medium">ICD:</span> {chargeData.icdCode.code} - {chargeData.icdCode.description}
                  </div>
                )}
                <div>
                  <span className="font-medium">Units:</span> {chargeData.units} × {chargeData.quantity}
                </div>
                {chargeData.notes && (
                  <div>
                    <span className="font-medium">Notes:</span> {chargeData.notes}
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Action Buttons */}
          <div className="space-y-3">
            <button
              onClick={handleSave}
              disabled={!canSave || isSaving}
              className={`w-full flex items-center justify-center px-4 py-2 rounded-lg font-medium ${
                canSave && !isSaving
                  ? 'bg-blue-600 hover:bg-blue-700 text-white'
                  : 'bg-gray-300 text-gray-500 cursor-not-allowed'
              }`}
            >
              {isSaving ? (
                <>
                  <Clock className="h-4 w-4 mr-2 animate-spin" />
                  Saving...
                </>
              ) : (
                <>
                  <Save className="h-4 w-4 mr-2" />
                  Save as Draft
                </>
              )}
            </button>
            
            <button
              onClick={handleSave}
              disabled={!canSave || isSaving}
              className={`w-full flex items-center justify-center px-4 py-2 rounded-lg font-medium border ${
                canSave && !isSaving
                  ? 'border-green-600 text-green-600 hover:bg-green-50'
                  : 'border-gray-300 text-gray-500 cursor-not-allowed'
              }`}
            >
              <CheckCircle className="h-4 w-4 mr-2" />
              Save & Submit
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

// Charge List component for viewing existing charges
const ChargeList = () => {
  const [charges, setCharges] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({
    status: '',
    dateFrom: '',
    dateTo: '',
    provider: ''
  });
  const [showFilters, setShowFilters] = useState(false);

  useEffect(() => {
    loadCharges();
  }, [filters]);

  const loadCharges = async () => {
    setLoading(true);
    try {
      const result = await api.getCharges(filters);
      setCharges(result.charges);
    } catch (error) {
      console.error('Failed to load charges:', error);
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'draft': return 'bg-yellow-100 text-yellow-800';
      case 'submitted': return 'bg-blue-100 text-blue-800';
      case 'billed': return 'bg-green-100 text-green-800';
      case 'rejected': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getStatusCounts = () => {
    const counts = charges.reduce((acc, charge) => {
      acc[charge.status] = (acc[charge.status] || 0) + 1;
      return acc;
    }, {});
    
    return {
      total: charges.length,
      draft: counts.draft || 0,
      submitted: counts.submitted || 0,
      billed: counts.billed || 0,
      rejected: counts.rejected || 0
    };
  };

  const statusCounts = getStatusCounts();

  return (
    <div className="max-w-6xl mx-auto p-6 bg-white">
      {/* Header */}
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Charge Management</h1>
        <div className="flex space-x-3">
          <button
            onClick={() => setShowFilters(!showFilters)}
            className="flex items-center px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
          >
            <Filter className="h-4 w-4 mr-2" />
            Filters
          </button>
          <button className="flex items-center px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700">
            <Download className="h-4 w-4 mr-2" />
            Export
          </button>
          <button className="flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
            <Plus className="h-4 w-4 mr-2" />
            New Charge
          </button>
        </div>
      </div>

      {/* Filters */}
      {showFilters && (
        <div className="bg-gray-50 rounded-lg p-4 mb-6">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Status</label>
              <select
                value={filters.status}
                onChange={(e) => setFilters(prev => ({ ...prev, status: e.target.value }))}
                className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              >
                <option value="">All Statuses</option>
                <option value="draft">Draft</option>
                <option value="submitted">Submitted</option>
                <option value="billed">Billed</option>
                <option value="rejected">Rejected</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Date From</label>
              <input
                type="date"
                value={filters.dateFrom}
                onChange={(e) => setFilters(prev => ({ ...prev, dateFrom: e.target.value }))}
                className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Date To</label>
              <input
                type="date"
                value={filters.dateTo}
                onChange={(e) => setFilters(prev => ({ ...prev, dateTo: e.target.value }))}
                className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Provider</label>
              <select
                value={filters.provider}
                onChange={(e) => setFilters(prev => ({ ...prev, provider: e.target.value }))}
                className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              >
                <option value="">All Providers</option>
                <option value="dr-smith">Dr. Smith</option>
                <option value="dr-johnson">Dr. Johnson</option>
                <option value="dr-davis">Dr. Davis</option>
              </select>
            </div>
          </div>
        </div>
      )}

      {/* Statistics */}
      <div className="grid grid-cols-1 md:grid-cols-5 gap-4 mb-6">
        <div className="bg-blue-50 rounded-lg p-4">
          <div className="text-2xl font-bold text-blue-600">{statusCounts.total}</div>
          <div className="text-sm text-blue-600">Total Charges</div>
        </div>
        <div className="bg-yellow-50 rounded-lg p-4">
          <div className="text-2xl font-bold text-yellow-600">{statusCounts.draft}</div>
          <div className="text-sm text-yellow-600">Draft</div>
        </div>
        <div className="bg-blue-50 rounded-lg p-4">
          <div className="text-2xl font-bold text-blue-600">{statusCounts.submitted}</div>
          <div className="text-sm text-blue-600">Submitted</div>
        </div>
        <div className="bg-green-50 rounded-lg p-4">
          <div className="text-2xl font-bold text-green-600">{statusCounts.billed}</div>
          <div className="text-sm text-green-600">Billed</div>
        </div>
        <div className="bg-red-50 rounded-lg p-4">
          <div className="text-2xl font-bold text-red-600">{statusCounts.rejected}</div>
          <div className="text-sm text-red-600">Rejected</div>
        </div>
      </div>

      {/* Charges Table */}
      {loading ? (
        <div className="bg-white rounded-lg border border-gray-200 p-8">
          <div className="flex items-center justify-center">
            <Clock className="h-6 w-6 mr-2 animate-spin" />
            <span>Loading charges...</span>
          </div>
        </div>
      ) : (
        <div className="bg-white rounded-lg border border-gray-200 overflow-hidden">
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Patient
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Encounter Date
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Codes
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Provider
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Amount
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Status
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Captured
                  </th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {charges.map((charge) => (
                  <tr key={charge.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm font-medium text-gray-900">{charge.patientName}</div>
                      <div className="text-sm text-gray-500">{charge.patientMrn}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-900">
                        {new Date(charge.encounterDate).toLocaleDateString()}
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <div className="text-sm text-gray-900">
                        <div className="font-medium">CPT: {charge.cptCode}</div>
                        <div className="text-gray-600">{charge.cptDescription}</div>
                        <div className="font-medium mt-1">ICD: {charge.icdCode}</div>
                        <div className="text-gray-600">{charge.icdDescription}</div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-900">{charge.providerName}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-900">${charge.amount.toFixed(2)}</div>
                      <div className="text-sm text-gray-500">{charge.units}u × {charge.quantity}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getStatusColor(charge.status)}`}>
                        {charge.status.charAt(0).toUpperCase() + charge.status.slice(1)}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-900">
                        {new Date(charge.capturedAt).toLocaleDateString()}
                      </div>
                      <div className="text-sm text-gray-500">
                        {new Date(charge.capturedAt).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                      <div className="flex justify-end space-x-2">
                        <button className="text-blue-600 hover:text-blue-900 p-1">
                          <Edit className="h-4 w-4" />
                        </button>
                        <button className="text-red-600 hover:text-red-900 p-1">
                          <Trash2 className="h-4 w-4" />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {charges.length === 0 && (
            <div className="p-8 text-center text-gray-500">
              No charges found matching your criteria.
            </div>
          )}
        </div>
      )}

      {/* Pagination */}
      {charges.length > 0 && (
        <div className="flex items-center justify-between mt-6">
          <div className="text-sm text-gray-700">
            Showing <span className="font-medium">1</span> to <span className="font-medium">{charges.length}</span> of{' '}
            <span className="font-medium">{charges.length}</span> results
          </div>
          <div className="flex space-x-2">
            <button className="px-3 py-1 border border-gray-300 rounded hover:bg-gray-50 disabled:opacity-50" disabled>
              Previous
            </button>
            <button className="px-3 py-1 bg-blue-600 text-white rounded">1</button>
            <button className="px-3 py-1 border border-gray-300 rounded hover:bg-gray-50 disabled:opacity-50" disabled>
              Next
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

// Reports Dashboard component
const ReportsDashboard = () => {
  const [dateRange, setDateRange] = useState({
    from: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0], // 30 days ago
    to: new Date().toISOString().split('T')[0] // today
  });

  const [metrics, setMetrics] = useState({
    totalCharges: 156,
    averageChargeAmount: 185.50,
    captureRate: 94.2,
    averageCaptureTime: 3.2, // minutes
    topProviders: [
      { name: 'Dr. Smith', charges: 45, rate: 96.8 },
      { name: 'Dr. Johnson', charges: 38, rate: 92.1 },
      { name: 'Dr. Davis', charges: 32, rate: 98.5 }
    ],
    topCPTCodes: [
      { code: '99213', count: 42, description: 'Office visit, established patient' },
      { code: '99214', count: 28, description: 'Office visit, moderate complexity' },
      { code: '93306', count: 15, description: 'Echocardiogram' }
    ],
    chargesByStatus: {
      draft: 12,
      submitted: 28,
      billed: 98,
      rejected: 8
    }
  });

  return (
    <div className="max-w-7xl mx-auto p-6 bg-white">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900 mb-4">Charge Capture Analytics</h1>
        
        {/* Date Range Selector */}
        <div className="flex items-center space-x-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">From</label>
            <input
              type="date"
              value={dateRange.from}
              onChange={(e) => setDateRange(prev => ({ ...prev, from: e.target.value }))}
              className="p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">To</label>
            <input
              type="date"
              value={dateRange.to}
              onChange={(e) => setDateRange(prev => ({ ...prev, to: e.target.value }))}
              className="p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <button className="mt-6 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
            Update Report
          </button>
        </div>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div className="bg-blue-50 rounded-lg p-6">
          <div className="text-3xl font-bold text-blue-600">{metrics.totalCharges}</div>
          <div className="text-sm text-blue-600">Total Charges</div>
          <div className="text-xs text-gray-500 mt-1">Last 30 days</div>
        </div>
        <div className="bg-green-50 rounded-lg p-6">
          <div className="text-3xl font-bold text-green-600">${metrics.averageChargeAmount}</div>
          <div className="text-sm text-green-600">Avg Charge Amount</div>
          <div className="text-xs text-gray-500 mt-1">Per encounter</div>
        </div>
        <div className="bg-purple-50 rounded-lg p-6">
          <div className="text-3xl font-bold text-purple-600">{metrics.captureRate}%</div>
          <div className="text-sm text-purple-600">Capture Rate</div>
          <div className="text-xs text-gray-500 mt-1">Encounters with charges</div>
        </div>
        <div className="bg-orange-50 rounded-lg p-6">
          <div className="text-3xl font-bold text-orange-600">{metrics.averageCaptureTime}m</div>
          <div className="text-sm text-orange-600">Avg Capture Time</div>
          <div className="text-xs text-gray-500 mt-1">From encounter to charge</div>
        </div>
      </div>

      {/* Charts and Tables */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Provider Performance */}
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Top Performing Providers</h3>
          <div className="space-y-4">
            {metrics.topProviders.map((provider, index) => (
              <div key={index} className="flex items-center justify-between">
                <div>
                  <div className="font-medium text-gray-900">{provider.name}</div>
                  <div className="text-sm text-gray-500">{provider.charges} charges</div>
                </div>
                <div className="text-right">
                  <div className="font-medium text-gray-900">{provider.rate}%</div>
                  <div className="text-sm text-gray-500">capture rate</div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Top CPT Codes */}
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Most Used CPT Codes</h3>
          <div className="space-y-4">
            {metrics.topCPTCodes.map((code, index) => (
              <div key={index} className="flex items-center justify-between">
                <div>
                  <div className="font-medium text-gray-900">{code.code}</div>
                  <div className="text-sm text-gray-500">{code.description}</div>
                </div>
                <div className="text-right">
                  <div className="font-medium text-gray-900">{code.count}</div>
                  <div className="text-sm text-gray-500">uses</div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Charge Status Distribution */}
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Charge Status Distribution</h3>
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <div className="flex items-center">
                <div className="w-3 h-3 bg-green-500 rounded-full mr-2"></div>
                <span className="text-sm text-gray-700">Billed</span>
              </div>
              <span className="font-medium">{metrics.chargesByStatus.billed}</span>
            </div>
            <div className="flex items-center justify-between">
              <div className="flex items-center">
                <div className="w-3 h-3 bg-blue-500 rounded-full mr-2"></div>
                <span className="text-sm text-gray-700">Submitted</span>
              </div>
              <span className="font-medium">{metrics.chargesByStatus.submitted}</span>
            </div>
            <div className="flex items-center justify-between">
              <div className="flex items-center">
                <div className="w-3 h-3 bg-yellow-500 rounded-full mr-2"></div>
                <span className="text-sm text-gray-700">Draft</span>
              </div>
              <span className="font-medium">{metrics.chargesByStatus.draft}</span>
            </div>
            <div className="flex items-center justify-between">
              <div className="flex items-center">
                <div className="w-3 h-3 bg-red-500 rounded-full mr-2"></div>
                <span className="text-sm text-gray-700">Rejected</span>
              </div>
              <span className="font-medium">{metrics.chargesByStatus.rejected}</span>
            </div>
          </div>
        </div>

        {/* Missed Charges Alert */}
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Missed Charges Alert</h3>
          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
            <div className="flex items-center">
              <AlertTriangle className="h-5 w-5 text-yellow-500 mr-2" />
              <div>
                <div className="font-medium text-yellow-800">5 Encounters Missing Charges</div>
                <div className="text-sm text-yellow-700">Encounters completed but no charges captured</div>
              </div>
            </div>
            <button className="mt-3 text-sm text-yellow-800 hover:text-yellow-900 font-medium">
              View Details →
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

// Main App component that combines all interfaces
const ChargeCaptureApp = () => {
  const [currentView, setCurrentView] = useState('capture'); // 'capture', 'list', 'reports', 'ai-assistant'
  const [aiAssistantTab, setAiAssistantTab] = useState('chat'); // 'chat', 'tools'

  const renderCurrentView = () => {
    switch (currentView) {
      case 'capture':
        return <ChargeCaptureInterface />;
      case 'list':
        return <ChargeList />;
      case 'reports':
        return <ReportsDashboard />;
      case 'ai-assistant':
        return <AIAssistantInterface />;
      default:
        return <ChargeCaptureInterface />;
    }
  };

  // AI Assistant Interface Component
  const AIAssistantInterface = () => {
    return (
      <div className="space-y-6">
        {/* Header */}
        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="p-3 bg-gradient-to-r from-blue-500 to-indigo-600 rounded-lg">
                <Bot className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">AI Charge Capture Assistant</h1>
                <p className="text-gray-600">
                  Intelligent automation for charge capture and analysis
                </p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                <span className="text-sm text-gray-600">AI Agent Online</span>
              </div>
              <div className="flex items-center space-x-2">
                <Sparkles className="w-4 h-4 text-blue-600" />
                <span className="text-sm text-gray-600">Enhanced Mode</span>
              </div>
            </div>
          </div>
        </div>

        {/* Navigation Tabs */}
        <div className="bg-white rounded-lg shadow-sm border">
          <div className="border-b border-gray-200">
            <nav className="flex space-x-8 px-6">
              <button
                onClick={() => setAiAssistantTab('chat')}
                className={`py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
                  aiAssistantTab === 'chat'
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                <div className="flex items-center space-x-2">
                  <MessageSquare className="w-4 h-4" />
                  <span>AI Assistant</span>
                </div>
              </button>
              <button
                onClick={() => setAiAssistantTab('tools')}
                className={`py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
                  aiAssistantTab === 'tools'
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                <div className="flex items-center space-x-2">
                  <Settings className="w-4 h-4" />
                  <span>AI Tools</span>
                </div>
              </button>
            </nav>
          </div>

          {/* Content */}
          <div className="p-6">
            <div className="h-[600px]">
              {aiAssistantTab === 'chat' ? <AgentChat /> : <AgentTools />}
            </div>
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Navigation */}
      <nav className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <h1 className="text-xl font-semibold text-gray-900">Practice Management System</h1>
              </div>
              <div className="ml-10 flex space-x-8">
                <button
                  onClick={() => setCurrentView('capture')}
                  className={`${
                    currentView === 'capture'
                      ? 'border-blue-500 text-gray-900'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  } border-b-2 py-4 px-1 text-sm font-medium`}
                >
                  Charge Capture
                </button>
                <button
                  onClick={() => setCurrentView('list')}
                  className={`${
                    currentView === 'list'
                      ? 'border-blue-500 text-gray-900'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  } border-b-2 py-4 px-1 text-sm font-medium`}
                >
                  Charge Management
                </button>
                <button
                  onClick={() => setCurrentView('reports')}
                  className={`${
                    currentView === 'reports'
                      ? 'border-blue-500 text-gray-900'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  } border-b-2 py-4 px-1 text-sm font-medium`}
                >
                  Reports & Analytics
                </button>
                <button
                  onClick={() => setCurrentView('ai-assistant')}
                  className={`${
                    currentView === 'ai-assistant'
                      ? 'border-blue-500 text-gray-900'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  } border-b-2 py-4 px-1 text-sm font-medium`}
                >
                  AI Assistant
                </button>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <div className="text-sm text-gray-500">
                <span className="font-medium">Dr. Smith</span> | Internal Medicine
              </div>
              <div className="h-8 w-8 bg-blue-500 rounded-full flex items-center justify-center text-white text-sm font-medium">
                DS
              </div>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="py-8">
        {renderCurrentView()}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 py-4">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center text-sm text-gray-500">
            Charge Capture System v1.0 | Last updated: {new Date().toLocaleDateString()}
          </div>
        </div>
      </footer>
    </div>
  );
};

export default ChargeCaptureApp;

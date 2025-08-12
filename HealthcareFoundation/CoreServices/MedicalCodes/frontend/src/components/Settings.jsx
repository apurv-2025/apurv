import React, { useState, useEffect } from 'react';
import { Settings as SettingsIcon, Database, RefreshCw, Download, Upload, AlertCircle, CheckCircle, Clock, Activity, ExternalLink, FileText, FileJson } from 'lucide-react';

const Settings = () => {
  const [comprehensiveStats, setComprehensiveStats] = useState(null);
  const [syncStatus, setSyncStatus] = useState({});
  const [loading, setLoading] = useState(false);
  const [lastUpdate, setLastUpdate] = useState(null);
  const [dataSources, setDataSources] = useState({});
  const [specialties, setSpecialties] = useState({});
  const [healthStatus, setHealthStatus] = useState({});
  const [exportStats, setExportStats] = useState({});
  const [exportOptions, setExportOptions] = useState({
    format: 'json',
    formatType: 'detailed',
    specialtyFilter: '',
    includeSummary: true
  });
  
  // New state for interactive specialty browser
  const [selectedSpecialty, setSelectedSpecialty] = useState(null);
  const [specialtyCodes, setSpecialtyCodes] = useState({});
  const [loadingSpecialtyCodes, setLoadingSpecialtyCodes] = useState(false);
  const [selectedCode, setSelectedCode] = useState(null);
  const [showCodeModal, setShowCodeModal] = useState(false);

  const API_BASE = 'http://localhost:8003/api';

  useEffect(() => {
    fetchComprehensiveStats();
    fetchDataSources();
    fetchSpecialties();
    fetchHealthStatus();
    fetchExportStats();
  }, []);

  const fetchExportStats = async () => {
    try {
      const response = await fetch(`${API_BASE}/export/stats`);
      if (response.ok) {
        const data = await response.json();
        setExportStats(data.export_stats);
      }
    } catch (error) {
      console.error('Error fetching export stats:', error);
    }
  };

  // New functions for interactive specialty browser
  const handleSpecialtyClick = async (specialty) => {
    setSelectedSpecialty(specialty);
    setLoadingSpecialtyCodes(true);
    
    try {
      const response = await fetch(`${API_BASE}/comprehensive/search?specialty=${encodeURIComponent(specialty)}`);
      if (response.ok) {
        const data = await response.json();
        setSpecialtyCodes(data.results);
      } else {
        setSpecialtyCodes({});
      }
    } catch (error) {
      console.error('Error fetching specialty codes:', error);
      setSpecialtyCodes({});
    } finally {
      setLoadingSpecialtyCodes(false);
    }
  };

  const handleCodeClick = (code, codeType) => {
    setSelectedCode({ ...code, codeType });
    setShowCodeModal(true);
  };

  const closeCodeModal = () => {
    setShowCodeModal(false);
    setSelectedCode(null);
  };

  const closeSpecialtyView = () => {
    setSelectedSpecialty(null);
    setSpecialtyCodes({});
  };

  const getCodeTypeColor = (codeType) => {
    switch (codeType) {
      case 'cpt_codes': return 'bg-blue-100 text-blue-700';
      case 'icd10_codes': return 'bg-green-100 text-green-700';
      case 'hcpcs_codes': return 'bg-purple-100 text-purple-700';
      case 'modifier_codes': return 'bg-orange-100 text-orange-700';
      default: return 'bg-gray-100 text-gray-700';
    }
  };

  const getCodeTypeLabel = (codeType) => {
    switch (codeType) {
      case 'cpt_codes': return 'CPT';
      case 'icd10_codes': return 'ICD-10';
      case 'hcpcs_codes': return 'HCPCS';
      case 'modifier_codes': return 'MODIFIER';
      default: return codeType.toUpperCase();
    }
  };

  const exportToJson = async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams({
        format_type: exportOptions.formatType
      });
      
      if (exportOptions.specialtyFilter) {
        params.append('specialty_filter', exportOptions.specialtyFilter);
      }
      
      const response = await fetch(`${API_BASE}/export/json?${params}`);
      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = response.headers.get('content-disposition')?.split('filename=')[1] || 'medical_codes_export.json';
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        
        setSyncStatus({ type: 'success', message: 'JSON export completed successfully' });
      } else {
        setSyncStatus({ type: 'error', message: 'Failed to export JSON' });
      }
    } catch (error) {
      setSyncStatus({ type: 'error', message: 'Error exporting JSON' });
    } finally {
      setLoading(false);
    }
  };

  const exportToPdf = async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams({
        include_summary: exportOptions.includeSummary.toString()
      });
      
      if (exportOptions.specialtyFilter) {
        params.append('specialty_filter', exportOptions.specialtyFilter);
      }
      
      const response = await fetch(`${API_BASE}/export/pdf?${params}`);
      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = response.headers.get('content-disposition')?.split('filename=')[1] || 'medical_codes_export.pdf';
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        
        setSyncStatus({ type: 'success', message: 'PDF export completed successfully' });
      } else {
        setSyncStatus({ type: 'error', message: 'Failed to export PDF' });
      }
    } catch (error) {
      setSyncStatus({ type: 'error', message: 'Error exporting PDF' });
    } finally {
      setLoading(false);
    }
  };

  const fetchComprehensiveStats = async () => {
    try {
      const response = await fetch(`${API_BASE}/comprehensive/stats`);
      if (response.ok) {
        const data = await response.json();
        setComprehensiveStats(data.database_stats);
        setDataSources(data.data_sources);
      }
    } catch (error) {
      console.error('Error fetching comprehensive stats:', error);
    }
  };

  const fetchDataSources = async () => {
    try {
      const response = await fetch(`${API_BASE}/sync/sources`);
      if (response.ok) {
        const data = await response.json();
        setDataSources(data.sources);
      }
    } catch (error) {
      console.error('Error fetching data sources:', error);
    }
  };

  const fetchSpecialties = async () => {
    try {
      const response = await fetch(`${API_BASE}/comprehensive/specialties`);
      if (response.ok) {
        const data = await response.json();
        setSpecialties(data.specialties);
      }
    } catch (error) {
      console.error('Error fetching specialties:', error);
    }
  };

  const fetchHealthStatus = async () => {
    try {
      const response = await fetch(`${API_BASE}/comprehensive/health`);
      if (response.ok) {
        const data = await response.json();
        setHealthStatus(data);
      }
    } catch (error) {
      console.error('Error fetching health status:', error);
    }
  };

  const loadComprehensiveDatabase = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE}/comprehensive/load`, {
        method: 'POST'
      });
      if (response.ok) {
        const data = await response.json();
        setSyncStatus({ type: 'success', message: 'Comprehensive database loaded successfully', data });
        fetchComprehensiveStats();
      } else {
        setSyncStatus({ type: 'error', message: 'Failed to load comprehensive database' });
      }
    } catch (error) {
      setSyncStatus({ type: 'error', message: 'Error loading comprehensive database' });
    } finally {
      setLoading(false);
    }
  };

  const syncFromOfficialSources = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE}/sync/start`, {
        method: 'POST'
      });
      if (response.ok) {
        const data = await response.json();
        setSyncStatus({ type: 'success', message: 'Data synchronization started', data });
      } else {
        setSyncStatus({ type: 'error', message: 'Failed to start data synchronization' });
      }
    } catch (error) {
      setSyncStatus({ type: 'error', message: 'Error starting data synchronization' });
    } finally {
      setLoading(false);
    }
  };

  const scrapeToDatabase = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE}/sync/scrape-to-database?save_to_db=true&save_to_file=false`, {
        method: 'POST'
      });
      if (response.ok) {
        const data = await response.json();
        setSyncStatus({ type: 'success', message: 'Data scraping completed', data });
        fetchComprehensiveStats();
      } else {
        setSyncStatus({ type: 'error', message: 'Failed to scrape data' });
      }
    } catch (error) {
      setSyncStatus({ type: 'error', message: 'Error scraping data' });
    } finally {
      setLoading(false);
    }
  };

  const StatusCard = ({ icon: Icon, title, value, subtitle, color, status }) => (
    <div className={`bg-white rounded-lg shadow-sm p-6 border-l-4 ${color}`}>
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-gray-600">{title}</p>
          <p className="text-3xl font-bold text-gray-900 mt-1">
            {typeof value === 'number' ? value.toLocaleString() : value}
          </p>
          {subtitle && <p className="text-sm text-gray-500 mt-1">{subtitle}</p>}
          {status && (
            <div className="flex items-center gap-2 mt-2">
              {status === 'healthy' ? (
                <CheckCircle className="w-4 h-4 text-green-500" />
              ) : (
                <AlertCircle className="w-4 h-4 text-red-500" />
              )}
              <span className={`text-xs font-medium ${
                status === 'healthy' ? 'text-green-600' : 'text-red-600'
              }`}>
                {status === 'healthy' ? 'Healthy' : 'Needs Attention'}
              </span>
            </div>
          )}
        </div>
        <div className="p-3 rounded-lg bg-blue-100">
          <Icon className="w-6 h-6 text-blue-600" />
        </div>
      </div>
    </div>
  );

  const ActionButton = ({ icon: Icon, title, description, onClick, loading, variant = 'primary' }) => (
    <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-200">
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <div className="flex items-center gap-3 mb-2">
            <div className={`p-2 rounded-lg ${
              variant === 'primary' ? 'bg-blue-100' : 
              variant === 'success' ? 'bg-green-100' : 
              variant === 'warning' ? 'bg-yellow-100' : 'bg-gray-100'
            }`}>
              <Icon className={`w-5 h-5 ${
                variant === 'primary' ? 'text-blue-600' : 
                variant === 'success' ? 'text-green-600' : 
                variant === 'warning' ? 'text-yellow-600' : 'text-gray-600'
              }`} />
            </div>
            <h3 className="text-lg font-semibold text-gray-900">{title}</h3>
          </div>
          <p className="text-sm text-gray-600 mb-4">{description}</p>
          <button
            onClick={onClick}
            disabled={loading}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              variant === 'primary' ? 'bg-blue-600 hover:bg-blue-700 text-white' :
              variant === 'success' ? 'bg-green-600 hover:bg-green-700 text-white' :
              variant === 'warning' ? 'bg-yellow-600 hover:bg-yellow-700 text-white' :
              'bg-gray-600 hover:bg-gray-700 text-white'
            } disabled:opacity-50 disabled:cursor-not-allowed`}
          >
            {loading ? 'Processing...' : 'Execute'}
          </button>
        </div>
      </div>
    </div>
  );

  const DataSourceCard = ({ source, data }) => (
    <div className="bg-white rounded-lg shadow-sm p-4 border border-gray-200">
      <div className="flex items-center justify-between mb-3">
        <h4 className="font-semibold text-gray-900">{source.name}</h4>
        <span className={`px-2 py-1 rounded text-xs font-medium ${
          source.license_required ? 'bg-orange-100 text-orange-700' : 'bg-green-100 text-green-700'
        }`}>
          {source.license_required ? 'License Required' : 'Free Access'}
        </span>
      </div>
      <p className="text-sm text-gray-600 mb-2">{source.description}</p>
      <div className="flex items-center justify-between text-xs text-gray-500">
        <span>Estimated Codes: {source.estimated_codes?.toLocaleString()}</span>
        <a 
          href={source.url} 
          target="_blank" 
          rel="noopener noreferrer"
          className="text-blue-600 hover:text-blue-700 flex items-center gap-1"
        >
          Visit Source
          <ExternalLink className="w-3 h-3" />
        </a>
      </div>
    </div>
  );

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex items-center gap-3 mb-6">
        <div className="p-2 bg-blue-600 rounded-lg">
          <SettingsIcon className="w-6 h-6 text-white" />
        </div>
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Settings & Data Management</h1>
          <p className="text-sm text-gray-600">Manage comprehensive database and synchronization</p>
        </div>
      </div>

      {/* Status Overview */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatusCard
          icon={Database}
          title="Total Codes"
          value={comprehensiveStats?.total_codes || 0}
          subtitle="Comprehensive Database"
          color="border-l-blue-500"
          status={healthStatus?.status}
        />
        <StatusCard
          icon={Activity}
          title="CPT Codes"
          value={comprehensiveStats?.total_cpt_codes || 0}
          subtitle="Current Procedural Terminology"
          color="border-l-green-500"
        />
        <StatusCard
          icon={Activity}
          title="ICD-10 Codes"
          value={comprehensiveStats?.total_icd10_codes || 0}
          subtitle="International Classification"
          color="border-l-purple-500"
        />
        <StatusCard
          icon={Activity}
          title="HCPCS Codes"
          value={comprehensiveStats?.total_hcpcs_codes || 0}
          subtitle="Healthcare Common Procedure"
          color="border-l-orange-500"
        />
      </div>

      {/* Data Synchronization Actions */}
      <div className="bg-white rounded-lg shadow-sm p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-6">Data Synchronization</h2>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <ActionButton
            icon={Database}
            title="Load Comprehensive Database"
            description="Load the comprehensive medical codes database into local cache for fast searching"
            onClick={loadComprehensiveDatabase}
            loading={loading}
            variant="primary"
          />
          
          <ActionButton
            icon={RefreshCw}
            title="Sync from Official Sources"
            description="Synchronize data from official AMA, CMS, and other authoritative sources"
            onClick={syncFromOfficialSources}
            loading={loading}
            variant="success"
          />
          
          <ActionButton
            icon={Download}
            title="Scrape to Database"
            description="Scrape latest codes from official websites and save to local database"
            onClick={scrapeToDatabase}
            loading={loading}
            variant="warning"
          />
        </div>

        {/* Status Messages */}
        {syncStatus.message && (
          <div className={`mt-6 p-4 rounded-lg ${
            syncStatus.type === 'success' ? 'bg-green-50 border border-green-200' : 'bg-red-50 border border-red-200'
          }`}>
            <div className="flex items-center gap-2">
              {syncStatus.type === 'success' ? (
                <CheckCircle className="w-5 h-5 text-green-600" />
              ) : (
                <AlertCircle className="w-5 h-5 text-red-600" />
              )}
              <span className={`font-medium ${
                syncStatus.type === 'success' ? 'text-green-800' : 'text-red-800'
              }`}>
                {syncStatus.message}
              </span>
            </div>
            {syncStatus.data && (
              <pre className="mt-2 text-sm text-gray-600 bg-white p-2 rounded border">
                {JSON.stringify(syncStatus.data, null, 2)}
              </pre>
            )}
          </div>
        )}
      </div>

      {/* Data Sources */}
      <div className="bg-white rounded-lg shadow-sm p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-6">Official Data Sources</h2>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {Object.entries(dataSources).map(([key, source]) => (
            <DataSourceCard key={key} source={source} />
          ))}
        </div>
      </div>

      {/* Available Specialties */}
      <div className="bg-white rounded-lg shadow-sm p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-6">Available Medical Specialties</h2>
        
        {!selectedSpecialty ? (
          // Specialty Grid View
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {specialties.sample_specialties?.map((specialty, index) => (
              <button
                key={index}
                onClick={() => handleSpecialtyClick(specialty)}
                className="bg-gray-50 rounded-lg p-4 border border-gray-200 hover:bg-blue-50 hover:border-blue-300 transition-colors text-left group"
              >
                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium text-gray-700 group-hover:text-blue-700">{specialty}</span>
                  <span className="text-xs text-gray-400 group-hover:text-blue-400">→</span>
                </div>
                <p className="text-xs text-gray-500 mt-1">Click to view codes</p>
              </button>
            ))}
          </div>
        ) : (
          // Specialty Codes View
          <div className="space-y-6">
            {/* Header */}
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-lg font-semibold text-gray-900">{selectedSpecialty} Codes</h3>
                <p className="text-sm text-gray-600">Click on any code to view details</p>
              </div>
              <button
                onClick={closeSpecialtyView}
                className="px-4 py-2 text-sm text-gray-600 hover:text-gray-900 font-medium"
              >
                ← Back to Specialties
              </button>
            </div>

            {/* Loading State */}
            {loadingSpecialtyCodes && (
              <div className="flex items-center justify-center py-8">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
                <span className="ml-3 text-gray-600">Loading codes...</span>
              </div>
            )}

            {/* Codes Display */}
            {!loadingSpecialtyCodes && (
              <div className="space-y-6">
                {Object.entries(specialtyCodes).map(([codeType, codes]) => {
                  if (!codes || codes.length === 0) return null;
                  
                  return (
                    <div key={codeType} className="space-y-3">
                      <div className="flex items-center gap-2">
                        <span className={`px-2 py-1 rounded text-xs font-medium ${getCodeTypeColor(codeType)}`}>
                          {getCodeTypeLabel(codeType)}
                        </span>
                        <span className="text-sm text-gray-600">({codes.length} codes)</span>
                      </div>
                      
                      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                        {codes.map((code, index) => (
                          <button
                            key={index}
                            onClick={() => handleCodeClick(code, codeType)}
                            className="bg-white border border-gray-200 rounded-lg p-3 hover:bg-blue-50 hover:border-blue-300 transition-colors text-left group"
                          >
                            <div className="flex items-start justify-between">
                              <div className="flex-1">
                                <div className="font-mono font-bold text-sm text-gray-900 group-hover:text-blue-700">
                                  {code.code || code.modifier}
                                </div>
                                <div className="text-xs text-gray-600 mt-1 line-clamp-2">
                                  {code.description}
                                </div>
                              </div>
                              <span className="text-xs text-gray-400 group-hover:text-blue-400 ml-2">→</span>
                            </div>
                          </button>
                        ))}
                      </div>
                    </div>
                  );
                })}
                
                {Object.keys(specialtyCodes).length === 0 && (
                  <div className="text-center py-8 text-gray-500">
                    No codes found for this specialty.
                  </div>
                )}
              </div>
            )}
          </div>
        )}
      </div>

      {/* Database Health */}
      <div className="bg-white rounded-lg shadow-sm p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-6">Database Health</h2>
        
        <div className="space-y-4">
          <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
            <div className="flex items-center gap-3">
              <div className={`p-2 rounded-lg ${
                healthStatus?.status === 'healthy' ? 'bg-green-100' : 'bg-red-100'
              }`}>
                {healthStatus?.status === 'healthy' ? (
                  <CheckCircle className="w-5 h-5 text-green-600" />
                ) : (
                  <AlertCircle className="w-5 h-5 text-red-600" />
                )}
              </div>
              <div>
                <p className="font-medium text-gray-900">Comprehensive Database Status</p>
                <p className="text-sm text-gray-600">
                  {healthStatus?.status === 'healthy' ? 'All systems operational' : 'Database needs attention'}
                </p>
              </div>
            </div>
            <span className={`px-3 py-1 rounded-full text-xs font-medium ${
              healthStatus?.status === 'healthy' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'
            }`}>
              {healthStatus?.status || 'Unknown'}
            </span>
          </div>
          
          {comprehensiveStats?.last_updated && (
            <div className="flex items-center gap-3 p-4 bg-blue-50 rounded-lg">
              <Clock className="w-5 h-5 text-blue-600" />
              <div>
                <p className="font-medium text-gray-900">Last Updated</p>
                <p className="text-sm text-gray-600">
                  {new Date(comprehensiveStats.last_updated).toLocaleString()}
                </p>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Export Section */}
      <div className="bg-white rounded-lg shadow-sm p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-6">Export Medical Codes</h2>
        
        {/* Export Statistics */}
        <div className="mb-6">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Export Statistics</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <div className="bg-blue-50 rounded-lg p-4 border border-blue-200">
              <div className="text-2xl font-bold text-blue-600">{exportStats.total_specialties || 0}</div>
              <div className="text-sm text-blue-700">Total Specialties</div>
            </div>
            <div className="bg-green-50 rounded-lg p-4 border border-green-200">
              <div className="text-2xl font-bold text-green-600">{exportStats.total_codes || 0}</div>
              <div className="text-sm text-green-700">Total Codes</div>
            </div>
            <div className="bg-purple-50 rounded-lg p-4 border border-purple-200">
              <div className="text-2xl font-bold text-purple-600">2</div>
              <div className="text-sm text-purple-700">Export Formats</div>
            </div>
            <div className="bg-orange-50 rounded-lg p-4 border border-orange-200">
              <div className="text-2xl font-bold text-orange-600">{Object.keys(exportStats.specialties || {}).length}</div>
              <div className="text-sm text-orange-700">Available Specialties</div>
            </div>
          </div>
        </div>

        {/* Export Options */}
        <div className="mb-6">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Export Options</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {/* Format Selection */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Export Format</label>
              <select
                value={exportOptions.format}
                onChange={(e) => setExportOptions({...exportOptions, format: e.target.value})}
                className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="json">JSON</option>
                <option value="pdf">PDF</option>
              </select>
            </div>

            {/* Format Type (JSON only) */}
            {exportOptions.format === 'json' && (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">JSON Format</label>
                <select
                  value={exportOptions.formatType}
                  onChange={(e) => setExportOptions({...exportOptions, formatType: e.target.value})}
                  className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="detailed">Detailed</option>
                  <option value="summary">Summary</option>
                </select>
              </div>
            )}

            {/* Specialty Filter */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Specialty Filter</label>
              <select
                value={exportOptions.specialtyFilter}
                onChange={(e) => setExportOptions({...exportOptions, specialtyFilter: e.target.value})}
                className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="">All Specialties</option>
                {Object.keys(exportStats.specialties || {}).map(specialty => (
                  <option key={specialty} value={specialty}>{specialty}</option>
                ))}
              </select>
            </div>

            {/* Include Summary (PDF only) */}
            {exportOptions.format === 'pdf' && (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Include Summary</label>
                <select
                  value={exportOptions.includeSummary.toString()}
                  onChange={(e) => setExportOptions({...exportOptions, includeSummary: e.target.value === 'true'})}
                  className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="true">Yes</option>
                  <option value="false">No</option>
                </select>
              </div>
            )}
          </div>
        </div>

        {/* Export Actions */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <ActionButton
            icon={FileJson}
            title="Export to JSON"
            description={`Export medical codes to JSON format (${exportOptions.formatType})`}
            onClick={exportToJson}
            loading={loading}
            variant="primary"
          />
          
          <ActionButton
            icon={FileText}
            title="Export to PDF"
            description="Export medical codes to PDF format with tables and formatting"
            onClick={exportToPdf}
            loading={loading}
            variant="success"
          />
        </div>

        {/* Export Preview */}
        <div className="mt-6">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Export Preview</h3>
          <div className="bg-gray-50 rounded-lg p-4 border border-gray-200">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
              <div>
                <span className="font-medium">Format:</span> {exportOptions.format.toUpperCase()}
              </div>
              <div>
                <span className="font-medium">Specialty:</span> {exportOptions.specialtyFilter || 'All Specialties'}
              </div>
              {exportOptions.format === 'json' && (
                <div>
                  <span className="font-medium">JSON Type:</span> {exportOptions.formatType}
                </div>
              )}
              {exportOptions.format === 'pdf' && (
                <div>
                  <span className="font-medium">Include Summary:</span> {exportOptions.includeSummary ? 'Yes' : 'No'}
                </div>
              )}
              <div>
                <span className="font-medium">Estimated Codes:</span> {exportOptions.specialtyFilter ? 
                  (exportStats.specialties?.[exportOptions.specialtyFilter]?.total_count || 0) : 
                  (exportStats.total_codes || 0)
                }
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Code Detail Modal */}
      {showCodeModal && selectedCode && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
            {/* Modal Header */}
            <div className="flex items-center justify-between p-6 border-b border-gray-200">
              <div className="flex items-center gap-3">
                <span className={`px-2 py-1 rounded text-xs font-medium ${getCodeTypeColor(selectedCode.codeType)}`}>
                  {getCodeTypeLabel(selectedCode.codeType)}
                </span>
                <h3 className="text-lg font-semibold text-gray-900">
                  {selectedCode.code || selectedCode.modifier}
                </h3>
              </div>
              <button
                onClick={closeCodeModal}
                className="text-gray-400 hover:text-gray-600 transition-colors"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            {/* Modal Content */}
            <div className="p-6 space-y-6">
              {/* Description */}
              <div>
                <h4 className="font-medium text-gray-900 mb-2">Description</h4>
                <p className="text-gray-700 leading-relaxed">{selectedCode.description}</p>
              </div>

              {/* Specialty */}
              {selectedCode.specialty && (
                <div>
                  <h4 className="font-medium text-gray-900 mb-2">Specialty</h4>
                  <span className="inline-block px-3 py-1 bg-blue-50 text-blue-700 rounded-full text-sm font-medium">
                    {selectedCode.specialty}
                  </span>
                </div>
              )}

              {/* Code Classification Details */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {selectedCode.category && (
                  <div>
                    <h4 className="font-medium text-gray-900 mb-1">Category</h4>
                    <p className="text-gray-700">{selectedCode.category}</p>
                  </div>
                )}
                
                {selectedCode.section && (
                  <div>
                    <h4 className="font-medium text-gray-900 mb-1">Section</h4>
                    <p className="text-gray-700">{selectedCode.section}</p>
                  </div>
                )}
                
                {selectedCode.subsection && (
                  <div>
                    <h4 className="font-medium text-gray-900 mb-1">Subsection</h4>
                    <p className="text-gray-700">{selectedCode.subsection}</p>
                  </div>
                )}
                
                {selectedCode.chapter && (
                  <div>
                    <h4 className="font-medium text-gray-900 mb-1">Chapter</h4>
                    <p className="text-gray-700">{selectedCode.chapter}</p>
                  </div>
                )}
                
                {selectedCode.level && (
                  <div>
                    <h4 className="font-medium text-gray-900 mb-1">Level</h4>
                    <p className="text-gray-700">{selectedCode.level}</p>
                  </div>
                )}
                
                {selectedCode.code_type && (
                  <div>
                    <h4 className="font-medium text-gray-900 mb-1">Code Type</h4>
                    <p className="text-gray-700">{selectedCode.code_type}</p>
                  </div>
                )}
              </div>

              {/* Status Badges */}
              <div>
                <h4 className="font-medium text-gray-900 mb-2">Status</h4>
                <div className="flex flex-wrap gap-2">
                  {selectedCode.is_billable === 'Y' && (
                    <span className="px-2 py-1 bg-green-100 text-green-700 rounded-full text-xs font-medium">
                      Billable
                    </span>
                  )}
                  {selectedCode.is_active === 'Y' && (
                    <span className="px-2 py-1 bg-blue-100 text-blue-700 rounded-full text-xs font-medium">
                      Active
                    </span>
                  )}
                  {selectedCode.is_active === 'N' && (
                    <span className="px-2 py-1 bg-red-100 text-red-700 rounded-full text-xs font-medium">
                      Inactive
                    </span>
                  )}
                  {selectedCode.is_billable === 'N' && (
                    <span className="px-2 py-1 bg-yellow-100 text-yellow-700 rounded-full text-xs font-medium">
                      Non-Billable
                    </span>
                  )}
                </div>
              </div>
            </div>

            {/* Modal Footer */}
            <div className="flex justify-end gap-3 p-6 border-t border-gray-200">
              <button
                onClick={closeCodeModal}
                className="px-4 py-2 text-gray-600 hover:text-gray-800 font-medium transition-colors"
              >
                Close
              </button>
              <button
                onClick={() => {
                  navigator.clipboard.writeText(selectedCode.code || selectedCode.modifier);
                  closeCodeModal();
                }}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium"
              >
                Copy Code
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Settings; 
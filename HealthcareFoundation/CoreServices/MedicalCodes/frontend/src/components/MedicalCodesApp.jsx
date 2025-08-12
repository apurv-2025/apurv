import React, { useState, useEffect, useRef } from 'react';
import { Search, FileText, Activity, Stethoscope, Users, BarChart3, ChevronDown, ExternalLink, Copy, Check, Settings, BookOpen } from 'lucide-react';
import SettingsComponent from './Settings';
import ResourcesComponent from './Resources';

const MedicalCodesApp = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [selectedCodeType, setSelectedCodeType] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('');
  const [selectedSpecialty, setSelectedSpecialty] = useState('');
  const [selectedSection, setSelectedSection] = useState('');
  const [selectedSubsection, setSelectedSubsection] = useState('');
  const [selectedChapter, setSelectedChapter] = useState('');
  const [selectedLevel, setSelectedLevel] = useState('');
  const [showAdvancedFilters, setShowAdvancedFilters] = useState(false);
  const [categories, setCategories] = useState({});
  const [stats, setStats] = useState({});
  const [activeTab, setActiveTab] = useState('search');
  const [copiedCode, setCopiedCode] = useState('');
  const searchInputRef = useRef(null);

  const API_BASE = 'http://localhost:8003/api';  // Fixed port to match docker-compose

  // Fetch categories and stats on component mount
  useEffect(() => {
    fetchCategories();
    fetchStats();
  }, []);

  const fetchCategories = async () => {
    try {
      const response = await fetch(`${API_BASE}/categories`);
      if (response.ok) {
        const data = await response.json();
        setCategories(data);
      }
    } catch (error) {
      console.error('Error fetching categories:', error);
    }
  };

  const fetchStats = async () => {
    try {
      const response = await fetch(`${API_BASE}/stats`);
      if (response.ok) {
        const data = await response.json();
        setStats(data);
      }
    } catch (error) {
      console.error('Error fetching stats:', error);
    }
  };

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!searchQuery.trim() && !selectedCodeType && !selectedSpecialty && !selectedCategory && !selectedSection) return;

    setLoading(true);
    try {
      const params = new URLSearchParams();
      
      // Add search query if provided
      if (searchQuery.trim()) {
        params.append('query', searchQuery.trim());
      }
      
      // Add filters if selected
      if (selectedCodeType) params.append('code_types', selectedCodeType);
      if (selectedSpecialty) params.append('specialty', selectedSpecialty);
      if (selectedCategory) params.append('category', selectedCategory);
      if (selectedSection) params.append('section', selectedSection);
      if (selectedSubsection) params.append('subsection', selectedSubsection);
      if (selectedChapter) params.append('chapter', selectedChapter);
      if (selectedLevel) params.append('level', selectedLevel);

      // Use comprehensive search endpoint
      const response = await fetch(`${API_BASE}/comprehensive/search?${params}`);
      if (response.ok) {
        const data = await response.json();
        setResults(data);
      } else {
        console.error('Search failed');
        setResults({ total_results: 0, results: {} });
      }
    } catch (error) {
      console.error('Error searching:', error);
      setResults({ total_results: 0, results: {} });
    } finally {
      setLoading(false);
    }
  };

  const copyToClipboard = async (text) => {
    try {
      await navigator.clipboard.writeText(text);
      setCopiedCode(text);
      setTimeout(() => setCopiedCode(''), 2000);
    } catch (error) {
      console.error('Failed to copy:', error);
    }
  };

  const CodeCard = ({ code, type, title, color }) => (
    <div className={`bg-white rounded-lg border-l-4 ${color} shadow-sm hover:shadow-md transition-shadow p-4 mb-3`}>
      {/* Header with Code and Copy Button */}
      <div className="flex justify-between items-start mb-3">
        <div className="flex items-center gap-2">
          <span className={`px-2 py-1 rounded text-xs font-medium ${
            type === 'cpt' ? 'bg-blue-100 text-blue-700' :
            type === 'icd10' ? 'bg-green-100 text-green-700' :
            type === 'hcpcs' ? 'bg-purple-100 text-purple-700' :
            'bg-orange-100 text-orange-700'
          }`}>
            {type.toUpperCase()}
          </span>
          <span className="font-mono font-bold text-xl">{code.code || code.modifier}</span>
        </div>
        <button
          onClick={() => copyToClipboard(code.code || code.modifier)}
          className="p-2 hover:bg-gray-100 rounded transition-colors"
          title="Copy code"
        >
          {copiedCode === (code.code || code.modifier) ? 
            <Check className="w-5 h-5 text-green-600" /> : 
            <Copy className="w-5 h-5 text-gray-500" />
          }
        </button>
      </div>
      
      {/* Main Description */}
      <div className="mb-4">
        <h3 className="font-semibold text-gray-900 text-lg mb-2">Description</h3>
        <p className="text-gray-800 leading-relaxed text-sm">{code.description}</p>
      </div>

      {/* Specialty Information */}
      {code.specialty && (
        <div className="mb-3">
          <h4 className="font-medium text-gray-700 text-sm mb-1">Specialty</h4>
          <span className="inline-block px-3 py-1 bg-blue-50 text-blue-700 rounded-full text-sm font-medium">
            {code.specialty}
          </span>
        </div>
      )}

      {/* Code Classification Details */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mb-4">
        {/* Left Column */}
        <div className="space-y-2">
          {code.category && (
            <div>
              <span className="text-xs font-medium text-gray-500 uppercase tracking-wide">Category</span>
              <p className="text-sm text-gray-800">{code.category}</p>
            </div>
          )}
          {code.section && (
            <div>
              <span className="text-xs font-medium text-gray-500 uppercase tracking-wide">Section</span>
              <p className="text-sm text-gray-800">{code.section}</p>
            </div>
          )}
          {code.subsection && (
            <div>
              <span className="text-xs font-medium text-gray-500 uppercase tracking-wide">Subsection</span>
              <p className="text-sm text-gray-800">{code.subsection}</p>
            </div>
          )}
        </div>

        {/* Right Column */}
        <div className="space-y-2">
          {code.chapter && (
            <div>
              <span className="text-xs font-medium text-gray-500 uppercase tracking-wide">Chapter</span>
              <p className="text-sm text-gray-800">{code.chapter}</p>
            </div>
          )}
          {code.level && (
            <div>
              <span className="text-xs font-medium text-gray-500 uppercase tracking-wide">Level</span>
              <p className="text-sm text-gray-800">{code.level}</p>
            </div>
          )}
          {code.code_type && (
            <div>
              <span className="text-xs font-medium text-gray-500 uppercase tracking-wide">Code Type</span>
              <p className="text-sm text-gray-800">{code.code_type}</p>
            </div>
          )}
        </div>
      </div>

      {/* Status Badges */}
      <div className="flex flex-wrap gap-2">
        {code.is_billable === 'Y' && (
          <span className="px-2 py-1 bg-green-100 text-green-700 rounded-full text-xs font-medium">
            Billable
          </span>
        )}
        {code.is_active === 'Y' && (
          <span className="px-2 py-1 bg-blue-100 text-blue-700 rounded-full text-xs font-medium">
            Active
          </span>
        )}
        {code.is_active === 'N' && (
          <span className="px-2 py-1 bg-red-100 text-red-700 rounded-full text-xs font-medium">
            Inactive
          </span>
        )}
        {code.is_billable === 'N' && (
          <span className="px-2 py-1 bg-yellow-100 text-yellow-700 rounded-full text-xs font-medium">
            Non-Billable
          </span>
        )}
      </div>
    </div>
  );

  const StatCard = ({ icon: Icon, title, value, subtitle, color }) => (
    <div className="bg-white rounded-lg shadow-sm p-6 border-l-4 border-l-blue-500">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-gray-600">{title}</p>
          <p className="text-3xl font-bold text-gray-900 mt-1">
            {typeof value === 'number' ? value.toLocaleString() : value}
          </p>
          {subtitle && <p className="text-sm text-gray-500 mt-1">{subtitle}</p>}
        </div>
        <div className={`p-3 rounded-lg ${color}`}>
          <Icon className="w-6 h-6 text-white" />
        </div>
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-blue-600 rounded-lg">
                <Stethoscope className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">Medical Codes Lookup</h1>
                <p className="text-sm text-gray-600">CPT, ICD-10, HCPCS & Modifiers Database</p>
              </div>
            </div>
            
            <nav className="flex space-x-4">
              <button
                onClick={() => setActiveTab('search')}
                className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                  activeTab === 'search' 
                    ? 'bg-blue-100 text-blue-700' 
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                Search
              </button>
              <button
                onClick={() => setActiveTab('dashboard')}
                className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                  activeTab === 'dashboard' 
                    ? 'bg-blue-100 text-blue-700' 
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                Dashboard
              </button>
              <button
                onClick={() => setActiveTab('resources')}
                className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                  activeTab === 'resources' 
                    ? 'bg-blue-100 text-blue-700' 
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                <div className="flex items-center gap-2">
                  <BookOpen className="w-4 h-4" />
                  Resources
                </div>
              </button>
              <button
                onClick={() => setActiveTab('settings')}
                className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                  activeTab === 'settings' 
                    ? 'bg-blue-100 text-blue-700' 
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                <div className="flex items-center gap-2">
                  <Settings className="w-4 h-4" />
                  Settings
                </div>
              </button>
            </nav>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activeTab === 'search' && (
          <>
            {/* Search Section */}
            <div className="bg-white rounded-lg shadow-sm p-6 mb-8">
              <div className="space-y-4">
                <div className="flex flex-col sm:flex-row gap-4">
                  <div className="flex-1 relative">
                    <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                    <input
                      ref={searchInputRef}
                      type="text"
                      value={searchQuery}
                      onChange={(e) => setSearchQuery(e.target.value)}
                      onKeyPress={(e) => e.key === 'Enter' && handleSearch(e)}
                      placeholder="Search medical codes (e.g., '99213', 'office visit', 'diabetes')..."
                      className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                  </div>
                  <button
                    onClick={handleSearch}
                    disabled={loading || (!searchQuery.trim() && !selectedCodeType && !selectedSpecialty && !selectedCategory && !selectedSection)}
                    className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed font-medium transition-colors"
                  >
                    {loading ? 'Searching...' : 'Search'}
                  </button>
                </div>

                {/* Filters */}
                <div className="space-y-4 pt-2">
                  {/* Basic Filters */}
                  <div className="flex flex-col sm:flex-row gap-4">
                    <div className="flex-1">
                      <label className="block text-sm font-medium text-gray-700 mb-1">Code Type</label>
                      <div className="relative">
                        <select
                          value={selectedCodeType}
                          onChange={(e) => setSelectedCodeType(e.target.value)}
                          className="w-full appearance-none bg-white border border-gray-300 rounded-lg px-3 py-2 pr-8 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        >
                          <option value="">All Types</option>
                          <option value="cpt">CPT Codes</option>
                          <option value="icd10">ICD-10 Codes</option>
                          <option value="hcpcs">HCPCS Codes</option>
                          <option value="modifier">Modifiers</option>
                        </select>
                        <ChevronDown className="absolute right-2 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4 pointer-events-none" />
                      </div>
                    </div>

                    <div className="flex-1">
                      <label className="block text-sm font-medium text-gray-700 mb-1">Specialty</label>
                      <div className="relative">
                        <select
                          value={selectedSpecialty}
                          onChange={(e) => setSelectedSpecialty(e.target.value)}
                          className="w-full appearance-none bg-white border border-gray-300 rounded-lg px-3 py-2 pr-8 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        >
                          <option value="">All Specialties</option>
                          <option value="Psychiatry">Psychiatry</option>
                          <option value="Primary Care">Primary Care</option>
                          <option value="Cardiology">Cardiology</option>
                          <option value="Orthopedics">Orthopedics</option>
                          <option value="Gastroenterology">Gastroenterology</option>
                          <option value="Radiology">Radiology</option>
                          <option value="Pathology">Pathology</option>
                          <option value="Pulmonology">Pulmonology</option>
                          <option value="Surgery">Surgery</option>
                        </select>
                        <ChevronDown className="absolute right-2 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4 pointer-events-none" />
                      </div>
                    </div>

                    <div className="flex-1">
                      <label className="block text-sm font-medium text-gray-700 mb-1">Category</label>
                      <div className="relative">
                        <select
                          value={selectedCategory}
                          onChange={(e) => setSelectedCategory(e.target.value)}
                          className="w-full appearance-none bg-white border border-gray-300 rounded-lg px-3 py-2 pr-8 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        >
                          <option value="">All Categories</option>
                          <option value="Category I">Category I</option>
                          <option value="Category II">Category II</option>
                          <option value="Category III">Category III</option>
                          <option value="Mental Health Services">Mental Health Services</option>
                          <option value="Diagnosis">Diagnosis</option>
                        </select>
                        <ChevronDown className="absolute right-2 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4 pointer-events-none" />
                      </div>
                    </div>
                  </div>

                  {/* Advanced Filters Toggle */}
                  <div className="flex justify-center">
                    <button
                      onClick={() => setShowAdvancedFilters(!showAdvancedFilters)}
                      className="flex items-center gap-2 text-sm text-blue-600 hover:text-blue-700 font-medium"
                    >
                      <ChevronDown className={`w-4 h-4 transition-transform ${showAdvancedFilters ? 'rotate-180' : ''}`} />
                      {showAdvancedFilters ? 'Hide Advanced Filters' : 'Show Advanced Filters'}
                    </button>
                  </div>

                  {/* Advanced Filters */}
                  {showAdvancedFilters && (
                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 p-4 bg-gray-50 rounded-lg">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Section</label>
                        <div className="relative">
                          <select
                            value={selectedSection}
                            onChange={(e) => setSelectedSection(e.target.value)}
                            className="w-full appearance-none bg-white border border-gray-300 rounded-lg px-3 py-2 pr-8 focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
                          >
                            <option value="">All Sections</option>
                            <option value="Medicine">Medicine</option>
                            <option value="Surgery">Surgery</option>
                            <option value="Radiology">Radiology</option>
                            <option value="Pathology and Laboratory">Pathology and Laboratory</option>
                            <option value="Evaluation and Management">Evaluation and Management</option>
                          </select>
                          <ChevronDown className="absolute right-2 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4 pointer-events-none" />
                        </div>
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Subsection</label>
                        <div className="relative">
                          <select
                            value={selectedSubsection}
                            onChange={(e) => setSelectedSubsection(e.target.value)}
                            className="w-full appearance-none bg-white border border-gray-300 rounded-lg px-3 py-2 pr-8 focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
                          >
                            <option value="">All Subsections</option>
                            <option value="Psychiatry">Psychiatry</option>
                            <option value="Office or Other Outpatient Services">Office or Other Outpatient Services</option>
                            <option value="Cardiovascular">Cardiovascular</option>
                            <option value="Pulmonary">Pulmonary</option>
                            <option value="Integumentary System">Integumentary System</option>
                            <option value="Musculoskeletal System">Musculoskeletal System</option>
                            <option value="Digestive System">Digestive System</option>
                            <option value="Diagnostic Radiology">Diagnostic Radiology</option>
                            <option value="Chemistry">Chemistry</option>
                            <option value="Hematology and Coagulation">Hematology and Coagulation</option>
                            <option value="Microbiology">Microbiology</option>
                          </select>
                          <ChevronDown className="absolute right-2 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4 pointer-events-none" />
                        </div>
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Chapter (ICD-10)</label>
                        <div className="relative">
                          <select
                            value={selectedChapter}
                            onChange={(e) => setSelectedChapter(e.target.value)}
                            className="w-full appearance-none bg-white border border-gray-300 rounded-lg px-3 py-2 pr-8 focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
                          >
                            <option value="">All Chapters</option>
                            <option value="Mental, Behavioral and Neurodevelopmental disorders">Mental, Behavioral and Neurodevelopmental disorders</option>
                            <option value="Factors influencing health status and contact with health services">Factors influencing health status and contact with health services</option>
                          </select>
                          <ChevronDown className="absolute right-2 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4 pointer-events-none" />
                        </div>
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Level (HCPCS)</label>
                        <div className="relative">
                          <select
                            value={selectedLevel}
                            onChange={(e) => setSelectedLevel(e.target.value)}
                            className="w-full appearance-none bg-white border border-gray-300 rounded-lg px-3 py-2 pr-8 focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
                          >
                            <option value="">All Levels</option>
                            <option value="Level II">Level II</option>
                          </select>
                          <ChevronDown className="absolute right-2 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4 pointer-events-none" />
                        </div>
                      </div>
                    </div>
                  )}

                  {/* Clear Filters Button */}
                  {(selectedCodeType || selectedSpecialty || selectedCategory || selectedSection || selectedSubsection || selectedChapter || selectedLevel) && (
                    <div className="flex justify-center">
                      <button
                        onClick={() => {
                          setSelectedCodeType('');
                          setSelectedSpecialty('');
                          setSelectedCategory('');
                          setSelectedSection('');
                          setSelectedSubsection('');
                          setSelectedChapter('');
                          setSelectedLevel('');
                        }}
                        className="text-sm text-gray-500 hover:text-gray-700 font-medium"
                      >
                        Clear All Filters
                      </button>
                    </div>
                  )}
                </div>
              </div>
            </div>

            {/* Results */}
            {results && (
              <div className="space-y-6">
                <div className="flex justify-between items-center">
                  <h2 className="text-xl font-semibold text-gray-900">
                    Search Results ({results.total_results || 0} found)
                  </h2>
                  {(results.total_results || 0) > 0 && (
                    <button
                      onClick={() => setResults(null)}
                      className="text-sm text-gray-500 hover:text-gray-700"
                    >
                      Clear results
                    </button>
                  )}
                </div>

                {(results.total_results || 0) === 0 ? (
                  <div className="text-center py-12">
                    <FileText className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                    <h3 className="text-lg font-medium text-gray-900 mb-2">No results found</h3>
                    <p className="text-gray-600">Try a different search term or adjust your filters.</p>
                  </div>
                ) : (
                  <div className="space-y-8">
                    {/* CPT Codes */}
                    {results.results?.cpt_codes?.length > 0 && (
                      <div>
                        <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
                          <div className="w-3 h-3 bg-blue-500 rounded"></div>
                          CPT Codes ({results.results.cpt_codes.length})
                        </h3>
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
                          {results.results.cpt_codes.map(code => (
                            <CodeCard
                              key={code.code}
                              code={code}
                              type="cpt"
                              color="border-l-blue-500"
                            />
                          ))}
                        </div>
                      </div>
                    )}

                    {/* ICD-10 Codes */}
                    {results.results?.icd10_codes?.length > 0 && (
                      <div>
                        <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
                          <div className="w-3 h-3 bg-green-500 rounded"></div>
                          ICD-10 Codes ({results.results.icd10_codes.length})
                        </h3>
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
                          {results.results.icd10_codes.map(code => (
                            <CodeCard
                              key={code.code}
                              code={code}
                              type="icd10"
                              color="border-l-green-500"
                            />
                          ))}
                        </div>
                      </div>
                    )}

                    {/* HCPCS Codes */}
                    {results.results?.hcpcs_codes?.length > 0 && (
                      <div>
                        <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
                          <div className="w-3 h-3 bg-purple-500 rounded"></div>
                          HCPCS Codes ({results.results.hcpcs_codes.length})
                        </h3>
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
                          {results.results.hcpcs_codes.map(code => (
                            <CodeCard
                              key={code.code}
                              code={code}
                              type="hcpcs"
                              color="border-l-purple-500"
                            />
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Modifier Codes */}
                    {results.results?.modifier_codes?.length > 0 && (
                      <div>
                        <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
                          <div className="w-3 h-3 bg-orange-500 rounded"></div>
                          Modifiers ({results.results.modifier_codes.length})
                        </h3>
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
                          {results.results.modifier_codes.map(code => (
                            <CodeCard
                              key={code.code}
                              code={code}
                              type="modifier"
                              color="border-l-orange-500"
                            />
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </div>
            )}
          </>
        )}
        
        {activeTab === 'dashboard' && (
          <div className="space-y-8">
            <div>
              <h2 className="text-2xl font-bold text-gray-900 mb-2">Database Statistics</h2>
              <p className="text-gray-600">Overview of medical codes in the database</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <StatCard
                icon={Activity}
                title="Total CPT Codes"
                value={stats.total_cpt_codes || 0}
                subtitle={`${stats.active_cpt_codes || 0} active`}
                color="bg-blue-500"
              />
              <StatCard
                icon={FileText}
                title="Total ICD-10 Codes"
                value={stats.total_icd10_codes || 0}
                subtitle={`${stats.active_icd10_codes || 0} active`}
                color="bg-green-500"
              />
              <StatCard
                icon={Users}
                title="Total HCPCS Codes"
                value={stats.total_hcpcs_codes || 0}
                subtitle={`${stats.active_hcpcs_codes || 0} active`}
                color="bg-purple-500"
              />
              <StatCard
                icon={BarChart3}
                title="Total Modifiers"
                value={stats.total_modifier_codes || 0}
                subtitle="All active"
                color="bg-orange-500"
              />
            </div>

            {/* Quick Actions */}
            <div className="bg-white rounded-lg shadow-sm p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Search Examples</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {[
                  { query: 'office visit', desc: 'Find E&M codes for office visits' },
                  { query: '99213', desc: 'Look up specific CPT code' },
                  { query: 'diabetes', desc: 'Find diabetes-related codes' },
                  { query: 'colonoscopy', desc: 'Colonoscopy procedures' },
                  { query: 'x-ray', desc: 'Radiology procedures' },
                  { query: 'blood test', desc: 'Laboratory procedures' }
                ].map((example, idx) => (
                  <button
                    key={idx}
                    onClick={() => {
                      setSearchQuery(example.query);
                      setActiveTab('search');
                      setTimeout(() => searchInputRef.current?.focus(), 100);
                    }}
                    className="text-left p-3 border border-gray-200 rounded-lg hover:border-blue-300 hover:bg-blue-50 transition-colors"
                  >
                    <div className="font-medium text-gray-900">{example.query}</div>
                    <div className="text-sm text-gray-600 mt-1">{example.desc}</div>
                  </button>
                ))}
              </div>
            </div>
          </div>
        )}
        
        {activeTab === 'resources' && (
          <ResourcesComponent />
        )}

        {activeTab === 'settings' && (
          <SettingsComponent />
        )}
      </main>
    </div>
  );
};

export default MedicalCodesApp; 
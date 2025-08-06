import React, { useState, useEffect, useRef } from 'react';
import { Search, Filter, FileText, Calendar, Activity, Stethoscope, Users, BarChart3, ChevronDown, ExternalLink, Copy, Check } from 'lucide-react';

const MedicalCodesApp = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [selectedCodeType, setSelectedCodeType] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('');
  const [categories, setCategories] = useState({});
  const [stats, setStats] = useState({});
  const [activeTab, setActiveTab] = useState('search');
  const [copiedCode, setCopiedCode] = useState('');
  const searchInputRef = useRef(null);

  const API_BASE = 'http://localhost:8000/api';

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
    if (!searchQuery.trim()) return;

    setLoading(true);
    try {
      const params = new URLSearchParams({
        query: searchQuery,
        limit: '25'
      });
      
      if (selectedCodeType) params.append('code_type', selectedCodeType);
      if (selectedCategory) params.append('category', selectedCategory);

      const response = await fetch(`${API_BASE}/search?${params}`);
      if (response.ok) {
        const data = await response.json();
        setResults(data);
      } else {
        console.error('Search failed');
      }
    } catch (error) {
      console.error('Error searching:', error);
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
      <div className="flex justify-between items-start mb-2">
        <div className="flex items-center gap-2">
          <span className={`px-2 py-1 rounded text-xs font-medium ${
            type === 'cpt' ? 'bg-blue-100 text-blue-700' :
            type === 'icd10' ? 'bg-green-100 text-green-700' :
            type === 'hcpcs' ? 'bg-purple-100 text-purple-700' :
            'bg-orange-100 text-orange-700'
          }`}>
            {type.toUpperCase()}
          </span>
          <span className="font-mono font-bold text-lg">{code.code || code.modifier}</span>
        </div>
        <button
          onClick={() => copyToClipboard(code.code || code.modifier)}
          className="p-1 hover:bg-gray-100 rounded transition-colors"
          title="Copy code"
        >
          {copiedCode === (code.code || code.modifier) ? 
            <Check className="w-4 h-4 text-green-600" /> : 
            <Copy className="w-4 h-4 text-gray-500" />
          }
        </button>
      </div>
      
      <p className="text-gray-800 mb-3 leading-relaxed">{code.description}</p>
      
      <div className="flex flex-wrap gap-2 text-xs">
        {code.category && (
          <span className="px-2 py-1 bg-gray-100 text-gray-600 rounded">
            {code.category}
          </span>
        )}
        {code.section && (
          <span className="px-2 py-1 bg-gray-100 text-gray-600 rounded">
            {code.section}
          </span>
        )}
        {code.chapter && (
          <span className="px-2 py-1 bg-gray-100 text-gray-600 rounded">
            {code.chapter}
          </span>
        )}
        {code.level && (
          <span className="px-2 py-1 bg-gray-100 text-gray-600 rounded">
            {code.level}
          </span>
        )}
        {code.is_billable === 'Y' && (
          <span className="px-2 py-1 bg-green-100 text-green-700 rounded">
            Billable
          </span>
        )}
        {code.is_active === 'Y' && (
          <span className="px-2 py-1 bg-blue-100 text-blue-700 rounded">
            Active
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
            </nav>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activeTab === 'search' ? (
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
                    disabled={loading || !searchQuery.trim()}
                    className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed font-medium transition-colors"
                  >
                    {loading ? 'Searching...' : 'Search'}
                  </button>
                </div>

                {/* Filters */}
                <div className="flex flex-col sm:flex-row gap-4 pt-2">
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
                    <label className="block text-sm font-medium text-gray-700 mb-1">Category</label>
                    <div className="relative">
                      <select
                        value={selectedCategory}
                        onChange={(e) => setSelectedCategory(e.target.value)}
                        className="w-full appearance-none bg-white border border-gray-300 rounded-lg px-3 py-2 pr-8 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      >
                        <option value="">All Categories</option>
                        {categories.cpt_categories?.map(cat => (
                          <option key={cat} value={cat}>{cat}</option>
                        ))}
                        {categories.icd10_chapters?.map(chap => (
                          <option key={chap} value={chap}>{chap}</option>
                        ))}
                        {categories.hcpcs_categories?.map(cat => (
                          <option key={cat} value={cat}>{cat}</option>
                        ))}
                      </select>
                      <ChevronDown className="absolute right-2 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4 pointer-events-none" />
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Results */}
            {results && (
              <div className="space-y-6">
                <div className="flex justify-between items-center">
                  <h2 className="text-xl font-semibold text-gray-900">
                    Search Results ({results.total_results} found)
                  </h2>
                  {results.total_results > 0 && (
                    <button
                      onClick={() => setResults(null)}
                      className="text-sm text-gray-500 hover:text-gray-700"
                    >
                      Clear results
                    </button>
                  )}
                </div>

                {results.total_results === 0 ? (
                  <div className="text-center py-12">
                    <FileText className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                    <h3 className="text-lg font-medium text-gray-900 mb-2">No results found</h3>
                    <p className="text-gray-600">Try a different search term or adjust your filters.</p>
                  </div>
                ) : (
                  <div className="grid lg:grid-cols-2 gap-6">
                    {/* CPT Codes */}
                    {results.cpt_codes?.length > 0 && (
                      <div>
                        <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
                          <div className="w-3 h-3 bg-blue-500 rounded"></div>
                          CPT Codes ({results.cpt_codes.length})
                        </h3>
                        {results.cpt_codes.map(code => (
                          <CodeCard
                            key={code.id}
                            code={code}
                            type="cpt"
                            color="border-l-blue-500"
                          />
                        ))}
                      </div>
                    )}

                    {/* ICD-10 Codes */}
                    {results.icd10_codes?.length > 0 && (
                      <div>
                        <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
                          <div className="w-3 h-3 bg-green-500 rounded"></div>
                          ICD-10 Codes ({results.icd10_codes.length})
                        </h3>
                        {results.icd10_codes.map(code => (
                          <CodeCard
                            key={code.id}
                            code={code}
                            type="icd10"
                            color="border-l-green-500"
                          />
                        ))}
                      </div>
                    )}

                    {/* HCPCS Codes */}
                    {results.hcpcs_codes?.length > 0 && (
                      <div>
                        <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
                          <div className="w-3 h-3 bg-purple-500 rounded"></div>
                          HCPCS Codes ({results.hcpcs_codes.length})
                        </h3>
                        {results.hcpcs_codes.map(code => (
                          <CodeCard
                            key={code.id}
                            code={code}
                            type="hcpcs"
                            color="border-l-purple-500"
                          />
                        ))}
                      </div>
                    )}

                    {/* Modifier Codes */}
                    {results.modifier_codes?.length > 0 && (
                      <div>
                        <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
                          <div className="w-3 h-3 bg-orange-500 rounded"></div>
                          Modifiers ({results.modifier_codes.length})
                        </h3>
                        {results.modifier_codes.map(code => (
                          <CodeCard
                            key={code.id}
                            code={code}
                            type="modifier"
                            color="border-l-orange-500"
                          />
                        ))}
                      </div>
                    )}
                  </div>
                )}
              </div>
            )}
          </>
        ) : (
          /* Dashboard */
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

            {/* Reference Links */}
            <div className="bg-white rounded-lg shadow-sm p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">External References</h3>
              <div className="space-y-3">
                <a
                  href="https://www.ama-assn.org/practice-management/cpt"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center gap-2 text-blue-600 hover:text-blue-700"
                >
                  <ExternalLink className="w-4 h-4" />
                  AMA CPT Codes
                </a>
                <a
                  href="https://www.cms.gov/medicare/coding-billing/icd-10-codes"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center gap-2 text-blue-600 hover:text-blue-700"
                >
                  <ExternalLink className="w-4 h-4" />
                  CMS ICD-10 Codes
                </a>
                <a
                  href="https://www.cms.gov/medicare/coding-billing/healthcare-common-procedure-system"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center gap-2 text-blue-600 hover:text-blue-700"
                >
                  <ExternalLink className="w-4 h-4" />
                  CMS HCPCS Codes
                </a>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
};

export default MedicalCodesApp; 
import React, { useState, useEffect } from 'react';
import { 
  FileText, Download, Eye, Calendar, User, Activity, AlertCircle, 
  CheckCircle, Clock, Search, Filter, ArrowRight, ExternalLink, X
} from 'lucide-react';
import { useAPI } from '../hooks/useAPI';
import { labResultsAPI } from '../services/api';

const Results = () => {
  const [activeTab, setActiveTab] = useState('all');
  const [results, setResults] = useState([]);
  const [filteredResults, setFilteredResults] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterDoctor, setFilterDoctor] = useState('all');
  const [loading, setLoading] = useState(true);
  const [selectedResult, setSelectedResult] = useState(null);

  const { data: labData, error } = useAPI(() => labResultsAPI.getLabResults(), []);

  useEffect(() => {
    // Mock comprehensive results data
    const mockResults = [
      {
        id: 1,
        type: 'Lab',
        category: 'Blood Work',
        name: 'Complete Blood Count (CBC)',
        orderDate: '2024-02-08',
        collectionDate: '2024-02-10',
        resultDate: '2024-02-11',
        doctor: 'Dr. Sarah Johnson',
        status: 'Final',
        isNew: true,
        abnormal: false,
        critical: false,
        results: [
          { test: 'White Blood Cells', value: '7.2', unit: 'K/uL', range: '4.5-11.0', status: 'normal' },
          { test: 'Red Blood Cells', value: '4.8', unit: 'M/uL', range: '4.2-5.4', status: 'normal' },
          { test: 'Hemoglobin', value: '14.2', unit: 'g/dL', range: '12.0-15.5', status: 'normal' },
          { test: 'Hematocrit', value: '42.1', unit: '%', range: '36.0-46.0', status: 'normal' }
        ],
        notes: 'All values within normal limits. Continue current medications.',
        downloadUrl: '/results/cbc-2024-02-11.pdf'
      },
      {
        id: 2,
        type: 'Lab',
        category: 'Chemistry',
        name: 'Comprehensive Metabolic Panel',
        orderDate: '2024-02-08',
        collectionDate: '2024-02-10',
        resultDate: '2024-02-11',
        doctor: 'Dr. Michael Chen',
        status: 'Final',
        isNew: true,
        abnormal: true,
        critical: false,
        results: [
          { test: 'Glucose', value: '105', unit: 'mg/dL', range: '70-100', status: 'high' },
          { test: 'BUN', value: '18', unit: 'mg/dL', range: '7-20', status: 'normal' },
          { test: 'Creatinine', value: '1.0', unit: 'mg/dL', range: '0.6-1.2', status: 'normal' },
          { test: 'Sodium', value: '140', unit: 'mEq/L', range: '136-145', status: 'normal' }
        ],
        notes: 'Slightly elevated glucose. Consider dietary modifications and follow-up in 3 months.',
        downloadUrl: '/results/cmp-2024-02-11.pdf'
      },
      {
        id: 3,
        type: 'Imaging',
        category: 'Radiology',
        name: 'Chest X-Ray',
        orderDate: '2024-02-05',
        collectionDate: '2024-02-07',
        resultDate: '2024-02-08',
        doctor: 'Dr. Emily Davis',
        status: 'Final',
        isNew: false,
        abnormal: false,
        critical: false,
        findings: 'Normal chest X-ray. No acute cardiopulmonary abnormalities. Heart size normal. Lungs clear.',
        impression: 'Normal chest radiograph',
        notes: 'No follow-up needed at this time.',
        downloadUrl: '/results/chest-xray-2024-02-08.pdf',
        imageUrl: '/results/chest-xray-2024-02-08.jpg'
      },
      {
        id: 4,
        type: 'Lab',
        category: 'Cardiology',
        name: 'Lipid Panel',
        orderDate: '2024-01-15',
        collectionDate: '2024-01-20',
        resultDate: '2024-01-21',
        doctor: 'Dr. Sarah Johnson',
        status: 'Final',
        isNew: false,
        abnormal: true,
        critical: false,
        results: [
          { test: 'Total Cholesterol', value: '220', unit: 'mg/dL', range: '<200', status: 'high' },
          { test: 'LDL Cholesterol', value: '145', unit: 'mg/dL', range: '<100', status: 'high' },
          { test: 'HDL Cholesterol', value: '45', unit: 'mg/dL', range: '>40', status: 'normal' },
          { test: 'Triglycerides', value: '150', unit: 'mg/dL', range: '<150', status: 'normal' }
        ],
        notes: 'Elevated cholesterol levels. Discuss statin therapy and lifestyle modifications.',
        downloadUrl: '/results/lipid-2024-01-21.pdf'
      }
    ];

    setResults(mockResults);
    setFilteredResults(mockResults);
    setLoading(false);
  }, [labData]);

  useEffect(() => {
    let filtered = results;

    // Filter by tab
    if (activeTab === 'lab') {
      filtered = filtered.filter(result => result.type === 'Lab');
    } else if (activeTab === 'imaging') {
      filtered = filtered.filter(result => result.type === 'Imaging');
    } else if (activeTab === 'new') {
      filtered = filtered.filter(result => result.isNew);
    } else if (activeTab === 'abnormal') {
      filtered = filtered.filter(result => result.abnormal);
    }

    // Filter by search term
    if (searchTerm) {
      filtered = filtered.filter(result =>
        result.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        result.category.toLowerCase().includes(searchTerm.toLowerCase()) ||
        result.doctor.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    // Filter by doctor
    if (filterDoctor !== 'all') {
      filtered = filtered.filter(result => result.doctor === filterDoctor);
    }

    setFilteredResults(filtered);
  }, [results, activeTab, searchTerm, filterDoctor]);

  const getStatusColor = (status) => {
    switch (status) {
      case 'Final': return 'bg-green-100 text-green-800';
      case 'Preliminary': return 'bg-yellow-100 text-yellow-800';
      case 'Pending': return 'bg-blue-100 text-blue-800';
      case 'Amended': return 'bg-orange-100 text-orange-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getResultStatusColor = (status) => {
    switch (status) {
      case 'normal': return 'text-green-600';
      case 'high': return 'text-red-600';
      case 'low': return 'text-blue-600';
      case 'critical': return 'text-red-800 font-bold';
      default: return 'text-gray-600';
    }
  };

  const downloadPDF = (result) => {
    // Simulate PDF download
    console.log(`Downloading PDF for ${result.name}`);
    // In real implementation, this would trigger a file download
    alert(`PDF download for ${result.name} would start here`);
  };

  const ResultCard = ({ result }) => (
    <div className="bg-white border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <div className="flex items-center space-x-3 mb-2">
            <h3 className="text-lg font-semibold text-gray-900">{result.name}</h3>
            <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(result.status)}`}>
              {result.status}
            </span>
            {result.isNew && (
              <span className="px-2 py-1 bg-blue-100 text-blue-800 rounded-full text-xs font-medium">
                New
              </span>
            )}
            {result.abnormal && (
              <AlertCircle className="w-5 h-5 text-orange-500" />
            )}
            {result.critical && (
              <AlertCircle className="w-5 h-5 text-red-500" />
            )}
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-4 text-sm text-gray-600">
            <div className="flex items-center space-x-2">
              <FileText className="w-4 h-4" />
              <span>{result.type} - {result.category}</span>
            </div>
            <div className="flex items-center space-x-2">
              <Calendar className="w-4 h-4" />
              <span>Result: {result.resultDate}</span>
            </div>
            <div className="flex items-center space-x-2">
              <User className="w-4 h-4" />
              <span>{result.doctor}</span>
            </div>
            <div className="flex items-center space-x-2">
              <Clock className="w-4 h-4" />
              <span>Collected: {result.collectionDate}</span>
            </div>
          </div>

          {result.results && (
            <div className="mb-4">
              <h4 className="font-medium text-gray-900 mb-2">Results Summary:</h4>
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-2">
                {result.results.slice(0, 4).map((test, index) => (
                  <div key={index} className="flex items-center justify-between p-2 bg-gray-50 rounded">
                    <span className="text-sm text-gray-700">{test.test}</span>
                    <div className="text-right">
                      <span className={`text-sm font-medium ${getResultStatusColor(test.status)}`}>
                        {test.value} {test.unit}
                      </span>
                      <div className="text-xs text-gray-500">({test.range})</div>
                    </div>
                  </div>
                ))}
              </div>
              {result.results.length > 4 && (
                <button 
                  onClick={() => setSelectedResult(result)}
                  className="mt-2 text-blue-600 hover:text-blue-800 text-sm flex items-center"
                >
                  View all results <ArrowRight className="w-4 h-4 ml-1" />
                </button>
              )}
            </div>
          )}

          {result.findings && (
            <div className="mb-4">
              <h4 className="font-medium text-gray-900 mb-1">Findings:</h4>
              <p className="text-sm text-gray-600">{result.findings}</p>
            </div>
          )}

          {result.impression && (
            <div className="mb-4">
              <h4 className="font-medium text-gray-900 mb-1">Impression:</h4>
              <p className="text-sm text-gray-600">{result.impression}</p>
            </div>
          )}

          {result.notes && (
            <div className="mb-4 p-3 bg-blue-50 border border-blue-200 rounded-lg">
              <h4 className="font-medium text-blue-800 mb-1">Provider Notes:</h4>
              <p className="text-sm text-blue-700">{result.notes}</p>
            </div>
          )}
        </div>

        <div className="flex flex-col space-y-2 ml-4">
          <button
            onClick={() => downloadPDF(result)}
            className="px-3 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm flex items-center"
          >
            <Download className="w-4 h-4 mr-1" />
            PDF
          </button>
          
          {result.imageUrl && (
            <button className="px-3 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors text-sm flex items-center">
              <Eye className="w-4 h-4 mr-1" />
              View Image
            </button>
          )}

          <button 
            onClick={() => setSelectedResult(result)}
            className="px-3 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors text-sm"
          >
            Details
          </button>
        </div>
      </div>
    </div>
  );

  const ResultDetailModal = () => {
    if (!selectedResult) return null;

    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
        <div className="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-y-auto">
          <div className="p-6 border-b border-gray-200">
            <div className="flex items-center justify-between">
              <h2 className="text-xl font-semibold text-gray-900">{selectedResult.name}</h2>
              <button 
                onClick={() => setSelectedResult(null)}
                className="text-gray-400 hover:text-gray-600"
              >
                <X className="w-6 h-6" />
              </button>
            </div>
          </div>

          <div className="p-6 space-y-6">
            {/* Result Details */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <h3 className="font-medium text-gray-900 mb-3">Test Information</h3>
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Type:</span>
                    <span className="text-gray-900">{selectedResult.type} - {selectedResult.category}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Ordered:</span>
                    <span className="text-gray-900">{selectedResult.orderDate}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Collected:</span>
                    <span className="text-gray-900">{selectedResult.collectionDate}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Result Date:</span>
                    <span className="text-gray-900">{selectedResult.resultDate}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Doctor:</span>
                    <span className="text-gray-900">{selectedResult.doctor}</span>
                  </div>
                </div>
              </div>

              <div>
                <h3 className="font-medium text-gray-900 mb-3">Status</h3>
                <div className="space-y-2">
                  <span className={`inline-block px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(selectedResult.status)}`}>
                    {selectedResult.status}
                  </span>
                  {selectedResult.abnormal && (
                    <div className="flex items-center space-x-2 text-orange-600">
                      <AlertCircle className="w-4 h-4" />
                      <span className="text-sm">Contains abnormal values</span>
                    </div>
                  )}
                  {selectedResult.critical && (
                    <div className="flex items-center space-x-2 text-red-600">
                      <AlertCircle className="w-4 h-4" />
                      <span className="text-sm font-medium">Critical values present</span>
                    </div>
                  )}
                </div>
              </div>
            </div>

            {/* Detailed Results */}
            {selectedResult.results && (
              <div>
                <h3 className="font-medium text-gray-900 mb-3">Detailed Results</h3>
                <div className="overflow-x-auto">
                  <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                      <tr>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Test</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Value</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Unit</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Reference Range</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                      </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                      {selectedResult.results.map((test, index) => (
                        <tr key={index}>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{test.test}</td>
                          <td className={`px-6 py-4 whitespace-nowrap text-sm font-medium ${getResultStatusColor(test.status)}`}>
                            {test.value}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{test.unit}</td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{test.range}</td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                              test.status === 'normal' ? 'bg-green-100 text-green-800' :
                              test.status === 'high' ? 'bg-red-100 text-red-800' :
                              test.status === 'low' ? 'bg-blue-100 text-blue-800' :
                              'bg-gray-100 text-gray-800'
                            }`}>
                              {test.status}
                            </span>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}

            {/* Actions */}
            <div className="flex space-x-4 pt-6 border-t border-gray-200">
              <button
                onClick={() => downloadPDF(selectedResult)}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors flex items-center"
              >
                <Download className="w-4 h-4 mr-2" />
                Download PDF
              </button>
              {selectedResult.imageUrl && (
                <button className="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors flex items-center">
                  <ExternalLink className="w-4 h-4 mr-2" />
                  View Images
                </button>
              )}
            </div>
          </div>
        </div>
      </div>
    );
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  const uniqueDoctors = [...new Set(results.map(result => result.doctor))];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Test Results</h1>
        <p className="text-gray-600">View and download your lab results and imaging reports</p>
      </div>

      {/* Filters and Search */}
      <div className="bg-white rounded-lg shadow p-6">
        <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between space-y-4 lg:space-y-0">
          <div className="flex space-x-4">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
              <input
                type="text"
                placeholder="Search results..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            <select
              value={filterDoctor}
              onChange={(e) => setFilterDoctor(e.target.value)}
              className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="all">All Doctors</option>
              {uniqueDoctors.map((doctor, index) => (
                <option key={index} value={doctor}>{doctor}</option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="bg-white rounded-lg shadow">
        <div className="border-b border-gray-200">
          <nav className="flex space-x-8 px-6">
            {[
              { id: 'all', label: 'All Results', count: results.length },
              { id: 'new', label: 'New', count: results.filter(r => r.isNew).length },
              { id: 'lab', label: 'Lab Results', count: results.filter(r => r.type === 'Lab').length },
              { id: 'imaging', label: 'Imaging', count: results.filter(r => r.type === 'Imaging').length },
              { id: 'abnormal', label: 'Abnormal', count: results.filter(r => r.abnormal).length }
            ].map(tab => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`py-4 px-1 border-b-2 font-medium text-sm ${
                  activeTab === tab.id
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                {tab.label} ({tab.count})
              </button>
            ))}
          </nav>
        </div>

        {/* Results List */}
        <div className="p-6">
          {filteredResults.length === 0 ? (
            <div className="text-center py-12">
              <FileText className="mx-auto h-12 w-12 text-gray-400" />
              <h3 className="mt-2 text-sm font-medium text-gray-900">No results found</h3>
              <p className="mt-1 text-sm text-gray-500">
                No test results match your current filters.
              </p>
            </div>
          ) : (
            <div className="space-y-4">
              {filteredResults.map(result => (
                <ResultCard key={result.id} result={result} />
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Detail Modal */}
      <ResultDetailModal />

      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <p className="text-red-700">Error loading results: {error}</p>
        </div>
      )}
    </div>
  );
};

export default Results;
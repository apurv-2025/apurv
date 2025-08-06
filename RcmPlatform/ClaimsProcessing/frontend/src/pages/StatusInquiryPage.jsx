// File: src/pages/StatusInquiryPage.jsx
import React, { useState } from 'react';
import { Search, AlertCircle, CheckCircle, Clock, XCircle } from 'lucide-react';

const StatusInquiryPage = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSearch = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    // Mock API call - replace with actual API
    setTimeout(() => {
      setSearchResults([
        {
          id: 'PA-12345678',
          patientName: 'John Doe',
          status: 'approved',
          submittedDate: '2025-06-10',
          lastUpdate: '2025-06-12'
        },
        {
          id: 'PA-87654321',
          patientName: 'Jane Smith',
          status: 'pending',
          submittedDate: '2025-06-11',
          lastUpdate: '2025-06-13'
        }
      ]);
      setLoading(false);
    }, 1000);
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'approved':
        return <CheckCircle className="w-5 h-5 text-green-500" />;
      case 'pending':
        return <Clock className="w-5 h-5 text-yellow-500" />;
      case 'denied':
        return <XCircle className="w-5 h-5 text-red-500" />;
      default:
        return <AlertCircle className="w-5 h-5 text-gray-500" />;
    }
  };

  return (
    <div className="p-6">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900 mb-2">Status Inquiry</h1>
        <p className="text-gray-600">Search for authorization request status</p>
      </div>

      <form onSubmit={handleSearch} className="mb-6">
        <div className="flex gap-4">
          <div className="flex-1">
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Enter request ID, patient name, or member ID..."
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          <button
            type="submit"
            disabled={loading}
            className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 flex items-center gap-2"
          >
            <Search className="w-4 h-4" />
            {loading ? 'Searching...' : 'Search'}
          </button>
        </div>
      </form>

      {searchResults.length > 0 && (
        <div className="bg-white rounded-lg shadow">
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="text-lg font-semibold">Search Results</h2>
          </div>
          <div className="divide-y divide-gray-200">
            {searchResults.map((result) => (
              <div key={result.id} className="p-6 hover:bg-gray-50">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    {getStatusIcon(result.status)}
                    <div>
                      <h3 className="font-semibold text-gray-900">{result.id}</h3>
                      <p className="text-sm text-gray-600">{result.patientName}</p>
                    </div>
                  </div>
                  <div className="text-right">
                    <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                      result.status === 'approved' ? 'bg-green-100 text-green-800' :
                      result.status === 'pending' ? 'bg-yellow-100 text-yellow-800' :
                      'bg-red-100 text-red-800'
                    }`}>
                      {result.status.charAt(0).toUpperCase() + result.status.slice(1)}
                    </span>
                    <p className="text-xs text-gray-500 mt-1">Updated: {result.lastUpdate}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default StatusInquiryPage;

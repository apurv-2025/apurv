import React, { useState, useEffect } from 'react';
import { TestTube, Calendar, User, Download, Eye, AlertTriangle, CheckCircle, XCircle } from 'lucide-react';
import { useAPI } from '../hooks/useAPI';

const LabResults = () => {
  const { get } = useAPI();
  const [labResults, setLabResults] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchLabResults();
  }, []);

  const fetchLabResults = async () => {
    try {
      const data = await get('/lab-results');
      setLabResults(data);
    } catch (error) {
      console.error('Error fetching lab results:', error);
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString();
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'normal':
        return <CheckCircle className="w-5 h-5 text-green-600" />;
      case 'abnormal':
        return <AlertTriangle className="w-5 h-5 text-yellow-600" />;
      case 'critical':
        return <XCircle className="w-5 h-5 text-red-600" />;
      default:
        return <TestTube className="w-5 h-5 text-gray-600" />;
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'normal':
        return 'bg-green-100 text-green-800';
      case 'abnormal':
        return 'bg-yellow-100 text-yellow-800';
      case 'critical':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-gray-800">Lab Results</h2>
      </div>

      <div className="bg-white rounded-lg shadow overflow-hidden">
        <div className="p-6 border-b border-gray-200">
          <h3 className="text-lg font-semibold text-gray-800">Recent Lab Results</h3>
        </div>
        
        {labResults.length === 0 ? (
          <div className="p-6 text-center text-gray-500">
            <TestTube className="w-12 h-12 mx-auto mb-4 text-gray-300" />
            <p>No lab results available</p>
          </div>
        ) : (
          <div className="divide-y divide-gray-200">
            {labResults.map((result) => (
              <div key={result.id} className="p-6 hover:bg-gray-50 transition-colors">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-4">
                    <div className="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center">
                      {getStatusIcon(result.status)}
                    </div>
                    <div className="flex-1">
                      <h4 className="text-lg font-medium text-gray-800">{result.test_name}</h4>
                      <div className="flex items-center space-x-4 text-sm text-gray-600 mt-1">
                        <span className="flex items-center space-x-1">
                          <Calendar className="w-4 h-4" />
                          <span>{formatDate(result.test_date)}</span>
                        </span>
                        <span>•</span>
                        <span className="flex items-center space-x-1">
                          <User className="w-4 h-4" />
                          <span>Dr. {result.ordering_doctor.first_name} {result.ordering_doctor.last_name}</span>
                        </span>
                      </div>
                      {result.result_value && (
                        <div className="mt-2">
                          <p className="text-sm text-gray-600">
                            <span className="font-medium">Result:</span> {result.result_value}
                          </p>
                          {result.reference_range && (
                            <p className="text-sm text-gray-600">
                              <span className="font-medium">Reference Range:</span> {result.reference_range}
                            </p>
                          )}
                        </div>
                      )}
                      {result.notes && (
                        <p className="text-sm text-gray-500 mt-1">{result.notes}</p>
                      )}
                    </div>
                  </div>
                  <div className="flex items-center space-x-3">
                    <span className={`px-3 py-1 rounded-full text-xs font-medium ${getStatusColor(result.status)}`}>
                      {result.status}
                    </span>
                    <div className="flex space-x-2">
                      <button className="p-2 text-gray-400 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors">
                        <Eye className="w-4 h-4" />
                      </button>
                      {result.file_path && (
                        <button className="p-2 text-gray-400 hover:text-green-600 hover:bg-green-50 rounded-lg transition-colors">
                          <Download className="w-4 h-4" />
                        </button>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Lab Results Information */}
      <div className="bg-purple-50 rounded-lg p-6">
        <div className="flex items-start space-x-3">
          <TestTube className="w-6 h-6 text-purple-600 mt-1" />
          <div>
            <h4 className="text-lg font-semibold text-purple-800 mb-2">Understanding Your Lab Results</h4>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm text-purple-700">
              <div>
                <p className="font-medium">Normal Results</p>
                <p>Results within the expected range for healthy individuals</p>
              </div>
              <div>
                <p className="font-medium">Abnormal Results</p>
                <p>Results outside the normal range, may require follow-up</p>
              </div>
              <div>
                <p className="font-medium">Critical Results</p>
                <p>Results requiring immediate medical attention</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LabResults; 
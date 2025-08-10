// File: src/pages/HistoryPage.js
import React, { useState } from 'react';
import { Clock, CheckCircle, Filter, Search } from 'lucide-react';
import Card from '../components/common/Card';
import Button from '../components/common/Button';
import { useApp } from '../contexts/AppContext';

const HistoryPage = () => {
  const { requests } = useApp();
  const [filter, setFilter] = useState('all');
  const [searchTerm, setSearchTerm] = useState('');

  const filteredRequests = requests.filter(request => {
    const matchesFilter = filter === 'all' || request.status === filter;
    const matchesSearch = request.member_id.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         request.id.toLowerCase().includes(searchTerm.toLowerCase());
    return matchesFilter && matchesSearch;
  });

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Request History</h1>
          <p className="text-gray-600">View and manage your eligibility verification requests</p>
        </div>
      </div>

      {/* Filters */}
      <Card>
        <div className="flex flex-col sm:flex-row gap-4">
          <div className="flex-1">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
              <input
                type="text"
                placeholder="Search by Member ID or Request ID..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10 w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>
          <div className="flex gap-2">
            {['all', 'submitted', 'completed'].map((status) => (
              <Button
                key={status}
                variant={filter === status ? 'primary' : 'secondary'}
                onClick={() => setFilter(status)}
                className="capitalize"
              >
                {status}
              </Button>
            ))}
          </div>
        </div>
      </Card>

      {/* Request List */}
      <Card>
        {filteredRequests.length === 0 ? (
          <div className="text-center py-12">
            <Clock className="h-12 w-12 text-gray-300 mx-auto mb-4" />
            <p className="text-gray-500">
              {requests.length === 0 ? 'No requests found' : 'No requests match your filters'}
            </p>
          </div>
        ) : (
          <div className="space-y-4">
            {filteredRequests.map((request) => (
              <div key={request.id} className="border border-gray-200 rounded-lg p-4">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    <div className={`h-3 w-3 rounded-full ${
                      request.status === 'completed' ? 'bg-green-400' : 'bg-yellow-400'
                    }`}></div>
                    <div>
                      <h3 className="text-sm font-medium text-gray-900">
                        Request ID: {request.id}
                      </h3>
                      <p className="text-sm text-gray-500">
                        Member ID: {request.member_id} | Provider NPI: {request.provider_npi}
                      </p>
                    </div>
                  </div>
                  
                  <div className="text-right">
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                      request.status === 'completed'
                        ? 'bg-green-100 text-green-800'
                        : 'bg-yellow-100 text-yellow-800'
                    }`}>
                      {request.status === 'completed' && <CheckCircle className="h-3 w-3 mr-1" />}
                      {request.status === 'submitted' && <Clock className="h-3 w-3 mr-1" />}
                      {request.status.charAt(0).toUpperCase() + request.status.slice(1)}
                    </span>
                    <p className="text-xs text-gray-500 mt-1">
                      {new Date(request.timestamp).toLocaleString()}
                    </p>
                  </div>
                </div>

                {request.result && (
                  <div className="mt-4 pt-4 border-t border-gray-100">
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                      <div>
                        <span className="font-medium text-gray-700">Status:</span>
                        <span className={`ml-2 ${
                          request.result.is_eligible ? 'text-green-600' : 'text-red-600'
                        }`}>
                          {request.result.is_eligible ? 'Eligible' : 'Not Eligible'}
                        </span>
                      </div>
                      <div>
                        <span className="font-medium text-gray-700">Processed:</span>
                        <span className="ml-2 text-gray-600">
                          {new Date(request.result.processed_at).toLocaleString()}
                        </span>
                      </div>
                      <div className="flex justify-end">
                        <Button
                          variant="secondary"
                          size="small"
                          onClick={() => {
                            // Implementation would show detailed results
                            console.log('Show details for:', request.id);
                          }}
                        >
                          View Details
                        </Button>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </Card>
    </div>
  );
};

export default HistoryPage;

import React, { useState, useEffect } from 'react';
import { Search, FileText, Eye, Download } from 'lucide-react';
import { claimsService } from '../services/claimsService';
import { formatCurrency, formatDate, filterClaims } from '../utils/helpers';
import StatusBadge from '../components/ui/StatusBadge';
import ClaimTypeBadge from '../components/ui/ClaimTypeBadge';
import LoadingSpinner from '../components/ui/LoadingSpinner';

const ClaimsList = () => {
  const [claims, setClaims] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('');

  useEffect(() => {
    const fetchClaims = async () => {
      try {
        setLoading(true);
        setError(null);
        const data = await claimsService.getClaims();
        setClaims(data);
      } catch (error) {
        console.error('Error fetching claims:', error);
        setError(error.message);
      } finally {
        setLoading(false);
      }
    };

    fetchClaims();
  }, []);

  const filteredClaims = filterClaims(claims, searchTerm, statusFilter);

  const handleViewClaim = (claimId) => {
    // TODO: Implement claim detail view
    console.log('View claim:', claimId);
  };

  const handleDownloadClaim = (claimId) => {
    // TODO: Implement claim download
    console.log('Download claim:', claimId);
  };

  if (loading) {
    return <LoadingSpinner fullPage text="Loading claims..." />;
  }

  if (error) {
    return (
      <div className="text-center py-12">
        <div className="text-red-600 mb-4">Error loading claims</div>
        <p className="text-gray-600">{error}</p>
        <button 
          onClick={() => window.location.reload()} 
          className="mt-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
        >
          Retry
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Filters */}
      <div className="bg-white p-6 rounded-lg shadow">
        <div className="flex flex-col sm:flex-row gap-4">
          <div className="flex-1">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
              <input
                type="text"
                placeholder="Search claims..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
          </div>
          <div className="sm:w-48">
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="">All Statuses</option>
              <option value="queued">Queued</option>
              <option value="validated">Validated</option>
              <option value="sent">Sent</option>
              <option value="paid">Paid</option>
              <option value="rejected">Rejected</option>
            </select>
          </div>
        </div>
      </div>

      {/* Claims Table */}
      <div className="bg-white shadow rounded-lg overflow-hidden">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Claim Details
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Patient
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Provider
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Financial
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Status
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {filteredClaims.map((claim) => (
                <tr key={claim.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex flex-col">
                      <div className="text-sm font-medium text-gray-900">{claim.claim_number}</div>
                      <div className="text-sm text-gray-500">
                        <ClaimTypeBadge type={claim.claim_type} />
                      </div>
                      <div className="text-xs text-gray-400 mt-1">
                        {formatDate(claim.created_at)}
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm font-medium text-gray-900">
                      {claim.patient_first_name} {claim.patient_last_name}
                    </div>
                    <div className="text-sm text-gray-500">{claim.payer?.name}</div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm font-medium text-gray-900">{claim.provider_name}</div>
                    <div className="text-sm text-gray-500">NPI: {claim.provider_npi}</div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm font-medium text-gray-900">
                      {formatCurrency(claim.total_charge)}
                    </div>
                    {claim.paid_amount && (
                      <div className="text-sm text-green-600">
                        Paid: {formatCurrency(claim.paid_amount)}
                      </div>
                    )}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <StatusBadge status={claim.status} />
                    {claim.validation_errors?.errors && (
                      <div className="text-xs text-red-600 mt-1">
                        {claim.validation_errors.errors.length} errors
                      </div>
                    )}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <button 
                      onClick={() => handleViewClaim(claim.id)}
                      className="text-blue-600 hover:text-blue-900 mr-3"
                      title="View claim details"
                    >
                      <Eye className="w-4 h-4" />
                    </button>
                    <button 
                      onClick={() => handleDownloadClaim(claim.id)}
                      className="text-gray-600 hover:text-gray-900"
                      title="Download claim"
                    >
                      <Download className="w-4 h-4" />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Empty State */}
      {filteredClaims.length === 0 && !loading && (
        <div className="text-center py-12">
          <FileText className="mx-auto h-12 w-12 text-gray-400" />
          <h3 className="mt-2 text-sm font-medium text-gray-900">No claims found</h3>
          <p className="mt-1 text-sm text-gray-500">
            {searchTerm || statusFilter 
              ? 'Try adjusting your search or filter criteria.' 
              : 'No claims have been uploaded yet.'}
          </p>
        </div>
      )}
    </div>
  );
};

export default ClaimsList;

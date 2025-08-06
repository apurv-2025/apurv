// File: src/pages/RemittancePage.jsx
import React, { useState, useEffect } from 'react';
import { Download, FileText, Calendar, DollarSign } from 'lucide-react';

const RemittancePage = () => {
  const [remittances, setRemittances] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Mock API call
    setTimeout(() => {
      setRemittances([
        {
          id: 'ERA-001',
          checkNumber: '12345',
          payerName: 'Blue Cross Blue Shield',
          amount: 1250.00,
          paymentDate: '2025-06-10',
          claimsCount: 5,
          status: 'processed'
        },
        {
          id: 'ERA-002',
          checkNumber: '12346',
          payerName: 'Aetna',
          amount: 890.50,
          paymentDate: '2025-06-12',
          claimsCount: 3,
          status: 'processed'
        }
      ]);
      setLoading(false);
    }, 1000);
  }, []);

  if (loading) {
    return (
      <div className="p-6">
        <div className="animate-pulse">
          <div className="h-8 bg-gray-300 rounded w-1/4 mb-4"></div>
          <div className="space-y-4">
            {[1, 2, 3].map(i => (
              <div key={i} className="h-20 bg-gray-300 rounded"></div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900 mb-2">Electronic Remittance Advice</h1>
        <p className="text-gray-600">View and download payment remittances</p>
      </div>

      <div className="bg-white rounded-lg shadow">
        <div className="px-6 py-4 border-b border-gray-200">
          <h2 className="text-lg font-semibold">Recent Remittances</h2>
        </div>
        <div className="divide-y divide-gray-200">
          {remittances.map((remittance) => (
            <div key={remittance.id} className="p-6">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                  <div className="p-3 bg-blue-100 rounded-lg">
                    <FileText className="w-6 h-6 text-blue-600" />
                  </div>
                  <div>
                    <h3 className="font-semibold text-gray-900">{remittance.id}</h3>
                    <p className="text-sm text-gray-600">{remittance.payerName}</p>
                    <div className="flex items-center gap-4 mt-1 text-xs text-gray-500">
                      <span className="flex items-center gap-1">
                        <Calendar className="w-3 h-3" />
                        {remittance.paymentDate}
                      </span>
                      <span className="flex items-center gap-1">
                        <DollarSign className="w-3 h-3" />
                        ${remittance.amount.toFixed(2)}
                      </span>
                      <span>{remittance.claimsCount} claims</span>
                    </div>
                  </div>
                </div>
                <button className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
                  <Download className="w-4 h-4" />
                  Download
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default RemittancePage;

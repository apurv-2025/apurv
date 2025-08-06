import React, { useState, useEffect } from 'react';
import { Pill, Calendar, User, RefreshCw, AlertCircle } from 'lucide-react';
import { useAPI } from '../hooks/useAPI';

const Medications = () => {
  const { get, post } = useAPI();
  const [medications, setMedications] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchMedications();
  }, []);

  const fetchMedications = async () => {
    try {
      const data = await get('/medications');
      setMedications(data);
    } catch (error) {
      console.error('Error fetching medications:', error);
    } finally {
      setLoading(false);
    }
  };

  const requestRefill = async (medicationId) => {
    try {
      await post(`/medications/${medicationId}/refill`);
      // Refresh medications after refill request
      fetchMedications();
    } catch (error) {
      console.error('Error requesting refill:', error);
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString();
  };

  const getRefillStatus = (refillsRemaining) => {
    if (refillsRemaining > 2) {
      return { color: 'text-green-600', icon: '✓', text: 'Good' };
    } else if (refillsRemaining > 0) {
      return { color: 'text-yellow-600', icon: '⚠', text: 'Low' };
    } else {
      return { color: 'text-red-600', icon: '✗', text: 'None' };
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
        <h2 className="text-2xl font-bold text-gray-800">Medications</h2>
      </div>

      <div className="bg-white rounded-lg shadow overflow-hidden">
        <div className="p-6 border-b border-gray-200">
          <h3 className="text-lg font-semibold text-gray-800">Current Medications</h3>
        </div>
        
        {medications.length === 0 ? (
          <div className="p-6 text-center text-gray-500">
            <Pill className="w-12 h-12 mx-auto mb-4 text-gray-300" />
            <p>No medications found</p>
          </div>
        ) : (
          <div className="divide-y divide-gray-200">
            {medications.map((medication) => {
              const refillStatus = getRefillStatus(medication.refills_remaining);
              return (
                <div key={medication.id} className="p-6 hover:bg-gray-50 transition-colors">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-4">
                      <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center">
                        <Pill className="w-6 h-6 text-green-600" />
                      </div>
                      <div className="flex-1">
                        <h4 className="text-lg font-medium text-gray-800">{medication.name}</h4>
                        <div className="flex items-center space-x-4 text-sm text-gray-600 mt-1">
                          <span>{medication.dosage}</span>
                          <span>•</span>
                          <span>{medication.frequency}</span>
                          <span>•</span>
                          <span className="flex items-center space-x-1">
                            <User className="w-4 h-4" />
                            <span>Dr. {medication.prescriber.first_name} {medication.prescriber.last_name}</span>
                          </span>
                        </div>
                        {medication.instructions && (
                          <p className="text-sm text-gray-500 mt-1">{medication.instructions}</p>
                        )}
                        <div className="flex items-center space-x-4 text-sm text-gray-600 mt-2">
                          <span className="flex items-center space-x-1">
                            <Calendar className="w-4 h-4" />
                            <span>Started: {formatDate(medication.start_date)}</span>
                          </span>
                          {medication.end_date && (
                            <>
                              <span>•</span>
                              <span>Ends: {formatDate(medication.end_date)}</span>
                            </>
                          )}
                        </div>
                      </div>
                    </div>
                    <div className="flex items-center space-x-4">
                      <div className="text-right">
                        <p className="text-sm text-gray-600">Refills Remaining</p>
                        <p className={`text-lg font-semibold ${refillStatus.color}`}>
                          {refillStatus.icon} {medication.refills_remaining}
                        </p>
                        <p className={`text-xs ${refillStatus.color}`}>{refillStatus.text}</p>
                      </div>
                      {medication.refills_remaining <= 2 && (
                        <button
                          onClick={() => requestRefill(medication.id)}
                          className="flex items-center space-x-2 bg-blue-600 text-white px-3 py-2 rounded-lg hover:bg-blue-700 transition-colors"
                        >
                          <RefreshCw className="w-4 h-4" />
                          <span>Request Refill</span>
                        </button>
                      )}
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>

      {/* Medication Tips */}
      <div className="bg-blue-50 rounded-lg p-6">
        <div className="flex items-start space-x-3">
          <AlertCircle className="w-6 h-6 text-blue-600 mt-1" />
          <div>
            <h4 className="text-lg font-semibold text-blue-800 mb-2">Medication Safety Tips</h4>
            <ul className="text-sm text-blue-700 space-y-1">
              <li>• Take medications exactly as prescribed by your doctor</li>
              <li>• Keep a list of all your medications and dosages</li>
              <li>• Don't stop taking medications without consulting your doctor</li>
              <li>• Store medications in a cool, dry place away from children</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Medications; 
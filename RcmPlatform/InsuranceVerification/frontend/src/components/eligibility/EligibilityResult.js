// File: src/components/eligibility/EligibilityResult.js
import React, { useState } from 'react';
import { CheckCircle, XCircle, Eye, Code } from 'lucide-react';
import Card from '../common/Card';
import Button from '../common/Button';
import Modal from '../common/Modal';

const EligibilityResult = ({ result }) => {
  const [showEDIModal, setShowEDIModal] = useState(false);

  const formatEDIContent = (content) => {
    return content.split('~').join('~\n');
  };

  return (
    <>
      <Card>
        <div className="flex items-center mb-4">
          {result.is_eligible ? (
            <CheckCircle className="h-6 w-6 text-green-500 mr-2" />
          ) : (
            <XCircle className="h-6 w-6 text-red-500 mr-2" />
          )}
          <h3 className="text-lg font-medium text-gray-900">
            Eligibility Result
          </h3>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Benefits Information */}
          <div>
            <h4 className="text-md font-medium text-gray-800 mb-3">
              Benefits Information
            </h4>
            <div className="space-y-3">
              <div className={`p-3 rounded-md ${
                result.is_eligible 
                  ? 'bg-green-50 border border-green-200' 
                  : 'bg-red-50 border border-red-200'
              }`}>
                <div className="text-sm font-medium">
                  Status: {result.is_eligible ? 'Eligible' : 'Not Eligible'}
                </div>
              </div>
              
              {result.benefits_info?.benefits && (
                <div className="space-y-2">
                  {Object.entries(result.benefits_info.benefits).map(([type, details]) => (
                    <div key={type} className="bg-gray-50 p-3 rounded-md">
                      <div className="text-sm font-medium text-gray-700 capitalize mb-1">
                        {type} Coverage
                      </div>
                      {Object.entries(details).map(([key, value]) => (
                        <div key={key} className="text-xs text-gray-600">
                          {key.replace('_', ' ')}: {value}
                        </div>
                      ))}
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>

          {/* EDI Response Preview */}
          <div>
            <div className="flex justify-between items-center mb-3">
              <h4 className="text-md font-medium text-gray-800">
                EDI 271 Response
              </h4>
              <Button
                variant="secondary"
                size="small"
                icon={Eye}
                onClick={() => setShowEDIModal(true)}
              >
                View Full Response
              </Button>
            </div>
            <div className="bg-gray-900 rounded-md p-4 overflow-hidden">
              <pre className="text-xs text-green-400 font-mono">
                {formatEDIContent(result.edi_271).substring(0, 200)}...
              </pre>
            </div>
          </div>
        </div>
      </Card>

      {/* EDI Full Response Modal */}
      <Modal
        isOpen={showEDIModal}
        onClose={() => setShowEDIModal(false)}
        title="Complete EDI 271 Response"
        size="large"
      >
        <div className="bg-gray-900 rounded-md p-4 max-h-96 overflow-auto">
          <pre className="text-xs text-green-400 font-mono whitespace-pre-wrap">
            {formatEDIContent(result.edi_271)}
          </pre>
        </div>
        <div className="mt-4 flex justify-end">
          <Button onClick={() => setShowEDIModal(false)}>
            Close
          </Button>
        </div>
      </Modal>
    </>
  );
};

export default EligibilityResult;

import React, { useState } from 'react';
import { X, CheckCircle, AlertCircle } from 'lucide-react';
import Survey from './Survey';

const SurveyModal = ({ 
  isOpen, 
  onClose, 
  surveyId, 
  surveyType = 'general', 
  appointmentId = null, 
  conversationId = null,
  onComplete = null 
}) => {
  const [isCompleted, setIsCompleted] = useState(false);

  const handleComplete = () => {
    setIsCompleted(true);
    if (onComplete) {
      onComplete();
    }
    // Auto-close after 3 seconds
    setTimeout(() => {
      handleClose();
    }, 3000);
  };

  const handleClose = () => {
    setIsCompleted(false);
    onClose();
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto">
      <div className="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        {/* Background overlay */}
        <div 
          className="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"
          onClick={handleClose}
        ></div>

        {/* Modal panel */}
        <div className="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-4xl sm:w-full">
          {/* Header */}
          <div className="bg-gray-50 px-4 py-3 sm:px-6 flex justify-between items-center">
            <h3 className="text-lg leading-6 font-medium text-gray-900">
              {isCompleted ? 'Survey Completed' : 'Patient Survey'}
            </h3>
            <button
              onClick={handleClose}
              className="text-gray-400 hover:text-gray-600 transition-colors"
            >
              <X className="w-6 h-6" />
            </button>
          </div>

          {/* Content */}
          <div className="px-4 py-6 sm:px-6">
            {isCompleted ? (
              <div className="text-center py-8">
                <CheckCircle className="w-16 h-16 text-green-500 mx-auto mb-4" />
                <h3 className="text-xl font-semibold text-gray-900 mb-2">
                  Thank You!
                </h3>
                <p className="text-gray-600 mb-4">
                  Your feedback has been submitted successfully. We appreciate your time and will use your responses to improve our services.
                </p>
                <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                  <div className="flex items-center space-x-2">
                    <AlertCircle className="w-5 h-5 text-green-500" />
                    <p className="text-green-700 text-sm">
                      This modal will close automatically in a few seconds.
                    </p>
                  </div>
                </div>
              </div>
            ) : (
              <Survey
                surveyId={surveyId}
                surveyType={surveyType}
                appointmentId={appointmentId}
                conversationId={conversationId}
                onComplete={handleComplete}
                onClose={handleClose}
              />
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default SurveyModal; 
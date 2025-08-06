import React, { useState } from 'react';
import { Bot, Loader2, CheckCircle, AlertCircle } from 'lucide-react';
import { agentService } from '../../services/agentService';

const ClaimAnalysisButton = ({ claimId, onAnalysisComplete }) => {
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysis, setAnalysis] = useState(null);
  const [error, setError] = useState(null);

  const handleAnalyze = async () => {
    setIsAnalyzing(true);
    setError(null);
    setAnalysis(null);

    try {
      const userId = 'user_' + Math.random().toString(36).substr(2, 9);
      const result = await agentService.analyzeClaim(claimId, userId);
      
      setAnalysis(result);
      if (onAnalysisComplete) {
        onAnalysisComplete(result);
      }
    } catch (err) {
      setError('Failed to analyze claim. Please try again.');
      console.error('Error analyzing claim:', err);
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleProcessRejection = async () => {
    setIsAnalyzing(true);
    setError(null);
    setAnalysis(null);

    try {
      const userId = 'user_' + Math.random().toString(36).substr(2, 9);
      const result = await agentService.processRejection(claimId, userId);
      
      setAnalysis(result);
      if (onAnalysisComplete) {
        onAnalysisComplete(result);
      }
    } catch (err) {
      setError('Failed to process rejection. Please try again.');
      console.error('Error processing rejection:', err);
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="relative">
      <div className="flex space-x-2">
        <button
          onClick={handleAnalyze}
          disabled={isAnalyzing}
          className="flex items-center px-3 py-1 text-xs bg-blue-100 text-blue-700 rounded-full hover:bg-blue-200 transition-colors disabled:opacity-50"
        >
          {isAnalyzing ? (
            <Loader2 className="w-3 h-3 mr-1 animate-spin" />
          ) : (
            <Bot className="w-3 h-3 mr-1" />
          )}
          Analyze
        </button>
        
        <button
          onClick={handleProcessRejection}
          disabled={isAnalyzing}
          className="flex items-center px-3 py-1 text-xs bg-red-100 text-red-700 rounded-full hover:bg-red-200 transition-colors disabled:opacity-50"
        >
          {isAnalyzing ? (
            <Loader2 className="w-3 h-3 mr-1 animate-spin" />
          ) : (
            <AlertCircle className="w-3 h-3 mr-1" />
          )}
          Fix Rejection
        </button>
      </div>

      {/* Analysis Results */}
      {analysis && (
        <div className="absolute top-full left-0 mt-2 w-80 bg-white border border-gray-200 rounded-lg shadow-lg z-10 p-4">
          <div className="flex items-center justify-between mb-3">
            <h4 className="font-medium text-gray-900">AI Analysis</h4>
            <button
              onClick={() => setAnalysis(null)}
              className="text-gray-400 hover:text-gray-600"
            >
              ×
            </button>
          </div>
          
          {analysis.analysis && (
            <div className="space-y-3">
              {analysis.analysis.status && (
                <div className="flex items-center space-x-2">
                  <CheckCircle className="w-4 h-4 text-green-600" />
                  <span className="text-sm font-medium text-gray-900">
                    Status: {analysis.analysis.status}
                  </span>
                </div>
              )}
              
              {analysis.analysis.confidence_score && (
                <div className="text-sm text-gray-600">
                  Confidence: {(analysis.analysis.confidence_score * 100).toFixed(1)}%
                </div>
              )}
              
              {analysis.analysis.recommendations && analysis.analysis.recommendations.length > 0 && (
                <div>
                  <p className="text-sm font-medium text-gray-900 mb-2">Recommendations:</p>
                  <ul className="text-sm text-gray-600 space-y-1">
                    {analysis.analysis.recommendations.map((rec, index) => (
                      <li key={index} className="flex items-start space-x-2">
                        <span className="text-blue-600 mt-1">•</span>
                        <span>{rec}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
              
              {analysis.analysis.suggested_fixes && analysis.analysis.suggested_fixes.length > 0 && (
                <div>
                  <p className="text-sm font-medium text-gray-900 mb-2">Suggested Fixes:</p>
                  <ul className="text-sm text-gray-600 space-y-1">
                    {analysis.analysis.suggested_fixes.map((fix, index) => (
                      <li key={index} className="flex items-start space-x-2">
                        <span className="text-green-600 mt-1">•</span>
                        <span>{fix}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
              
              {analysis.analysis.rejection_reason && (
                <div>
                  <p className="text-sm font-medium text-gray-900 mb-1">Rejection Reason:</p>
                  <p className="text-sm text-red-600">{analysis.analysis.rejection_reason}</p>
                </div>
              )}
            </div>
          )}
        </div>
      )}

      {/* Error Message */}
      {error && (
        <div className="absolute top-full left-0 mt-2 w-80 bg-red-50 border border-red-200 rounded-lg shadow-lg z-10 p-4">
          <div className="flex items-center space-x-2">
            <AlertCircle className="w-4 h-4 text-red-600" />
            <span className="text-sm text-red-800">{error}</span>
          </div>
        </div>
      )}
    </div>
  );
};

export default ClaimAnalysisButton; 
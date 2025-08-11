// File: src/hooks/useEligibilityCheck.js
import { useState, useCallback } from 'react';
import { apiService } from '../services/apiService';
import { useToast } from '../contexts/ToastContext';
import { useApp } from '../contexts/AppContext';

export const useEligibilityCheck = () => {
  const [submitting, setSubmitting] = useState(false);
  const { showSuccess, showError } = useToast();
  const { dispatch } = useApp();

  const checkResponse = useCallback(async (requestId) => {
    try {
      const result = await apiService.getEligibilityResponse(requestId);
      
      dispatch({ type: 'SET_ELIGIBILITY_RESULT', payload: result });
      dispatch({ 
        type: 'UPDATE_REQUEST', 
        payload: { id: requestId, status: 'completed', result } 
      });
      
      showSuccess('Eligibility response received!');
      
      return result;
    } catch (error) {
      console.error('Error checking eligibility response:', error);
    }
  }, [dispatch, showSuccess]);

  const submitEligibilityInquiry = useCallback(async (requestData) => {
    try {
      setSubmitting(true);
      
      const result = await apiService.submitEligibilityInquiry(requestData);
      
      const newRequest = {
        id: result.request_id,
        status: 'submitted',
        timestamp: new Date().toISOString(),
        member_id: requestData.member_id,
        provider_npi: requestData.provider_npi
      };
      
      dispatch({ type: 'ADD_REQUEST', payload: newRequest });
      
      showSuccess('Eligibility inquiry submitted successfully!');
      
      // Check for response after delay
      setTimeout(() => checkResponse(result.request_id), 2000);
      
      return result;
    } catch (error) {
      showError(error.message || 'Failed to submit eligibility inquiry');
      throw error;
    } finally {
      setSubmitting(false);
    }
  }, [dispatch, showSuccess, showError, checkResponse]);

  return {
    submitEligibilityInquiry,
    checkResponse,
    submitting
  };
};

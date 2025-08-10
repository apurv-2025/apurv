// File: src/hooks/usePriorAuthorization.js - Custom Hook for Prior Authorization
import { useState, useCallback } from 'react';
import { useAuthorization } from '../contexts/AuthorizationContext';
import { useNotification } from '../contexts/NotificationContext';
import { authorizationService } from '../services/authorizationService';
import { ValidationService } from '../services/validationService';

export const usePriorAuthorization = () => {
  const { dispatch } = useAuthorization();
  const { showSuccess, showError } = useNotification();
  const [validationErrors, setValidationErrors] = useState({});

  const submitRequest = useCallback(async (requestData) => {
    // Validate request data
    const validation = ValidationService.validatePriorAuthorizationRequest(requestData);
    
    if (!validation.isValid) {
      setValidationErrors(validation.errors);
      showError('Please correct the validation errors');
      return null;
    }

    setValidationErrors({});
    dispatch({ type: 'SET_LOADING', payload: true });

    try {
      // In a real app, this would call the API
      // const result = await authorizationService.submitPriorAuthorizationRequest(requestData);
      
      // Simulate API call for demo
      const result = {
        request_id: `AUTH${Date.now()}`,
        status: 'submitted',
        message: 'Prior authorization request submitted successfully'
      };

      const newRequest = {
        id: result.request_id,
        status: 'submitted',
        timestamp: new Date().toISOString(),
        patient_name: `${requestData.patient_first_name} ${requestData.patient_last_name}`,
        member_id: requestData.member_id,
        provider_npi: requestData.requesting_provider_npi,
        priority: requestData.priority
      };

      dispatch({ type: 'ADD_REQUEST', payload: newRequest });
      
      // Simulate response processing
      setTimeout(() => {
        const response = {
          id: result.request_id,
          status: 'completed',
          result: {
            response_code: 'A1',
            authorization_number: `AUTH${Math.random().toString(36).substr(2, 8).toUpperCase()}`,
            processed_at: new Date().toISOString(),
            decision_reason: 'Approved - meets medical necessity criteria'
          }
        };
        
        dispatch({ type: 'UPDATE_REQUEST', payload: response });
        showSuccess('Authorization request approved!');
      }, 3000);

      showSuccess('Prior authorization request submitted successfully!');
      return result;
    } catch (error) {
      dispatch({ type: 'SET_ERROR', payload: error.message });
      showError(`Failed to submit request: ${error.message}`);
      return null;
    }
  }, [dispatch, showSuccess, showError]);

  const checkResponse = useCallback(async (requestId) => {
    try {
      // In a real app: const result = await authorizationService.getPriorAuthorizationResponse(requestId);
      // For demo, we simulate the response
      showSuccess('Checking for response...');
    } catch (error) {
      showError(`Failed to check response: ${error.message}`);
    }
  }, [showSuccess, showError]);

  return {
    submitRequest,
    checkResponse,
    validationErrors,
    setValidationErrors
  };
};

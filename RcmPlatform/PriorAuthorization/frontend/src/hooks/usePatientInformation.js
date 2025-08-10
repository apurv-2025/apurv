// File: src/hooks/usePatientInformation.js - Custom Hook for Patient Information
import { useState, useCallback } from 'react';
import { useAuthorization } from '../contexts/AuthorizationContext';
import { useNotification } from '../contexts/NotificationContext';
import { authorizationService } from '../services/authorizationService';
import { ValidationService } from '../services/validationService';

export const usePatientInformation = () => {
  const { dispatch } = useAuthorization();
  const { showSuccess, showError } = useNotification();
  const [validationErrors, setValidationErrors] = useState({});

  const createPatient = useCallback(async (patientData) => {
    // Validate patient data
    const validation = ValidationService.validatePatientInformation(patientData);
    
    if (!validation.isValid) {
      setValidationErrors(validation.errors);
      showError('Please correct the validation errors');
      return null;
    }

    setValidationErrors({});
    dispatch({ type: 'SET_LOADING', payload: true });

    try {
      // In a real app: const result = await authorizationService.createPatientInformation(patientData);
      
      // Simulate API call for demo
      const result = {
        id: `PAT${Date.now()}`,
        patient_id: `PID${Date.now()}`,
        ...patientData,
        created_at: new Date().toISOString(),
        edi_275_content: `ISA*00*...~ST*275*...~` // Simulated EDI content
      };

      dispatch({ type: 'ADD_PATIENT', payload: result });
      showSuccess('Patient information created successfully!');
      return result;
    } catch (error) {
      dispatch({ type: 'SET_ERROR', payload: error.message });
      showError(`Failed to create patient: ${error.message}`);
      return null;
    }
  }, [dispatch, showSuccess, showError]);

  const generateEDI275 = useCallback(async (patientId) => {
    try {
      // In a real app: const result = await authorizationService.getPatientEDI275(patientId);
      showSuccess('EDI 275 generated successfully!');
      return { edi_275: 'ISA*00*...~ST*275*...~' }; // Simulated
    } catch (error) {
      showError(`Failed to generate EDI 275: ${error.message}`);
      return null;
    }
  }, [showSuccess, showError]);

  return {
    createPatient,
    generateEDI275,
    validationErrors,
    setValidationErrors
  };
};

// File: src/hooks/useFileUpload.js
import { useState, useCallback } from 'react';
import { fileService } from '../services/fileService';
import { apiService } from '../services/apiService';
import { useToast } from '../contexts/ToastContext';
import { useApp } from '../contexts/AppContext';

export const useFileUpload = () => {
  const [uploading, setUploading] = useState(false);
  const { showSuccess, showError } = useToast();
  const { dispatch } = useApp();

  const uploadFile = useCallback(async (file) => {
    try {
      setUploading(true);
      
      // Validate file
      fileService.validateFile(file);
      
      // Upload file
      const result = await apiService.uploadFile(file);
      
      // Update app state
      dispatch({ type: 'SET_EXTRACTED_DATA', payload: result.extracted_data });
      dispatch({ type: 'ADD_UPLOADED_FILE', payload: { file, result } });
      
      showSuccess('File uploaded and processed successfully!');
      
      return result;
    } catch (error) {
      showError(error.message || 'Failed to upload file');
      throw error;
    } finally {
      setUploading(false);
    }
  }, [dispatch, showSuccess, showError]);

  return {
    uploadFile,
    uploading
  };
};

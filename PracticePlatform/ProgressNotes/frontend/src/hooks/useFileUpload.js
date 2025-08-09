import { useState } from 'react';
import FileService from '../services/fileService';
import { validateFileUpload } from '../utils/fileUtils';

export const useFileUpload = (noteId, onSuccess, onError) => {
  const [uploading, setUploading] = useState(false);
  const [dragOver, setDragOver] = useState(false);

  const uploadFiles = async (files) => {
    setUploading(true);
    
    try {
      // Validate all files first
      Array.from(files).forEach(validateFileUpload);
      
      const result = await FileService.uploadFiles(noteId, files);
      onSuccess?.(result);
      return result;
    } catch (error) {
      onError?.(error.message);
      throw error;
    } finally {
      setUploading(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragOver(false);
    const files = e.dataTransfer.files;
    if (files.length > 0) {
      uploadFiles(files);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setDragOver(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setDragOver(false);
  };

  return {
    uploading,
    dragOver,
    uploadFiles,
    handleDrop,
    handleDragOver,
    handleDragLeave
  };
};

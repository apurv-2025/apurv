// File: src/components/upload/FileUpload.js
import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { Camera, Upload } from 'lucide-react';
import Card from '../common/Card';
import LoadingSpinner from '../common/LoadingSpinner';
import { useFileUpload } from '../../hooks/useFileUpload';

const FileUpload = () => {
  const { uploadFile, uploading } = useFileUpload();

  const onDrop = useCallback(async (acceptedFiles) => {
    if (acceptedFiles.length > 0) {
      await uploadFile(acceptedFiles[0]);
    }
  }, [uploadFile]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png', '.tiff'],
      'application/pdf': ['.pdf']
    },
    maxFiles: 1,
    disabled: uploading
  });

  return (
    <Card>
      <div
        {...getRootProps()}
        className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors cursor-pointer ${
          isDragActive
            ? 'border-blue-400 bg-blue-50'
            : 'border-gray-300 hover:border-gray-400'
        } ${uploading ? 'opacity-50 cursor-not-allowed' : ''}`}
      >
        <input {...getInputProps()} />
        
        {uploading ? (
          <LoadingSpinner size="large" text="Processing file..." />
        ) : (
          <>
            <Camera className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <p className="text-lg text-gray-600 mb-2">
              {isDragActive
                ? 'Drop your insurance card here'
                : 'Drop your insurance card image or PDF here'
              }
            </p>
            <p className="text-sm text-gray-500 mb-4">
              or click to browse files
            </p>
            <div className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700">
              <Upload className="h-4 w-4 mr-2" />
              Select File
            </div>
            <p className="text-xs text-gray-400 mt-4">
              Supports: JPEG, PNG, TIFF, PDF (Max 10MB)
            </p>
          </>
        )}
      </div>
    </Card>
  );
};

export default FileUpload;


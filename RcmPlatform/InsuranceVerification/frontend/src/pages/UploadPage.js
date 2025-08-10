// File: src/pages/UploadPage.js
import React from 'react';
import FileUpload from '../components/upload/FileUpload';
import ExtractedDataDisplay from '../components/upload/ExtractedDataDisplay';
import { useApp } from '../contexts/AppContext';

const UploadPage = () => {
  const { extractedData } = useApp();

  return (
    <div className="space-y-6">
      <div className="text-center">
        <h1 className="text-2xl font-bold text-gray-900 mb-2">
          Upload Insurance Card
        </h1>
        <p className="text-gray-600">
          Upload an image or PDF of an insurance card to extract information using OCR
        </p>
      </div>

      <FileUpload />
      
      {extractedData && <ExtractedDataDisplay data={extractedData} />}
    </div>
  );
};

export default UploadPage;

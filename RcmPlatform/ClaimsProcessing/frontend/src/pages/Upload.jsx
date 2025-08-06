import React, { useState } from 'react';
import { Upload as UploadIcon, CheckCircle, XCircle, Heart, Stethoscope, Building } from 'lucide-react';
import { claimsService } from '../services/claimsService';
import { PAYERS, UPLOAD_CONFIG } from '../utils/constants';

const Upload = () => {
  const [dragActive, setDragActive] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [uploadResult, setUploadResult] = useState(null);
  const [selectedPayer, setSelectedPayer] = useState('1');

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  const handleFileSelect = (e) => {
    if (e.target.files && e.target.files[0]) {
      handleFile(e.target.files[0]);
    }
  };

  const handleFile = async (file) => {
    setUploading(true);
    setUploadResult(null);

    try {
      const result = await claimsService.uploadClaim(file, selectedPayer);
      setUploadResult({
        success: true,
        message: 'File uploaded successfully!',
        claim: result
      });
    } catch (error) {
      setUploadResult({
        success: false,
        message: error.message || 'Upload failed. Please try again.'
      });
    } finally {
      setUploading(false);
    }
  };

  const resetUpload = () => {
    setUploadResult(null);
    // Reset file input
    const fileInput = document.getElementById('file-upload');
    if (fileInput) {
      fileInput.value = '';
    }
  };

  return (
    <div className="space-y-6">
      <div className="bg-white p-6 rounded-lg shadow">
        <h2 className="text-lg font-medium text-gray-900 mb-4">Upload EDI Claims File</h2>
        
        {/* Payer Selection */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Select Payer
          </label>
          <select
            value={selectedPayer}
            onChange={(e) => setSelectedPayer(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            disabled={uploading}
          >
            {PAYERS.map(payer => (
              <option key={payer.id} value={payer.id}>{payer.name}</option>
            ))}
          </select>
        </div>

        {/* Upload Area */}
        <div
          className={`relative border-2 border-dashed rounded-lg p-6 transition-colors ${
            dragActive
              ? 'border-blue-400 bg-blue-50'
              : 'border-gray-300 hover:border-gray-400'
          }`}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
        >
          <div className="text-center">
            <UploadIcon className="mx-auto h-12 w-12 text-gray-400" />
            <div className="mt-4">
              <label htmlFor="file-upload" className="cursor-pointer">
                <span className="mt-2 block text-sm font-medium text-gray-900">
                  Drop EDI files here, or{' '}
                  <span className="text-blue-600 hover:text-blue-500">browse</span>
                </span>
                <input
                  id="file-upload"
                  name="file-upload"
                  type="file"
                  className="sr-only"
                  accept={UPLOAD_CONFIG.acceptedMimeTypes}
                  onChange={handleFileSelect}
                  disabled={uploading}
                />
              </label>
              <p className="mt-1 text-xs text-gray-500">
                Supports: {UPLOAD_CONFIG.acceptedExtensions.join(', ')} files (Max {(UPLOAD_CONFIG.maxFileSize / (1024 * 1024)).toFixed(1)}MB)
              </p>
            </div>
          </div>

          {uploading && (
            <div className="absolute inset-0 bg-white bg-opacity-90 flex items-center justify-center rounded-lg">
              <div className="text-center">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 mx-auto"></div>
                <p className="mt-2 text-sm text-gray-600">Processing file...</p>
              </div>
            </div>
          )}
        </div>

        {/* Upload Result */}
        {uploadResult && (
          <div className={`mt-4 p-4 rounded-md ${
            uploadResult.success 
              ? 'bg-green-50 border border-green-200' 
              : 'bg-red-50 border border-red-200'
          }`}>
            <div className="flex">
              {uploadResult.success ? (
                <CheckCircle className="h-5 w-5 text-green-400" />
              ) : (
                <XCircle className="h-5 w-5 text-red-400" />
              )}
              <div className="ml-3 flex-1">
                <p className={`text-sm font-medium ${
                  uploadResult.success ? 'text-green-800' : 'text-red-800'
                }`}>
                  {uploadResult.message}
                </p>
                {uploadResult.success && uploadResult.claim && (
                  <p className="mt-1 text-sm text-green-600">
                    Claim Number: {uploadResult.claim.claim_number}
                  </p>
                )}
              </div>
              <button
                onClick={resetUpload}
                className="text-sm text-gray-500 hover:text-gray-700 ml-2"
              >
                ×
              </button>
            </div>
          </div>
        )}
      </div>

      {/* File Format Help */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
        <h3 className="text-lg font-medium text-blue-900 mb-3">Supported Claim Types</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="flex items-center">
            <Heart className="w-5 h-5 text-purple-600 mr-2 flex-shrink-0" />
            <div>
              <p className="font-medium text-purple-900">837D - Dental Claims</p>
              <p className="text-sm text-purple-700">CDT procedure codes, tooth numbers</p>
            </div>
          </div>
          <div className="flex items-center">
            <Stethoscope className="w-5 h-5 text-blue-600 mr-2 flex-shrink-0" />
            <div>
              <p className="font-medium text-blue-900">837P - Professional Claims</p>
              <p className="text-sm text-blue-700">CPT codes, physician services</p>
            </div>
          </div>
          <div className="flex items-center">
            <Building className="w-5 h-5 text-orange-600 mr-2 flex-shrink-0" />
            <div>
              <p className="font-medium text-orange-900">837I - Institutional Claims</p>
              <p className="text-sm text-orange-700">Hospital, facility services</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Upload;

import React, { useRef } from 'react';
import { Upload } from 'lucide-react';
import { useFileUpload } from '../../../hooks/useFileUpload';
import { useNotificationContext } from '../../common/Notification/NotificationProvider';

const FileUploadZone = ({ noteId, onFilesUploaded }) => {
  const fileInputRef = useRef(null);
  const { showSuccess, showError } = useNotificationContext();

  const {
    uploading,
    dragOver,
    uploadFiles,
    handleDrop,
    handleDragOver,
    handleDragLeave
  } = useFileUpload(
    noteId,
    (result) => {
      showSuccess(`${result.length} file(s) uploaded successfully`);
      onFilesUploaded?.(result);
    },
    (error) => showError(error)
  );

  const handleFileSelect = (files) => {
    if (files && files.length > 0) {
      uploadFiles(files);
    }
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-medium text-gray-900">Attachments</h3>
        <button
          onClick={() => fileInputRef.current?.click()}
          disabled={uploading}
          className="px-3 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 flex items-center"
        >
          <Upload className="h-4 w-4 mr-2" />
          {uploading ? 'Uploading...' : 'Add Files'}
        </button>
      </div>

      {/* Drag and Drop Area */}
      <div
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        className={`border-2 border-dashed rounded-lg p-6 text-center transition-colors ${
          dragOver 
            ? 'border-blue-500 bg-blue-50' 
            : 'border-gray-300 hover:border-gray-400'
        }`}
      >
        <Upload className="h-8 w-8 text-gray-400 mx-auto mb-2" />
        <p className="text-gray-600">
          Drag and drop files here, or{' '}
          <button
            onClick={() => fileInputRef.current?.click()}
            className="text-blue-600 hover:text-blue-800"
          >
            click to browse
          </button>
        </p>
        <p className="text-xs text-gray-500 mt-1">
          Supported formats: PDF, DOC, DOCX, JPG, PNG (Max 10MB)
        </p>
      </div>

      <input
        ref={fileInputRef}
        type="file"
        multiple
        accept=".pdf,.doc,.docx,.jpg,.jpeg,.png"
        onChange={(e) => handleFileSelect(e.target.files)}
        className="hidden"
      />
    </div>
  );
};

export default FileUploadZone;

// File: src/pages/EDIProcessingPage.jsx
import React, { useState } from 'react';
import { Upload, FileText, CheckCircle, AlertCircle, Clock } from 'lucide-react';

const EDIProcessingPage = () => {
  const [files, setFiles] = useState([]);
  const [dragActive, setDragActive] = useState(false);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    const droppedFiles = Array.from(e.dataTransfer.files);
    processFiles(droppedFiles);
  };

  const handleFileInput = (e) => {
    const selectedFiles = Array.from(e.target.files);
    processFiles(selectedFiles);
  };

  const processFiles = (newFiles) => {
    const processedFiles = newFiles.map(file => ({
      id: Math.random().toString(36).substr(2, 9),
      name: file.name,
      size: file.size,
      status: 'processing',
      type: file.name.includes('837') ? '837 (Claim)' : 
            file.name.includes('835') ? '835 (Remittance)' : 
            file.name.includes('278') ? '278 (Authorization)' : 'Unknown',
      uploadedAt: new Date().toISOString()
    }));

    setFiles(prev => [...prev, ...processedFiles]);

    // Simulate processing
    processedFiles.forEach(file => {
      setTimeout(() => {
        setFiles(prev => prev.map(f => 
          f.id === file.id 
            ? { ...f, status: Math.random() > 0.2 ? 'completed' : 'error' }
            : f
        ));
      }, Math.random() * 3000 + 1000);
    });
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'completed':
        return <CheckCircle className="w-5 h-5 text-green-500" />;
      case 'error':
        return <AlertCircle className="w-5 h-5 text-red-500" />;
      case 'processing':
        return <Clock className="w-5 h-5 text-yellow-500 animate-spin" />;
      default:
        return <FileText className="w-5 h-5 text-gray-500" />;
    }
  };

  return (
    <div className="p-6">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900 mb-2">EDI Processing</h1>
        <p className="text-gray-600">Upload and process EDI transaction files</p>
      </div>

      <div
        className={`mb-6 border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
          dragActive 
            ? 'border-blue-500 bg-blue-50' 
            : 'border-gray-300 hover:border-gray-400'
        }`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
      >
        <Upload className="w-12 h-12 text-gray-400 mx-auto mb-4" />
        <h3 className="text-lg font-semibold text-gray-900 mb-2">Upload EDI Files</h3>
        <p className="text-gray-600 mb-4">
          Drag and drop your EDI files here, or click to browse
        </p>
        <input
          type="file"
          multiple
          accept=".edi,.txt,.x12"
          onChange={handleFileInput}
          className="hidden"
          id="file-input"
        />
        <label
          htmlFor="file-input"
          className="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 cursor-pointer"
        >
          Choose Files
        </label>
      </div>

      {files.length > 0 && (
        <div className="bg-white rounded-lg shadow">
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="text-lg font-semibold">Processing Queue</h2>
          </div>
          <div className="divide-y divide-gray-200">
            {files.map((file) => (
              <div key={file.id} className="p-6">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    {getStatusIcon(file.status)}
                    <div>
                      <h3 className="font-medium text-gray-900">{file.name}</h3>
                      <p className="text-sm text-gray-600">{file.type}</p>
                    </div>
                  </div>
                  <div className="text-right">
                    <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                      file.status === 'completed' ? 'bg-green-100 text-green-800' :
                      file.status === 'error' ? 'bg-red-100 text-red-800' :
                      'bg-yellow-100 text-yellow-800'
                    }`}>
                      {file.status.charAt(0).toUpperCase() + file.status.slice(1)}
                    </span>
                    <p className="text-xs text-gray-500 mt-1">
                      {(file.size / 1024).toFixed(1)} KB
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default EDIProcessingPage;

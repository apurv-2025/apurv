// src/components/Tasks/CreateTaskModal.jsx
import React, { useState, useEffect } from 'react';
import { X, Upload, FileText, Trash2, ChevronDown } from 'lucide-react';

const CreateTaskModal = ({ 
  isOpen, 
  onClose, 
  onSave, 
  clients = [], 
  initialTask = null,
  loading = false 
}) => {
  const [taskData, setTaskData] = useState({
    name: '',
    description: '',
    dueDate: '',
    dueTime: '',
    priority: 'none',
    clientId: '',
    status: 'todo'
  });
  const [attachments, setAttachments] = useState([]);
  const [errors, setErrors] = useState([]);

  useEffect(() => {
    if (initialTask) {
      setTaskData(initialTask);
      setAttachments(initialTask.attachments || []);
    } else {
      setTaskData({
        name: '',
        description: '',
        dueDate: '',
        dueTime: '',
        priority: 'none',
        clientId: '',
        status: 'todo'
      });
      setAttachments([]);
    }
    setErrors([]);
  }, [initialTask, isOpen]);

  const handleInputChange = (field, value) => {
    setTaskData(prev => ({
      ...prev,
      [field]: value
    }));
    
    if (errors.length > 0) {
      setErrors([]);
    }
  };

  const handleFilesSelected = (files) => {
    const newAttachments = Array.from(files).map(file => ({
      id: Date.now() + Math.random(),
      file,
      fileName: file.name,
      fileSize: file.size,
      fileType: file.type,
      url: URL.createObjectURL(file)
    }));
    
    setAttachments(prev => [...prev, ...newAttachments]);
  };

  const removeAttachment = (attachmentId) => {
    setAttachments(prev => {
      const updated = prev.filter(att => att.id !== attachmentId);
      const removed = prev.find(att => att.id === attachmentId);
      if (removed && removed.url && removed.url.startsWith('blob:')) {
        URL.revokeObjectURL(removed.url);
      }
      return updated;
    });
  };

  const handleSave = async () => {
    if (!taskData.name.trim()) {
      setErrors(['Task name is required']);
      return;
    }

    try {
      const taskDataWithAttachments = {
        ...taskData,
        attachments: attachments
      };
      
      await onSave(taskDataWithAttachments);
      onClose();
    } catch (error) {
      setErrors([error.message || 'Failed to save task']);
    }
  };

  const priorityOptions = [
    { value: 'none', label: 'None' },
    { value: 'low', label: 'Low' },
    { value: 'medium', label: 'Medium' },
    { value: 'high', label: 'High' },
    { value: 'urgent', label: 'Urgent' }
  ];

  const clientOptions = [
    { value: '', label: 'Select client' },
    ...clients.map(client => ({
      value: client.id,
      label: client.name
    }))
  ];

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-end z-50">
      <div className="bg-white h-full w-96 overflow-y-auto">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <h2 className="text-lg font-semibold text-gray-900">
            {initialTask ? 'Edit task' : 'Create task'}
          </h2>
          <button
            onClick={onClose}
            className="p-1 hover:bg-gray-100 rounded"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Form */}
        <div className="p-6 space-y-6">
          {errors.length > 0 && (
            <div className="bg-red-50 border border-red-200 rounded-md p-3">
              <ul className="text-red-600 text-sm space-y-1">
                {errors.map((error, index) => (
                  <li key={index}>{error}</li>
                ))}
              </ul>
            </div>
          )}

          {/* Task Name */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Task name
            </label>
            <input
              type="text"
              value={taskData.name}
              onChange={(e) => handleInputChange('name', e.target.value)}
              placeholder="Write a task"
              className="form-input"
            />
          </div>

          {/* Description */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Description
            </label>
            <textarea
              value={taskData.description}
              onChange={(e) => handleInputChange('description', e.target.value)}
              placeholder="Add task description"
              rows={4}
              className="form-textarea"
            />
          </div>

          {/* Due Date and Time */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Due on
            </label>
            <div className="flex space-x-2">
              <input
                type="date"
                value={taskData.dueDate}
                onChange={(e) => handleInputChange('dueDate', e.target.value)}
                className="form-input flex-1"
              />
              <input
                type="time"
                value={taskData.dueTime}
                onChange={(e) => handleInputChange('dueTime', e.target.value)}
                className="form-input flex-1"
              />
            </div>
          </div>

          {/* Priority */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Priority
            </label>
            <div className="relative">
              <select
                value={taskData.priority}
                onChange={(e) => handleInputChange('priority', e.target.value)}
                className="form-select"
              >
                {priorityOptions.map((option) => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>
              <ChevronDown className="absolute right-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-500 pointer-events-none" />
            </div>
          </div>

          {/* Client */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Client
            </label>
            <div className="relative">
              <select
                value={taskData.clientId || ''}
                onChange={(e) => handleInputChange('clientId', e.target.value || null)}
                className="form-select"
              >
                {clientOptions.map((option) => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>
              <ChevronDown className="absolute right-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-500 pointer-events-none" />
            </div>
          </div>

          {/* Attachments */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Attachments
            </label>
            
            <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-gray-400 cursor-pointer">
              <input
                type="file"
                multiple
                className="hidden"
                id="file-upload"
                onChange={(e) => handleFilesSelected(e.target.files)}
                accept=".pdf,.doc,.docx,.txt,.jpg,.png,.gif"
              />
              <label htmlFor="file-upload" className="cursor-pointer">
                <div className="flex flex-col items-center space-y-2">
                  <div className="w-12 h-12 bg-gray-100 rounded-full flex items-center justify-center">
                    <Upload className="w-6 h-6 text-gray-400" />
                  </div>
                  
                  <div className="text-sm">
                    <span className="text-blue-600 hover:text-blue-700 font-medium">
                      Choose file
                    </span>
                    <span className="text-gray-500"> or drag and drop file</span>
                  </div>
                  
                  <div className="text-xs text-gray-500">
                    <div>Max number of attachments: 20</div>
                    <div>Max upload size: 50MB</div>
                  </div>
                </div>
              </label>
            </div>

            {/* Attachment List */}
            {attachments.length > 0 && (
              <div className="mt-4 space-y-2">
                {attachments.map((attachment) => (
                  <div
                    key={attachment.id}
                    className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
                  >
                    <div className="flex items-center space-x-3">
                      <FileText className="w-4 h-4 text-gray-500" />
                      <div>
                        <p className="text-sm font-medium text-gray-900">
                          {attachment.fileName}
                        </p>
                        <p className="text-xs text-gray-500">
                          {`${(attachment.fileSize / 1024).toFixed(1)} KB`}
                        </p>
                      </div>
                    </div>
                    <button
                      onClick={() => removeAttachment(attachment.id)}
                      className="p-1 hover:bg-gray-200 rounded"
                    >
                      <Trash2 className="w-4 h-4 text-gray-500" />
                    </button>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Footer */}
        <div className="border-t border-gray-200 p-6 flex justify-end space-x-3">
          <button
            onClick={onClose}
            disabled={loading}
            className="btn-secondary"
          >
            Cancel
          </button>
          <button
            onClick={handleSave}
            disabled={loading}
            className="btn-primary"
          >
            {loading && <div className="loading mr-2"></div>}
            {initialTask ? 'Update' : 'Save'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default CreateTaskModal;

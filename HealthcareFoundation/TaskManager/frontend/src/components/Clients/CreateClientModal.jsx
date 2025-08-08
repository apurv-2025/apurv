// src/components/Clients/CreateClientModal.jsx
import React, { useState, useEffect } from 'react';
import { X } from 'lucide-react';
import Button from '../UI/Button';
import Input from '../UI/Input';
import TextArea from '../UI/TextArea';

const CreateClientModal = ({ 
  isOpen, 
  onClose, 
  onSave, 
  initialClient = null,
  loading = false 
}) => {
  const [clientData, setClientData] = useState({
    name: '',
    email: '',
    phone: '',
    company: '',
    notes: ''
  });
  const [errors, setErrors] = useState({});

  useEffect(() => {
    if (initialClient) {
      setClientData(initialClient);
    } else {
      setClientData({
        name: '',
        email: '',
        phone: '',
        company: '',
        notes: ''
      });
    }
    setErrors({});
  }, [initialClient, isOpen]);

  const handleInputChange = (field, value) => {
    setClientData(prev => ({
      ...prev,
      [field]: value
    }));
    
    // Clear error when user starts typing
    if (errors[field]) {
      setErrors(prev => ({
        ...prev,
        [field]: null
      }));
    }
  };

  const validateForm = () => {
    const newErrors = {};
    
    if (!clientData.name.trim()) {
      newErrors.name = 'Name is required';
    }
    
    if (clientData.email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(clientData.email)) {
      newErrors.email = 'Invalid email format';
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSave = async () => {
    if (!validateForm()) return;
    
    try {
      await onSave(clientData);
      onClose();
    } catch (error) {
      setErrors({ general: error.message || 'Failed to save client' });
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg w-full max-w-md mx-4">
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <h2 className="text-lg font-semibold text-gray-900">
            {initialClient ? 'Edit Client' : 'Create Client'}
          </h2>
          <button
            onClick={onClose}
            className="p-1 hover:bg-gray-100 rounded"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="p-6 space-y-4">
          {errors.general && (
            <div className="bg-red-50 border border-red-200 rounded-md p-3">
              <p className="text-red-600 text-sm">{errors.general}</p>
            </div>
          )}

          <Input
            label="Name *"
            value={clientData.name}
            onChange={(e) => handleInputChange('name', e.target.value)}
            placeholder="Client name"
            error={errors.name}
          />

          <Input
            label="Email"
            type="email"
            value={clientData.email}
            onChange={(e) => handleInputChange('email', e.target.value)}
            placeholder="client@example.com"
            error={errors.email}
          />

          <Input
            label="Phone"
            value={clientData.phone}
            onChange={(e) => handleInputChange('phone', e.target.value)}
            placeholder="(555) 123-4567"
            error={errors.phone}
          />

          <Input
            label="Company"
            value={clientData.company}
            onChange={(e) => handleInputChange('company', e.target.value)}
            placeholder="Company name"
            error={errors.company}
          />

          <TextArea
            label="Notes"
            value={clientData.notes}
            onChange={(e) => handleInputChange('notes', e.target.value)}
            placeholder="Additional notes..."
            rows={3}
            error={errors.notes}
          />
        </div>

        <div className="border-t border-gray-200 p-6 flex justify-end space-x-3">
          <Button
            variant="secondary"
            onClick={onClose}
            disabled={loading}
          >
            Cancel
          </Button>
          <Button
            variant="primary"
            onClick={handleSave}
            loading={loading}
          >
            {initialClient ? 'Update' : 'Create'}
          </Button>
        </div>
      </div>
    </div>
  );
};

export default CreateClientModal;

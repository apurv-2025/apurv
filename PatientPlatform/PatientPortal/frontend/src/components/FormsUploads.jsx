import React, { useState, useEffect } from 'react';
import { 
  Upload, FileText, Camera, Download, Eye, Plus, Check, X, Clock, 
  AlertCircle, Search, Filter, Calendar, User, Paperclip, Shield,
  ChevronDown, ChevronRight, Edit, Trash2, Send, Save
} from 'lucide-react';
import { useAPI } from '../hooks/useAPI';

const FormsUploads = () => {
  const [activeTab, setActiveTab] = useState('forms');
  const [formsData, setFormsData] = useState({
    availableForms: [],
    completedForms: [],
    uploadedDocuments: [],
    pendingForms: []
  });
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState('all');
  const [loading, setLoading] = useState(true);
  const [showFormModal, setShowFormModal] = useState(false);
  const [selectedForm, setSelectedForm] = useState(null);
  const [showUploadModal, setShowUploadModal] = useState(false);
  const [dragActive, setDragActive] = useState(false);

  useEffect(() => {
    // Mock comprehensive forms and uploads data
    const mockData = {
      // Available Form Templates
      availableForms: [
        {
          id: 1,
          title: 'Patient Registration Form',
          category: 'Registration',
          description: 'Complete patient intake form for new patients',
          estimatedTime: '10-15 minutes',
          required: true,
          status: 'available',
          fields: [
            { name: 'personalInfo', label: 'Personal Information', type: 'section' },
            { name: 'firstName', label: 'First Name', type: 'text', required: true },
            { name: 'lastName', label: 'Last Name', type: 'text', required: true },
            { name: 'dateOfBirth', label: 'Date of Birth', type: 'date', required: true },
            { name: 'gender', label: 'Gender', type: 'select', options: ['Male', 'Female', 'Other', 'Prefer not to say'], required: true },
            { name: 'phone', label: 'Phone Number', type: 'tel', required: true },
            { name: 'email', label: 'Email Address', type: 'email', required: true },
            { name: 'address', label: 'Address', type: 'textarea', required: true },
            { name: 'emergencyContact', label: 'Emergency Contact', type: 'section' },
            { name: 'emergencyName', label: 'Emergency Contact Name', type: 'text', required: true },
            { name: 'emergencyPhone', label: 'Emergency Contact Phone', type: 'tel', required: true },
            { name: 'emergencyRelation', label: 'Relationship', type: 'text', required: true }
          ]
        },
        {
          id: 2,
          title: 'Medical History Questionnaire',
          category: 'Medical History',
          description: 'Comprehensive medical and family history form',
          estimatedTime: '20-25 minutes',
          required: true,
          status: 'available',
          fields: [
            { name: 'currentMedications', label: 'Current Medications', type: 'section' },
            { name: 'medications', label: 'List all current medications', type: 'textarea', placeholder: 'Include dosage and frequency' },
            { name: 'allergies', label: 'Known Allergies', type: 'textarea', placeholder: 'Include drug, food, and environmental allergies' },
            { name: 'medicalHistory', label: 'Medical History', type: 'section' },
            { name: 'previousSurgeries', label: 'Previous Surgeries', type: 'textarea' },
            { name: 'chronicConditions', label: 'Chronic Medical Conditions', type: 'textarea' },
            { name: 'familyHistory', label: 'Family Medical History', type: 'textarea' },
            { name: 'lifestyle', label: 'Lifestyle Information', type: 'section' },
            { name: 'smoking', label: 'Smoking Status', type: 'select', options: ['Never', 'Former', 'Current'] },
            { name: 'alcohol', label: 'Alcohol Use', type: 'select', options: ['Never', 'Occasional', 'Regular', 'Daily'] },
            { name: 'exercise', label: 'Exercise Frequency', type: 'select', options: ['None', '1-2 times/week', '3-4 times/week', 'Daily'] }
          ]
        },
        {
          id: 3,
          title: 'Insurance Information Form',
          category: 'Insurance',
          description: 'Update insurance and billing information',
          estimatedTime: '5-10 minutes',
          required: false,
          status: 'available',
          fields: [
            { name: 'primaryInsurance', label: 'Primary Insurance', type: 'section' },
            { name: 'insuranceCompany', label: 'Insurance Company', type: 'text', required: true },
            { name: 'policyNumber', label: 'Policy Number', type: 'text', required: true },
            { name: 'groupNumber', label: 'Group Number', type: 'text' },
            { name: 'subscriberName', label: 'Subscriber Name', type: 'text', required: true },
            { name: 'secondaryInsurance', label: 'Secondary Insurance (if applicable)', type: 'section' },
            { name: 'secondaryCompany', label: 'Secondary Insurance Company', type: 'text' },
            { name: 'secondaryPolicy', label: 'Secondary Policy Number', type: 'text' }
          ]
        },
        {
          id: 4,
          title: 'Pre-Visit Symptom Checker',
          category: 'Symptoms',
          description: 'Document current symptoms before your appointment',
          estimatedTime: '5-8 minutes',
          required: false,
          status: 'available',
          fields: [
            { name: 'chiefComplaint', label: 'Main Concern', type: 'textarea', placeholder: 'What brings you in today?', required: true },
            { name: 'symptomDuration', label: 'How long have you had these symptoms?', type: 'select', options: ['Less than 1 day', '1-3 days', '1 week', '2-4 weeks', 'More than 1 month'] },
            { name: 'painLevel', label: 'Pain Level (0-10)', type: 'range', min: 0, max: 10 },
            { name: 'additionalSymptoms', label: 'Additional Symptoms', type: 'textarea' },
            { name: 'medications', label: 'Medications taken for this issue', type: 'textarea' }
          ]
        },
        {
          id: 5,
          title: 'COVID-19 Screening Form',
          category: 'Screening',
          description: 'Required COVID-19 health screening',
          estimatedTime: '2-3 minutes',
          required: true,
          status: 'available',
          fields: [
            { name: 'symptoms', label: 'COVID-19 Symptoms', type: 'section' },
            { name: 'fever', label: 'Have you had a fever in the last 14 days?', type: 'radio', options: ['Yes', 'No'], required: true },
            { name: 'cough', label: 'Do you have a new or worsening cough?', type: 'radio', options: ['Yes', 'No'], required: true },
            { name: 'breathing', label: 'Do you have difficulty breathing?', type: 'radio', options: ['Yes', 'No'], required: true },
            { name: 'exposure', label: 'Have you been exposed to COVID-19?', type: 'radio', options: ['Yes', 'No', 'Unknown'], required: true },
            { name: 'travel', label: 'Have you traveled recently?', type: 'radio', options: ['Yes', 'No'], required: true }
          ]
        }
      ],

      // Completed Forms
      completedForms: [
        {
          id: 101,
          formId: 1,
          title: 'Patient Registration Form',
          completedDate: '2024-02-01',
          status: 'submitted',
          submittedBy: 'John Smith',
          reviewedBy: 'Dr. Sarah Johnson',
          reviewDate: '2024-02-02',
          responses: {
            firstName: 'John',
            lastName: 'Smith',
            dateOfBirth: '1985-05-15',
            gender: 'Male',
            phone: '555-0123',
            email: 'john.smith@email.com'
          }
        },
        {
          id: 102,
          formId: 5,
          title: 'COVID-19 Screening Form',
          completedDate: '2024-02-15',
          status: 'approved',
          submittedBy: 'John Smith',
          reviewedBy: 'Clinic Staff',
          reviewDate: '2024-02-15',
          responses: {
            fever: 'No',
            cough: 'No',
            breathing: 'No',
            exposure: 'No',
            travel: 'No'
          }
        }
      ],

      // Uploaded Documents
      uploadedDocuments: [
        {
          id: 201,
          fileName: 'Insurance_Card_Front.jpg',
          category: 'Insurance',
          fileType: 'image/jpeg',
          fileSize: '2.1 MB',
          uploadDate: '2024-02-10',
          uploadedBy: 'John Smith',
          status: 'verified',
          description: 'Primary insurance card - front side',
          tags: ['insurance', 'primary', 'blue-cross']
        },
        {
          id: 202,
          fileName: 'Insurance_Card_Back.jpg',
          category: 'Insurance',
          fileType: 'image/jpeg',
          fileSize: '1.8 MB',
          uploadDate: '2024-02-10',
          uploadedBy: 'John Smith',
          status: 'verified',
          description: 'Primary insurance card - back side',
          tags: ['insurance', 'primary', 'blue-cross']
        },
        {
          id: 203,
          fileName: 'Drivers_License.jpg',
          category: 'Identification',
          fileType: 'image/jpeg',
          fileSize: '1.5 MB',
          uploadDate: '2024-02-05',
          uploadedBy: 'John Smith',
          status: 'verified',
          description: 'Photo identification',
          tags: ['id', 'drivers-license']
        },
        {
          id: 204,
          fileName: 'Lab_Results_Jan2024.pdf',
          category: 'Medical Records',
          fileType: 'application/pdf',
          fileSize: '856 KB',
          uploadDate: '2024-01-25',
          uploadedBy: 'John Smith',
          status: 'reviewed',
          description: 'Lab results from previous provider',
          tags: ['lab-results', 'external', 'blood-work']
        }
      ],

      // Pending Forms
      pendingForms: [
        {
          id: 301,
          formId: 2,
          title: 'Medical History Questionnaire',
          assignedDate: '2024-02-01',
          dueDate: '2024-02-20',
          status: 'pending',
          priority: 'high',
          assignedBy: 'Dr. Sarah Johnson',
          reminder: true
        },
        {
          id: 302,
          formId: 4,
          title: 'Pre-Visit Symptom Checker',
          assignedDate: '2024-02-12',
          dueDate: '2024-02-18',
          status: 'in-progress',
          priority: 'medium',
          assignedBy: 'Dr. Michael Chen',
          reminder: false,
          progress: 60
        }
      ]
    };

    setFormsData(mockData);
    setLoading(false);
  }, []);

  const getStatusColor = (status) => {
    switch (status) {
      case 'submitted': case 'verified': case 'approved': return 'bg-green-100 text-green-800';
      case 'pending': case 'available': return 'bg-blue-100 text-blue-800';
      case 'in-progress': return 'bg-yellow-100 text-yellow-800';
      case 'rejected': case 'expired': return 'bg-red-100 text-red-800';
      case 'reviewed': return 'bg-purple-100 text-purple-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'submitted': case 'verified': case 'approved': return Check;
      case 'pending': case 'available': return Clock;
      case 'in-progress': return AlertCircle;
      case 'rejected': case 'expired': return X;
      default: return FileText;
    }
  };

  const getCategoryIcon = (category) => {
    switch (category) {
      case 'Insurance': return Shield;
      case 'Medical History': return FileText;
      case 'Registration': return User;
      case 'Screening': return AlertCircle;
      case 'Identification': return Camera;
      case 'Medical Records': return FileText;
      default: return FileText;
    }
  };

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

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
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFiles(e.dataTransfer.files);
    }
  };

  const handleFiles = (files) => {
    Array.from(files).forEach(file => {
      console.log('Uploading file:', file.name);
      // In real implementation, this would upload the file
      alert(`File "${file.name}" would be uploaded here`);
    });
  };

  const AvailableFormsTab = () => (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold text-gray-900">Available Forms</h3>
        <div className="flex space-x-4">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
            <input
              type="text"
              placeholder="Search forms..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          <select
            value={filterStatus}
            onChange={(e) => setFilterStatus(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="all">All Categories</option>
            <option value="Registration">Registration</option>
            <option value="Medical History">Medical History</option>
            <option value="Insurance">Insurance</option>
            <option value="Screening">Screening</option>
            <option value="Symptoms">Symptoms</option>
          </select>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {formsData.availableForms
          .filter(form => 
            (filterStatus === 'all' || form.category === filterStatus) &&
            (searchTerm === '' || form.title.toLowerCase().includes(searchTerm.toLowerCase()) || 
             form.description.toLowerCase().includes(searchTerm.toLowerCase()))
          )
          .map(form => {
            const CategoryIcon = getCategoryIcon(form.category);
            
            return (
              <div key={form.id} className="bg-white border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow">
                <div className="flex items-start justify-between mb-4">
                  <div className="flex items-center space-x-3">
                    <CategoryIcon className="w-6 h-6 text-blue-600" />
                    <div>
                      <h4 className="font-semibold text-gray-900">{form.title}</h4>
                      <p className="text-sm text-gray-600">{form.category}</p>
                    </div>
                  </div>
                  {form.required && (
                    <span className="px-2 py-1 bg-red-100 text-red-800 text-xs rounded-full font-medium">
                      Required
                    </span>
                  )}
                </div>

                <p className="text-sm text-gray-600 mb-4">{form.description}</p>

                <div className="flex items-center justify-between text-sm text-gray-500 mb-4">
                  <span>📝 {form.fields.length} fields</span>
                  <span>⏱️ {form.estimatedTime}</span>
                </div>

                <div className="flex space-x-3">
                  <button
                    onClick={() => {
                      setSelectedForm(form);
                      setShowFormModal(true);
                    }}
                    className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                  >
                    Fill Out Form
                  </button>
                  <button className="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors">
                    Preview
                  </button>
                </div>
              </div>
            );
          })}
      </div>
    </div>
  );

  const CompletedFormsTab = () => (
    <div className="space-y-6">
      <h3 className="text-lg font-semibold text-gray-900">Completed Forms</h3>
      
      <div className="space-y-4">
        {formsData.completedForms.map(form => {
          const StatusIcon = getStatusIcon(form.status);
          
          return (
            <div key={form.id} className="bg-white border border-gray-200 rounded-lg p-6">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center space-x-3 mb-2">
                    <StatusIcon className="w-5 h-5 text-green-600" />
                    <h4 className="font-semibold text-gray-900">{form.title}</h4>
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(form.status)}`}>
                      {form.status}
                    </span>
                  </div>
                  
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm text-gray-600">
                    <div className="flex items-center space-x-2">
                      <Calendar className="w-4 h-4" />
                      <span>Completed: {form.completedDate}</span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <User className="w-4 h-4" />
                      <span>Submitted by: {form.submittedBy}</span>
                    </div>
                    {form.reviewedBy && (
                      <div className="flex items-center space-x-2">
                        <Check className="w-4 h-4" />
                        <span>Reviewed by: {form.reviewedBy}</span>
                      </div>
                    )}
                  </div>
                </div>
                
                <div className="flex space-x-2 ml-4">
                  <button className="px-3 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors text-sm flex items-center">
                    <Eye className="w-4 h-4 mr-1" />
                    View
                  </button>
                  <button className="px-3 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors text-sm flex items-center">
                    <Download className="w-4 h-4 mr-1" />
                    PDF
                  </button>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );

  const DocumentsTab = () => (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold text-gray-900">Uploaded Documents</h3>
        <button
          onClick={() => setShowUploadModal(true)}
          className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors flex items-center"
        >
          <Upload className="w-4 h-4 mr-2" />
          Upload Document
        </button>
      </div>

      {/* Quick Upload Area */}
      <div
        className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
          dragActive ? 'border-blue-500 bg-blue-50' : 'border-gray-300'
        }`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
      >
        <Upload className="mx-auto h-12 w-12 text-gray-400" />
        <div className="mt-4">
          <label className="cursor-pointer">
            <span className="mt-2 block text-sm font-medium text-gray-900">
              Drop files here or click to upload
            </span>
            <span className="mt-1 block text-sm text-gray-500">
              PNG, JPG, PDF up to 10MB
            </span>
            <input
              type="file"
              className="sr-only"
              multiple
              accept=".png,.jpg,.jpeg,.pdf"
              onChange={(e) => handleFiles(e.target.files)}
            />
          </label>
        </div>
      </div>

      {/* Documents List */}
      <div className="space-y-4">
        {formsData.uploadedDocuments.map(doc => {
          const CategoryIcon = getCategoryIcon(doc.category);
          const StatusIcon = getStatusIcon(doc.status);
          
          return (
            <div key={doc.id} className="bg-white border border-gray-200 rounded-lg p-6">
              <div className="flex items-start justify-between">
                <div className="flex items-start space-x-4 flex-1">
                  <CategoryIcon className="w-8 h-8 text-blue-600 mt-1" />
                  
                  <div className="flex-1">
                    <div className="flex items-center space-x-3 mb-2">
                      <h4 className="font-medium text-gray-900">{doc.fileName}</h4>
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(doc.status)}`}>
                        {doc.status}
                      </span>
                    </div>
                    
                    <p className="text-sm text-gray-600 mb-2">{doc.description}</p>
                    
                    <div className="grid grid-cols-1 md:grid-cols-4 gap-4 text-sm text-gray-500">
                      <span>📁 {doc.category}</span>
                      <span>📄 {doc.fileType.split('/')[1].toUpperCase()}</span>
                      <span>💾 {doc.fileSize}</span>
                      <span>📅 {doc.uploadDate}</span>
                    </div>
                    
                    {doc.tags && (
                      <div className="flex flex-wrap gap-1 mt-3">
                        {doc.tags.map((tag, index) => (
                          <span key={index} className="px-2 py-1 bg-gray-100 text-gray-600 text-xs rounded">
                            {tag}
                          </span>
                        ))}
                      </div>
                    )}
                  </div>
                </div>
                
                <div className="flex space-x-2 ml-4">
                  <button className="px-3 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors text-sm">
                    <Eye className="w-4 h-4" />
                  </button>
                  <button className="px-3 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors text-sm">
                    <Download className="w-4 h-4" />
                  </button>
                  <button className="px-3 py-2 border border-red-300 text-red-700 rounded-lg hover:bg-red-50 transition-colors text-sm">
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );

  const PendingFormsTab = () => (
    <div className="space-y-6">
      <h3 className="text-lg font-semibold text-gray-900">Pending Forms</h3>
      
      <div className="space-y-4">
        {formsData.pendingForms.map(form => (
          <div key={form.id} className="bg-white border border-gray-200 rounded-lg p-6">
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <div className="flex items-center space-x-3 mb-2">
                  <h4 className="font-semibold text-gray-900">{form.title}</h4>
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                    form.priority === 'high' ? 'bg-red-100 text-red-800' :
                    form.priority === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                    'bg-green-100 text-green-800'
                  }`}>
                    {form.priority} priority
                  </span>
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(form.status)}`}>
                    {form.status}
                  </span>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm text-gray-600 mb-4">
                  <div className="flex items-center space-x-2">
                    <Calendar className="w-4 h-4" />
                    <span>Assigned: {form.assignedDate}</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <Clock className="w-4 h-4" />
                    <span>Due: {form.dueDate}</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <User className="w-4 h-4" />
                    <span>Assigned by: {form.assignedBy}</span>
                  </div>
                </div>

                {form.progress && (
                  <div className="mb-4">
                    <div className="flex items-center justify-between text-sm text-gray-600 mb-1">
                      <span>Progress</span>
                      <span>{form.progress}%</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div 
                        className="bg-blue-600 h-2 rounded-full" 
                        style={{ width: `${form.progress}%` }}
                      ></div>
                    </div>
                  </div>
                )}
              </div>
              
              <div className="flex space-x-2 ml-4">
                <button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm">
                  {form.status === 'in-progress' ? 'Continue' : 'Start'}
                </button>
                {form.reminder && (
                  <button className="px-3 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors text-sm">
                    Remind Later
                  </button>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  const FormModal = () => {
    const [formData, setFormData] = useState({});
    const [currentSection, setCurrentSection] = useState(0);

    if (!showFormModal || !selectedForm) return null;

    const handleSubmit = (e) => {
      e.preventDefault();
      console.log('Submitting form:', formData);
      alert('Form submitted successfully!');
      setShowFormModal(false);
      setSelectedForm(null);
      setFormData({});
    };

    const sections = selectedForm.fields.reduce((acc, field) => {
      if (field.type === 'section') {
        acc.push({ title: field.label, fields: [] });
      } else if (acc.length > 0) {
        acc[acc.length - 1].fields.push(field);
      }
      return acc;
    }, []);

    const currentSectionData = sections[currentSection];

    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
        <div className="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-y-auto">
          <div className="p-6 border-b border-gray-200">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-xl font-semibold text-gray-900">{selectedForm.title}</h2>
                <p className="text-gray-600">{selectedForm.description}</p>
              </div>
              <button 
                onClick={() => setShowFormModal(false)}
                className="text-gray-400 hover:text-gray-600"
              >
                <X className="w-6 h-6" />
              </button>
            </div>

            {/* Progress Bar */}
            <div className="mt-4">
              <div className="flex items-center justify-between text-sm text-gray-600 mb-2">
                <span>Section {currentSection + 1} of {sections.length}</span>
                <span>{Math.round(((currentSection + 1) / sections.length) * 100)}% Complete</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div 
                  className="bg-blue-600 h-2 rounded-full transition-all" 
                  style={{ width: `${((currentSection + 1) / sections.length) * 100}%` }}
                ></div>
              </div>
            </div>
          </div>

          <form onSubmit={handleSubmit} className="p-6">
            {currentSectionData && (
              <div className="space-y-6">
                <h3 className="text-lg font-medium text-gray-900">{currentSectionData.title}</h3>
                
                {currentSectionData.fields.map(field => (
                  <div key={field.name}>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      {field.label}
                      {field.required && <span className="text-red-500 ml-1">*</span>}
                    </label>
                    
                    {field.type === 'text' || field.type === 'email' || field.type === 'tel' ? (
                      <input
                        type={field.type}
                        value={formData[field.name] || ''}
                        onChange={(e) => setFormData({...formData, [field.name]: e.target.value})}
                        placeholder={field.placeholder}
                        required={field.required}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      />
                    ) : field.type === 'textarea' ? (
                      <textarea
                        value={formData[field.name] || ''}
                        onChange={(e) => setFormData({...formData, [field.name]: e.target.value})}
                        placeholder={field.placeholder}
                        required={field.required}
                        rows="3"
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      />
                    ) : field.type === 'select' ? (
                      <select
                        value={formData[field.name] || ''}
                        onChange={(e) => setFormData({...formData, [field.name]: e.target.value})}
                        required={field.required}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      >
                        <option value="">Select an option</option>
                        {field.options.map(option => (
                          <option key={option} value={option}>{option}</option>
                        ))}
                      </select>
                    ) : field.type === 'radio' ? (
                      <div className="space-y-2">
                        {field.options.map(option => (
                          <label key={option} className="flex items-center">
                            <input
                              type="radio"
                              name={field.name}
                              value={option}
                              checked={formData[field.name] === option}
                              onChange={(e) => setFormData({...formData, [field.name]: e.target.value})}
                              required={field.required}
                              className="mr-2"
                            />
                            <span className="text-sm text-gray-700">{option}</span>
                          </label>
                        ))}
                      </div>
                    ) : field.type === 'date' ? (
                      <input
                        type="date"
                        value={formData[field.name] || ''}
                        onChange={(e) => setFormData({...formData, [field.name]: e.target.value})}
                        required={field.required}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      />
                    ) : field.type === 'range' ? (
                      <div>
                        <input
                          type="range"
                          min={field.min}
                          max={field.max}
                          value={formData[field.name] || field.min}
                          onChange={(e) => setFormData({...formData, [field.name]: e.target.value})}
                          className="w-full"
                        />
                        <div className="flex justify-between text-sm text-gray-500 mt-1">
                          <span>{field.min}</span>
                          <span className="font-medium">{formData[field.name] || field.min}</span>
                          <span>{field.max}</span>
                        </div>
                      </div>
                    ) : null}
                  </div>
                ))}
              </div>
            )}

            <div className="flex justify-between pt-6 mt-6 border-t border-gray-200">
              <button
                type="button"
                onClick={() => setCurrentSection(Math.max(0, currentSection - 1))}
                disabled={currentSection === 0}
                className="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Previous
              </button>
              
              <div className="flex space-x-4">
                <button
                  type="button"
                  onClick={() => {
                    console.log('Saving draft:', formData);
                    alert('Draft saved!');
                  }}
                  className="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors flex items-center"
                >
                  <Save className="w-4 h-4 mr-2" />
                  Save Draft
                </button>
                
                {currentSection < sections.length - 1 ? (
                  <button
                    type="button"
                    onClick={() => setCurrentSection(currentSection + 1)}
                    className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                  >
                    Next
                  </button>
                ) : (
                  <button
                    type="submit"
                    className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors flex items-center"
                  >
                    <Send className="w-4 h-4 mr-2" />
                    Submit Form
                  </button>
                )}
              </div>
            </div>
          </form>
        </div>
      </div>
    );
  };

  const UploadModal = () => {
    const [uploadData, setUploadData] = useState({
      category: '',
      description: '',
      tags: ''
    });

    if (!showUploadModal) return null;

    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
        <div className="bg-white rounded-lg max-w-2xl w-full">
          <div className="p-6 border-b border-gray-200">
            <div className="flex items-center justify-between">
              <h2 className="text-xl font-semibold text-gray-900">Upload Document</h2>
              <button 
                onClick={() => setShowUploadModal(false)}
                className="text-gray-400 hover:text-gray-600"
              >
                <X className="w-6 h-6" />
              </button>
            </div>
          </div>

          <div className="p-6 space-y-6">
            <div
              className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center"
              onDrop={handleDrop}
              onDragOver={handleDrag}
            >
              <Upload className="mx-auto h-12 w-12 text-gray-400" />
              <div className="mt-4">
                <label className="cursor-pointer">
                  <span className="mt-2 block text-sm font-medium text-gray-900">
                    Click to upload or drag and drop
                  </span>
                  <span className="mt-1 block text-sm text-gray-500">
                    PNG, JPG, PDF up to 10MB
                  </span>
                  <input
                    type="file"
                    className="sr-only"
                    multiple
                    accept=".png,.jpg,.jpeg,.pdf"
                    onChange={(e) => handleFiles(e.target.files)}
                  />
                </label>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Document Category
              </label>
              <select
                value={uploadData.category}
                onChange={(e) => setUploadData({...uploadData, category: e.target.value})}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="">Select category</option>
                <option value="Insurance">Insurance</option>
                <option value="Identification">Identification</option>
                <option value="Medical Records">Medical Records</option>
                <option value="Lab Results">Lab Results</option>
                <option value="Prescriptions">Prescriptions</option>
                <option value="Other">Other</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Description
              </label>
              <textarea
                value={uploadData.description}
                onChange={(e) => setUploadData({...uploadData, description: e.target.value})}
                rows="3"
                placeholder="Brief description of the document..."
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Tags (comma separated)
              </label>
              <input
                type="text"
                value={uploadData.tags}
                onChange={(e) => setUploadData({...uploadData, tags: e.target.value})}
                placeholder="e.g., insurance, primary, blue-cross"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            <div className="flex space-x-4 pt-6">
              <button
                onClick={() => setShowUploadModal(false)}
                className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={() => {
                  console.log('Upload configuration:', uploadData);
                  alert('Upload configuration saved!');
                  setShowUploadModal(false);
                }}
                className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                Upload
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Forms & Uploads</h1>
        <p className="text-gray-600">Complete intake forms and upload important documents</p>
      </div>

      {/* Quick Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-white p-4 rounded-lg shadow border border-gray-200">
          <div className="flex items-center space-x-3">
            <FileText className="w-8 h-8 text-blue-600" />
            <div>
              <p className="text-sm text-gray-600">Available Forms</p>
              <p className="text-2xl font-bold text-gray-900">{formsData.availableForms.length}</p>
            </div>
          </div>
        </div>
        
        <div className="bg-white p-4 rounded-lg shadow border border-gray-200">
          <div className="flex items-center space-x-3">
            <Clock className="w-8 h-8 text-orange-600" />
            <div>
              <p className="text-sm text-gray-600">Pending Forms</p>
              <p className="text-2xl font-bold text-gray-900">{formsData.pendingForms.length}</p>
            </div>
          </div>
        </div>
        
        <div className="bg-white p-4 rounded-lg shadow border border-gray-200">
          <div className="flex items-center space-x-3">
            <Check className="w-8 h-8 text-green-600" />
            <div>
              <p className="text-sm text-gray-600">Completed Forms</p>
              <p className="text-2xl font-bold text-gray-900">{formsData.completedForms.length}</p>
            </div>
          </div>
        </div>
        
        <div className="bg-white p-4 rounded-lg shadow border border-gray-200">
          <div className="flex items-center space-x-3">
            <Paperclip className="w-8 h-8 text-purple-600" />
            <div>
              <p className="text-sm text-gray-600">Uploaded Documents</p>
              <p className="text-2xl font-bold text-gray-900">{formsData.uploadedDocuments.length}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="bg-white rounded-lg shadow">
        <div className="border-b border-gray-200">
          <nav className="flex space-x-8 px-6">
            {[
              { id: 'forms', label: 'Available Forms', count: formsData.availableForms.length },
              { id: 'pending', label: 'Pending', count: formsData.pendingForms.length },
              { id: 'completed', label: 'Completed', count: formsData.completedForms.length },
              { id: 'documents', label: 'Documents', count: formsData.uploadedDocuments.length }
            ].map(tab => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`py-4 px-1 border-b-2 font-medium text-sm ${
                  activeTab === tab.id
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                {tab.label} ({tab.count})
              </button>
            ))}
          </nav>
        </div>

        <div className="p-6">
          {activeTab === 'forms' && <AvailableFormsTab />}
          {activeTab === 'pending' && <PendingFormsTab />}
          {activeTab === 'completed' && <CompletedFormsTab />}
          {activeTab === 'documents' && <DocumentsTab />}
        </div>
      </div>

      {/* Modals */}
      <FormModal />
      <UploadModal />
    </div>
  );
};

export default FormsUploads;
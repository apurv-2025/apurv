import React, { useState, useEffect } from 'react';
import { X, Save, Clock, User, Activity, Search } from 'lucide-react';
import patientService from '../services/patientService';
import practitionerService from '../services/practitionerService';

const WaitlistForm = ({ entry, onSubmit, onCancel, isOpen }) => {
  const [formData, setFormData] = useState({
    patient_id: '',
    practitioner_id: '',
    service_type: '',
    priority: 'NORMAL',
    preferred_dates: [''],
    preferred_times: [''],
    notes: ''
  });

  const [errors, setErrors] = useState({});
  const [patients, setPatients] = useState([]);
  const [practitioners, setPractitioners] = useState([]);
  const [loadingPatients, setLoadingPatients] = useState(false);
  const [loadingPractitioners, setLoadingPractitioners] = useState(false);
  
  // Search states for dropdowns
  const [patientSearch, setPatientSearch] = useState('');
  const [showPatientSearch, setShowPatientSearch] = useState(false);

  useEffect(() => {
    if (entry) {
      setFormData({
        patient_id: entry.patient_id || '',
        practitioner_id: entry.practitioner_id || '',
        service_type: entry.service_type || '',
        priority: entry.priority || 'NORMAL',
        preferred_dates: entry.preferred_dates || [''],
        preferred_times: entry.preferred_times || [''],
        notes: entry.notes || ''
      });
    } else {
      setFormData({
        patient_id: '',
        practitioner_id: '',
        service_type: '',
        priority: 'NORMAL',
        preferred_dates: [''],
        preferred_times: [''],
        notes: ''
      });
    }
    setErrors({});
  }, [entry]);

  useEffect(() => {
    if (isOpen) {
      fetchPatients();
      fetchPractitioners();
    }
  }, [isOpen]);

  const fetchPatients = async () => {
    try {
      setLoadingPatients(true);
      const data = await patientService.getPatients({ limit: 50 });
      setPatients(data);
    } catch (error) {
      console.error('Error fetching patients:', error);
    } finally {
      setLoadingPatients(false);
    }
  };

  const fetchPractitioners = async () => {
    try {
      setLoadingPractitioners(true);
      const data = await practitionerService.getPractitioners({ limit: 50 });
      setPractitioners(data);
    } catch (error) {
      console.error('Error fetching practitioners:', error);
    } finally {
      setLoadingPractitioners(false);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    
    // Clear error when user starts typing
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
  };

  const handlePreferredDateChange = (index, value) => {
    const newPreferredDates = [...formData.preferred_dates];
    newPreferredDates[index] = value;
    setFormData(prev => ({ ...prev, preferred_dates: newPreferredDates }));
  };

  const addPreferredDate = () => {
    setFormData(prev => ({
      ...prev,
      preferred_dates: [...prev.preferred_dates, '']
    }));
  };

  const removePreferredDate = (index) => {
    if (formData.preferred_dates.length > 1) {
      const newPreferredDates = formData.preferred_dates.filter((_, i) => i !== index);
      setFormData(prev => ({ ...prev, preferred_dates: newPreferredDates }));
    }
  };

  const handlePreferredTimeChange = (index, value) => {
    const newPreferredTimes = [...formData.preferred_times];
    newPreferredTimes[index] = value;
    setFormData(prev => ({ ...prev, preferred_times: newPreferredTimes }));
  };

  const addPreferredTime = () => {
    setFormData(prev => ({
      ...prev,
      preferred_times: [...prev.preferred_times, '']
    }));
  };

  const removePreferredTime = (index) => {
    if (formData.preferred_times.length > 1) {
      const newPreferredTimes = formData.preferred_times.filter((_, i) => i !== index);
      setFormData(prev => ({ ...prev, preferred_times: newPreferredTimes }));
    }
  };

  const validateForm = () => {
    const newErrors = {};
    
    if (!formData.service_type) {
      newErrors.service_type = 'Service type is required';
    }
    
    if (!formData.priority) {
      newErrors.priority = 'Priority is required';
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (validateForm()) {
      // Filter out empty preferred dates and times
      const filteredPreferredDates = formData.preferred_dates.filter(date => date.trim());
      const filteredPreferredTimes = formData.preferred_times.filter(time => time.trim());
      
      const submitData = {
        ...formData,
        preferred_dates: filteredPreferredDates.length > 0 ? filteredPreferredDates : undefined,
        preferred_times: filteredPreferredTimes.length > 0 ? filteredPreferredTimes : undefined
      };
      
      onSubmit(submitData);
    }
  };

  const formatPatientName = (patient) => {
    if (!patient) return '';
    
    // Check if patient has a 'name' field (from backend transformation)
    if (patient.name) {
      return patient.name;
    }
    
    // Use FHIR format: family_name and given_names
    const familyName = patient.family_name || '';
    const givenNames = patient.given_names?.join(' ') || '';
    const result = `${givenNames} ${familyName}`.trim();
    return result || `Patient ${patient.id}`;
  };

  // Helper function to extract contact info from FHIR telecom array
  const extractContactInfo = (patient) => {
    if (!patient || !patient.telecom) return { email: '', phone: '' };
    
    let email = '';
    let phone = '';
    
    patient.telecom.forEach(contact => {
      if (contact.system === 'email') {
        email = contact.value || '';
      } else if (contact.system === 'phone') {
        phone = contact.value || '';
      }
    });
    
    return { email, phone };
  };

  const formatPractitionerName = (practitioner) => {
    return practitioner.name || practitioner.fhir_id;
  };

  // Filtered patients for search
  const filteredPatients = patients?.filter(patient => {
    const fullName = formatPatientName(patient).toLowerCase();
    const { email, phone } = extractContactInfo(patient);
    const searchTerm = patientSearch.toLowerCase();
    return fullName.includes(searchTerm) || 
           (email && email.toLowerCase().includes(searchTerm)) ||
           (phone && phone.toLowerCase().includes(searchTerm));
  }) || [];

  // Close dropdowns when clicking outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (!event.target.closest('.search-dropdown')) {
        setShowPatientSearch(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl w-full max-w-2xl max-h-[90vh] overflow-y-auto">
        <div className="flex items-center justify-between p-6 border-b">
          <div className="flex items-center space-x-2">
            <Clock className="h-5 w-5 text-orange-600" />
            <h2 className="text-xl font-semibold text-gray-900">
              {entry ? 'Edit Waitlist Entry' : 'Add New Waitlist Entry'}
            </h2>
          </div>
          <button
            onClick={onCancel}
            className="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="p-6 space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Person Selection */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Person (Optional)
              </label>
              <div className="relative">
                <div className="flex items-center border border-gray-300 rounded-md focus-within:ring-2 focus-within:ring-orange-500">
                  <input
                    type="text"
                    placeholder="Search persons..."
                    value={formData.patient_id ? 
                      formatPatientName(patients.find(p => p.id === formData.patient_id)) : 
                      patientSearch
                    }
                    onChange={(e) => {
                      setPatientSearch(e.target.value);
                      setShowPatientSearch(true);
                      if (!e.target.value) {
                        setFormData(prev => ({ ...prev, patient_id: '' }));
                      }
                    }}
                    onFocus={() => setShowPatientSearch(true)}
                    className="flex-1 px-3 py-2 border-0 focus:ring-0 focus:outline-none"
                  />
                  {formData.patient_id && (
                    <button
                      type="button"
                      onClick={() => {
                        setFormData(prev => ({ ...prev, patient_id: '' }));
                        setPatientSearch('');
                      }}
                      className="p-1 text-gray-400 hover:text-gray-600"
                    >
                      <X className="w-3 h-3" />
                    </button>
                  )}
                  <button
                    type="button"
                    onClick={() => setShowPatientSearch(!showPatientSearch)}
                    className="p-2 text-gray-400 hover:text-gray-600"
                  >
                    <Search className="w-4 h-4" />
                  </button>
                </div>

                {showPatientSearch && (
                  <div className="search-dropdown absolute z-10 w-full mt-1 bg-white border rounded-lg shadow-lg max-h-60 overflow-y-auto">
                    <div className="p-2">
                      <div className="text-xs text-gray-500 mb-2">Search by name, email, or phone</div>
                      {loadingPatients ? (
                        <div className="text-sm text-gray-500 py-2">Loading persons...</div>
                      ) : filteredPatients.length === 0 ? (
                        <div className="text-sm text-gray-500 py-2">No persons found</div>
                      ) : (
                        filteredPatients.map((patient) => (
                          <div
                            key={patient.id}
                            onClick={() => {
                              setFormData(prev => ({ ...prev, patient_id: patient.id }));
                              setPatientSearch('');
                              setShowPatientSearch(false);
                            }}
                            className="flex items-center justify-between p-2 hover:bg-gray-100 cursor-pointer rounded"
                          >
                            <div>
                              <div className="font-medium">{formatPatientName(patient)}</div>
                              <div className="text-sm text-gray-500">
                                {(() => {
                                  const { email, phone } = extractContactInfo(patient);
                                  if (email && phone) {
                                    return `${email} • ${phone}`;
                                  } else if (email) {
                                    return email;
                                  } else if (phone) {
                                    return phone;
                                  } else {
                                    return 'No contact info';
                                  }
                                })()}
                              </div>
                            </div>
                          </div>
                        ))
                      )}
                    </div>
                  </div>
                )}
              </div>
            </div>

            {/* Practitioner Selection */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Practitioner (Optional)
              </label>
              <select
                name="practitioner_id"
                value={formData.practitioner_id}
                onChange={handleInputChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500"
              >
                <option value="">Select a practitioner</option>
                {loadingPractitioners ? (
                  <option disabled>Loading practitioners...</option>
                ) : (
                  practitioners.map(practitioner => (
                    <option key={practitioner.id} value={practitioner.id}>
                      {formatPractitionerName(practitioner)}
                    </option>
                  ))
                )}
              </select>
            </div>

            {/* Service Type */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Service Type *
              </label>
              <select
                name="service_type"
                value={formData.service_type}
                onChange={handleInputChange}
                className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500 ${
                  errors.service_type ? 'border-red-500' : 'border-gray-300'
                }`}
              >
                <option value="">Select service type</option>
                <option value="THERAPY">Therapy</option>
                <option value="CONSULTATION">Consultation</option>
                <option value="ASSESSMENT">Assessment</option>
                <option value="MEDICAL">Medical</option>
                <option value="MENTAL_HEALTH">Mental Health</option>
                <option value="FOLLOW_UP">Follow-up</option>
                <option value="EMERGENCY">Emergency</option>
              </select>
              {errors.service_type && (
                <p className="mt-1 text-sm text-red-600">{errors.service_type}</p>
              )}
            </div>

            {/* Priority */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Priority *
              </label>
              <select
                name="priority"
                value={formData.priority}
                onChange={handleInputChange}
                className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500 ${
                  errors.priority ? 'border-red-500' : 'border-gray-300'
                }`}
              >
                <option value="LOW">Low</option>
                <option value="NORMAL">Normal</option>
                <option value="HIGH">High</option>
                <option value="URGENT">Urgent</option>
              </select>
              {errors.priority && (
                <p className="mt-1 text-sm text-red-600">{errors.priority}</p>
              )}
            </div>
          </div>

          {/* Preferred Dates */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Preferred Dates
            </label>
            <div className="space-y-2">
              {formData.preferred_dates.map((date, index) => (
                <div key={index} className="flex space-x-2">
                  <input
                    type="date"
                    value={date}
                    onChange={(e) => handlePreferredDateChange(index, e.target.value)}
                    className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500"
                  />
                  {formData.preferred_dates.length > 1 && (
                    <button
                      type="button"
                      onClick={() => removePreferredDate(index)}
                      className="px-3 py-2 text-red-600 hover:text-red-800 transition-colors"
                    >
                      <X className="h-4 w-4" />
                    </button>
                  )}
                </div>
              ))}
              <button
                type="button"
                onClick={addPreferredDate}
                className="text-orange-600 hover:text-orange-800 text-sm font-medium"
              >
                + Add preferred date
              </button>
            </div>
          </div>

          {/* Preferred Times */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Preferred Times
            </label>
            <div className="space-y-2">
              {formData.preferred_times.map((time, index) => (
                <div key={index} className="flex space-x-2">
                  <input
                    type="time"
                    value={time}
                    onChange={(e) => handlePreferredTimeChange(index, e.target.value)}
                    className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500"
                  />
                  {formData.preferred_times.length > 1 && (
                    <button
                      type="button"
                      onClick={() => removePreferredTime(index)}
                      className="px-3 py-2 text-red-600 hover:text-red-800 transition-colors"
                    >
                      <X className="h-4 w-4" />
                    </button>
                  )}
                </div>
              ))}
              <button
                type="button"
                onClick={addPreferredTime}
                className="text-orange-600 hover:text-orange-800 text-sm font-medium"
              >
                + Add preferred time
              </button>
            </div>
          </div>

          {/* Notes */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Notes
            </label>
            <textarea
              name="notes"
              value={formData.notes}
              onChange={handleInputChange}
              rows={3}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500"
              placeholder="Additional notes about this waitlist entry..."
            />
          </div>

          {/* Form Actions */}
          <div className="flex justify-end space-x-3 pt-6 border-t">
            <button
              type="button"
              onClick={onCancel}
              className="px-4 py-2 text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-md transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-4 py-2 bg-orange-600 text-white hover:bg-orange-700 rounded-md transition-colors flex items-center space-x-2"
            >
              <Save className="h-4 w-4" />
              <span>{entry ? 'Update Entry' : 'Create Entry'}</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default WaitlistForm; 
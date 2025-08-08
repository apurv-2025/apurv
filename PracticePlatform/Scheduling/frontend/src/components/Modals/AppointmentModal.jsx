import React, { useState, useEffect } from 'react';
import { X, Calendar, Clock, User, MapPin, FileText, Edit, Trash2, Search, Plus } from 'lucide-react';
import moment from 'moment';
import { toast } from 'react-toastify';

const AppointmentModal = ({ 
  isOpen, 
  onClose, 
  event, 
  slot, 
  practitioners, 
  patients,
  appointmentTypes,
  onSave,
  onDelete 
}) => {
  const [isEditing, setIsEditing] = useState(false);
  const [formData, setFormData] = useState({
    title: '',
    patient_id: '',
    practitioner_id: '',
    appointment_type_id: '',
    appointment_date: '',
    start_time: '',
    end_time: '',
    location: '',
    notes: ''
  });

  // Search states
  const [patientSearch, setPatientSearch] = useState('');
  const [practitionerSearch, setPractitionerSearch] = useState('');
  const [showPatientSearch, setShowPatientSearch] = useState(false);
  const [showPractitionerSearch, setShowPractitionerSearch] = useState(false);

  useEffect(() => {
    if (event) {
      // Map appointment type name to ID for the dropdown
      let appointmentTypeId = '';
      if (event.resource?.appointment_type && appointmentTypes) {
        const eventAppointmentType = event.resource.appointment_type.toUpperCase();
        
        // Create a mapping for common variations
        const appointmentType = appointmentTypes.find(type => {
          const typeName = type.name.toUpperCase();
          const typeNameNoSpaces = typeName.replace(/\s+/g, '_');
          
          return (
            typeName === eventAppointmentType ||
            typeNameNoSpaces === eventAppointmentType ||
            // Specific mappings for backend data format
            (eventAppointmentType === 'CONSULTATION' && typeName.includes('CONSULTATION')) ||
            (eventAppointmentType === 'THERAPY' && typeName.includes('THERAPY')) ||
            (eventAppointmentType === 'FOLLOW_UP' && typeName.includes('FOLLOW-UP')) ||
            (eventAppointmentType === 'EMERGENCY' && typeName.includes('EMERGENCY'))
          );
        });
        
        appointmentTypeId = appointmentType ? appointmentType.id.toString() : '';
      }

      setFormData({
        title: event.title || '',
        patient_id: event.resource?.patient_id || '',
        practitioner_id: event.resource?.practitioner_id || '',
        appointment_type_id: appointmentTypeId,
        appointment_date: moment(event.start).format('YYYY-MM-DD'),
        start_time: moment(event.start).format('HH:mm'),
        end_time: moment(event.end).format('HH:mm'),
        location: event.resource?.location || '',
        notes: event.resource?.notes || ''
      });
    } else if (slot) {
      setFormData({
        title: '',
        patient_id: '',
        practitioner_id: '',
        appointment_type_id: '',
        appointment_date: moment(slot.start).format('YYYY-MM-DD'),
        start_time: moment(slot.start).format('HH:mm'),
        end_time: moment(slot.end).format('HH:mm'),
        location: '',
        notes: ''
      });
    } else {
      // New appointment without slot - set to today by default
      const today = new Date();
      setFormData({
        title: '',
        patient_id: '',
        practitioner_id: '',
        appointment_type_id: '',
        appointment_date: moment(today).format('YYYY-MM-DD'),
        start_time: '',
        end_time: '',
        location: '',
        notes: ''
      });
    }
  }, [event, slot, appointmentTypes]);

  // Close dropdowns when clicking outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (!event.target.closest('.search-dropdown')) {
        setShowPatientSearch(false);
        setShowPractitionerSearch(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  // Handle escape key to close modal
  useEffect(() => {
    const handleEscape = (event) => {
      if (event.key === 'Escape') {
        onClose();
      }
    };

    if (isOpen) {
      document.addEventListener('keydown', handleEscape);
      return () => document.removeEventListener('keydown', handleEscape);
    }
  }, [isOpen, onClose]);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSave = () => {
    // Validation
    if (!formData.practitioner_id) {
      toast.error('Please select a practitioner');
      return;
    }
    if (!formData.appointment_date) {
      toast.error('Please select an appointment date');
      return;
    }
    if (!formData.start_time || !formData.end_time) {
      toast.error('Please set start and end times');
      return;
    }
    if (!formData.appointment_type_id) {
      toast.error('Please select an appointment type');
      return;
    }

    // Optional validation for patient
    if (!formData.patient_id) {
      const proceed = window.confirm('No person selected. Do you want to create an appointment without a person?');
      if (!proceed) {
        return;
      }
    }

    if (onSave) {
      onSave(formData);
    }
    setIsEditing(false);
  };

  const handleDelete = () => {
    if (onDelete && event) {
      onDelete(event.id);
    }
    onClose();
  };

  // Helper functions
  const formatPractitionerName = (practitioner) => {
    if (!practitioner) return '';
    
    // Check if practitioner has a 'name' field (from backend transformation)
    if (practitioner.name) {
      return practitioner.name;
    }
    
    // Fallback to FHIR format if available
    const familyName = practitioner.family_name || '';
    const givenNames = practitioner.given_names?.join(' ') || '';
    const result = familyName + (givenNames ? `, ${givenNames}` : '');
    return result || `Practitioner ${practitioner.id}`;
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

  // Filter functions
  const filteredPatients = patients?.filter(patient => {
    const fullName = formatPatientName(patient).toLowerCase();
    const { email, phone } = extractContactInfo(patient);
    const searchTerm = patientSearch.toLowerCase();
    return fullName.includes(searchTerm) || 
           (email && email.toLowerCase().includes(searchTerm)) ||
           (phone && phone.toLowerCase().includes(searchTerm));
  }) || [];

  const filteredPractitioners = practitioners?.filter(practitioner => {
    const fullName = formatPractitionerName(practitioner).toLowerCase();
    const specialty = (practitioner.specialty || '').toLowerCase();
    const searchTerm = practitionerSearch.toLowerCase();
    return fullName.includes(searchTerm) || 
           specialty.includes(searchTerm);
  }) || [];

  const selectedPatient = patients?.find(p => p.id == formData.patient_id);
  const selectedPractitioner = practitioners?.find(p => p.id == formData.practitioner_id);

  if (!isOpen) return null;

  return (
    <div className="modal-overlay">
      <div className="modal-content max-w-2xl">
        <div className="p-6">
          {/* Header */}
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-semibold text-gray-900">
              {event ? (isEditing ? 'Edit Appointment' : 'Appointment Details') : 'New Appointment'}
            </h2>
            <div className="flex items-center gap-2">
              {event && !isEditing && (
                <>
                  <button
                    onClick={() => setIsEditing(true)}
                    className="p-2 text-gray-400 hover:text-gray-600"
                  >
                    <Edit className="w-4 h-4" />
                  </button>
                  <button
                    onClick={handleDelete}
                    className="p-2 text-red-400 hover:text-red-600"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </>
              )}
              <button
                onClick={onClose}
                className="p-2 text-gray-400 hover:text-gray-600"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
          </div>

          {/* Content */}
          <div className="space-y-6">
            {!isEditing && event ? (
              // View Mode
              <div className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div className="flex items-center gap-2">
                    <Calendar className="w-4 h-4 text-gray-400" />
                    <span className="text-sm text-gray-600">
                      {moment(event.start).format('MMMM D, YYYY')}
                    </span>
                  </div>
                  <div className="flex items-center gap-2">
                    <Clock className="w-4 h-4 text-gray-400" />
                    <span className="text-sm text-gray-600">
                      {moment(event.start).format('HH:mm')} - {moment(event.end).format('HH:mm')}
                    </span>
                  </div>
                </div>

                <div className="flex items-center gap-2">
                  <User className="w-4 h-4 text-gray-400" />
                  <span className="text-sm text-gray-600">
                    {event.resource?.practitioner_name || 'No practitioner assigned'}
                  </span>
                </div>

                {event.resource?.location && (
                  <div className="flex items-center gap-2">
                    <MapPin className="w-4 h-4 text-gray-400" />
                    <span className="text-sm text-gray-600">
                      {event.resource.location}
                    </span>
                  </div>
                )}

                {event.resource?.notes && (
                  <div className="flex items-start gap-2">
                    <FileText className="w-4 h-4 text-gray-400 mt-0.5" />
                    <span className="text-sm text-gray-600">
                      {event.resource.notes}
                    </span>
                  </div>
                )}

                <div className="flex items-center gap-2">
                  <span className="text-sm font-medium text-gray-700">Status:</span>
                  <span className={`px-2 py-1 text-xs rounded-full ${
                    event.resource?.status === 'CONFIRMED' ? 'bg-green-100 text-green-800' :
                    event.resource?.status === 'SCHEDULED' ? 'bg-blue-100 text-blue-800' :
                    'bg-gray-100 text-gray-800'
                  }`}>
                    {event.resource?.status || 'Unknown'}
                  </span>
                </div>
              </div>
            ) : (
              // Edit/Create Mode
              <div className="space-y-4">
                <div className="form-group">
                  <label className="form-label">Title</label>
                  <input
                    type="text"
                    name="title"
                    value={formData.title}
                    onChange={handleInputChange}
                    className="input"
                    placeholder="Appointment title"
                  />
                </div>

                <div className="grid grid-cols-2 gap-4">
                  {/* Person Selection */}
                  <div className="form-group">
                    <label className="form-label">Person</label>
                    <div className="relative">
                      <div className="flex items-center border rounded-lg focus-within:ring-2 focus-within:ring-blue-500">
                        <input
                          type="text"
                          placeholder="Search persons..."
                          value={selectedPatient ? formatPatientName(selectedPatient) : patientSearch}
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
                        {selectedPatient && (
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
                            {filteredPatients.length === 0 ? (
                              <div className="text-sm text-gray-500 py-2">
                                No persons found
                                <button
                                  onClick={() => {
                                    toast.info('Add new person feature coming soon!');
                                    setShowPatientSearch(false);
                                  }}
                                  className="ml-2 text-blue-600 hover:text-blue-800 flex items-center"
                                >
                                  <Plus className="w-3 h-3 mr-1" />
                                  Add New
                                </button>
                              </div>
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
                  <div className="form-group">
                    <label className="form-label">Practitioner</label>
                    <div className="relative">
                      <div className="flex items-center border rounded-lg focus-within:ring-2 focus-within:ring-blue-500">
                        <input
                          type="text"
                          placeholder="Search practitioners..."
                          value={selectedPractitioner ? formatPractitionerName(selectedPractitioner) : practitionerSearch}
                          onChange={(e) => {
                            setPractitionerSearch(e.target.value);
                            setShowPractitionerSearch(true);
                            if (!e.target.value) {
                              setFormData(prev => ({ ...prev, practitioner_id: '' }));
                            }
                          }}
                          onFocus={() => setShowPractitionerSearch(true)}
                          className="flex-1 px-3 py-2 border-0 focus:ring-0 focus:outline-none"
                        />
                        {selectedPractitioner && (
                          <button
                            type="button"
                            onClick={() => {
                              setFormData(prev => ({ ...prev, practitioner_id: '' }));
                              setPractitionerSearch('');
                            }}
                            className="p-1 text-gray-400 hover:text-gray-600"
                          >
                            <X className="w-3 h-3" />
                          </button>
                        )}
                        <button
                          type="button"
                          onClick={() => setShowPractitionerSearch(!showPractitionerSearch)}
                          className="p-2 text-gray-400 hover:text-gray-600"
                        >
                          <Search className="w-4 h-4" />
                        </button>
                      </div>
                      
                      {showPractitionerSearch && (
                        <div className="search-dropdown absolute z-10 w-full mt-1 bg-white border rounded-lg shadow-lg max-h-60 overflow-y-auto">
                          <div className="p-2">
                            <div className="text-xs text-gray-500 mb-2">Search by name or specialty</div>
                            {filteredPractitioners.length === 0 ? (
                              <div className="text-sm text-gray-500 py-2">No practitioners found</div>
                            ) : (
                              filteredPractitioners.map((practitioner) => (
                                <div
                                  key={practitioner.id}
                                  onClick={() => {
                                    setFormData(prev => ({ ...prev, practitioner_id: practitioner.id }));
                                    setPractitionerSearch('');
                                    setShowPractitionerSearch(false);
                                  }}
                                  className="flex items-center justify-between p-2 hover:bg-gray-100 cursor-pointer rounded"
                                >
                                  <div>
                                    <div className="font-medium">{formatPractitionerName(practitioner)}</div>
                                    <div className="text-sm text-gray-500">
                                      {practitioner.specialty || 'General Practice'}
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
                </div>

                <div className="form-group">
                  <label className="form-label">Appointment Type</label>
                  <select
                    name="appointment_type_id"
                    value={formData.appointment_type_id}
                    onChange={handleInputChange}
                    className="input"
                  >
                    <option value="">Select type</option>
                    {appointmentTypes?.map((type) => (
                      <option key={type.id} value={type.id}>
                        {type.name} ({type.duration_minutes} min)
                      </option>
                    ))}
                  </select>
                  {formData.appointment_type_id && (
                    <div className="mt-1 text-sm text-gray-500">
                      {(() => {
                        const selectedType = appointmentTypes?.find(t => t.id == formData.appointment_type_id);
                        return selectedType ? `Duration: ${selectedType.duration_minutes} minutes` : '';
                      })()}
                    </div>
                  )}
                </div>

                {/* Quick Actions */}
                <div className="bg-gray-50 p-4 rounded-lg">
                  <h4 className="text-sm font-medium text-gray-700 mb-3">Quick Actions</h4>
                  <div className="flex flex-wrap gap-2">
                    <button
                      type="button"
                      onClick={() => {
                        const now = new Date();
                        const startTime = new Date(now.getTime() + 30 * 60000); // 30 minutes from now
                        setFormData(prev => ({
                          ...prev,
                          start_time: startTime.toTimeString().slice(0, 5),
                          end_time: new Date(startTime.getTime() + 60 * 60000).toTimeString().slice(0, 5)
                        }));
                      }}
                      className="px-3 py-1 text-xs bg-blue-100 text-blue-700 rounded hover:bg-blue-200 transition-colors"
                    >
                      Set to 30 min from now
                    </button>
                    <button
                      type="button"
                      onClick={() => {
                        setFormData(prev => ({
                          ...prev,
                          start_time: '09:00',
                          end_time: '10:00'
                        }));
                      }}
                      className="px-3 py-1 text-xs bg-green-100 text-green-700 rounded hover:bg-green-200 transition-colors"
                    >
                      Set to 9:00 AM
                    </button>
                    <button
                      type="button"
                      onClick={() => {
                        setFormData(prev => ({
                          ...prev,
                          start_time: '14:00',
                          end_time: '15:00'
                        }));
                      }}
                      className="px-3 py-1 text-xs bg-purple-100 text-purple-700 rounded hover:bg-purple-200 transition-colors"
                    >
                      Set to 2:00 PM
                    </button>
                  </div>
                </div>

                <div className="form-group">
                  <label className="form-label">Appointment Date</label>
                  <input
                    type="date"
                    name="appointment_date"
                    value={formData.appointment_date}
                    onChange={handleInputChange}
                    className="input"
                  />
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div className="form-group">
                    <label className="form-label">Start Time</label>
                    <input
                      type="time"
                      name="start_time"
                      value={formData.start_time}
                      onChange={handleInputChange}
                      className="input"
                    />
                  </div>

                  <div className="form-group">
                    <label className="form-label">End Time</label>
                    <input
                      type="time"
                      name="end_time"
                      value={formData.end_time}
                      onChange={handleInputChange}
                      className="input"
                    />
                  </div>
                </div>

                <div className="form-group">
                  <label className="form-label">Location</label>
                  <input
                    type="text"
                    name="location"
                    value={formData.location}
                    onChange={handleInputChange}
                    className="input"
                    placeholder="Appointment location"
                  />
                </div>

                <div className="form-group">
                  <label className="form-label">Notes</label>
                  <textarea
                    name="notes"
                    value={formData.notes}
                    onChange={handleInputChange}
                    className="input"
                    rows="3"
                    placeholder="Additional notes"
                  />
                </div>

                {/* Appointment Summary */}
                {(formData.practitioner_id || formData.patient_id || formData.appointment_type_id) && (
                  <div className="bg-blue-50 p-4 rounded-lg border border-blue-200">
                    <h4 className="text-sm font-medium text-blue-700 mb-3">Appointment Summary</h4>
                    <div className="space-y-2 text-sm">
                      {selectedPractitioner && (
                        <div className="flex items-center gap-2">
                          <User className="w-4 h-4 text-blue-600" />
                          <span className="text-blue-800">
                            <strong>Practitioner:</strong> {formatPractitionerName(selectedPractitioner)}
                          </span>
                        </div>
                      )}
                      {selectedPatient && (
                        <div className="flex items-center gap-2">
                          <User className="w-4 h-4 text-blue-600" />
                          <span className="text-blue-800">
                            <strong>Person:</strong> {formatPatientName(selectedPatient)}
                          </span>
                        </div>
                      )}
                      {formData.appointment_type_id && (
                        <div className="flex items-center gap-2">
                          <Calendar className="w-4 h-4 text-blue-600" />
                          <span className="text-blue-800">
                            <strong>Type:</strong> {appointmentTypes?.find(t => t.id == formData.appointment_type_id)?.name}
                          </span>
                        </div>
                      )}
                      {formData.appointment_date && (
                        <div className="flex items-center gap-2">
                          <Calendar className="w-4 h-4 text-blue-600" />
                          <span className="text-blue-800">
                            <strong>Date:</strong> {moment(formData.appointment_date).format('MMMM DD, YYYY')}
                          </span>
                        </div>
                      )}
                      {formData.start_time && formData.end_time && (
                        <div className="flex items-center gap-2">
                          <Clock className="w-4 h-4 text-blue-600" />
                          <span className="text-blue-800">
                            <strong>Time:</strong> {formData.start_time} - {formData.end_time}
                          </span>
                        </div>
                      )}
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>

          {/* Footer */}
          <div className="flex justify-end gap-3 mt-6 pt-6 border-t border-gray-200">
            <button
              onClick={onClose}
              className="btn-secondary"
            >
              Cancel
            </button>
            {isEditing && (
              <button
                onClick={() => setIsEditing(false)}
                className="btn-secondary"
              >
                Cancel Edit
              </button>
            )}
            {(isEditing || !event) && (
              <button
                onClick={handleSave}
                className="btn-primary"
              >
                {event ? 'Update Appointment' : 'Create Appointment'}
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default AppointmentModal; 
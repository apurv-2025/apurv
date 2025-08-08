import React, { useState, useEffect } from 'react';
import { useCalendar } from '../hooks/useCalendar';
import CalendarComponent from '../components/Calendar/Calendar';
import CalendarStats from '../components/Calendar/CalendarStats';
import AppointmentModal from '../components/Modals/AppointmentModal';
import { Filter, Plus, Search, X } from 'lucide-react';
import { toast } from 'react-toastify';

const AppointmentCalendar = () => {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedEvent, setSelectedEvent] = useState(null);
  const [selectedSlot, setSelectedSlot] = useState(null);
  
  // Search states for filters
  const [practitionerSearch, setPractitionerSearch] = useState('');
  const [patientSearch, setPatientSearch] = useState('');
  const [showPractitionerSearch, setShowPractitionerSearch] = useState(false);
  const [showPatientSearch, setShowPatientSearch] = useState(false);

  const {
    calendarEvents,
    practitioners,
    patients,
    appointmentTypes,
    loading,
    error,
    selectedDate,
    selectedPractitioner,
    selectedPatient,
    selectedAppointmentType,
    availableSlots,
    setSelectedDate,
    setSelectedPractitioner,
    setSelectedPatient,
    setSelectedAppointmentType,
    createAppointment,
    updateAppointment,
    deleteAppointment,
    fetchAppointments
  } = useCalendar();

  // Helper functions for formatting names
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
    return result || 'Unknown Practitioner';
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
    return result || 'Unknown Patient';
  };

  // Helper function to format contact info
  const formatContactInfo = (email, phone) => {
    const hasEmail = email && email !== 'undefined' && email.trim() !== '';
    const hasPhone = phone && phone !== 'undefined' && phone.trim() !== '';
    
    if (hasEmail && hasPhone) {
      return `${email} • ${phone}`;
    } else if (hasEmail) {
      return email;
    } else if (hasPhone) {
      return phone;
    } else {
      return 'No contact info';
    }
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

  // Filtered lists for search
  const filteredPractitioners = practitioners?.filter(practitioner => {
    const fullName = formatPractitionerName(practitioner).toLowerCase();
    const specialty = (practitioner.specialty || '').toLowerCase();
    const searchTerm = practitionerSearch.toLowerCase();
    return fullName.includes(searchTerm) || 
           specialty.includes(searchTerm);
  }) || [];

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
        setShowPractitionerSearch(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleSelectEvent = (event) => {
    setSelectedEvent(event);
    setSelectedSlot(null);
    setIsModalOpen(true);
  };

  const handleSelectSlot = (slotInfo) => {
    setSelectedSlot(slotInfo);
    setSelectedEvent(null);
    setIsModalOpen(true);
  };

  const handleCreateNewAppointment = () => {
    setSelectedEvent(null);
    setSelectedSlot(null);
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    // Close modal
    setIsModalOpen(false);
    
    // Reset all modal-related state
    setSelectedEvent(null);
    setSelectedSlot(null);
    
    // Small delay to ensure modal is fully closed before any other operations
    setTimeout(() => {
      // Force a re-render of the calendar
      window.dispatchEvent(new Event('resize'));
    }, 50);
  };

  const handleSaveAppointment = async (formData) => {
    try {
      // Determine the appointment date
      let appointmentDate;
      if (selectedEvent) {
        // For existing appointments, use the existing date or form date if provided
        appointmentDate = formData.appointment_date 
          ? new Date(formData.appointment_date)
          : new Date(selectedEvent.start);
      } else if (selectedSlot) {
        // For new appointments from slot selection, use the slot date
        appointmentDate = new Date(selectedSlot.start);
      } else {
        // For new appointments from "New Appointment" button, use form date or today
        appointmentDate = formData.appointment_date 
          ? new Date(formData.appointment_date)
          : new Date();
      }
      
      const appointmentDateStr = appointmentDate.toISOString().split('T')[0];

      if (selectedEvent) {
        // Update existing appointment - transform formData like we do for creates
        const appointmentData = {
          title: formData.title || selectedEvent.title,
          start: `${appointmentDateStr}T${formData.start_time}:00`,
          end: `${appointmentDateStr}T${formData.end_time}:00`,
          practitioner_id: formData.practitioner_id || selectedEvent.resource?.practitioner_id,
          patient_id: formData.patient_id || selectedEvent.resource?.patient_id,
          appointment_type: formData.appointment_type_id ? 
            appointmentTypes.find(t => t.id == formData.appointment_type_id)?.name : 
            (selectedEvent.resource?.appointment_type || 'CONSULTATION'),
          status: selectedEvent.resource?.status || 'SCHEDULED',
          location: formData.location || '',
          notes: formData.notes || ''
        };
        await updateAppointment(selectedEvent.id, appointmentData);
        toast.success('Appointment updated successfully!');
      } else {
        // Create new appointment
        const appointmentData = {
          title: formData.title || 'New Appointment',
          start: `${appointmentDateStr}T${formData.start_time}:00`,
          end: `${appointmentDateStr}T${formData.end_time}:00`,
          practitioner_id: formData.practitioner_id || selectedPractitioner?.id || null,
          patient_id: formData.patient_id || selectedPatient?.id || null,
          appointment_type: formData.appointment_type_id ? 
            appointmentTypes.find(t => t.id == formData.appointment_type_id)?.name : 'CONSULTATION',
          status: 'SCHEDULED',
          location: formData.location || '',
          notes: formData.notes || ''
        };
        await createAppointment(appointmentData);
        toast.success('Appointment created successfully!');
      }
      
      // Close modal and refresh calendar data
      handleCloseModal();
      
      // Show loading feedback
      toast.info('Updating calendar...');
      
      // Refresh appointments to show the new/updated appointment
      setTimeout(() => {
        fetchAppointments();
      }, 200);
      
    } catch (error) {
      console.error('Error saving appointment:', error);
      toast.error('Failed to save appointment. Please try again.');
    }
  };

  const handleDeleteAppointment = async (appointmentId) => {
    try {
      await deleteAppointment(appointmentId);
      toast.success('Appointment deleted successfully!');
      
      // Close modal and refresh calendar data
      handleCloseModal();
      
      // Show loading feedback
      toast.info('Updating calendar...');
      
      // Refresh appointments to reflect the deletion
      setTimeout(() => {
        fetchAppointments();
      }, 200);
      
    } catch (error) {
      console.error('Error deleting appointment:', error);
      toast.error('Failed to delete appointment. Please try again.');
    }
  };



  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Appointment Calendar</h1>
          <p className="text-gray-600">View and manage appointments in calendar format</p>
          
          {/* Active Filters Display */}
          {(selectedPractitioner || selectedPatient || selectedAppointmentType) && (
            <div className="flex items-center gap-2 mt-2">
              <span className="text-sm text-gray-500">Active filters:</span>
              {selectedPractitioner && formatPractitionerName(selectedPractitioner) && (
                <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                  Dr. {formatPractitionerName(selectedPractitioner)}
                </span>
              )}
              {selectedPatient && formatPatientName(selectedPatient) && (
                <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
                  {formatPatientName(selectedPatient)}
                </span>
              )}
              {selectedAppointmentType && (
                <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-purple-100 text-purple-800">
                  {selectedAppointmentType.name}
                </span>
              )}
              <span className="text-sm text-gray-500">
                ({calendarEvents.length} appointment{calendarEvents.length !== 1 ? 's' : ''})
              </span>
            </div>
          )}
        </div>
        <div className="flex items-center gap-3">
          <button className="btn-secondary">
            <Filter className="w-4 h-4 mr-2" />
            Filter
          </button>
          <button 
            className="btn-primary"
            onClick={handleCreateNewAppointment}
          >
            <Plus className="w-4 h-4 mr-2" />
            New Appointment
          </button>
        </div>
      </div>

      {/* Calendar Statistics */}
      <CalendarStats 
        appointments={calendarEvents}
        patients={patients}
        practitioners={practitioners}
        selectedDate={selectedDate}
      />

      {/* Filters */}
      <div className="card">
        <div className="card-body">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
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
                        setSelectedPractitioner(null);
                      }
                    }}
                    onFocus={() => setShowPractitionerSearch(true)}
                    className="flex-1 px-3 py-2 border-0 focus:ring-0 focus:outline-none"
                  />
                  {selectedPractitioner && (
                    <button
                      type="button"
                      onClick={() => {
                        setSelectedPractitioner(null);
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
                              setSelectedPractitioner(practitioner);
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
                        setSelectedPatient(null);
                      }
                    }}
                    onFocus={() => setShowPatientSearch(true)}
                    className="flex-1 px-3 py-2 border-0 focus:ring-0 focus:outline-none"
                  />
                  {selectedPatient && (
                    <button
                      type="button"
                      onClick={() => {
                        setSelectedPatient(null);
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
                        <div className="text-sm text-gray-500 py-2">No persons found</div>
                      ) : (
                        filteredPatients.map((patient) => (
                          <div
                            key={patient.id}
                            onClick={() => {
                              setSelectedPatient(patient);
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
                                  return formatContactInfo(email, phone);
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

            <div className="form-group">
              <label className="form-label">Date</label>
              <input
                type="date"
                value={selectedDate.toISOString().split('T')[0]}
                onChange={(e) => setSelectedDate(new Date(e.target.value))}
                className="input"
              />
            </div>

            <div className="form-group">
              <label className="form-label">Appointment Type</label>
              <select 
                className="input"
                value={selectedAppointmentType?.id || ''}
                onChange={(e) => {
                  const typeId = e.target.value;
                  if (typeId) {
                    const type = appointmentTypes.find(t => t.id.toString() === typeId);
                    setSelectedAppointmentType(type);
                  } else {
                    setSelectedAppointmentType(null);
                  }
                }}
              >
                <option value="">All Types</option>
                {appointmentTypes?.map((type) => (
                  <option key={type.id} value={type.id}>
                    {type.name}
                  </option>
                ))}
              </select>
            </div>
          </div>
          
          {/* Clear Filters Button */}
          <div className="flex justify-end mt-4">
            <button
              onClick={() => {
                setSelectedPractitioner(null);
                setSelectedPatient(null);
                setSelectedAppointmentType(null);
                setPractitionerSearch('');
                setPatientSearch('');
                setSelectedDate(new Date());
                setShowPractitionerSearch(false);
                setShowPatientSearch(false);
              }}
              className="btn-secondary text-sm"
            >
              <X className="w-4 h-4 mr-2" />
              Clear All Filters
            </button>
          </div>
        </div>
      </div>

      {/* Calendar */}
      <CalendarComponent
        events={calendarEvents}
        loading={loading}
        onSelectEvent={handleSelectEvent}
        onSelectSlot={handleSelectSlot}
        practitioners={practitioners}
        patients={patients}
        appointmentTypes={appointmentTypes}
      />

      {/* Available Slots (if practitioner and date selected) */}
      {selectedPractitioner && (
        <div className="card">
          <div className="card-header">
            <h3 className="text-lg font-medium text-gray-900">
              Available Slots - {formatPractitionerName(selectedPractitioner)} on {selectedDate.toLocaleDateString()}
            </h3>
          </div>
          <div className="card-body">
            {availableSlots.length > 0 ? (
              <div className="grid grid-cols-4 md:grid-cols-8 gap-2">
                {availableSlots.map((slot, index) => (
                  <button
                    key={index}
                    className={`p-2 text-sm rounded border ${
                      slot.available
                        ? 'bg-green-50 border-green-200 text-green-700 hover:bg-green-100'
                        : 'bg-gray-50 border-gray-200 text-gray-500 cursor-not-allowed'
                    }`}
                    disabled={!slot.available}
                  >
                    {slot.start_time}
                  </button>
                ))}
              </div>
            ) : (
              <div className="text-center py-4 text-gray-500">
                <p>No available slots found for this date.</p>
                <p className="text-sm mt-1">Try selecting a different date or practitioner.</p>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Error Display */}
      {error && (
        <div className="card border-error-200 bg-error-50">
          <div className="card-body">
            <p className="text-error-700">Error: {error}</p>
          </div>
        </div>
      )}

      {/* Appointment Modal */}
      <AppointmentModal
        isOpen={isModalOpen}
        onClose={handleCloseModal}
        event={selectedEvent}
        slot={selectedSlot}
        practitioners={practitioners}
        patients={patients}
        appointmentTypes={appointmentTypes}
        onSave={handleSaveAppointment}
        onDelete={handleDeleteAppointment}
      />
    </div>
  );
};

export default AppointmentCalendar; 
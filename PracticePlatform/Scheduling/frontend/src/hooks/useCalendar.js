import { useState, useEffect, useCallback } from 'react';
import { toast } from 'react-toastify';
import calendarService from '../services/calendarService';

export const useCalendar = () => {
  const [appointments, setAppointments] = useState([]);
  const [practitioners, setPractitioners] = useState([]);
  const [patients, setPatients] = useState([]);
  const [appointmentTypes, setAppointmentTypes] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [selectedDate, setSelectedDate] = useState(new Date());
  const [selectedPractitioner, setSelectedPractitioner] = useState(null);
  const [selectedPatient, setSelectedPatient] = useState(null);
  const [selectedAppointmentType, setSelectedAppointmentType] = useState(null);
  const [availableSlots, setAvailableSlots] = useState([]);

  // Fetch appointments
  const fetchAppointments = useCallback(async (params = {}) => {
    setLoading(true);
    setError(null);
    try {
      const data = await calendarService.getAppointments(params);
      setAppointments(data);
    } catch (err) {
      setError(err.message);
      toast.error('Failed to fetch appointments');
    } finally {
      setLoading(false);
    }
  }, []);

  // Fetch practitioners
  const fetchPractitioners = useCallback(async () => {
    try {
      const data = await calendarService.getPractitioners();
      setPractitioners(data);
    } catch (err) {
      toast.error('Failed to fetch practitioners');
    }
  }, []);

  // Fetch patients
  const fetchPatients = useCallback(async () => {
    try {
      const data = await calendarService.getPatients({ limit: 100 });
      setPatients(data);
    } catch (err) {
      toast.error('Failed to fetch patients');
    }
  }, []);

  // Fetch appointment types
  const fetchAppointmentTypes = useCallback(async () => {
    try {
      const data = await calendarService.getAppointmentTypes();
      setAppointmentTypes(data);
    } catch (err) {
      toast.error('Failed to fetch appointment types');
    }
  }, []);

  // Fetch available slots
  const fetchAvailableSlots = useCallback(async (practitionerId, date, appointmentTypeId = null) => {
    if (!practitionerId || !date) return;
    
    try {
      // Ensure date is in YYYY-MM-DD format
      const formattedDate = date instanceof Date ? date.toISOString().split('T')[0] : date;
      const data = await calendarService.getAvailableSlots(practitionerId, formattedDate, appointmentTypeId);
      setAvailableSlots(data.slots || []);
    } catch (err) {
      console.error('Error fetching available slots:', err);
      toast.error('Failed to fetch available slots');
    }
  }, []);

  // Create appointment
  const createAppointment = useCallback(async (appointmentData) => {
    try {
      const newAppointment = await calendarService.createAppointment(appointmentData);
      setAppointments(prev => [...prev, newAppointment]);
      toast.success('Appointment created successfully');
      return newAppointment;
    } catch (err) {
      toast.error('Failed to create appointment');
      throw err;
    }
  }, []);

  // Update appointment
  const updateAppointment = useCallback(async (appointmentId, appointmentData) => {
    try {
      const updatedAppointment = await calendarService.updateAppointment(appointmentId, appointmentData);
      setAppointments(prev => 
        prev.map(apt => apt.id === appointmentId ? updatedAppointment : apt)
      );
      toast.success('Appointment updated successfully');
      return updatedAppointment;
    } catch (err) {
      toast.error('Failed to update appointment');
      throw err;
    }
  }, []);

  // Delete appointment
  const deleteAppointment = useCallback(async (appointmentId) => {
    try {
      await calendarService.deleteAppointment(appointmentId);
      setAppointments(prev => prev.filter(apt => apt.id !== appointmentId));
      toast.success('Appointment deleted successfully');
    } catch (err) {
      toast.error('Failed to delete appointment');
      throw err;
    }
  }, []);

  // Convert appointments to calendar events format
  const getCalendarEvents = useCallback(() => {
    // Filter appointments based on selected practitioner and patient
    let filteredAppointments = appointments;
    
    if (selectedPractitioner) {
      filteredAppointments = filteredAppointments.filter(appointment => 
        String(appointment.practitioner_id) === String(selectedPractitioner.id)
      );
    }
    
    if (selectedPatient) {
      filteredAppointments = filteredAppointments.filter(appointment => 
        String(appointment.patient_id) === String(selectedPatient.id)
      );
    }
    
    // Filter by selected date (show appointments on the selected date)
    if (selectedDate) {
      const selectedDateStr = selectedDate.toISOString().split('T')[0];
      filteredAppointments = filteredAppointments.filter(appointment => {
        const appointmentDateStr = appointment.start.split('T')[0];
        return appointmentDateStr === selectedDateStr;
      });
    }
    
    // Filter by selected appointment type
    if (selectedAppointmentType) {
      filteredAppointments = filteredAppointments.filter(appointment => {
        const appointmentTypeName = selectedAppointmentType.name.toUpperCase();
        const appointmentType = appointment.appointment_type?.toUpperCase();
        
        return (
          appointmentType === appointmentTypeName ||
          // Handle name variations
          (appointmentTypeName.includes('CONSULTATION') && appointmentType === 'CONSULTATION') ||
          (appointmentTypeName.includes('THERAPY') && appointmentType === 'THERAPY') ||
          (appointmentTypeName.includes('FOLLOW') && appointmentType === 'FOLLOW_UP') ||
          (appointmentTypeName.includes('EMERGENCY') && appointmentType === 'EMERGENCY') ||
          (appointmentTypeName.includes('ASSESSMENT') && appointmentType === 'ASSESSMENT')
        );
      });
    }
    
    return filteredAppointments.map(appointment => {
      // Find patient and practitioner details
      const patient = patients.find(p => p.id === appointment.patient_id);
      const practitioner = practitioners.find(p => p.id === appointment.practitioner_id);
      
      // Format patient name
      const formatPatientName = (patient) => {
        if (!patient) return '';
        if (patient.name) return patient.name;
        const familyName = patient.family_name || '';
        const givenNames = patient.given_names?.join(' ') || '';
        const result = `${givenNames} ${familyName}`.trim();
        return result || 'Unknown Patient';
      };
      
      // Format practitioner name
      const formatPractitionerName = (practitioner) => {
        if (!practitioner) return '';
        if (practitioner.name) return practitioner.name;
        const familyName = practitioner.family_name || '';
        const givenNames = practitioner.given_names?.join(' ') || '';
        const result = familyName + (givenNames ? `, ${givenNames}` : '');
        return result || 'Unknown Practitioner';
      };
      
      // Extract contact info from FHIR telecom array
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
      
      const patientName = formatPatientName(patient);
      const practitionerName = formatPractitionerName(practitioner);
      const { email, phone } = extractContactInfo(patient);
      
      return {
        id: appointment.id,
        title: appointment.title || `${patientName} - ${appointment.appointment_type || 'Appointment'}`,
        start: new Date(appointment.start),
        end: new Date(appointment.end),
        resource: {
          practitioner_id: appointment.practitioner_id,
          practitioner_name: practitionerName,
          patient_id: appointment.patient_id,
          patient_name: patientName,
          patient_phone: phone,
          patient_email: email,

          appointment_type: appointment.appointment_type,
          status: appointment.status,
          location: appointment.location,
          notes: appointment.notes,
          color: appointment.color,
          duration_minutes: appointment.duration_minutes,
          billing_type: appointment.billing_type,
          fee_amount: appointment.fee_amount
        }
      };
    });
  }, [appointments, patients, practitioners, selectedPractitioner, selectedPatient, selectedDate, selectedAppointmentType]);

  // Initialize data on mount
  useEffect(() => {
    fetchAppointments();
    fetchPractitioners();
    fetchPatients();
    fetchAppointmentTypes();
  }, [fetchAppointments, fetchPractitioners, fetchPatients, fetchAppointmentTypes]);

  // Fetch available slots when practitioner or date changes
  useEffect(() => {
    if (selectedPractitioner && selectedDate) {
      const dateString = selectedDate.toISOString().split('T')[0];
      console.log('Fetching available slots for:', {
        practitionerId: selectedPractitioner.id,
        date: dateString,
        practitioner: selectedPractitioner
      });
      fetchAvailableSlots(selectedPractitioner.id, dateString);
    }
  }, [selectedPractitioner, selectedDate, fetchAvailableSlots]);

  return {
    // State
    appointments,
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
    
    // Actions
    setSelectedDate,
    setSelectedPractitioner,
    setSelectedPatient,
    setSelectedAppointmentType,
    fetchAppointments,
    fetchAvailableSlots,
    createAppointment,
    updateAppointment,
    deleteAppointment,
    getCalendarEvents,
    
    // Computed
    calendarEvents: getCalendarEvents()
  };
}; 
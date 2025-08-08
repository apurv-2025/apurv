import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor to include auth token
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export const practitionerAvailabilityService = {
  // Create single availability entry
  createAvailability: async (availabilityData) => {
    try {
      const response = await apiClient.post('/practitioner-availability/', availabilityData);
      return response.data;
    } catch (error) {
      console.error('Error creating availability:', error);
      throw error;
    }
  },

  // Create bulk availability entries
  createBulkAvailability: async (bulkData) => {
    try {
      const response = await apiClient.post('/practitioner-availability/bulk', bulkData);
      return response.data;
    } catch (error) {
      console.error('Error creating bulk availability:', error);
      throw error;
    }
  },

  // Get practitioner availability
  getPractitionerAvailability: async (practitionerId, params = {}) => {
    try {
      const response = await apiClient.get(`/practitioner-availability/${practitionerId}`, { params });
      return response.data;
    } catch (error) {
      console.error('Error fetching practitioner availability:', error);
      throw error;
    }
  },

  // Get practitioner schedule
  getPractitionerSchedule: async (practitionerId, startDate, endDate) => {
    try {
      const response = await apiClient.get(`/practitioner-availability/${practitionerId}/schedule`, {
        params: { start_date: startDate, end_date: endDate }
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching practitioner schedule:', error);
      throw error;
    }
  },

  // Get weekly schedule
  getWeeklySchedule: async (practitionerId, weekStart) => {
    try {
      const response = await apiClient.get(`/practitioner-availability/${practitionerId}/weekly-schedule`, {
        params: { week_start: weekStart }
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching weekly schedule:', error);
      throw error;
    }
  },

  // Get available slots
  getAvailableSlots: async (practitionerId, appointmentDate, appointmentTypeId = null, durationMinutes = null) => {
    try {
      const params = { appointment_date: appointmentDate };
      if (appointmentTypeId) {
        params.appointment_type_id = appointmentTypeId;
      }
      if (durationMinutes) {
        params.duration_minutes = durationMinutes;
      }
      
      const response = await apiClient.get(`/practitioner-availability/${practitionerId}/available-slots`, { params });
      return response.data;
    } catch (error) {
      console.error('Error fetching available slots:', error);
      throw error;
    }
  },

  // Update availability
  updateAvailability: async (availabilityId, updateData) => {
    try {
      const response = await apiClient.put(`/practitioner-availability/${availabilityId}`, updateData);
      return response.data;
    } catch (error) {
      console.error('Error updating availability:', error);
      throw error;
    }
  },

  // Delete availability
  deleteAvailability: async (availabilityId) => {
    try {
      const response = await apiClient.delete(`/practitioner-availability/${availabilityId}`);
      return response.data;
    } catch (error) {
      console.error('Error deleting availability:', error);
      throw error;
    }
  },

  // Deactivate availability (soft delete)
  deactivateAvailability: async (availabilityId) => {
    try {
      const response = await apiClient.patch(`/practitioner-availability/${availabilityId}/deactivate`);
      return response.data;
    } catch (error) {
      console.error('Error deactivating availability:', error);
      throw error;
    }
  },

  // Helper function to create weekly availability pattern
  createWeeklyPattern: (practitionerId, pattern) => {
    const availabilities = [];
    const daysOfWeek = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'];
    
    // Get current week's Monday
    const today = new Date();
    const monday = new Date(today);
    monday.setDate(today.getDate() - today.getDay() + 1);
    
    daysOfWeek.forEach((day, index) => {
      if (pattern[day] && pattern[day].enabled) {
        const date = new Date(monday);
        date.setDate(monday.getDate() + index);
        
        availabilities.push({
          date: date.toISOString().split('T')[0],
          start_time: pattern[day].startTime,
          end_time: pattern[day].endTime,
          notes: pattern[day].notes || null
        });
      }
    });
    
    return {
      practitioner_id: practitionerId,
      availabilities: availabilities
    };
  },

  // Helper function to create recurring availability
  createRecurringAvailability: (practitionerId, startDate, endDate, pattern) => {
    const availabilities = [];
    const daysOfWeek = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'];
    
    const start = new Date(startDate);
    const end = new Date(endDate);
    
    for (let date = new Date(start); date <= end; date.setDate(date.getDate() + 1)) {
      const dayName = daysOfWeek[date.getDay()];
      if (pattern[dayName] && pattern[dayName].enabled) {
        availabilities.push({
          date: date.toISOString().split('T')[0],
          start_time: pattern[dayName].startTime,
          end_time: pattern[dayName].endTime,
          notes: pattern[dayName].notes || null
        });
      }
    }
    
    return {
      practitioner_id: practitionerId,
      availabilities: availabilities
    };
  }
};

export default practitionerAvailabilityService; 
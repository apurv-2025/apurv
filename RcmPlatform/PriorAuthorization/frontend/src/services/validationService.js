// File: src/services/validationService.js - Form Validation
export class ValidationService {
  static validateNPI(npi) {
    if (!npi || typeof npi !== 'string') return false;
    return /^\d{10}$/.test(npi);
  }

  static validateMemberID(memberId) {
    if (!memberId || typeof memberId !== 'string') return false;
    return memberId.trim().length >= 3;
  }

  static validateDate(dateString) {
    if (!dateString) return false;
    const date = new Date(dateString);
    return date instanceof Date && !isNaN(date);
  }

  static validateEmail(email) {
    if (!email) return true; // Email is optional
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  }

  static validatePhone(phone) {
    if (!phone) return true; // Phone is optional
    const phoneRegex = /^\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})$/;
    return phoneRegex.test(phone);
  }

  static validateRequired(value) {
    return value !== null && value !== undefined && value.toString().trim() !== '';
  }

  static validatePriorAuthorizationRequest(request) {
    const errors = {};

    if (!this.validateRequired(request.patient_first_name)) {
      errors.patient_first_name = 'First name is required';
    }

    if (!this.validateRequired(request.patient_last_name)) {
      errors.patient_last_name = 'Last name is required';
    }

    if (!this.validateDate(request.patient_dob)) {
      errors.patient_dob = 'Valid date of birth is required';
    }

    if (!this.validateRequired(request.member_id)) {
      errors.member_id = 'Member ID is required';
    }

    if (!this.validateNPI(request.requesting_provider_npi)) {
      errors.requesting_provider_npi = 'Valid 10-digit NPI is required';
    }

    if (!this.validateDate(request.service_date_from)) {
      errors.service_date_from = 'Service date is required';
    }

    if (!this.validateRequired(request.medical_necessity)) {
      errors.medical_necessity = 'Medical necessity is required';
    }

    return {
      isValid: Object.keys(errors).length === 0,
      errors
    };
  }

  static validatePatientInformation(patient) {
    const errors = {};

    if (!this.validateRequired(patient.first_name)) {
      errors.first_name = 'First name is required';
    }

    if (!this.validateRequired(patient.last_name)) {
      errors.last_name = 'Last name is required';
    }

    if (!this.validateDate(patient.date_of_birth)) {
      errors.date_of_birth = 'Valid date of birth is required';
    }

    if (!this.validateRequired(patient.member_id_primary)) {
      errors.member_id_primary = 'Primary member ID is required';
    }

    if (!this.validateEmail(patient.email)) {
      errors.email = 'Valid email address is required';
    }

    if (!this.validatePhone(patient.phone_home)) {
      errors.phone_home = 'Valid phone number is required';
    }

    return {
      isValid: Object.keys(errors).length === 0,
      errors
    };
  }
}

// Date formatting utilities
export const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString();
};

export const formatDateTime = (dateString) => {
  return new Date(dateString).toLocaleString();
};

// Currency formatting
export const formatCurrency = (amount) => {
  if (amount === null || amount === undefined) return '$0.00';
  return `$${Number(amount).toLocaleString('en-US', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  })}`;
};

// Percentage calculation
export const calculatePercentage = (numerator, denominator) => {
  if (!denominator || denominator === 0) return 0;
  return ((numerator / denominator) * 100).toFixed(1);
};

// File validation
export const validateFile = (file, acceptedExtensions, maxSize) => {
  const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
  
  if (!acceptedExtensions.includes(fileExtension)) {
    return {
      valid: false,
      error: `Invalid file type. Accepted formats: ${acceptedExtensions.join(', ')}`
    };
  }
  
  if (file.size > maxSize) {
    return {
      valid: false,
      error: `File too large. Maximum size: ${(maxSize / (1024 * 1024)).toFixed(1)}MB`
    };
  }
  
  return { valid: true };
};

// Search/filter utilities
export const filterClaims = (claims, searchTerm, statusFilter) => {
  return claims.filter(claim => {
    const matchesSearch = 
      claim.claim_number.toLowerCase().includes(searchTerm.toLowerCase()) ||
      claim.patient_first_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      claim.patient_last_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      claim.provider_name.toLowerCase().includes(searchTerm.toLowerCase());
    
    const matchesStatus = !statusFilter || claim.status === statusFilter;
    
    return matchesSearch && matchesStatus;
  });
};

// Generate random claim number
export const generateClaimNumber = () => {
  return `CLM${Math.random().toString().substr(2, 8)}`;
};

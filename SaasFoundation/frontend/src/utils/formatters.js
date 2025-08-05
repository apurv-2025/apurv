// ===== DATE & TIME FORMATTERS =====

/**
 * Format a date to a readable string
 * @param {Date|string} date - Date to format
 * @param {string} format - Format type: 'short', 'medium', 'long', 'full'
 * @returns {string} Formatted date string
 */
export const formatDate = (date, format = 'medium') => {
  if (!date) return '';
  
  const dateObj = new Date(date);
  if (isNaN(dateObj.getTime())) return '';

  const options = {
    short: { month: 'short', day: 'numeric', year: 'numeric' },
    medium: { month: 'short', day: 'numeric', year: 'numeric', hour: 'numeric', minute: '2-digit' },
    long: { 
      weekday: 'long', 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric',
      hour: 'numeric',
      minute: '2-digit'
    },
    full: {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: 'numeric',
      minute: '2-digit',
      second: '2-digit',
      timeZoneName: 'short'
    }
  };

  return dateObj.toLocaleDateString('en-US', options[format] || options.medium);
};

/**
 * Format a date to relative time (e.g., "2 hours ago", "in 3 days")
 * @param {Date|string} date - Date to format
 * @returns {string} Relative time string
 */
export const formatRelativeTime = (date) => {
  if (!date) return '';
  
  const dateObj = new Date(date);
  if (isNaN(dateObj.getTime())) return '';

  const now = new Date();
  const diffInSeconds = Math.floor((now - dateObj) / 1000);
  const diffInMinutes = Math.floor(diffInSeconds / 60);
  const diffInHours = Math.floor(diffInMinutes / 60);
  const diffInDays = Math.floor(diffInHours / 24);
  const diffInWeeks = Math.floor(diffInDays / 7);
  const diffInMonths = Math.floor(diffInDays / 30);
  const diffInYears = Math.floor(diffInDays / 365);

  // Future dates
  if (diffInSeconds < 0) {
    const absDiffInSeconds = Math.abs(diffInSeconds);
    const absDiffInMinutes = Math.abs(diffInMinutes);
    const absDiffInHours = Math.abs(diffInHours);
    const absDiffInDays = Math.abs(diffInDays);

    if (absDiffInSeconds < 60) return 'in a few seconds';
    if (absDiffInMinutes === 1) return 'in 1 minute';
    if (absDiffInMinutes < 60) return `in ${absDiffInMinutes} minutes`;
    if (absDiffInHours === 1) return 'in 1 hour';
    if (absDiffInHours < 24) return `in ${absDiffInHours} hours`;
    if (absDiffInDays === 1) return 'tomorrow';
    if (absDiffInDays < 7) return `in ${absDiffInDays} days`;
    return formatDate(date, 'short');
  }

  // Past dates
  if (diffInSeconds < 30) return 'just now';
  if (diffInSeconds < 60) return `${diffInSeconds} seconds ago`;
  if (diffInMinutes === 1) return '1 minute ago';
  if (diffInMinutes < 60) return `${diffInMinutes} minutes ago`;
  if (diffInHours === 1) return '1 hour ago';
  if (diffInHours < 24) return `${diffInHours} hours ago`;
  if (diffInDays === 1) return 'yesterday';
  if (diffInDays < 7) return `${diffInDays} days ago`;
  if (diffInWeeks === 1) return '1 week ago';
  if (diffInWeeks < 4) return `${diffInWeeks} weeks ago`;
  if (diffInMonths === 1) return '1 month ago';
  if (diffInMonths < 12) return `${diffInMonths} months ago`;
  if (diffInYears === 1) return '1 year ago';
  return `${diffInYears} years ago`;
};

/**
 * Alias for formatRelativeTime for backward compatibility
 */
export const formatTimeAgo = formatRelativeTime;

/**
 * Format time duration in a human readable format
 * @param {number} seconds - Duration in seconds
 * @returns {string} Formatted duration
 */
export const formatDuration = (seconds) => {
  if (!seconds || seconds < 0) return '0s';

  const hours = Math.floor(seconds / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  const remainingSeconds = seconds % 60;

  const parts = [];
  if (hours > 0) parts.push(`${hours}h`);
  if (minutes > 0) parts.push(`${minutes}m`);
  if (remainingSeconds > 0 || parts.length === 0) parts.push(`${remainingSeconds}s`);

  return parts.join(' ');
};

/**
 * Format time to HH:MM format
 * @param {Date|string} date - Date to format
 * @returns {string} Time in HH:MM format
 */
export const formatTime = (date) => {
  if (!date) return '';
  
  const dateObj = new Date(date);
  if (isNaN(dateObj.getTime())) return '';

  return dateObj.toLocaleTimeString('en-US', {
    hour: '2-digit',
    minute: '2-digit',
    hour12: false
  });
};

// ===== CURRENCY FORMATTERS =====

/**
 * Format currency amount
 * @param {number} amount - Amount in cents
 * @param {string} currency - Currency code (default: USD)
 * @param {boolean} showCents - Whether to show cents (default: true)
 * @returns {string} Formatted currency string
 */
export const formatCurrency = (amount, currency = 'USD', showCents = true) => {
  if (amount === null || amount === undefined) return '';
  
  const value = typeof amount === 'number' ? amount / 100 : parseFloat(amount) / 100;
  
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: currency.toUpperCase(),
    minimumFractionDigits: showCents ? 2 : 0,
    maximumFractionDigits: showCents ? 2 : 0
  }).format(value);
};

/**
 * Format currency for display in plans/pricing
 * @param {number} amount - Amount in cents
 * @param {string} currency - Currency code
 * @param {string} period - Billing period (month, year, etc.)
 * @returns {string} Formatted price string
 */
export const formatPrice = (amount, currency = 'USD', period = 'month') => {
  const formattedAmount = formatCurrency(amount, currency, false);
  return period ? `${formattedAmount}/${period}` : formattedAmount;
};

// ===== NUMBER FORMATTERS =====

/**
 * Format large numbers with abbreviations (K, M, B)
 * @param {number} num - Number to format
 * @param {number} decimals - Number of decimal places
 * @returns {string} Formatted number string
 */
export const formatNumber = (num, decimals = 1) => {
  if (num === null || num === undefined || isNaN(num)) return '0';
  
  const absNum = Math.abs(num);
  
  if (absNum >= 1e9) {
    return (num / 1e9).toFixed(decimals) + 'B';
  }
  if (absNum >= 1e6) {
    return (num / 1e6).toFixed(decimals) + 'M';
  }
  if (absNum >= 1e3) {
    return (num / 1e3).toFixed(decimals) + 'K';
  }
  
  return num.toString();
};

/**
 * Format number with commas for thousands
 * @param {number} num - Number to format
 * @returns {string} Formatted number with commas
 */
export const formatNumberWithCommas = (num) => {
  if (num === null || num === undefined || isNaN(num)) return '0';
  return num.toLocaleString('en-US');
};

/**
 * Format percentage
 * @param {number} value - Value to format as percentage
 * @param {number} decimals - Number of decimal places
 * @returns {string} Formatted percentage
 */
export const formatPercentage = (value, decimals = 1) => {
  if (value === null || value === undefined || isNaN(value)) return '0%';
  return `${value.toFixed(decimals)}%`;
};

// ===== FILE SIZE FORMATTERS =====

/**
 * Format file size in bytes to human readable format
 * @param {number} bytes - File size in bytes
 * @param {number} decimals - Number of decimal places
 * @returns {string} Formatted file size
 */
export const formatFileSize = (bytes, decimals = 2) => {
  if (bytes === 0) return '0 Bytes';
  if (!bytes || bytes < 0) return '';

  const k = 1024;
  const dm = decimals < 0 ? 0 : decimals;
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB'];

  const i = Math.floor(Math.log(bytes) / Math.log(k));

  return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
};

// ===== TEXT FORMATTERS =====

/**
 * Truncate text to specified length
 * @param {string} text - Text to truncate
 * @param {number} maxLength - Maximum length
 * @param {string} suffix - Suffix to add when truncated
 * @returns {string} Truncated text
 */
export const truncateText = (text, maxLength = 100, suffix = '...') => {
  if (!text) return '';
  if (text.length <= maxLength) return text;
  return text.substring(0, maxLength - suffix.length) + suffix;
};

/**
 * Format name for display (First Last or First L.)
 * @param {string} firstName - First name
 * @param {string} lastName - Last name
 * @param {boolean} abbreviated - Whether to abbreviate last name
 * @returns {string} Formatted name
 */
export const formatName = (firstName, lastName, abbreviated = false) => {
  if (!firstName && !lastName) return '';
  if (!firstName) return lastName;
  if (!lastName) return firstName;
  
  if (abbreviated && lastName.length > 1) {
    return `${firstName} ${lastName.charAt(0).toUpperCase()}.`;
  }
  
  return `${firstName} ${lastName}`;
};

/**
 * Format initials from name
 * @param {string} firstName - First name
 * @param {string} lastName - Last name
 * @returns {string} Initials
 */
export const formatInitials = (firstName, lastName) => {
  const first = firstName ? firstName.charAt(0).toUpperCase() : '';
  const last = lastName ? lastName.charAt(0).toUpperCase() : '';
  return first + last || '?';
};

/**
 * Format phone number
 * @param {string} phoneNumber - Phone number to format
 * @returns {string} Formatted phone number
 */
export const formatPhoneNumber = (phoneNumber) => {
  if (!phoneNumber) return '';
  
  // Remove all non-digits
  const cleaned = phoneNumber.replace(/\D/g, '');
  
  // Format as (XXX) XXX-XXXX for US numbers
  if (cleaned.length === 10) {
    return `(${cleaned.slice(0, 3)}) ${cleaned.slice(3, 6)}-${cleaned.slice(6)}`;
  }
  
  // Return original if not a standard US number
  return phoneNumber;
};

// ===== STATUS FORMATTERS =====

/**
 * Format status text for display
 * @param {string} status - Status to format
 * @returns {string} Formatted status
 */
export const formatStatus = (status) => {
  if (!status) return '';
  
  return status
    .split('_')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
    .join(' ');
};

/**
 * Get status color class for badges
 * @param {string} status - Status to get color for
 * @returns {string} CSS class string
 */
export const getStatusColor = (status) => {
  const statusColors = {
    // Subscription statuses
    active: 'bg-green-100 text-green-800',
    trialing: 'bg-blue-100 text-blue-800',
    past_due: 'bg-orange-100 text-orange-800',
    cancelled: 'bg-red-100 text-red-800',
    canceled: 'bg-red-100 text-red-800',
    paused: 'bg-gray-100 text-gray-800',
    
    // Invitation statuses
    pending: 'bg-yellow-100 text-yellow-800',
    accepted: 'bg-green-100 text-green-800',
    declined: 'bg-red-100 text-red-800',
    expired: 'bg-gray-100 text-gray-800',
    
    // User statuses
    online: 'bg-green-100 text-green-800',
    offline: 'bg-gray-100 text-gray-800',
    away: 'bg-yellow-100 text-yellow-800',
    
    // Payment statuses
    paid: 'bg-green-100 text-green-800',
    unpaid: 'bg-red-100 text-red-800',
    processing: 'bg-blue-100 text-blue-800',
    failed: 'bg-red-100 text-red-800',
    
    // General statuses
    success: 'bg-green-100 text-green-800',
    error: 'bg-red-100 text-red-800',
    warning: 'bg-orange-100 text-orange-800',
    info: 'bg-blue-100 text-blue-800'
  };
  
  return statusColors[status?.toLowerCase()] || 'bg-gray-100 text-gray-800';
};

// ===== URL & EMAIL FORMATTERS =====

/**
 * Format URL for display (remove protocol, shorten)
 * @param {string} url - URL to format
 * @param {number} maxLength - Maximum length
 * @returns {string} Formatted URL
 */
export const formatUrl = (url, maxLength = 50) => {
  if (!url) return '';
  
  let formatted = url.replace(/^https?:\/\//, '').replace(/^www\./, '');
  return truncateText(formatted, maxLength);
};

/**
 * Mask email for privacy (john****@example.com)
 * @param {string} email - Email to mask
 * @returns {string} Masked email
 */
export const maskEmail = (email) => {
  if (!email || !email.includes('@')) return email;
  
  const [username, domain] = email.split('@');
  if (username.length <= 2) return email;
  
  const maskedUsername = username.charAt(0) + '*'.repeat(username.length - 2) + username.slice(-1);
  return `${maskedUsername}@${domain}`;
};

// ===== VALIDATION HELPERS =====

/**
 * Check if a date string is valid
 * @param {string} dateString - Date string to validate
 * @returns {boolean} Whether the date is valid
 */
export const isValidDate = (dateString) => {
  const date = new Date(dateString);
  return date instanceof Date && !isNaN(date.getTime());
};

/**
 * Format error message for display
 * @param {Error|string} error - Error to format
 * @returns {string} Formatted error message
 */
export const formatError = (error) => {
  if (!error) return '';
  
  if (typeof error === 'string') return error;
  
  return error.message || 'An unexpected error occurred';
};

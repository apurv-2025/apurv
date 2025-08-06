// frontend/src/utils/dateUtils.js
import { format, parseISO, isValid } from 'date-fns';

export const formatDate = (dateString, formatStr = 'MMM dd, yyyy') => {
  if (!dateString) return '';
  
  try {
    const date = typeof dateString === 'string' ? parseISO(dateString) : dateString;
    if (!isValid(date)) return '';
    return format(date, formatStr);
  } catch (error) {
    console.error('Date formatting error:', error);
    return '';
  }
};

export const formatDateTime = (dateString) => {
  return formatDate(dateString, 'MMM dd, yyyy h:mm a');
};

export const formatTime = (dateString) => {
  return formatDate(dateString, 'h:mm a');
};

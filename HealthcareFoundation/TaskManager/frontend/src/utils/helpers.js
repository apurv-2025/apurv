// src/utils/helpers.js
/**
 * Utility functions for the application
 */

export const formatDate = (date) => {
  if (!date) return null;
  return new Date(date).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  });
};

export const formatDateTime = (date, time) => {
  if (!date) return null;
  
  const dateStr = formatDate(date);
  if (!time) return dateStr;
  
  return `${dateStr} at ${formatTime(time)}`;
};

export const formatTime = (time) => {
  if (!time) return null;
  
  const [hours, minutes] = time.split(':');
  const hour = parseInt(hours);
  const ampm = hour >= 12 ? 'PM' : 'AM';
  const displayHour = hour === 0 ? 12 : hour > 12 ? hour - 12 : hour;
  
  return `${displayHour}:${minutes} ${ampm}`;
};

export const isOverdue = (dueDate, dueTime, status) => {
  if (!dueDate || status === 'completed') return false;
  
  const dueDateTimeString = `${dueDate}T${dueTime || '23:59'}`;
  const dueDateTime = new Date(dueDateTimeString);
  
  return dueDateTime < new Date();
};

export const getDaysUntilDue = (dueDate) => {
  if (!dueDate) return null;
  
  const due = new Date(dueDate);
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  due.setHours(0, 0, 0, 0);
  
  const diffTime = due - today;
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
  
  return diffDays;
};

export const getRelativeDateString = (dueDate) => {
  const days = getDaysUntilDue(dueDate);
  
  if (days === null) return null;
  if (days === 0) return 'Due today';
  if (days === 1) return 'Due tomorrow';
  if (days === -1) return '1 day overdue';
  if (days < -1) return `${Math.abs(days)} days overdue`;
  if (days > 1) return `Due in ${days} days`;
  
  return formatDate(dueDate);
};

export const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes';
  
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
};

export const truncateText = (text, maxLength = 100) => {
  if (!text || text.length <= maxLength) return text;
  return text.substring(0, maxLength) + '...';
};

export const debounce = (func, wait) => {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
};

export const classNames = (...classes) => {
  return classes.filter(Boolean).join(' ');
};

export const generateId = () => {
  return Math.random().toString(36).substr(2, 9);
};

export const validateEmail = (email) => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

export const validatePhone = (phone) => {
  const phoneRegex = /^[\+]?[1-9][\d]{0,15}$/;
  return phoneRegex.test(phone.replace(/\s/g, ''));
};


// src/services/user.js
import api from './api';
import { API_ENDPOINTS } from '../utils/constants';

export const userService = {
  getProfile: async () => {
    const response = await api.get(API_ENDPOINTS.USER.PROFILE);
    return response.data;
  },

  updateProfile: async (data) => {
    const response = await api.put(API_ENDPOINTS.USER.PROFILE, data);
    return response.data;
  },

  changePassword: async (currentPassword, newPassword) => {
    const response = await api.put(API_ENDPOINTS.USER.PASSWORD, {
      current_password: currentPassword,
      new_password: newPassword
    });
    return response.data;
  },

  getPreferences: async () => {
    const response = await api.get(API_ENDPOINTS.USER.PREFERENCES);
    return response.data;
  },

  updatePreferences: async (preferences) => {
    const response = await api.put(API_ENDPOINTS.USER.PREFERENCES, preferences);
    return response.data;
  },

  exportData: async () => {
    const response = await api.get(API_ENDPOINTS.USER.EXPORT, {
      responseType: 'blob'
    });
    return response.data;
  },

  deleteAccount: async () => {
    const response = await api.delete(API_ENDPOINTS.USER.DELETE);
    return response.data;
  }
};

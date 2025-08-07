// src/services/team.js
import api from './api';
import { API_ENDPOINTS } from '../utils/constants';

export const teamService = {
  getOrganization: async () => {
    const response = await api.get(API_ENDPOINTS.ORGANIZATIONS.CURRENT);
    return response.data;
  },

  updateOrganization: async (data) => {
    const response = await api.put(API_ENDPOINTS.ORGANIZATIONS.UPDATE, data);
    return response.data;
  },

  getMembers: async () => {
    const response = await api.get(API_ENDPOINTS.ORGANIZATIONS.MEMBERS);
    return response.data;
  },

  updateMemberRole: async (memberId, role) => {
    const response = await api.put(`${API_ENDPOINTS.ORGANIZATIONS.MEMBERS}/${memberId}`, {
      role
    });
    return response.data;
  },

  removeMember: async (memberId) => {
    const response = await api.delete(`${API_ENDPOINTS.ORGANIZATIONS.MEMBERS}/${memberId}`);
    return response.data;
  },

  getInvitations: async () => {
    const response = await api.get(API_ENDPOINTS.ORGANIZATIONS.INVITATIONS);
    return response.data;
  },

 
  inviteMember: async (data) => {
    const response = await api.post(API_ENDPOINTS.ORGANIZATIONS.INVITE, data);
    return response.data;
  },

  resendInvitation: async (invitationId) => {
    const response = await api.post(API_ENDPOINTS.INVITATIONS.RESEND(invitationId));
    return response.data;
  },

  cancelInvitation: async (invitationId) => {
    const response = await api.delete(API_ENDPOINTS.INVITATIONS.CANCEL(invitationId));
    return response.data;
  },

  getInvitationDetails: async (token) => {
    const response = await api.get(API_ENDPOINTS.INVITATIONS.DETAILS(token));
    return response.data;
  },

  acceptInvitation: async (token) => {
    console.log('teamService.acceptInvitation called with token:', token);
    console.log('API endpoint:', API_ENDPOINTS.INVITATIONS.ACCEPT(token));
    const response = await api.post(API_ENDPOINTS.INVITATIONS.ACCEPT(token));
    console.log('teamService.acceptInvitation response:', response);
    return response.data;
  }
};

import { useState, useCallback } from 'react';
import { teamService } from '../services/team';
import { useAuth } from './useAuth';

export const useTeam = () => {
  const { user } = useAuth();
  const [members, setMembers] = useState([]);
  const [invitations, setInvitations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [currentUserRole, setCurrentUserRole] = useState('admin');

  // Fetch all team data (members and invitations)
  const fetchTeamData = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      
      const [membersResponse, invitationsResponse,orgResponse] = await Promise.all([
        teamService.getOrganization(),
        teamService.getMembers(),
        teamService.getInvitations()
      ]);
      
      setMembers(membersResponse.data || []);
      setInvitations(invitationsResponse.data || []);
      setCurrentUserRole(orgResponse.current_user_role);
    } catch (err) {
      setError(err.message || 'Failed to fetch team data');
      console.error('Error fetching team data:', err);
    } finally {
      setLoading(false);
    }
  }, []);

  // Fetch only team members
  const fetchMembers = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await teamService.getMembers();
      setMembers(response.data || []);
    } catch (err) {
      setError(err.message || 'Failed to fetch team members');
      console.error('Error fetching members:', err);
    } finally {
      setLoading(false);
    }
  }, []);

  // Fetch only invitations
  const fetchInvitations = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await teamService.getInvitations();
      setInvitations(response.data || []);
    } catch (err) {
      setError(err.message || 'Failed to fetch invitations');
      console.error('Error fetching invitations:', err);
    } finally {
      setLoading(false);
    }
  }, []);

  // Invite a new team member
  const inviteMember = useCallback(async (inviteData) => {
    try {
      setError(null);
      
      const response = await teamService.inviteMember(inviteData);
      
      // Add the new invitation to the state
      setInvitations(prev => [response.data, ...prev]);
      
      return response.data;
    } catch (err) {
      const errorMessage = err.message || 'Failed to send invitation';
      setError(errorMessage);
      throw new Error(errorMessage);
    }
  }, []);

  // Remove a team member
  const removeMember = useCallback(async (memberId) => {
    try {
      setError(null);
      
      await teamService.removeMember(memberId);
      
      // Remove the member from state
      setMembers(prev => prev.filter(member => member.id !== memberId));
    } catch (err) {
      const errorMessage = err.message || 'Failed to remove team member';
      setError(errorMessage);
      throw new Error(errorMessage);
    }
  }, []);

  // Update a team member's role
  const updateMemberRole = useCallback(async (memberId, newRole) => {
    try {
      setError(null);
      
      const response = await teamService.updateMemberRole(memberId, newRole);
      
      // Update the member in state
      setMembers(prev => 
        prev.map(member => 
          member.id === memberId 
            ? { ...member, role: newRole, updatedAt: new Date().toISOString() }
            : member
        )
      );
      
      return response.data;
    } catch (err) {
      const errorMessage = err.message || 'Failed to update member role';
      setError(errorMessage);
      throw new Error(errorMessage);
    }
  }, []);

  // Cancel a pending invitation
  const cancelInvitation = useCallback(async (invitationId) => {
    try {
      setError(null);
      
      await teamService.cancelInvitation(invitationId);
      
      // Remove the invitation from state
      setInvitations(prev => prev.filter(invitation => invitation.id !== invitationId));
    } catch (err) {
      const errorMessage = err.message || 'Failed to cancel invitation';
      setError(errorMessage);
      throw new Error(errorMessage);
    }
  }, []);

  // Resend a pending invitation
  const resendInvitation = useCallback(async (invitationId) => {
    try {
      setError(null);
      
      const response = await teamService.resendInvitation(invitationId);
      
      // Update the invitation in state with new sent date
      setInvitations(prev => 
        prev.map(invitation => 
          invitation.id === invitationId 
            ? { ...invitation, sentAt: new Date().toISOString(), resendCount: (invitation.resendCount || 0) + 1 }
            : invitation
        )
      );
      
      return response.data;
    } catch (err) {
      const errorMessage = err.message || 'Failed to resend invitation';
      setError(errorMessage);
      throw new Error(errorMessage);
    }
  }, []);

  // Accept an invitation (for the invited user)
  const acceptInvitation = useCallback(async (invitationData) => {
    try {
      setError(null);
      
      const response = await teamService.acceptInvitation(invitationData);
      return response.data;
    } catch (err) {
      const errorMessage = err.message || 'Failed to accept invitation';
      setError(errorMessage);
      throw new Error(errorMessage);
    }
  }, []);

  // Decline an invitation (for the invited user)
  const declineInvitation = useCallback(async (invitationData) => {
    try {
      setError(null);
      
      const response = await teamService.declineInvitation(invitationData);
      return response.data;
    } catch (err) {
      const errorMessage = err.message || 'Failed to decline invitation';
      setError(errorMessage);
      throw new Error(errorMessage);
    }
  }, []);

  // Transfer team ownership
  const transferOwnership = useCallback(async (newOwnerId) => {
    try {
      setError(null);
      
      const response = await teamService.transferOwnership(newOwnerId);
      
      // Update members state to reflect new roles
      setMembers(prev => 
        prev.map(member => {
          if (member.id === newOwnerId) {
            return { ...member, role: 'owner' };
          }
          if (member.id === user.id) {
            return { ...member, role: 'admin' };
          }
          return member;
        })
      );
      
      return response.data;
    } catch (err) {
      const errorMessage = err.message || 'Failed to transfer ownership';
      setError(errorMessage);
      throw new Error(errorMessage);
    }
  }, [user.id]);

  // Get team statistics
  const getTeamStats = useCallback(() => {
    const stats = {
      totalMembers: members.length,
      activeMembers: members.filter(m => m.status === 'active').length,
      pendingInvitations: invitations.length,
      adminCount: members.filter(m => m.role === 'admin').length,
      memberCount: members.filter(m => m.role === 'member').length,
      viewerCount: members.filter(m => m.role === 'viewer').length,
      ownerCount: members.filter(m => m.role === 'owner').length
    };
    
    return stats;
  }, [members, invitations]);

  // Check if current user can manage team
  const canManageTeam = useCallback(() => {
    if (!user) return false;
    return ['owner', 'admin'].includes(user.role);
  }, [user]);

  // Check if current user can manage specific member
  const canManageMember = useCallback((member) => {
    if (!user || !member) return false;
    
    // Owner can manage everyone except themselves
    if (user.role === 'owner') {
      return member.id !== user.id;
    }
    
    // Admin can manage members and viewers, but not other admins or owners
    if (user.role === 'admin') {
      return ['member', 'viewer'].includes(member.role) && member.id !== user.id;
    }
    
    return false;
  }, [user]);

  // Get available roles for assignment
  const getAvailableRoles = useCallback(() => {
    if (!user) return [];
    
    const allRoles = [
      { value: 'viewer', label: 'Viewer', description: 'Can view team data' },
      { value: 'member', label: 'Member', description: 'Can edit and collaborate' },
      { value: 'admin', label: 'Admin', description: 'Can manage team members' },
      { value: 'owner', label: 'Owner', description: 'Full control of the team' }
    ];
    
    // Owner can assign any role except owner
    if (user.role === 'owner') {
      return allRoles.filter(role => role.value !== 'owner');
    }
    
    // Admin can assign viewer and member roles
    if (user.role === 'admin') {
      return allRoles.filter(role => ['viewer', 'member'].includes(role.value));
    }
    
    return [];
  }, [user]);

  // Clear error
  const clearError = useCallback(() => {
    setError(null);
  }, []);

  // Refresh team data
  const refreshTeam = useCallback(() => {
    return fetchTeamData();
  }, [fetchTeamData]);

  return {
    // State
    members,
    invitations,
    loading,
    error,
    currentUserRole,
    
    // Data fetching
    fetchTeamData,
    fetchMembers,
    fetchInvitations,
    refreshTeam,
    
    // Member management
    inviteMember,
    removeMember,
    updateMemberRole,
    transferOwnership,
    
    // Invitation management
    cancelInvitation,
    resendInvitation,
    acceptInvitation,
    declineInvitation,
    
    // Utility functions
    getTeamStats,
    canManageTeam,
    canManageMember,
    getAvailableRoles,
    clearError,
    
    // Computed values
    teamStats: getTeamStats(),
    canManage: canManageTeam()
  };
};

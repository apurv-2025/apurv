import React, { useState, useEffect } from 'react';
import { layout } from '../../components/layout';
import { Card, Button, Badge, Modal } from '../../components/ui';
import { MemberCard, InvitationCard, InviteForm } from '../../components/team';
import RoleSelect from './RoleSelect';
import { EmptyState, EmptyStates, SuccessMessage, ErrorMessage } from '../../components/common';

import '../../styles/pages/teammanagement.css';  

import { useAuthContext } from '../../contexts/AuthContext';
import api from '../../services/api';
import { API_ENDPOINTS } from '../../utils/constants';

function TeamManagement() {
  const { user } = useAuthContext();
  const [activeTab, setActiveTab] = useState('members');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState({ type: '', text: '' });
  
  // Team data state
  const [organization, setOrganization] = useState(null);
  const [members, setMembers] = useState([]);
  const [invitations, setInvitations] = useState([]);
  const [currentUserRole, setCurrentUserRole] = useState('member');
  
  // Invite form state
  const [inviteForm, setInviteForm] = useState({
    email: '',
    role: 'member'
  });
  
  // Organization form state
  const [orgForm, setOrgForm] = useState({
    name: '',
    description: ''
  });

  useEffect(() => {
    fetchTeamData();
  }, []);

  const fetchTeamData = async () => {
    setLoading(true);
    try {
      const [orgResponse, membersResponse, invitationsResponse] = await Promise.all([
        api.get(API_ENDPOINTS.ORGANIZATIONS.CURRENT),
        api.get(API_ENDPOINTS.ORGANIZATIONS.MEMBERS),
        api.get(API_ENDPOINTS.ORGANIZATIONS.INVITATIONS)
      ]);
      
      setOrganization(orgResponse.data.organization);
      setMembers(membersResponse.data);
      setInvitations(invitationsResponse.data);
      setCurrentUserRole(orgResponse.data.current_user_role);
      
      if (orgResponse.data.organization) {
        setOrgForm({
          name: orgResponse.data.organization.name,
          description: orgResponse.data.organization.description || ''
        });
      }
    } catch (error) {
      console.error('Failed to fetch team data:', error);
      showMessage('error', 'Failed to load team data');
    } finally {
      setLoading(false);
    }
  };

  const showMessage = (type, text) => {
    setMessage({ type, text });
    setTimeout(() => setMessage({ type: '', text: '' }), 5000);
  };

  const handleInviteUser = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      await api.post(API_ENDPOINTS.ORGANIZATIONS.INVITE, inviteForm);
      showMessage('success', 'Invitation sent successfully!');
      setInviteForm({ email: '', role: 'member' });
      fetchTeamData(); // Refresh data
    } catch (error) {
      showMessage('error', error.response?.data?.detail || 'Failed to send invitation');
    } finally {
      setLoading(false);
    }
  };


  const handleUpdateMemberRole = async (memberId, newRole) => {
    setLoading(true);
    
    try {
      await api.put(`/api/v1/organizations/current/members/${memberId}`, {
        role: newRole
      });
      showMessage('success', 'Member role updated successfully!');
      fetchTeamData();
    } catch (error) {
      showMessage('error', 'Failed to update member role');
    } finally {
      setLoading(false);
    }
  };

  const handleRemoveMember = async (memberId) => {
    if (!window.confirm('Are you sure you want to remove this member?')) {
      return;
    }
    
    setLoading(true);
    
    try {
      await api.delete(`/api/v1/organizations/current/members/${memberId}`);
      showMessage('success', 'Member removed successfully!');
      fetchTeamData();
    } catch (error) {
      showMessage('error', 'Failed to remove member');
    } finally {
      setLoading(false);
    }
  };

  const handleCancelInvitation = async (invitationId) => {
    setLoading(true);
    
    try {
      await api.delete(`/api/v1/organizations/current/invitations/${invitationId}`);
      showMessage('success', 'Invitation cancelled');
      fetchTeamData();
    } catch (error) {
      showMessage('error', 'Failed to cancel invitation');
    } finally {
      setLoading(false);
    }
  };

  const handleResendInvitation = async (invitationId) => {
    setLoading(true);
    
    try {
      await api.post(`/api/v1/organizations/current/invitations/${invitationId}/resend`);
      showMessage('success', 'Invitation resent successfully!');
    } catch (error) {
      showMessage('error', 'Failed to resend invitation');
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateOrganization = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      await api.put('/api/v1/organizations/current', orgForm);
      showMessage('success', 'Organization updated successfully!');
      fetchTeamData();
    } catch (error) {
      showMessage('error', 'Failed to update organization');
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  const getRoleColor = (role) => {
    switch (role) {
      case 'owner': return 'role-owner';
      case 'admin': return 'role-admin';
      case 'member': return 'role-member';
      default: return 'role-member';
    }
  };

  const canManageMembers = currentUserRole === 'owner' || currentUserRole === 'admin';
  
  if (loading && !organization) {
    return <div className="loading">Loading team data...</div>;
  }

  return (
    <div className="team-container">
      <div className="team-header">
        <div className="header-info">
          <h1>Team Management</h1>
          {organization && (
            <p className="org-info">
              {organization.name} • {members.length} member{members.length !== 1 ? 's' : ''}
            </p>
          )}
        </div>
        {canManageMembers && (
          <button 
            className="btn-primary"
            onClick={() => setActiveTab('invite')}
          >
            Invite Members
          </button>
        )}
      </div>

      {message.text && (
        <div className={`message ${message.type}`}>
          {message.text}
        </div>
      )}

      <div className="team-tabs">
        <button
          className={`tab ${activeTab === 'members' ? 'active' : ''}`}
          onClick={() => setActiveTab('members')}
        >
          Team Members ({members.length})
        </button>
        {canManageMembers && (
          <>
            <button
              className={`tab ${activeTab === 'invitations' ? 'active' : ''}`}
              onClick={() => setActiveTab('invitations')}
            >
              Pending Invitations ({invitations.length})
            </button>
            <button
              className={`tab ${activeTab === 'invite' ? 'active' : ''}`}
              onClick={() => setActiveTab('invite')}
            >
              Invite New Member
            </button>
          </>
        )}
        {currentUserRole === 'owner' && (
          <button
            className={`tab ${activeTab === 'settings' ? 'active' : ''}`}
            onClick={() => setActiveTab('settings')}
          >
            Organization Settings
          </button>
        )}
      </div>

      <div className="tab-content">
        {activeTab === 'members' && (
          <div className="members-section">
            <h3>Team Members</h3>
            <div className="members-list">
              {members.map((member) => (
                <div key={member.id} className="member-card">
                  <div className="member-info">
                    <div className="member-avatar">
                      {member.user.first_name.charAt(0)}{member.user.last_name.charAt(0)}
                    </div>
                    <div className="member-details">
                      <h4>{member.user.first_name} {member.user.last_name}</h4>
                      <p className="member-email">{member.user.email}</p>
                      <div className="member-meta">
                        <span className={`role-badge ${getRoleColor(member.role)}`}>
                          {member.role.toUpperCase()}
                        </span>
                        <span className="join-date">
                          Joined {formatDate(member.joined_at)}
                        </span>
                      </div>
                    </div>
                  </div>
                  
                  {canManageMembers && member.user.id !== user.id && (
                    <div className="member-actions">
                      <RoleSelect
                        value={member.role}
                        onChange={(e) => handleUpdateMemberRole(member.id, e.target.value)}
                        currentUserRole={currentUserRole}
                        disabled={member.role === 'owner'}
                        size="sm"
                      />
                      <button
                        onClick={() => handleRemoveMember(member.id)}
                        className="btn-danger-small"
                        disabled={member.role === 'owner'}
                      >
                        Remove
                      </button>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {activeTab === 'invitations' && canManageMembers && (
          <div className="invitations-section">
            <h3>Pending Invitations</h3>
            {invitations.length > 0 ? (
              <div className="invitations-list">
                {invitations.map((invitation) => (
                  <div key={invitation.id} className="invitation-card">
                    <div className="invitation-info">
                      <h4>{invitation.email}</h4>
                      <div className="invitation-meta">
                        <span className={`role-badge ${getRoleColor(invitation.role)}`}>
                          {invitation.role.toUpperCase()}
                        </span>
                        <span className="invite-date">
                          Invited {formatDate(invitation.created_at)}
                        </span>
                        <span className="expires-date">
                          Expires {formatDate(invitation.expires_at)}
                        </span>
                      </div>
                    </div>
                    
                    <div className="invitation-actions">
                      <button
                        onClick={() => handleResendInvitation(invitation.id)}
                        className="btn-secondary-small"
                      >
                        Resend
                      </button>
                      <button
                        onClick={() => handleCancelInvitation(invitation.id)}
                        className="btn-danger-small"
                      >
                        Cancel
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="empty-state">
                <p>No pending invitations</p>
              </div>
            )}
          </div>
        )}

        {activeTab === 'invite' && canManageMembers && (
          <div className="invite-section">
            <h3>Invite New Team Member</h3>
            <div className="invite-form-container">
              <form onSubmit={handleInviteUser} className="invite-form">
                <div className="form-group">
                  <label htmlFor="email">Email Address</label>
                  <input
                    type="email"
                    id="email"
                    value={inviteForm.email}
                    onChange={(e) => setInviteForm(prev => ({
                      ...prev,
                      email: e.target.value
                    }))}
                    className="form-input"
                    placeholder="Enter email address"
                    required
                  />
                </div>
                
                <div className="form-group">
                  <label htmlFor="role">Role</label>
                  <RoleSelect
                    value={inviteForm.role}
                    onChange={(e) => setInviteForm(prev => ({
                      ...prev,
                      role: e.target.value
                    }))}
                    currentUserRole={currentUserRole}
                    includeDescriptions={true}
                  />
                  <small className="form-help">
                    Select the appropriate role for this team member based on their responsibilities.
                  </small>
                </div>
                
                <button
                  type="submit"
                  disabled={loading}
                  className="btn-primary"
                >
                  {loading ? 'Sending Invitation...' : 'Send Invitation'}
                </button>
              </form>
              
              <div className="invite-info">
                <h4>Role Permissions</h4>
                <div className="permissions-grid">
                  <div className="permission-item">
                    <strong>Member</strong>
                    <ul>
                      <li>Access dashboard and features</li>
                      <li>View organization data</li>
                      <li>Use platform within plan limits</li>
                    </ul>
                  </div>
                  <div className="permission-item">
                    <strong>Admin</strong>
                    <ul>
                      <li>All member permissions</li>
                      <li>Invite and manage team members</li>
                      <li>Manage organization settings</li>
                      <li>View billing information</li>
                    </ul>
                  </div>
                  <div className="permission-item">
                    <strong>Owner</strong>
                    <ul>
                      <li>All admin permissions</li>
                      <li>Manage subscription and billing</li>
                      <li>Transfer ownership</li>
                      <li>Delete organization</li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'settings' && currentUserRole === 'owner' && (
          <div className="org-settings-section">
            <h3>Organization Settings</h3>
            <form onSubmit={handleUpdateOrganization} className="org-form">
              <div className="form-group">
                <label htmlFor="orgName">Organization Name</label>
                <input
                  type="text"
                  id="orgName"
                  value={orgForm.name}
                  onChange={(e) => setOrgForm(prev => ({
                    ...prev,
                    name: e.target.value
                  }))}
                  className="form-input"
                  required
                />
              </div>
              
              <div className="form-group">
                <label htmlFor="orgDescription">Description</label>
                <textarea
                  id="orgDescription"
                  value={orgForm.description}
                  onChange={(e) => setOrgForm(prev => ({
                    ...prev,
                    description: e.target.value
                  }))}
                  className="form-textarea"
                  rows="3"
                  placeholder="Optional organization description"
                />
              </div>
              
              <button
                type="submit"
                disabled={loading}
                className="btn-primary"
              >
                {loading ? 'Updating...' : 'Update Organization'}
              </button>
            </form>
            
            <div className="danger-zone">
              <h4>Danger Zone</h4>
              <div className="danger-item">
                <div className="danger-info">
                  <strong>Delete Organization</strong>
                  <p>Permanently delete this organization and all associated data. This action cannot be undone.</p>
                </div>
                <button className="btn-danger">
                  Delete Organization
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default TeamManagement;

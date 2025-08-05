// src/components/team/MemberCard.jsx
import React, { useState } from 'react';
import { 
  UserIcon, 
  EllipsisVerticalIcon,
  ShieldCheckIcon,
  CalendarIcon,
  EnvelopeIcon
} from '@heroicons/react/24/outline';
import { Card, CardContent } from '../ui/Card';
import Button from '../ui/Button';
import Badge from '../ui/Badge';
import { ConfirmModal } from '../ui/Modal';
import RoleSelect from './RoleSelect';
import { formatDate } from '../../utils/formatters';
import { cn } from '../../utils/helpers';

const MemberCard = ({ 
  member, 
  currentUserRole, 
  currentUserId, 
  onUpdateRole, 
  onRemoveMember,
  loading = false,
  className 
}) => {
  const [showMenu, setShowMenu] = useState(false);
  const [showRemoveModal, setShowRemoveModal] = useState(false);
  const [isUpdatingRole, setIsUpdatingRole] = useState(false);

  const {
    id,
    user,
    role,
    joined_at,
    status = 'active',
    last_active_at,
    permissions = []
  } = member;

  const canManage = (currentUserRole === 'owner' || currentUserRole === 'admin') && 
                    user.id !== currentUserId;
  const canChangeRole = canManage && role !== 'owner';
  const canRemove = canManage && role !== 'owner';

  // Get role styling
  const getRoleVariant = (role) => {
    switch (role) {
      case 'owner': return 'warning';
      case 'admin': return 'info';
      case 'member': return 'secondary';
      default: return 'secondary';
    }
  };

  // Get role icon
  const getRoleIcon = (role) => {
    switch (role) {
      case 'owner': return '👑';
      case 'admin': return '🛡️';
      case 'member': return '👤';
      default: return '👤';
    }
  };

  // Get user initials
  const getUserInitials = (firstName, lastName) => {
    return `${firstName?.charAt(0) || ''}${lastName?.charAt(0) || ''}`.toUpperCase();
  };

  // Handle role update
  const handleRoleUpdate = async (newRole) => {
    if (newRole === role) return;
    
    setIsUpdatingRole(true);
    try {
      await onUpdateRole?.(id, newRole);
    } catch (error) {
      console.error('Failed to update role:', error);
    } finally {
      setIsUpdatingRole(false);
    }
  };

  // Handle member removal
  const handleRemove = async () => {
    try {
      await onRemoveMember?.(id);
      setShowRemoveModal(false);
    } catch (error) {
      console.error('Failed to remove member:', error);
    }
  };

  // Get status color
  const getStatusColor = (status) => {
    switch (status) {
      case 'active': return 'text-green-600';
      case 'pending': return 'text-yellow-600';
      case 'inactive': return 'text-gray-400';
      default: return 'text-gray-400';
    }
  };

  return (
    <>
      <Card className={cn("relative transition-all duration-200 hover:shadow-md", className)}>
        <CardContent className="pt-6">
          <div className="flex items-start justify-between">
            {/* Member Info */}
            <div className="flex items-start space-x-4 flex-1">
              {/* Avatar */}
              <div className="relative">
                <div className="w-12 h-12 bg-gradient-to-r from-blue-600 to-blue-600 rounded-full flex items-center justify-center text-white font-semibold text-lg">
                  {user.avatar_url ? (
                    <img 
                      src={user.avatar_url} 
                      alt={`${user.first_name} ${user.last_name}`}
                      className="w-12 h-12 rounded-full object-cover"
                    />
                  ) : (
                    getUserInitials(user.first_name, user.last_name)
                  )}
                </div>
                
                {/* Status indicator */}
                <div className={cn(
                  "absolute -bottom-1 -right-1 w-4 h-4 rounded-full border-2 border-white",
                  status === 'active' ? 'bg-green-500' : 
                  status === 'pending' ? 'bg-yellow-500' : 'bg-gray-400'
                )} />
              </div>

              {/* Member Details */}
              <div className="flex-1 min-w-0">
                <div className="flex items-center space-x-2 mb-2">
                  <h4 className="text-lg font-semibold text-gray-900 truncate">
                    {user.first_name} {user.last_name}
                  </h4>
                  {user.id === currentUserId && (
                    <Badge variant="info" className="text-xs">You</Badge>
                  )}
                </div>

                <div className="space-y-1">
                  <div className="flex items-center text-sm text-gray-600">
                    <EnvelopeIcon className="h-4 w-4 mr-1" />
                    <span className="truncate">{user.email}</span>
                  </div>
                  
                  {user.title && (
                    <div className="flex items-center text-sm text-gray-600">
                      <UserIcon className="h-4 w-4 mr-1" />
                      <span>{user.title}</span>
                    </div>
                  )}

                  <div className="flex items-center text-sm text-gray-600">
                    <CalendarIcon className="h-4 w-4 mr-1" />
                    <span>Joined {formatDate(joined_at)}</span>
                  </div>

                  {last_active_at && (
                    <div className="text-xs text-gray-500">
                      Last active: {formatDate(last_active_at)}
                    </div>
                  )}
                </div>

                {/* Role and Permissions */}
                <div className="mt-3 flex items-center space-x-3">
                  <div className="flex items-center space-x-2">
                    <span className="text-lg">{getRoleIcon(role)}</span>
                    <Badge variant={getRoleVariant(role)} className="text-xs">
                      {role.toUpperCase()}
                    </Badge>
                  </div>
                  
                  {permissions.length > 0 && (
                    <div className="flex items-center space-x-1">
                      <ShieldCheckIcon className="h-4 w-4 text-gray-400" />
                      <span className="text-xs text-gray-500">
                        {permissions.length} permission{permissions.length > 1 ? 's' : ''}
                      </span>
                    </div>
                  )}
                </div>
              </div>
            </div>

            {/* Actions */}
            {canManage && (
              <div className="relative ml-4">
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => setShowMenu(!showMenu)}
                  className="p-2"
                  disabled={loading}
                >
                  <EllipsisVerticalIcon className="h-4 w-4" />
                </Button>

                {showMenu && (
                  <div className="absolute right-0 top-8 w-48 bg-white border border-gray-200 rounded-md shadow-lg z-10">
                    <div className="py-1">
                      <div className="px-4 py-2 text-xs font-medium text-gray-500 uppercase">
                        Actions
                      </div>
                      
                      {canChangeRole && (
                        <button
                          onClick={() => {
                            setShowMenu(false);
                            // You could open a role edit modal here
                          }}
                          className="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                        >
                          Change Role
                        </button>
                      )}
                      
                      <button
                        onClick={() => {
                          setShowMenu(false);
                          // Send invitation or resend
                        }}
                        className="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                      >
                        Send Message
                      </button>
                      
                      {canRemove && (
                        <button
                          onClick={() => {
                            setShowRemoveModal(true);
                            setShowMenu(false);
                          }}
                          className="block w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50"
                        >
                          Remove Member
                        </button>
                      )}
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>

          {/* Role Management (if user can manage) */}
          {canChangeRole && (
            <div className="mt-4 pt-4 border-t border-gray-200">
              <div className="flex items-center justify-between">
                <label className="text-sm font-medium text-gray-700">
                  Role:
                </label>
                <div className="flex items-center space-x-2">
                  <RoleSelect
                    value={role}
                    onChange={handleRoleUpdate}
                    currentUserRole={currentUserRole}
                    disabled={loading || isUpdatingRole}
                    size="sm"
                  />
                  {canRemove && (
                    <Button
                      variant="danger"
                      size="sm"
                      onClick={() => setShowRemoveModal(true)}
                      disabled={loading}
                    >
                      Remove
                    </Button>
                  )}
                </div>
              </div>
            </div>
          )}

          {/* Status Messages */}
          {status === 'pending' && (
            <div className="mt-3 p-2 bg-yellow-50 border border-yellow-200 rounded-md">
              <p className="text-xs text-yellow-800">
                📧 Invitation pending - User hasn't accepted yet
              </p>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Remove Confirmation Modal */}
      <ConfirmModal
        isOpen={showRemoveModal}
        onClose={() => setShowRemoveModal(false)}
        onConfirm={handleRemove}
        title="Remove Team Member"
        message={`Are you sure you want to remove ${user.first_name} ${user.last_name} from the team? They will lose access to all team resources.`}
        confirmText="Remove Member"
        cancelText="Keep Member"
        variant="danger"
        loading={loading}
      />

      {/* Click outside to close menu */}
      {showMenu && (
        <div
          className="fixed inset-0 z-0"
          onClick={() => setShowMenu(false)}
        />
      )}
    </>
  );
};

export default MemberCard;

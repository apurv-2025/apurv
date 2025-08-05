import React, { useState } from 'react';
import { 
  PaperAirplaneIcon,
  ClockIcon,
  ExclamationTriangleIcon
} from '@heroicons/react/24/outline';

import { Card, CardContent } from '../ui/Card';
import Button from '../ui/Button';
import Badge from '../ui/Badge';
import { ConfirmModal } from '../ui/Modal';
import { formatDate, formatTimeAgo } from '../../utils/formatters';
import { cn } from '../../utils/helpers';

const InvitationCard = ({ 
  invitation, 
  onResendInvitation, 
  onCancelInvitation,
  loading = false,
  className 
}) => {
  const [showCancelModal, setShowCancelModal] = useState(false);
  const [actionLoading, setActionLoading] = useState('');

  const {
    id,
    email,
    role,
    invited_by,
    created_at,
    expires_at,
    status = 'pending',
    resent_count = 0,
    last_resent_at
  } = invitation;

  // Check if invitation is expired
  const isExpired = new Date(expires_at) < new Date();
  const daysUntilExpiry = Math.ceil((new Date(expires_at) - new Date()) / (1000 * 60 * 60 * 24));

  // Get role styling
  const getRoleVariant = (role) => {
    switch (role) {
      case 'owner': return 'warning';
      case 'admin': return 'info';
      case 'member': return 'secondary';
      default: return 'secondary';
    }
  };

  // Get status styling
  const getStatusInfo = (status, isExpired) => {
    if (isExpired) {
      return {
        variant: 'danger',
        label: 'Expired',
        icon: ExclamationTriangleIcon
      };
    }

    switch (status) {
      case 'pending':
        return {
          variant: 'warning',
          label: 'Pending',
          icon: ClockIcon
        };
      case 'accepted':
        return {
          variant: 'success',
          label: 'Accepted',
          icon: null
        };
      case 'declined':
        return {
          variant: 'danger',
          label: 'Declined',
          icon: null
        };
      default:
        return {
          variant: 'secondary',
          label: status,
          icon: null
        };
    }
  };

  const statusInfo = getStatusInfo(status, isExpired);

  // Handle resend invitation
  const handleResend = async () => {
    setActionLoading('resend');
    try {
      await onResendInvitation?.(id);
    } catch (error) {
      console.error('Failed to resend invitation:', error);
    } finally {
      setActionLoading('');
    }
  };

  // Handle cancel invitation
  const handleCancel = async () => {
    setActionLoading('cancel');
    try {
      await onCancelInvitation?.(id);
      setShowCancelModal(false);
    } catch (error) {
      console.error('Failed to cancel invitation:', error);
    } finally {
      setActionLoading('');
    }
  };

  // Get user initials for invited_by
  const getInitials = (firstName, lastName) => {
    return `${firstName?.charAt(0) || ''}${lastName?.charAt(0) || ''}`.toUpperCase();
  };

  return (
    <>
      <Card className={cn(
        "relative transition-all duration-200 hover:shadow-md",
        isExpired && "border-red-200 bg-red-50",
        className
      )}>
        <CardContent className="pt-6">
          <div className="flex items-start justify-between">
            {/* Invitation Info */}
            <div className="flex items-start space-x-4 flex-1">
              {/* Email Avatar */}
              <div className="w-12 h-12 bg-gray-100 rounded-full flex items-center justify-center">
                <span className="text-gray-600 font-medium text-sm">
                  {email.charAt(0).toUpperCase()}
                </span>
              </div>

              {/* Invitation Details */}
              <div className="flex-1 min-w-0">
                <div className="flex items-center space-x-2 mb-2">
                  <h4 className="text-lg font-semibold text-gray-900 truncate">
                    {email}
                  </h4>
                  <Badge variant={statusInfo.variant} className="text-xs">
                    {statusInfo.icon && <statusInfo.icon className="h-3 w-3 mr-1" />}
                    {statusInfo.label}
                  </Badge>
                </div>

                <div className="space-y-1">
                  <div className="flex items-center text-sm text-gray-600">
                    <span className="text-lg mr-2">
                      {role === 'owner' ? '👑' : role === 'admin' ? '🛡️' : '👤'}
                    </span>
                    <Badge variant={getRoleVariant(role)} className="text-xs mr-2">
                      {role.toUpperCase()}
                    </Badge>
                    <span>role</span>
                  </div>

                  <div className="text-sm text-gray-600">
                    Invited by{' '}
                    <span className="font-medium">
                      {invited_by.first_name} {invited_by.last_name}
                    </span>
                    {' '}• {formatTimeAgo(created_at)}
                  </div>

                  <div className="text-sm text-gray-600">
                    {isExpired ? (
                      <span className="text-red-600 font-medium">
                        Expired {formatTimeAgo(expires_at)}
                      </span>
                    ) : (
                      <span>
                        Expires in {daysUntilExpiry} day{daysUntilExpiry !== 1 ? 's' : ''} 
                        ({formatDate(expires_at)})
                      </span>
                    )}
                  </div>

                  {resent_count > 0 && (
                    <div className="text-xs text-gray-500">
                      Resent {resent_count} time{resent_count > 1 ? 's' : ''}
                      {last_resent_at && ` • Last resent ${formatTimeAgo(last_resent_at)}`}
                    </div>
                  )}
                </div>
              </div>
            </div>

            {/* Actions */}
            <div className="flex items-center space-x-2 ml-4">
              {(status === 'pending' && !isExpired) && (
                <Button
                  variant="secondary"
                  size="sm"
                  onClick={handleResend}
                  disabled={loading || actionLoading === 'resend'}
                  loading={actionLoading === 'resend'}
                >
                  <PaperAirplaneIcon className="h-4 w-4 mr-1" />
                  Resend
                </Button>
              )}

              <Button
                variant="danger"
                size="sm"
                onClick={() => setShowCancelModal(true)}
                disabled={loading || actionLoading === 'cancel'}
              >
                Cancel
              </Button>
            </div>
          </div>

          {/* Warning for expiring invitations */}
          {!isExpired && daysUntilExpiry <= 2 && (
            <div className="mt-3 p-2 bg-yellow-50 border border-yellow-200 rounded-md">
              <p className="text-xs text-yellow-800">
                ⚠️ This invitation expires in {daysUntilExpiry} day{daysUntilExpiry !== 1 ? 's' : ''}. 
                Consider resending if the user hasn't responded.
              </p>
            </div>
          )}

          {/* Expired invitation notice */}
          {isExpired && (
            <div className="mt-3 p-2 bg-red-50 border border-red-200 rounded-md">
              <p className="text-xs text-red-800">
                🚫 This invitation has expired. You'll need to send a new invitation.
              </p>
            </div>
          )}

          {/* Invitation link info */}
          {status === 'pending' && !isExpired && (
            <div className="mt-3 p-2 bg-blue-50 border border-blue-200 rounded-md">
              <p className="text-xs text-blue-800">
                📧 The user will receive an email with instructions to join your team.
              </p>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Cancel Confirmation Modal */}
      <ConfirmModal
        isOpen={showCancelModal}
        onClose={() => setShowCancelModal(false)}
        onConfirm={handleCancel}
        title="Cancel Invitation"
        message={`Are you sure you want to cancel the invitation for ${email}? They will no longer be able to join using this invitation link.`}
        confirmText="Cancel Invitation"
        cancelText="Keep Invitation"
        variant="warning"
        loading={actionLoading === 'cancel'}
      />
    </>
  );
};

export default InvitationCard;


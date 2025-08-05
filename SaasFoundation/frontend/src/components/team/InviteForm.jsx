// src/components/team/InviteForm.jsx
import React, { useState } from 'react';
import { 
  PaperAirplaneIcon,
  UserPlusIcon,
  InformationCircleIcon
} from '@heroicons/react/24/outline';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/Card';
import Button from '../ui/Button';
import Input from '../ui/Input';
import Textarea from '../ui/Textarea';
import { Alert, AlertDescription } from '../ui/Alert';
import RoleSelect from './RoleSelect';
import { validateEmail } from '../../utils/validators';
import { cn } from '../../utils/helpers';

const InviteForm = ({ 
  onInviteUser, 
  currentUserRole, 
  loading = false,
  className,
  organizationName 
}) => {
  const [formData, setFormData] = useState({
    email: '',
    role: 'member',
    message: '',
    send_welcome_email: true
  });
  const [errors, setErrors] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Handle form input changes
  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));

    // Clear error when user starts typing
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
  };

  // Validate form
  const validateForm = () => {
    const newErrors = {};

    // Email validation
    if (!formData.email.trim()) {
      newErrors.email = 'Email address is required';
    } else if (!validateEmail(formData.email)) {
      newErrors.email = 'Please enter a valid email address';
    }

    // Role validation
    if (!formData.role) {
      newErrors.role = 'Please select a role';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log('Sending team invitation:',formData.email);
    if (!validateForm()) return;

    setIsSubmitting(true);
    try {
      await onInviteUser?.(formData);
      
      // Reset form on success
      setFormData({
        email: '',
        role: 'member',
        message: '',
        send_welcome_email: true
      });
      setErrors({});
    } catch (error) {
      console.error('Failed to send invitation:', error);
    } finally {
      setIsSubmitting(false);
    }
  };

  // Get role permissions description
  const getRoleDescription = (role) => {
    switch (role) {
      case 'owner':
        return 'Full access to all features including billing, team management, and organization settings. Can transfer ownership and delete the organization.';
      case 'admin':
        return 'Can manage team members, organization settings, and access most features. Cannot manage billing or delete the organization.';
      case 'member':
        return 'Can access and use the platform features within plan limits. Cannot manage team members or organization settings.';
      default:
        return '';
    }
  };

  return (
    <div className={cn("grid grid-cols-1 lg:grid-cols-2 gap-8", className)}>
      {/* Invite Form */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <UserPlusIcon className="h-5 w-5 mr-2" />
            Invite Team Member
          </CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Email Input */}
            <div className="space-y-2">
              <label htmlFor="email" className="text-sm font-medium text-gray-700">
                Email Address *
              </label>
              <Input
                type="email"
                id="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                placeholder="colleague@yourpractice.com"
                className={errors.email ? 'border-red-300 focus:border-red-500 focus:ring-red-500' : ''}
                disabled={isSubmitting || loading}
              />
              {errors.email && (
                <p className="text-sm text-red-600">{errors.email}</p>
              )}
            </div>

            {/* Role Selection */}
            <div className="space-y-2">
              <label htmlFor="role" className="text-sm font-medium text-gray-700">
                Role *
              </label>
              <RoleSelect
                value={formData.role}
                onChange={(e) => handleChange({ target: { name: 'role', value: e.target.value } })}
                currentUserRole={currentUserRole}
                disabled={isSubmitting || loading}
                includeDescriptions={false}
              />
              {errors.role && (
                <p className="text-sm text-red-600">{errors.role}</p>
              )}
              
              {/* Role Description */}
              {formData.role && (
                <div className="p-3 bg-blue-50 border border-blue-200 rounded-md">
                  <p className="text-sm text-blue-800">
                    <strong>{formData.role.charAt(0).toUpperCase() + formData.role.slice(1)}:</strong>{' '}
                    {getRoleDescription(formData.role)}
                  </p>
                </div>
              )}
            </div>

            {/* Personal Message */}
            <div className="space-y-2">
              <label htmlFor="message" className="text-sm font-medium text-gray-700">
                Personal Message (Optional)
              </label>
              <Textarea
                id="message"
                name="message"
                value={formData.message}
                onChange={handleChange}
                placeholder={`Hi! I'd like to invite you to join our team at ${organizationName || 'our organization'}. Looking forward to working together!`}
                rows={3}
                disabled={isSubmitting || loading}
              />
              <p className="text-xs text-gray-500">
                This message will be included in the invitation email
              </p>
            </div>

            {/* Send Welcome Email */}
            <div className="flex items-center space-x-2">
              <input
                type="checkbox"
                id="send_welcome_email"
                name="send_welcome_email"
                checked={formData.send_welcome_email}
                onChange={handleChange}
                className="h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                disabled={isSubmitting || loading}
              />
              <label htmlFor="send_welcome_email" className="text-sm text-gray-700">
                Send welcome email with getting started guide
              </label>
            </div>

            {/* Submit Button */}
            <Button
              type="submit"
              disabled={isSubmitting || loading}
              loading={isSubmitting}
              className="w-full"
            >
              <PaperAirplaneIcon className="h-4 w-4 mr-2" />
              Invite
            </Button>
          </form>
        </CardContent>
      </Card>

      {/* Information Panel */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <InformationCircleIcon className="h-5 w-5 mr-2" />
            Invitation Details
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-6">
          {/* Role Permissions */}
          <div>
            <h4 className="font-medium text-gray-900 mb-3">Role Permissions</h4>
            <div className="space-y-3">
              <div className="p-3 bg-gray-50 rounded-md">
                <div className="flex items-center space-x-2 mb-1">
                  <span className="text-lg">👤</span>
                  <h5 className="font-medium text-gray-900">Member</h5>
                </div>
                <ul className="text-sm text-gray-600 space-y-1">
                  <li>• Access platform features</li>
                  <li>• View team information</li>
                  <li>• Use within plan limits</li>
                </ul>
              </div>

              <div className="p-3 bg-blue-50 rounded-md">
                <div className="flex items-center space-x-2 mb-1">
                  <span className="text-lg">🛡️</span>
                  <h5 className="font-medium text-gray-900">Admin</h5>
                </div>
                <ul className="text-sm text-gray-600 space-y-1">
                  <li>• All member permissions</li>
                  <li>• Manage team members</li>
                  <li>• Organization settings</li>
                  <li>• View billing information</li>
                </ul>
              </div>

              {currentUserRole === 'owner' && (
                <div className="p-3 bg-yellow-50 rounded-md">
                  <div className="flex items-center space-x-2 mb-1">
                    <span className="text-lg">👑</span>
                    <h5 className="font-medium text-gray-900">Owner</h5>
                  </div>
                  <ul className="text-sm text-gray-600 space-y-1">
                    <li>• All admin permissions</li>
                    <li>• Manage subscription & billing</li>
                    <li>• Transfer ownership</li>
                    <li>• Delete organization</li>
                  </ul>
                </div>
              )}
            </div>
          </div>

          {/* Invitation Process */}
          <div>
            <h4 className="font-medium text-gray-900 mb-3">What happens next?</h4>
            <div className="space-y-2 text-sm text-gray-600">
              <div className="flex items-start space-x-2">
                <span className="flex-shrink-0 w-5 h-5 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center text-xs font-medium">1</span>
                <p>Invitation email is sent to the recipient</p>
              </div>
              <div className="flex items-start space-x-2">
                <span className="flex-shrink-0 w-5 h-5 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center text-xs font-medium">2</span>
                <p>They click the invitation link to join</p>
              </div>
              <div className="flex items-start space-x-2">
                <span className="flex-shrink-0 w-5 h-5 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center text-xs font-medium">3</span>
                <p>Account is created or linked to existing account</p>
              </div>
              <div className="flex items-start space-x-2">
                <span className="flex-shrink-0 w-5 h-5 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center text-xs font-medium">4</span>
                <p>They gain access with the assigned role</p>
              </div>
            </div>
          </div>

          {/* Important Notes */}
          <Alert>
            <InformationCircleIcon className="h-4 w-4" />
            <AlertDescription>
              <strong>Important:</strong> Invitations expire after 7 days. 
              You can resend expired invitations from the team management page.
            </AlertDescription>
          </Alert>
        </CardContent>
      </Card>
    </div>
  );
};

export default InviteForm;

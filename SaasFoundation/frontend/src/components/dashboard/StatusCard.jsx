// src/components/dashboard/StatusCard.jsx
import React from 'react';
import DashboardCard from './DashboardCard';
import Badge from '../ui/Badge';
import { formatDate } from '../../utils/formatters';

const StatusCard = ({ user }) => {
  return (
    <DashboardCard title="Account Status">
      <div className="space-y-4">
        <div className="flex justify-between items-center">
          <span className="text-sm font-medium text-gray-700">Email:</span>
          <span className="text-sm text-gray-900">{user.email}</span>
        </div>
        
        <div className="flex justify-between items-center">
          <span className="text-sm font-medium text-gray-700">Verification:</span>
          <Badge variant={user.is_verified ? 'verified' : 'unverified'}>
            {user.is_verified ? 'Verified' : 'Unverified'}
          </Badge>
        </div>
        
        <div className="flex justify-between items-center">
          <span className="text-sm font-medium text-gray-700">Member since:</span>
          <span className="text-sm text-gray-900">{formatDate(user.created_at)}</span>
        </div>
        
        {!user.is_verified && (
          <div className="mt-4 p-3 bg-yellow-50 border border-yellow-200 rounded-md">
            <p className="text-sm text-yellow-800 font-medium">⚠️ Please verify your email address</p>
            <p className="text-sm text-yellow-700 mt-1">Check your inbox for the verification email.</p>
          </div>
        )}
      </div>
    </DashboardCard>
  );
};

export default StatusCard;

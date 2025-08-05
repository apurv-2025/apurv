// src/components/auth/PublicRoute.jsx
import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';
import LoadingState from '../common/LoadingState';

const PublicRoute = ({ children }) => {
  const { user, loading } = useAuth();
  
  if (loading) {
    return <LoadingState />;
  }
  
  return user ? <Navigate to="/dashboard" /> : children;
};

export default PublicRoute;

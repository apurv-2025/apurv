import React, { createContext, useContext, useState, useEffect } from 'react';
import { authService } from '../services/auth';

const AuthContext = createContext({});

export const useAuthContext = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuthContext must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [initialized, setInitialized] = useState(false);

  // Initialize authentication on app load
  useEffect(() => {
    initializeAuth();
  }, []);

  const initializeAuth = async () => {
    try {
      setLoading(true);
      
      // Initialize the auth service
      await authService.initialize();
      
      // Check if user is authenticated
      const authStatus = await authService.checkAuthStatus();
      
      if (authStatus.authenticated) {
        setUser(authStatus.user);
      }
    } catch (error) {
      console.error('Auth initialization error:', error);
      // Clear any invalid tokens
      authService.clearTokens();
      authService.clearUser();
    } finally {
      setLoading(false);
      setInitialized(true);
    }
  };

  const login = async (credentials) => {
    try {
      setLoading(true);
      const result = await authService.login(credentials);
      
      console.log('API Result:', result);
      if (result.success) {
        setUser(result.data.user);
        return result;
      }
      
      throw new Error(result.message || 'Login failed');
    } catch (error) {
      console.error('Login error:', error);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const register = async (userData) => {
    try {
      setLoading(true);
      const result = await authService.register(userData);
      
      if (result.success) {
        // If registration includes auto-login
        if (result.data.user) {
          setUser(result.data.user);
        }
        return result;
      }
      
      throw new Error(result.message || 'Registration failed');
    } catch (error) {
      console.error('Registration error:', error);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const logout = async () => {
    try {
      setLoading(true);
      await authService.logout();
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      setUser(null);
      setLoading(false);
    }
  };

  const updateProfile = async (profileData) => {
    try {
      const result = await authService.updateProfile(profileData);
      
      if (result.success) {
        setUser(result.data);
        return result;
      }
      
      throw new Error(result.message || 'Profile update failed');
    } catch (error) {
      console.error('Profile update error:', error);
      throw error;
    }
  };

  const changePassword = async (currentPassword, newPassword) => {
    try {
      const result = await authService.changePassword(currentPassword, newPassword);
      
      if (result.success) {
        return result;
      }
      
      throw new Error(result.message || 'Password change failed');
    } catch (error) {
      console.error('Password change error:', error);
      throw error;
    }
  };

  const verifyEmail = async (token) => {
    try {
      const result = await authService.verifyEmail(token);
      
      if (result.success && result.data.user) {
        setUser(result.data.user);
      }
      
      return result;
    } catch (error) {
      console.error('Email verification error:', error);
      throw error;
    }
  };

  const resendVerificationEmail = async (email) => {
    try {
      const result = await authService.resendVerificationEmail(email);
      return result;
    } catch (error) {
      console.error('Resend verification error:', error);
      throw error;
    }
  };

  const forgotPassword = async (email) => {
    try {
      const result = await authService.forgotPassword(email);
      return result;
    } catch (error) {
      console.error('Forgot password error:', error);
      throw error;
    }
  };

  const resetPassword = async (token, newPassword) => {
    try {
      const result = await authService.resetPassword(token, newPassword);
      return result;
    } catch (error) {
      console.error('Reset password error:', error);
      throw error;
    }
  };

  const acceptInvitation = async (invitationData) => {
    try {
      const result = await authService.acceptInvitation?.(invitationData);
      return result;
    } catch (error) {
      console.error('Accept invitation error:', error);
      throw error;
    }
  };

  // Utility functions
  const isAuthenticated = () => {
    return !!user && authService.isAuthenticated();
  };

  const hasPermission = (permission) => {
    return authService.hasPermission(permission);
  };

  const getUserPermissions = () => {
    return authService.getUserPermissions();
  };

  const isEmailVerified = () => {
    return user?.emailVerified || false;
  };

  const getUser = () => {
    return user;
  };

  const refreshUser = async () => {
    try {
      const result = await authService.getProfile();
      if (result.success) {
        setUser(result.data);
        return result.data;
      }
    } catch (error) {
      console.error('Refresh user error:', error);
      throw error;
    }
  };

  const value = {
    // State
    user,
    loading,
    initialized,
    
    // Authentication methods
    login,
    register,
    logout,
    
    // Profile management
    updateProfile,
    changePassword,
    refreshUser,
    
    // Email verification
    verifyEmail,
    resendVerificationEmail,
    
    // Password reset
    forgotPassword,
    resetPassword,
    
    // Invitations
    acceptInvitation,
    
    // Utility functions
    isAuthenticated,
    hasPermission,
    getUserPermissions,
    isEmailVerified,
    getUser
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthContext;

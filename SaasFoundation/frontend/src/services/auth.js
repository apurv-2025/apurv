import { api } from './api';
import {API_ENDPOINTS} from '../utils/constants'

// Token management
const TOKEN_KEY = 'auth_token';
const REFRESH_TOKEN_KEY = 'refresh_token';
const USER_KEY = 'user_data';

class AuthService {
  constructor() {
    this.token = localStorage.getItem(TOKEN_KEY);
    this.refreshToken = localStorage.getItem(REFRESH_TOKEN_KEY);
    this.user = this.getStoredUser();
  }

  // ===== TOKEN MANAGEMENT =====
  
  setTokens(token, refreshToken) {
    this.token = token;
    this.refreshToken = refreshToken;
    localStorage.setItem(TOKEN_KEY, token);
    localStorage.setItem(REFRESH_TOKEN_KEY, refreshToken);
    api.setAuthToken(token);
  }

  clearTokens() {
    this.token = null;
    this.refreshToken = null;
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(REFRESH_TOKEN_KEY);
    localStorage.removeItem(USER_KEY);
    api.clearAuthToken();
  }

  getToken() {
    return this.token || localStorage.getItem(TOKEN_KEY);
  }

  getRefreshToken() {
    return this.refreshToken || localStorage.getItem(REFRESH_TOKEN_KEY);
  }

  isAuthenticated() {
    return !!this.getToken();
  }

  // ===== USER DATA MANAGEMENT =====

  setUser(userData) {
    this.user = userData;
    localStorage.setItem(USER_KEY, JSON.stringify(userData));
  }

  getUser() {
    return this.user;
  }

  getStoredUser() {
    try {
      const storedUser = localStorage.getItem(USER_KEY);
      return storedUser ? JSON.parse(storedUser) : null;
    } catch (error) {
      console.error('Error parsing stored user data:', error);
      return null;
    }
  }

  clearUser() {
    this.user = null;
    localStorage.removeItem(USER_KEY);
  }

  // ===== AUTHENTICATION METHODS =====

  /////////////////////////////////////////////////////////
  //
  //Login  
  //
  //
  /////////////////////////////////////////////////////////
  async login(credentials) {
    try {
      const response = await api.post(API_ENDPOINTS.AUTH.LOGIN, credentials);
      
      if (response.success) {
        const { access_token, user } = response.data;
        this.setTokens(access_token, access_token);
        this.setUser(user);
        console.log('Access Token:', access_token);
        console.log('User:', user);     
        return {
          success: true,
          data: { user, access_token },
          message: 'Login successful'
        };
      }
      
      throw new Error(response.message || 'Login failed');
    } catch (error) {
      console.error('Login error:', error);
      throw new Error(error.message || 'Login failed');
    }
  }

  /////////////////////////////////////////////////////////
  //
  //Register  
  //
  //
  /////////////////////////////////////////////////////////
  async register(userData) {
    try {
      const response = await api.post(API_ENDPOINTS.AUTH.REGISTER, userData);
      
      if (response.success) {
        // Some apps auto-login after registration, others require email verification
        if (response.data.token) {
          const { token, refreshToken, user } = response.data;
          this.setTokens(token, refreshToken);
          this.setUser(user);
        }


        return {
          success: true,
          data: response.data,
          message: response.message || 'Registration successful'
        };
      }
      
      throw new Error(response.message || 'Registration failed');
    } catch (error) {
      console.error('Registration error:', error);
      throw new Error(error.message || 'Registration failed');
    }
  }

  /////////////////////////////////////////////////////////
  //
  //Logout Implementation
  //
  //
  /////////////////////////////////////////////////////////
  async logout() {
    try {

      // Call logout endpoint to invalidate server-side session
      if (this.getToken()) {

        await api.post(API_ENDPOINTS.AUTH.LOGOUT, {
          refreshToken: this.getRefreshToken()
        });
      }
    } catch (error) {
      console.error('Logout API error:', error);
      // Continue with client-side logout even if server call fails
    } finally {
      this.clearTokens();
      this.clearUser();
    }
  }
  /////////////////////////////////////////////////////////
  //
  //Refresh Token
  //
  //
  /////////////////////////////////////////////////////////
  async refreshAccessToken() {
    try {
      const refreshToken = this.getRefreshToken();
      if (!refreshToken) {
        throw new Error('No refresh token available');
      }

      const response = await api.post(API_ENDPOINTS.AUTH.REFRESH, { refreshToken });
      
      if (response.success) {
        const { token, refreshToken: newRefreshToken } = response.data;
        this.setTokens(token, newRefreshToken || refreshToken);
        return token;
      }
      
      throw new Error('Token refresh failed');
    } catch (error) {
      console.error('Token refresh error:', error);
      this.clearTokens();
      this.clearUser();
      throw error;
    }
  }

  // ===== EMAIL VERIFICATION =====

  async verifyEmail(token) {
    try {
      const response = await api.post(API_ENDPOINTS.AUTH.VERIFY_EMAIL, { token });
      
      if (response.success) {
        // Update user data if verification changes user status
        if (response.data.user) {
          this.setUser(response.data.user);
        }
        
        return {
          success: true,
          data: response.data,
          message: 'Email verified successfully'
        };
      }
      
      throw new Error(response.message || 'Email verification failed');
    } catch (error) {
      console.error('Email verification error:', error);
      throw new Error(error.message || 'Email verification failed');
    }
  }

  async resendVerificationEmail(email) {
    try {
      const response = await api.post(API_ENDPOINTS.AUTH.RESEND_VERIFICATION, { email });
      
      if (response.success) {
        return {
          success: true,
          message: 'Verification email sent successfully'
        };
      }
      
      throw new Error(response.message || 'Failed to send verification email');
    } catch (error) {
      console.error('Resend verification error:', error);
      throw new Error(error.message || 'Failed to send verification email');
    }
  }

  // ===== PASSWORD MANAGEMENT =====

  async forgotPassword(email) {
    try {
      const response = await api.post(API_ENDPOINTS.AUTH.FORGOT_PASSWORD, { email });
      
      if (response.success) {
        return {
          success: true,
          message: 'Password reset email sent successfully'
        };
      }
      
      throw new Error(response.message || 'Failed to send password reset email');
    } catch (error) {
      console.error('Forgot password error:', error);
      throw new Error(error.message || 'Failed to send password reset email');
    }
  }

  async resetPassword(token, newPassword) {
    try {
      const response = await api.post(API_ENDPOINTS.AUTH.RESET_PASSWORD, {
        token,
        password: newPassword
      });
      
      if (response.success) {
        return {
          success: true,
          message: 'Password reset successfully'
        };
      }
      
      throw new Error(response.message || 'Password reset failed');
    } catch (error) {
      console.error('Reset password error:', error);
      throw new Error(error.message || 'Password reset failed');
    }
  }

  async changePassword(currentPassword, newPassword) {
    try {
      const response = await api.put(API_ENDPOINTS.AUTH.CHANGE_PASSWORD, {
        currentPassword,
        newPassword
      });
      
      if (response.success) {
        return {
          success: true,
          message: 'Password changed successfully'
        };
      }
      
      throw new Error(response.message || 'Password change failed');
    } catch (error) {
      console.error('Change password error:', error);
      throw new Error(error.message || 'Password change failed');
    }
  }

  // ===== PROFILE MANAGEMENT =====

  async getProfile() {
    try {
      const response = await api.get(API_ENDPOINTS.USER.PROFILE);
      
      if (response.success) {
        this.setUser(response.data.user);
        return {
          success: true,
          data: response.data.user
        };
      }
      
      throw new Error(response.message || 'Failed to fetch profile');
    } catch (error) {
      console.error('Get profile error:', error);
      throw new Error(error.message || 'Failed to fetch profile');
    }
  }

  async updateProfile(profileData) {
    try {
      const response = await api.put(API_ENDPOINTS.USER.PROFILE, profileData);
      
      if (response.success) {
        const updatedUser = { ...this.user, ...response.data.user };
        this.setUser(updatedUser);
        
        return {
          success: true,
          data: updatedUser,
          message: 'Profile updated successfully'
        };
      }
      
      throw new Error(response.message || 'Profile update failed');
    } catch (error) {
      console.error('Update profile error:', error);
      throw new Error(error.message || 'Profile update failed');
    }
  }

  async deleteAccount(password) {
    try {
      const response = await api.delete(API_ENDPOINTS.AUTH.DELETE_ACCOUNT, {
        data: { password }
      });
      
      if (response.success) {
        this.clearTokens();
        this.clearUser();
        
        return {
          success: true,
          message: 'Account deleted successfully'
        };
      }
      
      throw new Error(response.message || 'Account deletion failed');
    } catch (error) {
      console.error('Delete account error:', error);
      throw new Error(error.message || 'Account deletion failed');
    }
  }

  // ===== TWO-FACTOR AUTHENTICATION =====

  async enable2FA() {
    try {
      const response = await api.post(API_ENDPOINTS.AUTH.ENABLE_2FA);
      
      if (response.success) {
        return {
          success: true,
          data: response.data, // Should include QR code and backup codes
          message: '2FA setup initiated'
        };
      }
      
      throw new Error(response.message || '2FA setup failed');
    } catch (error) {
      console.error('Enable 2FA error:', error);
      throw new Error(error.message || '2FA setup failed');
    }
  }

  async disable2FA(verificationCode) {
    try {
      const response = await api.post(API_ENDPOINTS.AUTH.DISABLE_2FA, {
        code: verificationCode
      });
      
      if (response.success) {
        // Update user data to reflect 2FA status
        const updatedUser = { ...this.user, twoFactorEnabled: false };
        this.setUser(updatedUser);
        
        return {
          success: true,
          message: '2FA disabled successfully'
        };
      }
      
      throw new Error(response.message || '2FA disable failed');
    } catch (error) {
      console.error('Disable 2FA error:', error);
      throw new Error(error.message || '2FA disable failed');
    }
  }

  async verify2FA(code) {
    try {
      const response = await api.post(API_ENDPOINTS.AUTH.VERIFY_2FA, { code });
      
      if (response.success) {
        // Update user data to reflect 2FA status
        const updatedUser = { ...this.user, twoFactorEnabled: true };
        this.setUser(updatedUser);
        
        return {
          success: true,
          data: response.data,
          message: '2FA verified successfully'
        };
      }
      
      throw new Error(response.message || '2FA verification failed');
    } catch (error) {
      console.error('Verify 2FA error:', error);
      throw new Error(error.message || '2FA verification failed');
    }
  }

  // ===== UTILITY METHODS =====

  async checkAuthStatus() {
    try {
      if (!this.isAuthenticated()) {
        return { authenticated: false };
      }

      const profile = await this.getProfile();
      return {
        authenticated: true,
        user: profile.data
      };
    } catch (error) {
      console.error('Auth status check failed:', error);
      this.clearTokens();
      this.clearUser();
      return { authenticated: false };
    }
  }

  // Initialize auth service
  async initialize() {
    const token = this.getToken();
    if (token) {
      api.setAuthToken(token);
      try {
        await this.checkAuthStatus();
      } catch (error) {
        console.error('Auth initialization failed:', error);
        this.clearTokens();
        this.clearUser();
      }
    }
  }

  // Get user permissions/roles
  getUserPermissions() {
    if (!this.user) return [];
    
    const rolePermissions = {
      owner: ['manage_team', 'manage_billing', 'manage_settings', 'view_analytics'],
      admin: ['manage_team', 'manage_settings', 'view_analytics'],
      member: ['view_analytics'],
      viewer: []
    };
    
    return rolePermissions[this.user.role] || [];
  }

  hasPermission(permission) {
    return this.getUserPermissions().includes(permission);
  }
}

// Create and export singleton instance
export const authService = new AuthService();

// Export the class for testing
export { AuthService };

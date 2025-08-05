import { useState, useEffect, useCallback } from 'react';
import { subscriptionService } from '../services/subscription';
import { useAuth } from './useAuth';

export const useSubscription = () => {
  const { user, isAuthenticated } = useAuth();
  const [subscription, setSubscription] = useState(null);
  const [usage, setUsage] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Fetch current subscription
  const fetchSubscription = useCallback(async () => {
    if (!isAuthenticated()) return;
    
    try {
      setLoading(true);
      setError(null);
      
      const result = await subscriptionService.getCurrentSubscription();
      setSubscription(result.data);
    } catch (err) {
      setError(err.message || 'Failed to fetch subscription');
      console.error('Subscription fetch error:', err);
    } finally {
      setLoading(false);
    }
  }, [isAuthenticated]);

  // Fetch current usage
  const fetchUsage = useCallback(async () => {
    if (!isAuthenticated()) return;
    
    try {
      const result = await subscriptionService.getCurrentUsage();
      
      // Transform usage data for dashboard display
      const transformedUsage = {};
      if (result.data) {
        Object.entries(result.data).forEach(([key, value]) => {
          if (typeof value === 'object' && value.used !== undefined) {
            transformedUsage[key] = value;
          } else {
            // Handle simple number values
            transformedUsage[key] = {
              used: value,
              limit: subscription?.limits?.[key] || -1,
              percentage: subscription?.limits?.[key] > 0 
                ? Math.min(100, (value / subscription.limits[key]) * 100)
                : 0
            };
          }
        });
      }
      
      setUsage(transformedUsage);
    } catch (err) {
      console.error('Usage fetch error:', err);
      // Don't set error for usage as it's not critical
    }
  }, [isAuthenticated, subscription]);

  // Subscribe to a plan
  const subscribe = useCallback(async (planData) => {
    try {
      setError(null);
      const result = await subscriptionService.subscribe(planData);
      setSubscription(result.data.subscription);
      return result;
    } catch (err) {
      setError(err.message || 'Subscription failed');
      throw err;
    }
  }, []);

  // Update subscription plan
  const updatePlan = useCallback(async (planData) => {
    try {
      setError(null);
      const result = await subscriptionService.updatePlan(planData);
      setSubscription(result.data.subscription);
      return result;
    } catch (err) {
      setError(err.message || 'Plan update failed');
      throw err;
    }
  }, []);

  // Cancel subscription
  const cancelSubscription = useCallback(async (cancellationData) => {
    try {
      setError(null);
      const result = await subscriptionService.cancelSubscription(cancellationData);
      setSubscription(result.data.subscription);
      return result;
    } catch (err) {
      setError(err.message || 'Cancellation failed');
      throw err;
    }
  }, []);

  // Resume subscription
  const resumeSubscription = useCallback(async () => {
    try {
      setError(null);
      const result = await subscriptionService.resumeSubscription();
      setSubscription(result.data.subscription);
      return result;
    } catch (err) {
      setError(err.message || 'Resume failed');
      throw err;
    }
  }, []);

  // Get available plans
  const getPlans = useCallback(async () => {
    try {
      const result = await subscriptionService.getAvailablePlans();
      return result.data;
    } catch (err) {
      throw new Error(err.message || 'Failed to fetch plans');
    }
  }, []);

  // Get billing information
  const getBillingInfo = useCallback(async () => {
    try {
      const result = await subscriptionService.getBillingInfo();
      return result.data;
    } catch (err) {
      throw new Error(err.message || 'Failed to fetch billing info');
    }
  }, []);

  // Get invoices
  const getInvoices = useCallback(async (params) => {
    try {
      const result = await subscriptionService.getInvoices(params);
      return result.data;
    } catch (err) {
      throw new Error(err.message || 'Failed to fetch invoices');
    }
  }, []);

  // Initialize data when user logs in
  useEffect(() => {
    if (user && isAuthenticated()) {
      fetchSubscription();
    } else {
      setSubscription(null);
      setUsage(null);
    }
  }, [user, isAuthenticated, fetchSubscription]);

  // Fetch usage when subscription changes
  useEffect(() => {
    if (subscription) {
      fetchUsage();
    }
  }, [subscription, fetchUsage]);

  // Utility functions
  const isActive = useCallback(() => {
    return subscriptionService.isSubscriptionActive();
  }, []);

  const isTrialing = useCallback(() => {
    return subscriptionService.isInTrial();
  }, []);

  const isCancelled = useCallback(() => {
    return subscriptionService.isCancelled();
  }, []);

  const getTrialDaysRemaining = useCallback(() => {
    return subscriptionService.getTrialDaysRemaining();
  }, []);

  const getUsagePercentage = useCallback((metricName) => {
    return subscriptionService.getUsagePercentage(metricName);
  }, []);

  const isUsageLimitExceeded = useCallback((metricName) => {
    return subscriptionService.isUsageLimitExceeded(metricName);
  }, []);

  const clearError = useCallback(() => {
    setError(null);
  }, []);

  const refreshSubscription = useCallback(() => {
    return fetchSubscription();
  }, [fetchSubscription]);

  const refreshUsage = useCallback(() => {
    return fetchUsage();
  }, [fetchUsage]);

  return {
    // State
    subscription,
    usage,
    loading,
    error,
    
    // Data fetching
    fetchSubscription,
    fetchUsage,
    refreshSubscription,
    refreshUsage,
    
    // Subscription management
    subscribe,
    updatePlan,
    cancelSubscription,
    resumeSubscription,
    
    // Data fetching methods
    getPlans,
    getBillingInfo,
    getInvoices,
    
    // Utility functions
    isActive,
    isTrialing,
    isCancelled,
    getTrialDaysRemaining,
    getUsagePercentage,
    isUsageLimitExceeded,
    clearError,
    
    // Computed values
    isSubscriptionActive: isActive(),
    isInTrial: isTrialing(),
    trialDaysRemaining: getTrialDaysRemaining()
  };
};

import { api } from './api';

const SUBSCRIPTION_ENDPOINTS = {
  // Plans
  PLANS: '/subscription/plans',
  CURRENT_PLAN: '/subscription/current',
  
  // Subscription management
  SUBSCRIBE: '/subscription/subscribe',
  UPDATE_PLAN: '/subscription/update-plan',
  CANCEL: '/subscription/cancel',
  PAUSE: '/subscription/pause',
  RESUME: '/subscription/resume',
  
  // Billing
  BILLING_INFO: '/subscription/billing',
  PAYMENT_METHODS: '/subscription/payment-methods',
  DEFAULT_PAYMENT_METHOD: '/subscription/payment-methods/default',
  
  // Usage and metrics
  USAGE: '/subscription/usage',
  USAGE_HISTORY: '/subscription/usage/history',
  METRICS: '/subscription/metrics',
  
  // Invoices
  INVOICES: '/subscription/invoices',
  INVOICE_DOWNLOAD: '/subscription/invoices/:id/download',
  
  // Billing portal
  PORTAL_SESSION: '/subscription/portal-session',
  
  // Webhooks
  WEBHOOK_VERIFY: '/subscription/webhook/verify'
};

class SubscriptionService {
  constructor() {
    this.currentSubscription = null;
    this.usage = null;
  }

  // ===== PLAN MANAGEMENT =====

  async getAvailablePlans() {
    try {
      const response = await api.get(SUBSCRIPTION_ENDPOINTS.PLANS);
      
      if (response.success) {
        return {
          success: true,
          data: response.data.plans || [],
          message: 'Plans fetched successfully'
        };
      }
      
      throw new Error(response.message || 'Failed to fetch plans');
    } catch (error) {
      console.error('Get plans error:', error);
      throw new Error(error.message || 'Failed to fetch available plans');
    }
  }

  async getCurrentSubscription() {
    try {
      const response = await api.get(SUBSCRIPTION_ENDPOINTS.CURRENT_PLAN);
      
      if (response.success) {
        this.currentSubscription = response.data.subscription;
        return {
          success: true,
          data: response.data.subscription,
          message: 'Current subscription fetched successfully'
        };
      }
      
      throw new Error(response.message || 'Failed to fetch current subscription');
    } catch (error) {
      console.error('Get current subscription error:', error);
      throw new Error(error.message || 'Failed to fetch current subscription');
    }
  }

  // ===== SUBSCRIPTION LIFECYCLE =====

  async subscribe(planData) {
    try {
      const response = await api.post(SUBSCRIPTION_ENDPOINTS.SUBSCRIBE, planData);
      
      if (response.success) {
        this.currentSubscription = response.data.subscription;
        return {
          success: true,
          data: response.data,
          message: 'Subscription created successfully'
        };
      }
      
      throw new Error(response.message || 'Subscription failed');
    } catch (error) {
      console.error('Subscribe error:', error);
      throw new Error(error.message || 'Failed to create subscription');
    }
  }

  async updatePlan(planUpdateData) {
    try {
      const response = await api.put(SUBSCRIPTION_ENDPOINTS.UPDATE_PLAN, planUpdateData);
      
      if (response.success) {
        this.currentSubscription = response.data.subscription;
        return {
          success: true,
          data: response.data,
          message: 'Plan updated successfully'
        };
      }
      
      throw new Error(response.message || 'Plan update failed');
    } catch (error) {
      console.error('Update plan error:', error);
      throw new Error(error.message || 'Failed to update plan');
    }
  }

  async cancelSubscription(cancellationData = {}) {
    try {
      const response = await api.post(SUBSCRIPTION_ENDPOINTS.CANCEL, {
        reason: cancellationData.reason,
        feedback: cancellationData.feedback,
        cancelAtPeriodEnd: cancellationData.cancelAtPeriodEnd || true
      });
      
      if (response.success) {
        this.currentSubscription = response.data.subscription;
        return {
          success: true,
          data: response.data,
          message: 'Subscription cancelled successfully'
        };
      }
      
      throw new Error(response.message || 'Cancellation failed');
    } catch (error) {
      console.error('Cancel subscription error:', error);
      throw new Error(error.message || 'Failed to cancel subscription');
    }
  }

  async pauseSubscription(pauseData = {}) {
    try {
      const response = await api.post(SUBSCRIPTION_ENDPOINTS.PAUSE, pauseData);
      
      if (response.success) {
        this.currentSubscription = response.data.subscription;
        return {
          success: true,
          data: response.data,
          message: 'Subscription paused successfully'
        };
      }
      
      throw new Error(response.message || 'Pause failed');
    } catch (error) {
      console.error('Pause subscription error:', error);
      throw new Error(error.message || 'Failed to pause subscription');
    }
  }

  async resumeSubscription() {
    try {
      const response = await api.post(SUBSCRIPTION_ENDPOINTS.RESUME);
      
      if (response.success) {
        this.currentSubscription = response.data.subscription;
        return {
          success: true,
          data: response.data,
          message: 'Subscription resumed successfully'
        };
      }
      
      throw new Error(response.message || 'Resume failed');
    } catch (error) {
      console.error('Resume subscription error:', error);
      throw new Error(error.message || 'Failed to resume subscription');
    }
  }

  // ===== BILLING MANAGEMENT =====

  async getBillingInfo() {
    try {
      const response = await api.get(SUBSCRIPTION_ENDPOINTS.BILLING_INFO);
      
      if (response.success) {
        return {
          success: true,
          data: response.data,
          message: 'Billing information fetched successfully'
        };
      }
      
      throw new Error(response.message || 'Failed to fetch billing info');
    } catch (error) {
      console.error('Get billing info error:', error);
      throw new Error(error.message || 'Failed to fetch billing information');
    }
  }

  async updateBillingInfo(billingData) {
    try {
      const response = await api.put(SUBSCRIPTION_ENDPOINTS.BILLING_INFO, billingData);
      
      if (response.success) {
        return {
          success: true,
          data: response.data,
          message: 'Billing information updated successfully'
        };
      }
      
      throw new Error(response.message || 'Billing update failed');
    } catch (error) {
      console.error('Update billing info error:', error);
      throw new Error(error.message || 'Failed to update billing information');
    }
  }

  async getPaymentMethods() {
    try {
      const response = await api.get(SUBSCRIPTION_ENDPOINTS.PAYMENT_METHODS);
      
      if (response.success) {
        return {
          success: true,
          data: response.data.paymentMethods || [],
          message: 'Payment methods fetched successfully'
        };
      }
      
      throw new Error(response.message || 'Failed to fetch payment methods');
    } catch (error) {
      console.error('Get payment methods error:', error);
      throw new Error(error.message || 'Failed to fetch payment methods');
    }
  }

  async addPaymentMethod(paymentMethodData) {
    try {
      const response = await api.post(SUBSCRIPTION_ENDPOINTS.PAYMENT_METHODS, paymentMethodData);
      
      if (response.success) {
        return {
          success: true,
          data: response.data,
          message: 'Payment method added successfully'
        };
      }
      
      throw new Error(response.message || 'Failed to add payment method');
    } catch (error) {
      console.error('Add payment method error:', error);
      throw new Error(error.message || 'Failed to add payment method');
    }
  }

  async removePaymentMethod(paymentMethodId) {
    try {
      const response = await api.delete(`${SUBSCRIPTION_ENDPOINTS.PAYMENT_METHODS}/${paymentMethodId}`);
      
      if (response.success) {
        return {
          success: true,
          message: 'Payment method removed successfully'
        };
      }
      
      throw new Error(response.message || 'Failed to remove payment method');
    } catch (error) {
      console.error('Remove payment method error:', error);
      throw new Error(error.message || 'Failed to remove payment method');
    }
  }

  async setDefaultPaymentMethod(paymentMethodId) {
    try {
      const response = await api.put(SUBSCRIPTION_ENDPOINTS.DEFAULT_PAYMENT_METHOD, {
        paymentMethodId
      });
      
      if (response.success) {
        return {
          success: true,
          data: response.data,
          message: 'Default payment method updated successfully'
        };
      }
      
      throw new Error(response.message || 'Failed to update default payment method');
    } catch (error) {
      console.error('Set default payment method error:', error);
      throw new Error(error.message || 'Failed to set default payment method');
    }
  }

  // ===== USAGE TRACKING =====

  async getCurrentUsage() {
    try {
      const response = await api.get(SUBSCRIPTION_ENDPOINTS.USAGE);
      
      if (response.success) {
        this.usage = response.data.usage;
        return {
          success: true,
          data: response.data.usage,
          message: 'Usage data fetched successfully'
        };
      }
      
      throw new Error(response.message || 'Failed to fetch usage data');
    } catch (error) {
      console.error('Get usage error:', error);
      throw new Error(error.message || 'Failed to fetch current usage');
    }
  }

  async getUsageHistory(params = {}) {
    try {
      const queryParams = new URLSearchParams({
        startDate: params.startDate,
        endDate: params.endDate,
        granularity: params.granularity || 'daily',
        ...params
      }).toString();
      
      const response = await api.get(`${SUBSCRIPTION_ENDPOINTS.USAGE_HISTORY}?${queryParams}`);
      
      if (response.success) {
        return {
          success: true,
          data: response.data,
          message: 'Usage history fetched successfully'
        };
      }
      
      throw new Error(response.message || 'Failed to fetch usage history');
    } catch (error) {
      console.error('Get usage history error:', error);
      throw new Error(error.message || 'Failed to fetch usage history');
    }
  }

  async getMetrics(timeframe = '30d') {
    try {
      const response = await api.get(`${SUBSCRIPTION_ENDPOINTS.METRICS}?timeframe=${timeframe}`);
      
      if (response.success) {
        return {
          success: true,
          data: response.data.metrics,
          message: 'Metrics fetched successfully'
        };
      }
      
      throw new Error(response.message || 'Failed to fetch metrics');
    } catch (error) {
      console.error('Get metrics error:', error);
      throw new Error(error.message || 'Failed to fetch usage metrics');
    }
  }

  // ===== INVOICE MANAGEMENT =====

  async getInvoices(params = {}) {
    try {
      const queryParams = new URLSearchParams({
        page: params.page || 1,
        limit: params.limit || 20,
        status: params.status,
        startDate: params.startDate,
        endDate: params.endDate
      }).toString();
      
      const response = await api.get(`${SUBSCRIPTION_ENDPOINTS.INVOICES}?${queryParams}`);
      
      if (response.success) {
        return {
          success: true,
          data: response.data,
          message: 'Invoices fetched successfully'
        };
      }
      
      throw new Error(response.message || 'Failed to fetch invoices');
    } catch (error) {
      console.error('Get invoices error:', error);
      throw new Error(error.message || 'Failed to fetch invoices');
    }
  }

  async getInvoice(invoiceId) {
    try {
      const response = await api.get(`${SUBSCRIPTION_ENDPOINTS.INVOICES}/${invoiceId}`);
      
      if (response.success) {
        return {
          success: true,
          data: response.data.invoice,
          message: 'Invoice fetched successfully'
        };
      }
      
      throw new Error(response.message || 'Failed to fetch invoice');
    } catch (error) {
      console.error('Get invoice error:', error);
      throw new Error(error.message || 'Failed to fetch invoice details');
    }
  }

  async downloadInvoice(invoiceId, format = 'pdf') {
    try {
      const endpoint = SUBSCRIPTION_ENDPOINTS.INVOICE_DOWNLOAD.replace(':id', invoiceId);
      const response = await api.get(`${endpoint}?format=${format}`, {
        responseType: 'blob'
      });
      
      if (response.data) {
        // Create download link
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', `invoice-${invoiceId}.${format}`);
        document.body.appendChild(link);
        link.click();
        link.remove();
        window.URL.revokeObjectURL(url);
        
        return {
          success: true,
          message: 'Invoice downloaded successfully'
        };
      }
      
      throw new Error('Failed to download invoice');
    } catch (error) {
      console.error('Download invoice error:', error);
      throw new Error(error.message || 'Failed to download invoice');
    }
  }

  // ===== BILLING PORTAL =====

  async createPortalSession(returnUrl) {
    try {
      const response = await api.post(SUBSCRIPTION_ENDPOINTS.PORTAL_SESSION, {
        returnUrl: returnUrl || window.location.href
      });
      
      if (response.success) {
        return {
          success: true,
          data: response.data,
          message: 'Portal session created successfully'
        };
      }
      
      throw new Error(response.message || 'Failed to create portal session');
    } catch (error) {
      console.error('Create portal session error:', error);
      throw new Error(error.message || 'Failed to access billing portal');
    }
  }

  // ===== UTILITY METHODS =====

  // Check if subscription is active
  isSubscriptionActive() {
    if (!this.currentSubscription) return false;
    
    const status = this.currentSubscription.status;
    return ['active', 'trialing'].includes(status);
  }

  // Check if subscription is in trial
  isInTrial() {
    if (!this.currentSubscription) return false;
    return this.currentSubscription.status === 'trialing';
  }

  // Check if subscription is cancelled
  isCancelled() {
    if (!this.currentSubscription) return false;
    return ['cancelled', 'canceled'].includes(this.currentSubscription.status);
  }

  // Get days remaining in trial
  getTrialDaysRemaining() {
    if (!this.currentSubscription || !this.isInTrial()) return 0;
    
    const trialEnd = new Date(this.currentSubscription.trialEnd);
    const now = new Date();
    const diffTime = trialEnd - now;
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    
    return Math.max(0, diffDays);
  }

  // Get usage percentage for a specific metric
  getUsagePercentage(metricName) {
    if (!this.usage || !this.currentSubscription) return 0;
    
    const used = this.usage[metricName] || 0;
    const limit = this.currentSubscription.limits?.[metricName];
    
    if (!limit || limit === -1) return 0; // Unlimited
    
    return Math.min(100, (used / limit) * 100);
  }

  // Check if usage limit is exceeded
  isUsageLimitExceeded(metricName) {
    return this.getUsagePercentage(metricName) >= 100;
  }

  // Get next billing date
  getNextBillingDate() {
    if (!this.currentSubscription) return null;
    return new Date(this.currentSubscription.currentPeriodEnd);
  }

  // Format currency amount
  formatCurrency(amount, currency = 'USD') {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: currency
    }).format(amount / 100); // Assuming amounts are in cents
  }

  // Calculate prorated amount for plan changes
  calculateProration(currentPlan, newPlan, daysRemaining) {
    const currentDailyRate = currentPlan.price / 30;
    const newDailyRate = newPlan.price / 30;
    const proratedRefund = currentDailyRate * daysRemaining;
    const proratedCharge = newDailyRate * daysRemaining;
    
    return {
      refund: proratedRefund,
      charge: proratedCharge,
      net: proratedCharge - proratedRefund
    };
  }

  // Get subscription status badge color
  getStatusBadgeColor(status) {
    const statusColors = {
      active: 'bg-green-100 text-green-800',
      trialing: 'bg-blue-100 text-blue-800',
      past_due: 'bg-orange-100 text-orange-800',
      cancelled: 'bg-red-100 text-red-800',
      paused: 'bg-gray-100 text-gray-800'
    };
    
    return statusColors[status] || 'bg-gray-100 text-gray-800';
  }
}

// Create and export singleton instance
export const subscriptionService = new SubscriptionService();

// Export the class for testing
export { SubscriptionService };

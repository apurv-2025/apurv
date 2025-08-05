// frontend/src/components/Pricing.js
import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import api from '../services/api';
import { API_ENDPOINTS } from '../utils/constants';

import { API_ENDPOINTS } from '../utils/constants';

function Pricing({ onSelectPlan, currentPlanId }) {
  const [plans, setPlans] = useState([]);
  const [billingCycle, setBillingCycle] = useState('monthly');
  const [loading, setLoading] = useState(true);
  const [processingPlan, setProcessingPlan] = useState(null);
  const { user } = useAuth();

  useEffect(() => {
    fetchPlans();
  }, []);

  const fetchPlans = async () => {
    try {
      const response = await api.get(API_ENDPOINTS.PRICING);
      setPlans(response.data);
    } catch (error) {
      console.error('Failed to fetch plans:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSelectPlan = async (plan) => {
    if (!user) return;
    
    setProcessingPlan(plan.id);
    try {
      await onSelectPlan(plan, billingCycle);
    } catch (error) {
      console.error('Failed to select plan:', error);
    } finally {
      setProcessingPlan(null);
    }
  };

  const formatPrice = (price) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0
    }).format(price);
  };

  const getYearlyDiscount = (monthly, yearly) => {
    if (monthly === 0) return 0;
    const yearlyEquivalent = monthly * 12;
    const discount = ((yearlyEquivalent - yearly) / yearlyEquivalent) * 100;
    return Math.round(discount);
  };

  if (loading) {
    return <div className="loading">Loading pricing plans...</div>;
  }

  return (
    <div className="pricing-container">
      <div className="pricing-header">
        <h2>Choose Your Plan</h2>
        <p>Select the perfect plan for your needs</p>
        
        <div className="billing-toggle">
          <button
            className={`toggle-btn ${billingCycle === 'monthly' ? 'active' : ''}`}
            onClick={() => setBillingCycle('monthly')}
          >
            Monthly
          </button>
          <button
            className={`toggle-btn ${billingCycle === 'yearly' ? 'active' : ''}`}
            onClick={() => setBillingCycle('yearly')}
          >
            Yearly
            <span className="discount-badge">Save up to 20% with yearly</span>
          </button>
        </div>
      </div>

      <div className="pricing-grid">
        {plans.map((plan) => {
          const price = billingCycle === 'yearly' ? plan.price_yearly : plan.price_monthly;
          const yearlyDiscount = getYearlyDiscount(plan.price_monthly, plan.price_yearly);
          const isCurrentPlan = currentPlanId === plan.id;
          const isProcessing = processingPlan === plan.id;
          const isFree = plan.name === 'free';
          const isPopular = plan.name === 'professional';

          return (
            <div
              key={plan.id}
              className={`pricing-card ${isPopular ? 'popular' : ''} ${isCurrentPlan ? 'current' : ''}`}
            >
              {isPopular && <div className="popular-badge">Most Popular</div>}
              {isCurrentPlan && <div className="current-badge">Current Plan</div>}
              
              <div className="plan-header">
                <h3>{plan.display_name}</h3>
                <p className="plan-description">{plan.description}</p>
              </div>

              <div className="plan-price">
                <span className="price-amount">
                  {formatPrice(price)}
                </span>
                <span className="price-period">
                  {isFree ? '' : `/${billingCycle === 'yearly' ? 'year' : 'month'}`}
                </span>
                {billingCycle === 'yearly' && yearlyDiscount > 0 && (
                  <div className="yearly-savings">
                    Save {yearlyDiscount}% annually
                  </div>
                )}
              </div>

              <div className="plan-features">
                <ul>
                  {plan.features.map((feature, index) => (
                    <li key={index}>
                      <span className="feature-icon">✓</span>
                      {feature}
                    </li>
                  ))}
                </ul>
              </div>

              <div className="plan-limits">
                <div className="limits-grid">
                  {Object.entries(plan.limits).map(([key, value]) => (
                    <div key={key} className="limit-item">
                      <span className="limit-label">
                        {key.replace('_', ' ').toUpperCase()}:
                      </span>
                      <span className="limit-value">
                        {value === -1 ? 'Unlimited' : value.toLocaleString()}
                      </span>
                    </div>
                  ))}
                </div>
              </div>

              <div className="plan-action">
                {user ? (
                  <button
                    className={`plan-btn ${isCurrentPlan ? 'current' : isFree ? 'free' : 'upgrade'}`}
                    onClick={() => !isCurrentPlan && handleSelectPlan(plan)}
                    disabled={isCurrentPlan || isProcessing}
                  >
                    {isProcessing ? (
                      <span className="processing">
                        <span className="spinner"></span>
                        Processing...
                      </span>
                    ) : isCurrentPlan ? (
                      'Current Plan'
                    ) : isFree ? (
                      'Downgrade to Free'
                    ) : (
                      `Upgrade to ${plan.display_name}`
                    )}
                  </button>
                ) : (
                  <button className="plan-btn signup" onClick={() => window.location.href = '/register'}>
                    Get Started
                  </button>
                )}
              </div>
            </div>
          );
        })}
      </div>

      <div className="pricing-footer">
        <div className="feature-comparison">
          <h3>Feature Comparison</h3>
          <div className="comparison-table">
            <div className="comparison-header">
              <div className="feature-name">Feature</div>
              {plans.map(plan => (
                <div key={plan.id} className="plan-name">{plan.display_name}</div>
              ))}
            </div>
            
            {/* Projects */}
            <div className="comparison-row">
              <div className="feature-name">Projects</div>
              {plans.map(plan => (
                <div key={plan.id} className="feature-value">
                  {plan.limits.projects === -1 ? '∞' : plan.limits.projects}
                </div>
              ))}
            </div>
            
            {/* API Calls */}
            <div className="comparison-row">
              <div className="feature-name">API Calls/month</div>
              {plans.map(plan => (
                <div key={plan.id} className="feature-value">
                  {plan.limits.api_calls === -1 ? '∞' : plan.limits.api_calls.toLocaleString()}
                </div>
              ))}
            </div>
            
            {/* Storage */}
            <div className="comparison-row">
              <div className="feature-name">Storage</div>
              {plans.map(plan => (
                <div key={plan.id} className="feature-value">
                  {plan.limits.storage_gb === -1 ? '∞' : `${plan.limits.storage_gb} GB`}
                </div>
              ))}
            </div>
            
            {/* Team Members */}
            <div className="comparison-row">
              <div className="feature-name">Team Members</div>
              {plans.map(plan => (
                <div key={plan.id} className="feature-value">
                  {plan.limits.team_members === -1 ? '∞' : plan.limits.team_members}
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Pricing;

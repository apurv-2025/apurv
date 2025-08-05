// src/components/subscription/PricingCard.jsx
import React from 'react';
import { CheckIcon } from '@heroicons/react/20/solid';
import Button from '../ui/Button';
import Badge from '../ui/Badge';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '../ui/Card';
import { formatCurrency } from '../../utils/formatters';

const PricingCard = ({ 
  plan, 
  billingCycle = 'monthly', 
  isCurrentPlan = false, 
  isProcessing = false, 
  onSelectPlan,
  user 
}) => {
  const price = billingCycle === 'yearly' ? plan.price_yearly : plan.price_monthly;
  const yearlyDiscount = plan.price_monthly > 0 ? 
    Math.round(((plan.price_monthly * 12 - plan.price_yearly) / (plan.price_monthly * 12)) * 100) : 0;
  
  const isFree = plan.name === 'free';
  const isPopular = plan.name === 'professional';

  return (
    <Card className={`relative ${isPopular ? 'ring-2 ring-blue-600 scale-105' : ''} ${isCurrentPlan ? 'ring-2 ring-green-600' : ''}`}>
      {isPopular && (
        <div className="absolute -top-3 left-1/2 transform -translate-x-1/2">
          <Badge className="bg-blue-600 text-white">Most Popular</Badge>
        </div>
      )}
      {isCurrentPlan && (
        <div className="absolute -top-3 left-1/2 transform -translate-x-1/2">
          <Badge className="bg-green-600 text-white">Current Plan</Badge>
        </div>
      )}
      
      <CardHeader className="text-center">
        <CardTitle className="text-xl">{plan.display_name}</CardTitle>
        <CardDescription>{plan.description}</CardDescription>
      </CardHeader>

      <CardContent className="text-center">
        <div className="mb-6">
          <span className="text-4xl font-bold text-gray-900">
            {formatCurrency(price)}
          </span>
          {!isFree && (
            <span className="text-gray-600">
              /{billingCycle === 'yearly' ? 'year' : 'month'}
            </span>
          )}
          {billingCycle === 'yearly' && yearlyDiscount > 0 && (
            <div className="text-sm text-green-600 font-medium mt-1">
              Save {yearlyDiscount}% annually
            </div>
          )}
        </div>

        <div className="space-y-4 mb-6">
          <div>
            <h4 className="font-medium text-gray-900 mb-2">Features:</h4>
            <ul className="space-y-2">
              {plan.features.map((feature, index) => (
                <li key={index} className="flex items-center text-sm">
                  <CheckIcon className="h-4 w-4 text-green-500 mr-2 flex-shrink-0" />
                  {feature}
                </li>
              ))}
            </ul>
          </div>

          <div>
            <h4 className="font-medium text-gray-900 mb-2">Limits:</h4>
            <div className="space-y-1">
              {Object.entries(plan.limits).map(([key, value]) => (
                <div key={key} className="flex justify-between text-sm">
                  <span className="text-gray-600">{key.replace('_', ' ').toUpperCase()}:</span>
                  <span className="font-medium">
                    {value === -1 ? '∞' : value.toLocaleString()}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </CardContent>

      <CardFooter>
        {user ? (
          <Button
            className="w-full"
            variant={isCurrentPlan ? 'secondary' : isFree ? 'danger' : 'primary'}
            onClick={() => !isCurrentPlan && onSelectPlan?.(plan)}
            disabled={isCurrentPlan || isProcessing}
            loading={isProcessing}
          >
            {isCurrentPlan ? 
              'Current Plan' : 
              isFree ? 
                'Downgrade to Free' : 
                `Upgrade to ${plan.display_name}`
            }
          </Button>
        ) : (
          <Button 
            className="w-full" 
            onClick={() => window.location.href = '/register'}
          >
            Get Started
          </Button>
        )}
      </CardFooter>
    </Card>
  );
};

export default PricingCard;

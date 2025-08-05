// src/components/subscription/PlanSelector.jsx
import React, { useState } from 'react';
import { RadioGroup } from '@headlessui/react';
import { CheckIcon } from '@heroicons/react/20/solid';
import Button from '../ui/Button';
import Badge from '../ui/Badge';
import { cn } from '../../utils/helpers';
import { formatCurrency } from '../../utils/formatters';

const PlanSelector = ({ 
  plans = [], 
  selectedPlan, 
  onSelectPlan, 
  billingCycle = 'monthly',
  showFeatures = true,
  className 
}) => {
  const getPlanPrice = (plan) => {
    return billingCycle === 'yearly' ? plan.price_yearly : plan.price_monthly;
  };

  const isPopularPlan = (plan) => plan.name === 'professional';

  return (
    <div className={cn("space-y-4", className)}>
      <RadioGroup value={selectedPlan} onChange={onSelectPlan}>
        <RadioGroup.Label className="sr-only">Choose a plan</RadioGroup.Label>
        
        <div className="space-y-4">
          {plans.map((plan) => {
            const price = getPlanPrice(plan);
            const isPopular = isPopularPlan(plan);

            return (
              <RadioGroup.Option
                key={plan.id}
                value={plan}
                className={({ checked, active }) =>
                  cn(
                    "relative block cursor-pointer rounded-lg border px-6 py-4 focus:outline-none",
                    checked
                      ? "border-blue-600 bg-blue-50"
                      : "border-gray-300 bg-white hover:border-gray-400",
                    active && "ring-2 ring-blue-600 ring-offset-2",
                    isPopular && "ring-2 ring-blue-600"
                  )
                }
              >
                {({ checked }) => (
                  <>
                    {isPopular && (
                      <Badge className="absolute -top-2 left-4 bg-blue-600 text-white">
                        Most Popular
                      </Badge>
                    )}
                    
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="flex items-center">
                          <div className="text-sm">
                            <RadioGroup.Label
                              as="p"
                              className="font-semibold text-gray-900"
                            >
                              {plan.display_name}
                            </RadioGroup.Label>
                            <RadioGroup.Description
                              as="div"
                              className="text-gray-500"
                            >
                              <p>{plan.description}</p>
                            </RadioGroup.Description>
                          </div>
                        </div>
                        
                        {showFeatures && plan.features && (
                          <div className="mt-3">
                            <ul className="text-sm text-gray-600 space-y-1">
                              {plan.features.slice(0, 3).map((feature, index) => (
                                <li key={index} className="flex items-center">
                                  <CheckIcon className="h-4 w-4 text-green-500 mr-2" />
                                  {feature}
                                </li>
                              ))}
                              {plan.features.length > 3 && (
                                <li className="text-blue-600 font-medium">
                                  +{plan.features.length - 3} more features
                                </li>
                              )}
                            </ul>
                          </div>
                        )}
                      </div>

                      <div className="flex flex-col items-end">
                        <div className="text-right">
                          <span className="text-2xl font-bold text-gray-900">
                            {formatCurrency(price)}
                          </span>
                          {price > 0 && (
                            <span className="text-gray-600">
                              /{billingCycle === 'yearly' ? 'year' : 'month'}
                            </span>
                          )}
                        </div>
                        
                        <div className="mt-2">
                          <div
                            className={cn(
                              "flex h-6 w-6 items-center justify-center rounded-full border-2",
                              checked
                                ? "border-blue-600 bg-blue-600"
                                : "border-gray-300 bg-white"
                            )}
                          >
                            {checked && (
                              <CheckIcon className="h-4 w-4 text-white" />
                            )}
                          </div>
                        </div>
                      </div>
                    </div>
                  </>
                )}
              </RadioGroup.Option>
            );
          })}
        </div>
      </RadioGroup>
    </div>
  );
};

export default PlanSelector;


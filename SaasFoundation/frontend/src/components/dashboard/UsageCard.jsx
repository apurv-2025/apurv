// src/components/dashboard/UsageCard.jsx
import React from 'react';
import { Link } from 'react-router-dom';
import DashboardCard from './DashboardCard';
import Progress from '../ui/Progress';

const UsageCard = ({ usageMetrics, planLimits }) => {
  if (!usageMetrics?.length) return null;

  return (
    <DashboardCard title="Usage Overview">
      <div className="space-y-4">
        {usageMetrics.slice(0, 3).map((metric, index) => {
          const limit = planLimits[metric.metric_name];
          const hasLimit = limit && limit !== -1;
          const percentage = hasLimit ? (metric.metric_value / limit) * 100 : 0;

          return (
            <div key={index} className="space-y-2">
              <div className="flex justify-between items-center">
                <span className="text-sm font-medium text-gray-700">
                  {metric.metric_name.replace('_', ' ').toUpperCase()}
                </span>
                <span className="text-sm text-gray-900">
                  {metric.metric_value.toLocaleString()}
                  {hasLimit && (
                    <span className="text-gray-500">
                      / {limit.toLocaleString()}
                    </span>
                  )}
                </span>
              </div>
              {hasLimit && (
                <Progress value={percentage} className="h-2" />
              )}
            </div>
          );
        })}
        
        <Link 
          to="/subscription" 
          className="text-blue-600 hover:text-blue-700 text-sm font-medium inline-block mt-4"
        >
          View detailed usage →
        </Link>
      </div>
    </DashboardCard>
  );
};

export default UsageCard;

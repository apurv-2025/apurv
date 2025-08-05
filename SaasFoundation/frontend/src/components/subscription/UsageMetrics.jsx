// src/components/subscription/UsageMetrics.jsx
import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/Card';
import { formatDate } from '../../utils/formatters';

const UsageMetrics = ({ usageMetrics, planLimits }) => {
  if (!usageMetrics?.length) {
    return (
      <div className="text-center py-8">
        <p className="text-gray-600">No usage data available for the current billing period.</p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {usageMetrics.map((metric, index) => (
        <Card key={index}>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">
              {metric.metric_name.replace('_', ' ').toUpperCase()}
            </CardTitle>
            <div className="text-2xl font-bold text-blue-600">
              {metric.metric_value.toLocaleString()}
            </div>
          </CardHeader>
          <CardContent>
            <p className="text-xs text-gray-600 mb-4">
              {formatDate(metric.period_start)} - {formatDate(metric.period_end)}
            </p>
            
            {planLimits[metric.metric_name] && planLimits[metric.metric_name] !== -1 && (
              <div className="space-y-2">
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                    style={{
                      width: `${Math.min(100, (metric.metric_value / planLimits[metric.metric_name]) * 100)}%`
                    }}
                  />
                </div>
                <p className="text-xs text-gray-600">
                  {metric.metric_value} / {planLimits[metric.metric_name].toLocaleString()} 
                  ({Math.round((metric.metric_value / planLimits[metric.metric_name]) * 100)}%)
                </p>
              </div>
            )}
          </CardContent>
        </Card>
      ))}
    </div>
  );
};

export default UsageMetrics;

import React from 'react';
import { TrendingUp } from 'lucide-react';

const MetricCard = ({ metric }) => {
  const getTrendColor = (trend) => {
    switch (trend) {
      case 'up': return 'bg-green-100 text-green-600';
      case 'down': return 'bg-red-100 text-red-600';
      default: return 'bg-gray-100 text-gray-600';
    }
  };

  const getTrendRotation = (trend) => {
    return trend === 'down' ? 'rotate-180' : '';
  };

  return (
    <div className="bg-white p-6 rounded-xl shadow-sm border">
      <div className="flex items-center justify-between mb-2">
        <h3 className="text-sm font-medium text-gray-600">{metric.metric}</h3>
        <div className={`p-1 rounded-full ${getTrendColor(metric.trend)}`}>
          <TrendingUp className={`w-4 h-4 ${getTrendRotation(metric.trend)}`} />
        </div>
      </div>
      <div className="flex items-baseline space-x-2">
        <span className="text-3xl font-bold text-gray-900">{metric.value}</span>
        <span className="text-sm text-gray-500">{metric.unit}</span>
      </div>
    </div>
  );
};

export default MetricCard;

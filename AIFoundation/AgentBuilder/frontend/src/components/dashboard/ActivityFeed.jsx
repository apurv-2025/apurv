import React from 'react';
import { Settings, MessageCircle, Activity, Users } from 'lucide-react';

const ActivityFeed = ({ activities }) => {
  const getActivityIcon = (type) => {
    switch (type) {
      case 'update':
        return <Settings className="w-5 h-5 text-blue-600" />;
      case 'interaction':
        return <MessageCircle className="w-5 h-5 text-green-600" />;
      case 'system':
        return <Activity className="w-5 h-5 text-purple-600" />;
      case 'create':
        return <Users className="w-5 h-5 text-orange-600" />;
      default:
        return <Activity className="w-5 h-5 text-gray-600" />;
    }
  };

  const getActivityColor = (type) => {
    switch (type) {
      case 'update':
        return 'bg-blue-100';
      case 'interaction':
        return 'bg-green-100';
      case 'system':
        return 'bg-purple-100';
      case 'create':
        return 'bg-orange-100';
      default:
        return 'bg-gray-100';
    }
  };

  const defaultActivities = [
    { user: 'Dr. Smith', action: 'Updated billing agent configuration', time: '2 minutes ago', type: 'update' },
    { user: 'Jane Doe', action: 'Interacted with front desk agent', time: '5 minutes ago', type: 'interaction' },
    { user: 'System', action: 'Automated knowledge base update', time: '1 hour ago', type: 'system' },
    { user: 'Mike Johnson', action: 'Created new general assistant agent', time: '2 hours ago', type: 'create' }
  ];

  const displayActivities = activities || defaultActivities;

  return (
    <div className="bg-white rounded-xl shadow-sm border">
      <div className="p-6 border-b">
        <h2 className="text-xl font-semibold text-gray-900">Recent Activity</h2>
      </div>
      <div className="p-6">
        <div className="space-y-4">
          {displayActivities.map((activity, index) => (
            <div key={index} className="flex items-center space-x-4 p-4 border border-gray-200 rounded-lg">
              <div className={`w-10 h-10 rounded-full flex items-center justify-center ${getActivityColor(activity.type)}`}>
                {getActivityIcon(activity.type)}
              </div>
              <div className="flex-1">
                <p className="text-sm font-medium text-gray-900">{activity.user}</p>
                <p className="text-sm text-gray-600">{activity.action}</p>
              </div>
              <div className="text-sm text-gray-500">{activity.time}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default ActivityFeed;

import React from 'react';
import { NavLink } from 'react-router-dom';
import { 
  Home, 
  Calendar, 
  Users, 
  Clock, 
  Activity,
  Bot,
  BarChart3
} from 'lucide-react';

const Sidebar = () => {
  const navigation = [
    { name: 'Dashboard', href: '/dashboard', icon: Home },
    { name: 'Calendar', href: '/calendar', icon: Calendar },
    { name: 'Persons', href: '/patients', icon: Users },
    { name: 'Practitioners', href: '/practitioners', icon: Activity },
    { name: 'Waitlist', href: '/waitlist', icon: Clock },
    { name: 'AI Assistant', href: '/agent/chat', icon: Bot },
    { name: 'Agent Dashboard', href: '/agent/dashboard', icon: BarChart3 },
  ];

  return (
    <div className="w-64 bg-white shadow-sm border-r border-gray-200">
      <nav className="mt-5 px-2">
        <div className="space-y-1">
          {navigation.map((item) => {
            const Icon = item.icon;
            return (
              <NavLink
                key={item.name}
                to={item.href}
                className={({ isActive }) =>
                  `group flex items-center px-2 py-2 text-sm font-medium rounded-md transition-colors duration-200 ${
                    isActive
                      ? 'bg-primary-100 text-primary-900 border-r-2 border-primary-500'
                      : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                  }`
                }
              >
                <Icon className="mr-3 h-5 w-5" />
                {item.name}
              </NavLink>
            );
          })}
        </div>
      </nav>
    </div>
  );
};

export default Sidebar; 
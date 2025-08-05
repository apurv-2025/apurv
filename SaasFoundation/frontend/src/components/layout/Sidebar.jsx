// src/components/layout/Sidebar.jsx
import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { cn } from '../../utils/helpers';
import {
  HomeIcon,
  CreditCardIcon,
  UserGroupIcon,
  Cog6ToothIcon,
  PresentationChartBarIcon
} from '@heroicons/react/24/outline';

const Sidebar = ({ isOpen, onClose }) => {
  const location = useLocation();

  const patient_mgmt = [
    { name: 'Appointments', href: '/dashboard', icon: HomeIcon },
    { name: 'Billing', href: '/team', icon: PresentationChartBarIcon },
    { name: 'Support', href: '/subscription', icon: CreditCardIcon },
    { name: 'Analytics', href: '/pricing', icon: PresentationChartBarIcon },
    { name: 'Reports', href: '/settings', icon: PresentationChartBarIcon },
    { name: 'Assistants', href: '/subscription1', icon: CreditCardIcon }
  ];

  const practitioner_mgmt = [
    { name: 'Schedules', href: '/dashboard', icon: HomeIcon },
    { name: 'Analytics', href: '/team', icon: HomeIcon },
    { name: 'Reports', href: '/pricing', icon: PresentationChartBarIcon },
    { name: 'Assistants', href: '/settings', icon: PresentationChartBarIcon }
  ];

  const operation_mgmt = [
    { name: 'Revenue Cycle Management', href: '/dashboard', icon: HomeIcon },
    { name: 'AR & AP', href: '/subscription', icon: HomeIcon },
    { name: 'Analytics', href: '/pricing', icon: HomeIcon },
    { name: 'Assistants', href: '/settings', icon: PresentationChartBarIcon }
  ];

  const account_mgmt = [
    { name: 'Dashboard', href: '/dashboard', icon: HomeIcon },
    { name: 'Pricing', href: '/pricing', icon: PresentationChartBarIcon },
    { name: 'Subscription', href: '/subscription', icon: CreditCardIcon },
    { name: 'Team', href: '/team', icon: UserGroupIcon },
    { name: 'Settings', href: '/settings', icon: Cog6ToothIcon },
    { name: 'Assistants', href: '/pricing', icon: PresentationChartBarIcon }
  ];

  return (
    <>
      {/* Mobile backdrop */}
      {isOpen && (
        <div
          className="fixed inset-0 z-40 bg-black bg-opacity-50 lg:hidden"
          onClick={onClose}
        />
      )}

      {/* Sidebar */}
      <div
        className={cn(
          "fixed inset-y-0 left-0 z-50 w-60 bg-white shadow-lg transform transition-transform duration-300 ease-in-out lg:translate-x-0 lg:static lg:inset-0",
          isOpen ? "translate-x-0" : "-translate-x-full"
        )}
      >
        
        <div className="flex flex-col h-full">

        <div className="flex flex-col h-full">
          <div className="flex items-center h-16 px-6 border-b border-gray-200">
            <h2 className="text-lg font-semibold text-gray-900">Patient Management</h2>
          </div>

          <nav className="flex-1 px-4 py-6 space-y-2">
            {patient_mgmt.map((item) => {
              const Icon = item.icon;
              const isActive = location.pathname === item.href;

              return (
                <Link
                  key={item.name}
                  to={item.href}
                  className={cn(
                    "flex items-center px-3 py-2 text-sm font-medium rounded-md transition-colors",
                    isActive
                      ? "bg-blue-50 text-blue-700 border-r-2 border-blue-700"
                      : "text-gray-600 hover:bg-gray-50 hover:text-gray-900"
                  )}
                  onClick={onClose}
                >
                  <Icon className="w-5 h-5 mr-3" />
                  {item.name}
                </Link>
              );
            })}
          </nav>
        </div>


        <div className="flex flex-col h-full">
          <div className="flex items-center h-16 px-6 border-b border-gray-200">
            <h2 className="text-lg font-semibold text-gray-900">Practitioner Management</h2>
          </div>

          <nav className="flex-1 px-4 py-6 space-y-2">
            {practitioner_mgmt.map((item) => {
              const Icon = item.icon;
              const isActive = location.pathname === item.href;

              return (
                <Link
                  key={item.name}
                  to={item.href}
                  className={cn(
                    "flex items-center px-3 py-2 text-sm font-medium rounded-md transition-colors",
                    isActive
                      ? "bg-blue-50 text-blue-700 border-r-2 border-blue-700"
                      : "text-gray-600 hover:bg-gray-50 hover:text-gray-900"
                  )}
                  onClick={onClose}
                >
                  <Icon className="w-5 h-5 mr-3" />
                  {item.name}
                </Link>
              );
            })}
          </nav>
        </div>


 
        <div className="flex flex-col h-full">
          <div className="flex items-center h-16 px-6 border-b border-gray-200">
            <h2 className="text-lg font-semibold text-gray-900">Operations Management</h2>
          </div>

          <nav className="flex-1 px-4 py-6 space-y-2">
            {operation_mgmt.map((item) => {
              const Icon = item.icon;
              const isActive = location.pathname === item.href;

              return (
                <Link
                  key={item.name}
                  to={item.href}
                  className={cn(
                    "flex items-center px-3 py-2 text-sm font-medium rounded-md transition-colors",
                    isActive
                      ? "bg-blue-50 text-blue-700 border-r-2 border-blue-700"
                      : "text-gray-600 hover:bg-gray-50 hover:text-gray-900"
                  )}
                  onClick={onClose}
                >
                  <Icon className="w-5 h-5 mr-3" />
                  {item.name}
                </Link>
              );
            })}
          </nav>
        </div>       

          <div className="flex items-center h-16 px-6 border-b border-gray-200">
            <h2 className="text-lg font-semibold text-gray-900">Account Management</h2>
          </div>

          <nav className="flex-1 px-4 py-6 space-y-2">
            {account_mgmt.map((item) => {
              const Icon = item.icon;
              const isActive = location.pathname === item.href;

              return (
                <Link
                  key={item.name}
                  to={item.href}
                  className={cn(
                    "flex items-center px-3 py-2 text-sm font-medium rounded-md transition-colors",
                    isActive
                      ? "bg-blue-50 text-blue-700 border-r-2 border-blue-700"
                      : "text-gray-600 hover:bg-gray-50 hover:text-gray-900"
                  )}
                  onClick={onClose}
                >
                  <Icon className="w-5 h-5 mr-3" />
                  {item.name}
                </Link>
              );
            })}
          </nav>
        </div>


      </div>
    </>
  );
};

export default Sidebar;

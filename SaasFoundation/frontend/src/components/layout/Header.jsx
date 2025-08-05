// src/components/layout/Header.jsx
import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';
import Button from '../ui/Button';
import Badge from '../ui/Badge';

import Logo from '../ui/Logo';

import { 
  UserIcon, 
  Cog6ToothIcon, 
  ArrowRightStartOnRectangleIcon,
  CreditCardIcon,
  PresentationChartBarIcon
} from '@heroicons/react/24/outline';

const Header = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <header className="bg-gradient-to-r from-blue-600 to-blue-600 shadow-lg">
      <div className="max-w-7xl lg:max-w-none mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <Link to="/" className="flex items-center">
            <h1 className="text-xl font-bold text-white">Agentic Practice</h1>
          </Link>
          <nav className="flex items-center space-x-4">
            {user ? (
              <div className="flex items-center space-x-4">
                    
                <div className="flex items-center space-x-2 text-white">
                  <UserIcon className="h-5 w-5" />
                  <span className="text-sm font-medium">Welcome, {user.first_name}!</span>
                  {!user.is_verified && (
                    <Badge variant="warning" className="text-xs">
                      Unverified
                    </Badge>
                  )}
                </div>

                <Link to="/notifications" className="text-white hover:text-blue-100 px-3 py-2 rounded-md text-sm font-medium transition-colors">
                  Notifications
                </Link>
                
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={handleLogout}
                  className="text-white hover:bg-white/10 border border-white/20"
                >
                  <ArrowRightStartOnRectangleIcon className="h-4 w-4 mr-1" />
                  Logout
                </Button>
              </div>
            ) : (
              <div className="flex items-center space-x-4">
                <Link to="/pricing" className="text-white hover:text-blue-100 px-3 py-2 rounded-md text-sm font-medium transition-colors">
                  Pricing
                </Link>
                <Link to="/login" className="text-white hover:text-blue-100 px-3 py-2 rounded-md text-sm font-medium transition-colors">
                  Login
                </Link>
                <Button variant="secondary" size="sm" asChild>
                  <Link to="/register">Sign Up</Link>
                </Button>
              </div>
            )}
          </nav>
        </div>
      </div>
    </header>
  );
};

export default Header;

// frontend/src/components/Header.js
import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

function Header() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <header className="header">
      <div className="header-content">
        <Link to="/" className="logo">
          <h1>Agentic Practice</h1>
        </Link>
        
        <nav className="nav">
          {user ? (
            <div className="nav-authenticated">
              <Link to="/pricing" className="nav-link">Pricing</Link>
              <Link to="/subscription" className="nav-link">Subscription</Link>
              <Link to="/dashboard" className="nav-link">Dashboard</Link>
              <Link to="/settings" className="nav-link">Settings</Link>
              <span className="user-info">
                Welcome, {user.first_name}!
                {!user.is_verified && (
                  <span className="verification-badge">Unverified</span>
                )}
              </span>
              <button onClick={handleLogout} className="logout-btn">
                Logout
              </button>
            </div>
          ) : (
            <div className="nav-public">
              <Link to="/pricing" className="nav-link">Pricing</Link>
              <Link to="/login" className="nav-link">Login</Link>
              <Link to="/register" className="nav-link btn-primary">
                Sign Up
              </Link>
            </div>
          )}
        </nav>
      </div>
    </header>
  );
}

export default Header;

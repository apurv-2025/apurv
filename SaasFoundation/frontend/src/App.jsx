// src/App.jsx
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import ProtectedRoute from './components/auth/ProtectedRoute';
import PublicRoute from './components/auth/PublicRoute';

// Pages
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import EmailVerification from './pages/EmailVerification';
import Pricing from './pages/Pricing';
import SubscriptionManagement from './pages/SubscriptionManagement';
import Settings from './pages/Settings';
import TeamManagement from './pages/TeamManagement';
import InvitationAccept from './pages/InvitationAccept';
import NotificationManager from './pages/NotificationManager';

//Forgot and Reset Password
import PasswordReset from './pages/PasswordReset';
import PasswordResetEmail from './pages/PasswordResetEmail';

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="min-h-screen bg-gray-50">
          <main className="flex-1 py-2 px-4 sm:px-6 lg:px-8 lg:ml-5 max-w-7xl lg:max-w-none mx-auto">
            <Routes>
              <Route path="/" element={<Navigate to="/dashboard" />} />
              <Route path="/login" element={
                <PublicRoute>
                  <Login />
                </PublicRoute>
              } />
              <Route path="/forgot-password" element={<PasswordResetEmail />} />
              <Route path="/reset-password" element={<PasswordReset />} />

              <Route path="/register" element={
                <PublicRoute>
                  <Register />
                </PublicRoute>
              } />
              <Route path="/verify" element={<EmailVerification />} />
              <Route path="/invite" element={<InvitationAccept />} />
              <Route path="/pricing" element={<Pricing />} />
              <Route path="/dashboard" element={
                <ProtectedRoute>
                  <Dashboard />
                </ProtectedRoute>
              } />
              <Route path="/subscription" element={
                <ProtectedRoute>
                  <SubscriptionManagement />
                </ProtectedRoute>
              } />
              <Route path="/team" element={
                <ProtectedRoute>
                  <TeamManagement />
                </ProtectedRoute>
              } />
              <Route path="/notifications" element={
                  <NotificationManager />
              } />

              <Route path="/settings" element={
                <ProtectedRoute>
                  <Settings />
                </ProtectedRoute>
              } />
            </Routes>
          </main>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;

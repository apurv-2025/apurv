import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

// Import components
import Layout from './components/Layout/Layout';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import AppointmentCalendar from './pages/AppointmentCalendar';

import PatientManagement from './pages/PatientManagement';
import PractitionerManagement from './pages/PractitionerManagement';

import WaitlistManagement from './pages/WaitlistManagement';
import AgentChat from './pages/AgentChat';
import AgentDashboard from './pages/AgentDashboard';

// Import contexts
import { AuthProvider } from './contexts/AuthContext';

// Import styles
import './styles/globals.css';

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="App">
          <Routes>
            {/* Public routes */}
            <Route path="/login" element={<Login />} />
            
            {/* Protected routes */}
            <Route path="/" element={<Layout />}>
              <Route index element={<Navigate to="/dashboard" replace />} />
              <Route path="dashboard" element={<Dashboard />} />
              <Route path="calendar" element={<AppointmentCalendar />} />

              <Route path="patients" element={<PatientManagement />} />
              <Route path="practitioners" element={<PractitionerManagement />} />

                              <Route path="waitlist" element={<WaitlistManagement />} />
                <Route path="agent/chat" element={<AgentChat />} />
                <Route path="agent/dashboard" element={<AgentDashboard />} />
              </Route>
            
            {/* Catch all route */}
            <Route path="*" element={<Navigate to="/dashboard" replace />} />
          </Routes>
          
          {/* Toast notifications */}
          <ToastContainer
            position="top-right"
            autoClose={5000}
            hideProgressBar={false}
            newestOnTop={false}
            closeOnClick
            rtl={false}
            pauseOnFocusLoss
            draggable
            pauseOnHover
            theme="light"
          />
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App; 
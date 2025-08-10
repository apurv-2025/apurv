// File: src/App.js - Main Application Entry Point
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthorizationProvider } from './contexts/AuthorizationContext';
import { NotificationProvider } from './contexts/NotificationContext';
import Layout from './components/layout/Layout';
import Dashboard from './pages/Dashboard';
import PriorAuthorizationPage from './pages/PriorAuthorizationPage';
import PatientInformationPage from './pages/PatientInformationPage';
import HistoryPage from './pages/HistoryPage';
import './App.css';

function App() {
  return (
    <NotificationProvider>
      <AuthorizationProvider>
        <Router>
          <Layout>
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/prior-authorization" element={<PriorAuthorizationPage />} />
              <Route path="/patient-information" element={<PatientInformationPage />} />
              <Route path="/history" element={<HistoryPage />} />
            </Routes>
          </Layout>
        </Router>
      </AuthorizationProvider>
    </NotificationProvider>
  );
}

export default App;

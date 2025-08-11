// File: src/App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ToastProvider } from './contexts/ToastContext';
import { AppProvider } from './contexts/AppContext';
import Layout from './components/layout/Layout';
import Dashboard from './pages/Dashboard';
import UploadPage from './pages/UploadPage';
import EligibilityPage from './pages/EligibilityPage';
import HistoryPage from './pages/HistoryPage';
import AgentPage from './pages/AgentPage';
import './App.css';

function App() {
  return (
    <AppProvider>
      <ToastProvider>
        <Router>
          <Layout>
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/upload" element={<UploadPage />} />
              <Route path="/eligibility" element={<EligibilityPage />} />
              <Route path="/history" element={<HistoryPage />} />
              <Route path="/agent" element={<AgentPage />} />
            </Routes>
          </Layout>
        </Router>
      </ToastProvider>
    </AppProvider>
  );
}

export default App;

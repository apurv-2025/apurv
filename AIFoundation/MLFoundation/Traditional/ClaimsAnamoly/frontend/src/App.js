import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import Sidebar from './components/Sidebar';
import Dashboard from './pages/Dashboard';
import DataPipeline from './pages/DataPipeline';
import ModelTraining from './pages/ModelTraining';
import ModelManagement from './pages/ModelManagement';
import APIService from './pages/APIService';
import Monitoring from './pages/Monitoring';
import Settings from './pages/Settings';


function App() {
  return (
    <Router>
      <div className="h-screen flex overflow-hidden bg-gray-100">
        <Sidebar />
        
        <div className="flex-1 overflow-auto focus:outline-none">
          <main className="flex-1 relative z-0 overflow-y-auto py-6">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 md:px-8">
              <Routes>
                <Route path="/" element={<Dashboard />} />
                <Route path="/data-pipeline" element={<DataPipeline />} />
                <Route path="/model-training" element={<ModelTraining />} />
                <Route path="/model-management" element={<ModelManagement />} />
                <Route path="/api-service" element={<APIService />} />
                <Route path="/monitoring" element={<Monitoring />} />
                <Route path="/settings" element={<Settings />} />
              </Routes>
            </div>
          </main>
        </div>
        
        <Toaster
          position="top-right"
          toastOptions={{
            duration: 4000,
            style: {
              background: '#363636',
              color: '#fff',
            },
            success: {
              duration: 3000,
              iconTheme: {
                primary: '#22c55e',
                secondary: '#fff',
              },
            },
            error: {
              duration: 5000,
              iconTheme: {
                primary: '#ef4444',
                secondary: '#fff',
              },
            },
          }}
        />
      </div>
    </Router>
  );
}

export default App; 
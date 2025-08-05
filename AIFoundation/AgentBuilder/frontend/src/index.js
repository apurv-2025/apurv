import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';


// Main dashboard exports
export { default as AdvancedAnalytics } from './pages/AdvancedAnalytics';
export { default as TemplateLibrary } from './pages/TemplateLibrary';
export { default as ComplianceMonitoring } from './pages/ComplianceMonitoring';

// Component exports
export { default as MetricCard } from './components/dashboard/MetricCard';
export { default as ActivityFeed } from './components/dashboard/ActivityFeed';
export { InteractionsChart, UsageDistributionChart } from './components/charts/AnalyticsCharts';
export { default as TemplateCard } from './components/templates/TemplateCard';
export { default as SearchAndFilter } from './components/ui/SearchAndFilter';
export { default as ComplianceOverview } from './components/compliance/ComplianceOverview';
export { default as ComplianceControls } from './components/compliance/ComplianceControls';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

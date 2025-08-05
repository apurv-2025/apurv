import React, { useState } from 'react';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import Sidebar from './components/ui/Sidebar';
import LoadingSpinner from './components/ui/LoadingSpinner';
import Login from './pages/Login';

// Main pages
import Dashboard from './pages/Dashboard';
import AgentBuilder from './pages/AgentBuilding';
import AdvancedAnalytics from './pages/AdvancedAnalytics';
import TemplateLibrary from './pages/TemplateLibrary';
import ComplianceMonitoring from './pages/ComplianceMonitoring';
import GenericAgentReporting from './pages/AgentGenericReport';
import AgentManagement from './pages/AgentManagement';
import KnowledgeBase from './pages/KnowledgeBase';
import Settings from './pages/Settings';

// Agent Management sub-pages
import CreateAgent from './pages/agents/CreateAgent';
import AgentList from './pages/agents/AgentList';
import AgentTraining from './pages/agents/AgentTraining';
import AgentDeployment from './pages/agents/AgentDeployment';


// Knowledge Base sub-pages
import Documents from './pages/knowledge/Documents';
import Database from './pages/knowledge/Database';
import DataSources from './pages/knowledge/DataSources';

// Templates sub-pages
import AgentTemplates from './pages/templates/AgentTemplates';
import ResponseTemplates from './pages/templates/ResponseTemplates';
import WorkflowTemplates from './pages/templates/WorkflowTemplates';

// Analytics sub-pages
import Performance from './pages/analytics/Performance';
import UsageStats from './pages/analytics/UsageStats';
import Insights from './pages/analytics/Insights';

// Compliance sub-pages
import Policies from './pages/compliance/Policies';
import AuditTrail from './pages/compliance/AuditTrail';
import ComplianceReports from './pages/compliance/ComplianceReports';

// Help sub-pages
import Documentation from './pages/help/Documentation';
import Support from './pages/help/Support';
import Tutorials from './pages/help/Tutorials';

// Settings sub-pages
import GeneralSettings from './pages/settings/GeneralSettings';
import UserManagement from './pages/settings/UserManagement';
import SystemIntegrationsManager from './pages/settings/IntegrationManager';

// Fallback component for pages that don't exist yet
const ComingSoon = ({ title }) => (
  <div className="p-8">
    <div className="max-w-2xl mx-auto text-center">
      <div className="bg-white rounded-lg shadow-sm border p-8">
        <h1 className="text-2xl font-bold text-gray-900 mb-4">{title}</h1>
        <p className="text-gray-600 mb-6">This feature is coming soon!</p>
        <div className="w-16 h-16 mx-auto bg-blue-100 rounded-full flex items-center justify-center">
          <span className="text-2xl">🚀</span>
        </div>
      </div>
    </div>
  </div>
);

// Main App Component
const App = () => {
  const [activeTab, setActiveTab] = useState('dashboard');
  const { user, loading } = useAuth();

  if (loading) {
    return <LoadingSpinner />;
  }

  if (!user) {
    return <Login />;
  }

  // Enhanced routing system that handles both main and sub navigation
  const renderContent = () => {
    // Handle sub-navigation items
    if (activeTab.includes('.')) {
      const [mainSection, subSection] = activeTab.split('.');
      
      switch (mainSection) {
        case 'agents':
          switch (subSection) {
            case 'create':
              return <AgentBuilder />;
            case 'list':
              return <AgentList />;
            case 'test':
              return <AgentTraining />;
            case 'deploy':
              return <AgentDeployment />;
            case 'reports':
              return <GenericAgentReporting />;
            default:
              return <ComingSoon title="Agent Management" />;
          }
          
        case 'knowledge':
          switch (subSection) {
            case 'documents':
              return <Documents />;
            case 'database':
              return <Database />;
            case 'sources':
              return <DataSources />;
            default:
              return <ComingSoon title="Knowledge Base" />;
          }
          
        case 'templates':
          switch (subSection) {
            case 'agent':
              return <AgentTemplates />;
            case 'response':
              return <ResponseTemplates />;
            case 'workflow':
              return <WorkflowTemplates />;
            default:
              return <ComingSoon title="Templates" />;
          }
          
        case 'analytics':
          switch (subSection) {
            case 'performance':
              return <Performance />;
            case 'usage':
              return <UsageStats />;
            case 'insights':
              return <Insights />;
            default:
              return <ComingSoon title="Analytics" />;
          }
          
        case 'compliance':
          switch (subSection) {
            case 'policies':
              return <Policies />;
            case 'audit':
              return <AuditTrail />;
            case 'reports':
              return <ComplianceReports />;
            default:
              return <ComingSoon title="Compliance" />;
          }
          
        case 'help':
          switch (subSection) {
            case 'documentation':
              return <Documentation />;
            case 'support':
              return <Support />;
            case 'tutorials':
              return <Tutorials />;
            default:
              return <ComingSoon title="Help Center" />;
          }
          
        case 'settings':
          switch (subSection) {
            case 'general':
              return <GeneralSettings />;
            case 'users':
              return <UserManagement />;
            case 'integrations':
              return <SystemIntegrationsManager />;
            default:
              return <ComingSoon title="Settings" />;
          }
          
        default:
          return <ComingSoon title="Page Not Found" />;
      }
    }

    // Handle main navigation items (backwards compatibility)
    switch (activeTab) {
      case 'dashboard':
        return <Dashboard />;
      case 'agents':
        return <AgentManagement />;
      case 'knowledge':
        return <KnowledgeBase />;
      case 'templates':
        return <TemplateLibrary />;
      case 'analytics':
        return <AdvancedAnalytics />;
      case 'compliance':
        return <ComplianceMonitoring />;
      case 'help':
        return <ComingSoon title="Help Center" />;
      case 'settings':
        return <Settings />;
      default:
        return <Dashboard />;
    }
  };

  // Get page title for breadcrumb or header
  const getPageTitle = () => {
    if (activeTab.includes('.')) {
      const [mainSection, subSection] = activeTab.split('.');
      const mainTitles = {
        agents: 'Agent Management',
        knowledge: 'Knowledge Base',
        templates: 'Templates',
        analytics: 'Analytics',
        compliance: 'Compliance',
        help: 'Help Center',
        settings: 'Settings'
      };
      
      const subTitles = {
        'agents.create': 'Create Agent',
        'agents.test': 'Train & Test',
        'agents.deploy': 'Deploy & Monitor',
        'agents.list': 'Agents Library',
        'agents.decommission': 'DeCommission Agents',
        'knowledge.documents': 'Documents',
        'knowledge.database': 'Database',
        'knowledge.sources': 'Data Sources',
        'templates.agent': 'Agent Templates',
        'templates.response': 'Response Templates',
        'templates.workflow': 'Workflow Templates',
        'analytics.performance': 'Performance',
        'analytics.usage': 'Usage Statistics',
        'analytics.insights': 'Insights',
        'compliance.policies': 'Policies',
        'compliance.audit': 'Audit Trail',
        'compliance.reports': 'Reports',
        'help.documentation': 'Documentation',
        'help.support': 'Support',
        'help.tutorials': 'Tutorials',
        'settings.general': 'General Settings',
        'settings.users': 'User Management',
        'settings.integrations': 'Integrations'
      };
      
      return {
        main: mainTitles[mainSection] || mainSection,
        sub: subTitles[activeTab] || subSection,
        breadcrumb: `${mainTitles[mainSection]} > ${subTitles[activeTab] || subSection}`
      };
    }
    
    const mainTitles = {
      dashboard: 'Dashboard',
      agents: 'Agent Manager',
      knowledge: 'Knowledge Base',
      templates: 'Templates',
      analytics: 'Analytics',
      compliance: 'Compliance',
      help: 'Help Center',
      settings: 'Settings'
    };
    
    return {
      main: mainTitles[activeTab] || 'Dashboard',
      sub: null,
      breadcrumb: mainTitles[activeTab] || 'Dashboard'
    };
  };

  const pageTitle = getPageTitle();

  return (
    <div className="flex h-screen bg-gray-50">
      <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Optional: Add a header/breadcrumb bar */}
        {pageTitle.sub && (
          <div className="bg-white border-b px-6 py-4">
            <nav className="text-sm text-gray-600">
              <span className="font-medium text-gray-900">{pageTitle.breadcrumb}</span>
            </nav>
          </div>
        )}
        
        {/* Main content area */}
        <div className="flex-1 overflow-auto">
          {renderContent()}
        </div>
      </div>
    </div>
  );
};

// Root App with Auth Provider
const AIAgentBuilder = () => {
  return (
    <AuthProvider>
      <App />
    </AuthProvider>
  );
};

export default AIAgentBuilder;

import React, { useState } from 'react';
import { 
  Bot, 
  Settings as SettingsIcon,
  BarChart3,
  BookOpen,
  LogOut,
  User,
  ChevronDown,
  ChevronRight,
  Plus,
  List,
  Brain,
  Database,
  FileText,
  Users,
  Shield,
  HelpCircle,
  Palette,
  TestTube,
  Cloud,
  Rocket,
  Trash
} from 'lucide-react';
import { useAuth } from '../../contexts/AuthContext';

const Sidebar = ({ activeTab, setActiveTab }) => {
  const { user, logout } = useAuth();
  const [expandedItems, setExpandedItems] = useState(new Set(['agents'])); // Start with Agent Manager expanded

  const tabs = [
    { 
      id: 'dashboard', 
      label: 'Dashboard', 
      icon: BarChart3 
    },
    { 
      id: 'agents', 
      label: 'Agent Manager', 
      icon: Bot,
      subItems: [
        { id: 'agents.create', label: 'Build & Configure', icon: Rocket },
        { id: 'agents.test', label: 'Trian & Test', icon: Brain },
        { id: 'agents.deploy', label: 'Deploy & Monitor', icon: Cloud },
        { id: 'agents.reports', label: 'Agent Reports', icon: Brain },
        { id: 'agents.delete', label: 'Decommission', icon: Trash },
        { id: 'agents.list', label: 'Agent Library', icon: List },
      ]
    },
    { 
      id: 'knowledge', 
      label: 'Knowledge Base', 
      icon: BookOpen,
      subItems: [
        { id: 'knowledge.documents', label: 'Documents', icon: FileText },
        { id: 'knowledge.database', label: 'Database', icon: Database },
        { id: 'knowledge.sources', label: 'Data Sources', icon: Database },
      ]
    },
    { 
      id: 'templates', 
      label: 'Templates', 
      icon: Palette,
      subItems: [
        { id: 'templates.agent', label: 'Agent Templates', icon: Bot },
        { id: 'templates.response', label: 'Response Templates', icon: FileText },
        { id: 'templates.workflow', label: 'Workflow Templates', icon: List },
      ]
    },
    { 
      id: 'analytics', 
      label: 'Analytics', 
      icon: BarChart3,
      subItems: [
        { id: 'analytics.performance', label: 'Performance', icon: BarChart3 },
        { id: 'analytics.usage', label: 'Usage Stats', icon: Users },
        { id: 'analytics.insights', label: 'Insights', icon: Brain },
      ]
    },
    { 
      id: 'compliance', 
      label: 'Compliance', 
      icon: Shield,
      subItems: [
        { id: 'compliance.policies', label: 'Policies', icon: FileText },
        { id: 'compliance.audit', label: 'Audit Trail', icon: List },
        { id: 'compliance.reports', label: 'Reports', icon: BarChart3 },
      ]
    },
    { 
      id: 'help', 
      label: 'Help', 
      icon: HelpCircle,
      subItems: [
        { id: 'help.documentation', label: 'Documentation', icon: BookOpen },
        { id: 'help.support', label: 'Support', icon: Users },
        { id: 'help.tutorials', label: 'Tutorials', icon: FileText },
      ]
    },
    { 
      id: 'settings', 
      label: 'Settings', 
      icon: SettingsIcon,
      subItems: [
        { id: 'settings.general', label: 'General', icon: SettingsIcon },
        { id: 'settings.users', label: 'User Management', icon: Users },
        { id: 'settings.integrations', label: 'Integrations', icon: Database },
      ]
    },
  ];

  const toggleExpanded = (tabId) => {
    const newExpanded = new Set(expandedItems);
    if (newExpanded.has(tabId)) {
      newExpanded.delete(tabId);
    } else {
      newExpanded.add(tabId);
    }
    setExpandedItems(newExpanded);
  };

  const handleItemClick = (tab, subItem = null) => {
    if (subItem) {
      // Clicking on a sub-item
      setActiveTab(subItem.id);
    } else if (tab.subItems && tab.subItems.length > 0) {
      // Clicking on a parent item with sub-items - toggle expansion
      toggleExpanded(tab.id);
      // Also set as active if it wasn't already
      if (!expandedItems.has(tab.id)) {
        setActiveTab(tab.id);
      }
    } else {
      // Clicking on a regular item without sub-items
      setActiveTab(tab.id);
    }
  };

  const isActive = (tabId) => {
    if (activeTab === tabId) return true;
    // Check if any sub-item is active
    return activeTab.startsWith(tabId + '.');
  };

  const isSubItemActive = (subItemId) => {
    return activeTab === subItemId;
  };

  return (
    <div className="w-64 bg-white shadow-lg h-screen flex flex-col">
      <div className="p-6 border-b">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 bg-blue-600 rounded-full flex items-center justify-center">
            <Bot className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="text-lg font-semibold text-gray-900">AI Agent Studio</h1>
            <p className="text-sm text-gray-600">{user?.practice_name}</p>
          </div>
        </div>
      </div>

      <nav className="flex-1 p-4 overflow-y-auto">
        <ul className="space-y-1">
          {tabs.map((tab) => {
            const Icon = tab.icon;
            const hasSubItems = tab.subItems && tab.subItems.length > 0;
            const isExpanded = expandedItems.has(tab.id);
            const itemIsActive = isActive(tab.id);

            return (
              <li key={tab.id}>
                {/* Main navigation item */}
                <button
                  onClick={() => handleItemClick(tab)}
                  className={`w-full flex items-center justify-between px-4 py-3 rounded-lg text-left transition duration-200 ${
                    itemIsActive
                      ? 'bg-blue-100 text-blue-700 border border-blue-200'
                      : 'text-gray-700 hover:bg-gray-100'
                  }`}
                >
                  <div className="flex items-center space-x-3">
                    <Icon className="w-5 h-5" />
                    <span className="font-medium">{tab.label}</span>
                  </div>
                  {hasSubItems && (
                    <div className="ml-2">
                      {isExpanded ? (
                        <ChevronDown className="w-4 h-4" />
                      ) : (
                        <ChevronRight className="w-4 h-4" />
                      )}
                    </div>
                  )}
                </button>

                {/* Sub-navigation items */}
                {hasSubItems && isExpanded && (
                  <div className="mt-1 ml-4 border-l-2 border-gray-100">
                    <ul className="space-y-1">
                      {tab.subItems.map((subItem) => {
                        const SubIcon = subItem.icon;
                        const subItemActive = isSubItemActive(subItem.id);

                        return (
                          <li key={subItem.id}>
                            <button
                              onClick={() => handleItemClick(tab, subItem)}
                              className={`w-full flex items-center space-x-3 pl-6 pr-4 py-2 rounded-lg text-left transition duration-200 ${
                                subItemActive
                                  ? 'bg-blue-50 text-blue-700 border-l-2 border-blue-500 ml-[-2px]'
                                  : 'text-gray-600 hover:bg-gray-50 hover:text-gray-800'
                              }`}
                            >
                              <SubIcon className="w-4 h-4" />
                              <span className="text-sm font-medium">{subItem.label}</span>
                            </button>
                          </li>
                        );
                      })}
                    </ul>
                  </div>
                )}
              </li>
            );
          })}
        </ul>
      </nav>

      <div className="p-4 border-t">
        <div className="flex items-center space-x-3 mb-4">
          <div className="w-8 h-8 bg-gray-300 rounded-full flex items-center justify-center">
            <User className="w-4 h-4 text-gray-600" />
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-sm font-medium text-gray-900 truncate">{user?.full_name}</p>
            <p className="text-xs text-gray-500 truncate">{user?.email}</p>
          </div>
        </div>
        <button
          onClick={logout}
          className="w-full flex items-center space-x-2 px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded-lg transition duration-200"
        >
          <LogOut className="w-4 h-4" />
          <span>Sign out</span>
        </button>
      </div>
    </div>
  );
};

export default Sidebar;

// src/components/Clients/ClientsView.jsx
import React, { useState, useEffect } from 'react';
import { Plus, Search } from 'lucide-react';
import ClientList from './ClientList';
import CreateClientModal from './CreateClientModal';

// Mock data for development
const mockClients = [
  {
    id: 1,
    name: 'John Doe',
    email: 'john@example.com',
    phone: '(555) 123-4567',
    company: 'Acme Corp',
    notes: 'Primary contact for all projects'
  },
  {
    id: 2,
    name: 'Jane Smith',
    email: 'jane@example.com',
    phone: '(555) 987-6543',
    company: 'Tech Solutions',
    notes: 'Lead developer'
  }
];

const ClientsView = () => {
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedClient, setSelectedClient] = useState(null);
  const [clients, setClients] = useState(mockClients);
  const [loading, setLoading] = useState(false);

  const handleCreateClient = async (clientData) => {
    setLoading(true);
    try {
      const newClient = {
        id: clients.length + 1,
        ...clientData
      };
      setClients(prev => [newClient, ...prev]);
      setIsCreateModalOpen(false);
    } catch (error) {
      console.error('Failed to create client:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleEditClient = async (clientData) => {
    setLoading(true);
    try {
      setClients(prev => prev.map(client => 
        client.id === selectedClient.id ? { ...client, ...clientData } : client
      ));
      setIsCreateModalOpen(false);
      setSelectedClient(null);
    } catch (error) {
      console.error('Failed to update client:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteClient = async (clientId) => {
    if (window.confirm('Are you sure you want to delete this client?')) {
      setClients(prev => prev.filter(client => client.id !== clientId));
    }
  };

  const handleEditClick = (client) => {
    setSelectedClient(client);
    setIsCreateModalOpen(true);
  };

  const filteredClients = clients.filter(client =>
    client.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    client.email.toLowerCase().includes(searchQuery.toLowerCase()) ||
    (client.company && client.company.toLowerCase().includes(searchQuery.toLowerCase()))
  );

  return (
    <div className="h-full flex flex-col">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 px-6 py-4">
        <div className="flex items-center justify-between">
          <h1 className="text-2xl font-semibold text-gray-900">Clients</h1>
          
          <div className="flex items-center space-x-4">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
              <input
                type="text"
                placeholder="Search clients"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 w-64"
              />
            </div>
            
            <button
              onClick={() => setIsCreateModalOpen(true)}
              className="btn-primary flex items-center space-x-2"
            >
              <Plus className="w-4 h-4" />
              <span>Add Client</span>
            </button>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-auto">
        <ClientList
          clients={filteredClients}
          loading={loading}
          onEdit={handleEditClick}
          onDelete={handleDeleteClient}
        />
      </div>

      {/* Create/Edit Client Modal */}
      <CreateClientModal
        isOpen={isCreateModalOpen}
        onClose={() => {
          setIsCreateModalOpen(false);
          setSelectedClient(null);
        }}
        onSave={selectedClient ? handleEditClient : handleCreateClient}
        initialClient={selectedClient}
        loading={loading}
      />
    </div>
  );
};

export default ClientsView;

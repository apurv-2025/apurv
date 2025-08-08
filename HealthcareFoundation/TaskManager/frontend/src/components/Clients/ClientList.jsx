// src/components/Clients/ClientList.jsx
import React from 'react';
import { User, Mail, Building, MoreVertical } from 'lucide-react';

const ClientList = ({ clients, loading, onEdit, onDelete }) => {
  if (loading) {
    return (
      <div className="p-6">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {[...Array(6)].map((_, index) => (
            <div key={index} className="card p-4 animate-pulse">
              <div className="h-4 bg-gray-200 rounded mb-3"></div>
              <div className="h-3 bg-gray-200 rounded mb-2"></div>
              <div className="h-3 bg-gray-200 rounded w-2/3"></div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  if (clients.length === 0) {
    return (
      <div className="p-6 text-center">
        <div className="max-w-md mx-auto">
          <User className="w-12 h-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No clients found</h3>
          <p className="text-gray-600">Get started by adding your first client.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {clients.map((client) => (
          <div key={client.id} className="card p-4 hover:shadow-md transition-shadow">
            <div className="flex items-start justify-between mb-3">
              <div className="flex-1">
                <h3 className="font-medium text-gray-900">{client.name}</h3>
                {client.company && (
                  <p className="text-sm text-gray-600 flex items-center mt-1">
                    <Building className="w-4 h-4 mr-1" />
                    {client.company}
                  </p>
                )}
              </div>
              <div className="relative">
                <button className="p-1 hover:bg-gray-100 rounded">
                  <MoreVertical className="w-4 h-4 text-gray-500" />
                </button>
              </div>
            </div>

            <div className="space-y-2 text-sm text-gray-600">
              {client.email && (
                <div className="flex items-center">
                  <Mail className="w-4 h-4 mr-2" />
                  <span>{client.email}</span>
                </div>
              )}
              {client.phone && (
                <div className="flex items-center">
                  <span className="w-4 h-4 mr-2">📞</span>
                  <span>{client.phone}</span>
                </div>
              )}
            </div>

            <div className="mt-4 flex space-x-2">
              <button
                onClick={() => onEdit(client)}
                className="btn-secondary text-xs px-3 py-1"
              >
                Edit
              </button>
              <button
                onClick={() => onDelete(client.id)}
                className="btn-danger text-xs px-3 py-1"
              >
                Delete
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ClientList;

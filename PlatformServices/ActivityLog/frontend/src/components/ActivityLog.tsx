import React, { useState, useEffect } from 'react';
import { Calendar, Clock, MapPin, User, Shield, History, X } from 'lucide-react';

// Types
interface ActivityEvent {
  id: string;
  date: string;
  time: string;
  event: string;
  ipAddress?: string;
  location?: string;
  userId?: string;
  clientName?: string;
  eventType: 'sign_in' | 'hipaa_audit' | 'history';
  details?: Record<string, any>;
}

interface TabConfig {
  id: string;
  label: string;
  icon: React.ReactNode;
  eventType: 'sign_in' | 'hipaa_audit' | 'history';
}

// API Service
class ActivityLogService {
  private baseUrl = 'http://localhost:8001/api';

  async getEvents(eventType: string, filters: Record<string, any> = {}): Promise<ActivityEvent[]> {
    const params = new URLSearchParams({ event_type: eventType, ...filters });
    const response = await fetch(`${this.baseUrl}/activity-events?${params}`);
    if (!response.ok) throw new Error('Failed to fetch events');
    return response.json();
  }

  async createEvent(event: Partial<ActivityEvent>): Promise<ActivityEvent> {
    const response = await fetch(`${this.baseUrl}/activity-events`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(event),
    });
    if (!response.ok) throw new Error('Failed to create event');
    return response.json();
  }

  async getEventDetails(eventId: string): Promise<ActivityEvent> {
    const response = await fetch(`${this.baseUrl}/activity-events/${eventId}`);
    if (!response.ok) throw new Error('Failed to fetch event details');
    return response.json();
  }
}

// EventDetailsModal Component
const EventDetailsModal: React.FC<{
  event: ActivityEvent | null;
  isOpen: boolean;
  onClose: () => void;
}> = ({ event, isOpen, onClose }) => {
  if (!isOpen || !event) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full mx-4 max-h-[80vh] overflow-y-auto">
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <h2 className="text-xl font-semibold text-gray-900">Event Details</h2>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <X className="w-6 h-6" />
          </button>
        </div>
        
        <div className="p-6 space-y-6">
          {/* Basic Event Information */}
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Date</label>
              <p className="text-sm text-gray-900">{event.date}</p>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Time</label>
              <p className="text-sm text-gray-900">{event.time}</p>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Event</label>
            <p className="text-sm text-gray-900">{event.event}</p>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Event Type</label>
            <span className={`inline-flex px-2 py-1 text-xs font-medium rounded-full ${
              event.eventType === 'sign_in' ? 'bg-blue-100 text-blue-800' :
              event.eventType === 'hipaa_audit' ? 'bg-red-100 text-red-800' :
              'bg-green-100 text-green-800'
            }`}>
              {event.eventType.replace('_', ' ').toUpperCase()}
            </span>
          </div>

          {/* Location Information */}
          {(event.ipAddress || event.location) && (
            <div className="border-t border-gray-200 pt-6">
              <h3 className="text-lg font-medium text-gray-900 mb-4">Location Information</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {event.ipAddress && (
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">IP Address</label>
                    <p className="text-sm text-gray-900 flex items-center">
                      <MapPin className="w-4 h-4 mr-2 text-gray-400" />
                      {event.ipAddress}
                    </p>
                  </div>
                )}
                {event.location && (
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Location</label>
                    <p className="text-sm text-gray-900 flex items-center">
                      <MapPin className="w-4 h-4 mr-2 text-gray-400" />
                      {event.location}
                    </p>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Client Information */}
          {event.clientName && (
            <div className="border-t border-gray-200 pt-6">
              <h3 className="text-lg font-medium text-gray-900 mb-4">Client Information</h3>
              <p className="text-sm text-gray-900 flex items-center">
                <User className="w-4 h-4 mr-2 text-gray-400" />
                {event.clientName}
              </p>
            </div>
          )}

          {/* Additional Details */}
          {event.details && Object.keys(event.details).length > 0 && (
            <div className="border-t border-gray-200 pt-6">
              <h3 className="text-lg font-medium text-gray-900 mb-4">Additional Details</h3>
              <div className="bg-gray-50 rounded-lg p-4">
                <pre className="text-sm text-gray-700 whitespace-pre-wrap">
                  {JSON.stringify(event.details, null, 2)}
                </pre>
              </div>
            </div>
          )}

          {/* User Information */}
          <div className="border-t border-gray-200 pt-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">User Information</h3>
            <p className="text-sm text-gray-900">User ID: {event.userId}</p>
          </div>
        </div>

        <div className="flex justify-end p-6 border-t border-gray-200">
          <button
            onClick={onClose}
            className="px-4 py-2 bg-gray-600 text-white rounded-md hover:bg-gray-700 transition-colors"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
};

// EventTable Component
const EventTable: React.FC<{ 
  events: ActivityEvent[]; 
  hideDetails?: boolean;
  onViewDetails?: (event: ActivityEvent) => void;
}> = ({ 
  events, 
  hideDetails = false,
  onViewDetails 
}) => {
  return (
    <div className="overflow-x-auto bg-white rounded-lg shadow">
      <table className="min-w-full divide-y divide-gray-200">
        <thead className="bg-gray-50">
          <tr>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Date
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Time
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Event
            </th>
            {!hideDetails && (
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                Actions
              </th>
            )}
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {events.map((event) => (
            <tr key={event.id} className="hover:bg-gray-50">
              <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                {event.date}
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {event.time}
              </td>
              <td className="px-6 py-4 text-sm text-gray-900">
                <div className="space-y-1">
                  <div>{event.event}</div>
                  {event.ipAddress && (
                    <div className="flex items-center text-xs text-gray-500 space-x-4">
                      <span className="flex items-center">
                        <MapPin className="w-3 h-3 mr-1" />
                        IP Address {event.ipAddress}
                      </span>
                      {event.location && (
                        <span className="flex items-center">
                          <MapPin className="w-3 h-3 mr-1" />
                          {event.location}
                        </span>
                      )}
                    </div>
                  )}
                  {event.clientName && (
                    <div className="flex items-center text-xs text-gray-500">
                      <User className="w-3 h-3 mr-1" />
                      Client: {event.clientName}
                    </div>
                  )}
                </div>
              </td>
              {!hideDetails && (
                <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                  <button 
                    className="text-indigo-600 hover:text-indigo-900 transition-colors"
                    onClick={() => onViewDetails?.(event)}
                  >
                    View Details
                  </button>
                </td>
              )}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

// Filters Component
const ActivityFilters: React.FC<{
  onFilterChange: (filters: Record<string, any>) => void;
  showTimeFilter?: boolean;
}> = ({ onFilterChange, showTimeFilter = true }) => {
  const [filters, setFilters] = useState({
    dateRange: 'all',
    search: '',
  });

  const handleFilterChange = (key: string, value: any) => {
    const newFilters = { ...filters, [key]: value };
    setFilters(newFilters);
    onFilterChange(newFilters);
  };

  return (
    <div className="bg-white p-4 rounded-lg shadow mb-6">
      <div className="flex flex-wrap gap-4 items-center">
        <div className="flex items-center space-x-2">
          <select
            value={filters.dateRange}
            onChange={(e) => handleFilterChange('dateRange', e.target.value)}
            className="border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
          >
            <option value="all">All Time</option>
            <option value="today">Today</option>
            <option value="week">This Week</option>
            <option value="month">This Month</option>
          </select>
          <Calendar className="w-4 h-4 text-gray-400" />
        </div>
        
        <div className="flex-1 min-w-64">
          <input
            type="text"
            placeholder="Search events..."
            value={filters.search}
            onChange={(e) => handleFilterChange('search', e.target.value)}
            className="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </div>

        <button className="text-sm text-gray-600 hover:text-gray-900 border border-gray-300 rounded-md px-3 py-2">
          Hide details
        </button>
      </div>
    </div>
  );
};

// Individual Tab Components
const SignInEventsTab: React.FC<{ 
  events: ActivityEvent[];
  onViewDetails: (event: ActivityEvent) => void;
}> = ({ events, onViewDetails }) => {
  return (
    <div>
      <div className="mb-4">
        <h3 className="text-lg font-medium text-gray-900">Sign In Events</h3>
        <p className="text-sm text-gray-500">View all authentication and session events</p>
      </div>
      <EventTable events={events} onViewDetails={onViewDetails} />
    </div>
  );
};

const HIPAAAuditLogTab: React.FC<{ 
  events: ActivityEvent[];
  onViewDetails: (event: ActivityEvent) => void;
}> = ({ events, onViewDetails }) => {
  return (
    <div>
      <div className="mb-4">
        <h3 className="text-lg font-medium text-gray-900">HIPAA Audit Log</h3>
        <p className="text-sm text-gray-500">Track access to protected health information</p>
      </div>
      <EventTable events={events} onViewDetails={onViewDetails} />
    </div>
  );
};

const HistoryTab: React.FC<{ 
  events: ActivityEvent[];
  onViewDetails: (event: ActivityEvent) => void;
}> = ({ events, onViewDetails }) => {
  return (
    <div>
      <div className="mb-4">
        <h3 className="text-lg font-medium text-gray-900">Account History</h3>
        <p className="text-sm text-gray-500">View all account changes and updates</p>
      </div>
      <EventTable events={events} onViewDetails={onViewDetails} />
    </div>
  );
};

// Main ActivityLog Component
const ActivityLog: React.FC = () => {
  const [activeTab, setActiveTab] = useState('history');
  const [events, setEvents] = useState<ActivityEvent[]>([]);
  const [loading, setLoading] = useState(false);
  const [filters, setFilters] = useState<Record<string, any>>({});
  const [selectedEvent, setSelectedEvent] = useState<ActivityEvent | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [loadingDetails, setLoadingDetails] = useState(false);

  const service = new ActivityLogService();

  const tabs: TabConfig[] = [
    { id: 'history', label: 'History', icon: <History className="w-4 h-4" />, eventType: 'history' },
    { id: 'sign_in', label: 'Sign In Events', icon: <User className="w-4 h-4" />, eventType: 'sign_in' },
    { id: 'hipaa', label: 'HIPAA Audit Log', icon: <Shield className="w-4 h-4" />, eventType: 'hipaa_audit' },
  ];

  // Mock data for demonstration
  const mockEvents: Record<string, ActivityEvent[]> = {
    history: [
      {
        id: '1',
        date: '06/22/2025',
        time: '10:19 PM (ET)',
        event: "You updated team member John Dalton's information",
        eventType: 'history',
        ipAddress: '173.76.171.142',
        location: 'Westford, United States',
        userId: 'user_123',
        details: {
          action: "update_team_member",
          resource: "team_member",
          resource_id: "team_123",
          changes: ["email", "phone_number"],
          browser: "Chrome 91.0.4472.124"
        }
      },
      {
        id: '2',
        date: '06/22/2025',
        time: '10:18 PM (ET)',
        event: 'You created Superbill SB #0001 on 06/22/2025 for client Jamie D. Appleseed',
        eventType: 'history',
        clientName: 'Jamie D. Appleseed',
        userId: 'user_456'
      },
      {
        id: '3',
        date: '06/22/2025',
        time: '10:18 PM (ET)',
        event: 'You created Statement STMT #0001 on 06/22/2025 for client Jamie D. Appleseed',
        eventType: 'history',
        clientName: 'Jamie D. Appleseed'
      },
      {
        id: '4',
        date: '06/22/2025',
        time: '10:18 PM (ET)',
        event: 'You added a GAD-7 for Jamie D. Appleseed',
        eventType: 'history',
        clientName: 'Jamie D. Appleseed',
        ipAddress: '173.76.171.142',
        location: 'Westford, United States'
      }
    ],
    sign_in: [
      {
        id: '5',
        date: '06/24/2025',
        time: '8:58 PM (ET)',
        event: 'You signed in successfully to SimplePractice web app',
        eventType: 'sign_in',
        ipAddress: '173.76.171.142',
        location: 'Westford, United States'
      },
      {
        id: '6',
        date: '06/24/2025',
        time: '8:58 PM (ET)',
        event: 'You signed in successfully to SimplePractice account app',
        eventType: 'sign_in',
        ipAddress: '173.76.171.142',
        location: 'Westford, United States'
      },
      {
        id: '7',
        date: '06/24/2025',
        time: '8:07 PM (ET)',
        event: 'You signed out successfully from SimplePractice web app',
        eventType: 'sign_in',
        ipAddress: '173.76.171.142',
        location: 'Westford, United States'
      },
      {
        id: '8',
        date: '06/24/2025',
        time: '5:43 PM (ET)',
        event: 'You failed to sign in to SimplePractice account app due to invalid password',
        eventType: 'sign_in',
        ipAddress: '173.76.171.142',
        location: 'Westford, United States'
      }
    ],
    hipaa: [
      {
        id: '9',
        date: '06/24/2025',
        time: '9:01 PM (ET)',
        event: 'You viewed the client and contacts page',
        eventType: 'hipaa_audit',
        ipAddress: '173.76.171.142',
        location: 'Westford, United States'
      },
      {
        id: '10',
        date: '06/24/2025',
        time: '8:58 PM (ET)',
        event: 'You viewed a note for Jamie D. Appleseed',
        eventType: 'hipaa_audit',
        clientName: 'Jamie D. Appleseed',
        ipAddress: '173.76.171.142',
        location: 'Westford, United States'
      },
      {
        id: '11',
        date: '06/23/2025',
        time: '10:59 AM (ET)',
        event: 'You viewed the inquiries list',
        eventType: 'hipaa_audit',
        ipAddress: '173.76.171.142',
        location: 'Westford, United States'
      },
      {
        id: '12',
        date: '06/23/2025',
        time: '10:27 AM (ET)',
        event: 'You viewed the Payment Reports report 05/23/2025 - 06/23/2025',
        eventType: 'hipaa_audit',
        ipAddress: '173.76.171.142',
        location: 'Westford, United States'
      }
    ]
  };

  const loadEvents = async (tabType: string) => {
    setLoading(true);
    try {
      // In a real app, this would be: await service.getEvents(tabType, filters);
      // For demo, use mock data
      await new Promise(resolve => setTimeout(resolve, 300)); // Simulate API call
      setEvents(mockEvents[tabType] || []);
    } catch (error) {
      console.error('Failed to load events:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadEvents(activeTab);
  }, [activeTab, filters]);

  const handleTabChange = (tabId: string) => {
    setActiveTab(tabId);
  };

  const handleFilterChange = (newFilters: Record<string, any>) => {
    setFilters(newFilters);
  };

  const handleViewDetails = async (event: ActivityEvent) => {
    setLoadingDetails(true);
    try {
      // In a real app, fetch fresh details from the API:
      // const detailedEvent = await service.getEventDetails(event.id);
      // For demo, add some mock details to the existing event
      const eventWithDetails = {
        ...event,
        details: event.details || {
          action: "view",
          resource: "client_profile",
          timestamp: new Date().toISOString(),
          metadata: {
            browser: "Chrome 91.0.4472.124",
            userAgent: "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
          }
        }
      };
      setSelectedEvent(eventWithDetails);
      setIsModalOpen(true);
    } catch (error) {
      console.error('Failed to load event details:', error);
    } finally {
      setLoadingDetails(false);
    }
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setSelectedEvent(null);
  };

  const renderTabContent = () => {
    if (loading) {
      return (
        <div className="flex justify-center items-center h-64">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
        </div>
      );
    }

    switch (activeTab) {
      case 'sign_in':
        return <SignInEventsTab events={events} onViewDetails={handleViewDetails} />;
      case 'hipaa':
        return <HIPAAAuditLogTab events={events} onViewDetails={handleViewDetails} />;
      case 'history':
      default:
        return <HistoryTab events={events} onViewDetails={handleViewDetails} />;
    }
  };

  return (
    <div className="max-w-7xl mx-auto p-6">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Account Activity</h1>
        <p className="text-gray-600">Monitor and review all account activities and security events</p>
      </div>

      {/* Tab Navigation */}
      <div className="border-b border-gray-200 mb-6">
        <nav className="-mb-px flex space-x-8">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => handleTabChange(tab.id)}
              className={`py-2 px-1 border-b-2 font-medium text-sm flex items-center space-x-2 ${
                activeTab === tab.id
                  ? 'border-indigo-500 text-indigo-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              {tab.icon}
              <span>{tab.label}</span>
            </button>
          ))}
        </nav>
      </div>

      {/* Filters */}
      <ActivityFilters onFilterChange={handleFilterChange} />

      {/* Tab Content */}
      <div className="bg-gray-50 rounded-lg p-6">
        {renderTabContent()}
      </div>

      {/* Event Details Modal */}
      <EventDetailsModal 
        event={selectedEvent}
        isOpen={isModalOpen}
        onClose={handleCloseModal}
      />
    </div>
  );
};

export default ActivityLog;

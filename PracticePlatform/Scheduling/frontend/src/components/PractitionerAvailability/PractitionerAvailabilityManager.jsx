import React, { useState, useEffect } from 'react';
import { Calendar, Clock, User, Plus, Trash2, Edit, Save, X } from 'lucide-react';
import { toast } from 'react-toastify';
import practitionerAvailabilityService from '../../services/practitionerAvailabilityService';

const PractitionerAvailabilityManager = ({ practitioner, onClose, onUpdate }) => {
  const [availability, setAvailability] = useState([]);
  const [loading, setLoading] = useState(false);
  const [showAddForm, setShowAddForm] = useState(false);
  const [showWeeklyPattern, setShowWeeklyPattern] = useState(false);
  const [editingId, setEditingId] = useState(null);
  const [formData, setFormData] = useState({
    availability_date: '',
    start_time: '09:00',
    end_time: '17:00',
    notes: ''
  });
  const [weeklyPattern, setWeeklyPattern] = useState({
    monday: { enabled: false, startTime: '09:00', endTime: '17:00' },
    tuesday: { enabled: false, startTime: '09:00', endTime: '17:00' },
    wednesday: { enabled: false, startTime: '09:00', endTime: '17:00' },
    thursday: { enabled: false, startTime: '09:00', endTime: '17:00' },
    friday: { enabled: false, startTime: '09:00', endTime: '17:00' },
    saturday: { enabled: false, startTime: '09:00', endTime: '17:00' },
    sunday: { enabled: false, startTime: '09:00', endTime: '17:00' }
  });

  useEffect(() => {
    if (practitioner) {
      fetchAvailability();
    }
  }, [practitioner]);

  const fetchAvailability = async () => {
    if (!practitioner?.id) return;
    
    setLoading(true);
    try {
      const data = await practitionerAvailabilityService.getPractitionerAvailability(practitioner.id);
      setAvailability(data);
    } catch (error) {
      toast.error('Failed to fetch availability');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      const availabilityData = {
        ...formData,
        practitioner_id: practitioner.id
      };
      
      if (editingId) {
        await practitionerAvailabilityService.updateAvailability(editingId, formData);
        toast.success('Availability updated successfully');
      } else {
        await practitionerAvailabilityService.createAvailability(availabilityData);
        toast.success('Availability added successfully');
      }
      
      resetForm();
      fetchAvailability();
      if (onUpdate) onUpdate();
    } catch (error) {
      toast.error('Failed to save availability');
    }
  };

  const handleWeeklyPatternSubmit = async (e) => {
    e.preventDefault();
    
    try {
      const bulkData = practitionerAvailabilityService.createWeeklyPattern(practitioner.id, weeklyPattern);
      await practitionerAvailabilityService.createBulkAvailability(bulkData);
      toast.success('Weekly pattern created successfully');
      setShowWeeklyPattern(false);
      fetchAvailability();
      if (onUpdate) onUpdate();
    } catch (error) {
      toast.error('Failed to create weekly pattern');
    }
  };

  const handleDelete = async (availabilityId) => {
    if (!window.confirm('Are you sure you want to delete this availability?')) return;
    
    try {
      await practitionerAvailabilityService.deleteAvailability(availabilityId);
      toast.success('Availability deleted successfully');
      fetchAvailability();
      if (onUpdate) onUpdate();
    } catch (error) {
      toast.error('Failed to delete availability');
    }
  };

  const handleEdit = (item) => {
    setEditingId(item.id);
    setFormData({
      availability_date: item.availability_date,
      start_time: item.start_time,
      end_time: item.end_time,
      notes: item.notes || ''
    });
    setShowAddForm(true);
  };

  const resetForm = () => {
    setFormData({
      availability_date: '',
      start_time: '09:00',
      end_time: '17:00',
      notes: ''
    });
    setEditingId(null);
    setShowAddForm(false);
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      weekday: 'short',
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  const formatTime = (timeString) => {
    return new Date(`2000-01-01T${timeString}`).toLocaleTimeString('en-US', {
      hour: 'numeric',
      minute: '2-digit',
      hour12: true
    });
  };

  if (!practitioner) return null;

  return (
    <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div className="relative top-20 mx-auto p-5 border w-full max-w-4xl shadow-lg rounded-md bg-white">
        <div className="mt-3">
          {/* Header */}
          <div className="flex items-center justify-between mb-6">
            <div>
              <h3 className="text-lg font-medium text-gray-900">
                Manage Availability - {practitioner.family_name} {practitioner.given_names?.join(' ') || ''}
              </h3>
              <p className="text-sm text-gray-600">Set and manage practitioner availability</p>
            </div>
            <button
              onClick={onClose}
              className="p-2 text-gray-400 hover:text-gray-600"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          {/* Action Buttons */}
          <div className="flex gap-3 mb-6">
            <button
              onClick={() => setShowAddForm(true)}
              className="btn-primary flex items-center gap-2"
            >
              <Plus className="w-4 h-4" />
              Add Single Day
            </button>
            <button
              onClick={() => setShowWeeklyPattern(true)}
              className="btn-secondary flex items-center gap-2"
            >
              <Calendar className="w-4 h-4" />
              Weekly Pattern
            </button>
          </div>

          {/* Add/Edit Form */}
          {showAddForm && (
            <div className="mb-6 p-4 border rounded-lg bg-gray-50">
              <h4 className="font-medium text-gray-900 mb-4">
                {editingId ? 'Edit Availability' : 'Add Availability'}
              </h4>
              <form onSubmit={handleSubmit} className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div>
                    <label className="form-label">Date</label>
                    <input
                      type="date"
                      value={formData.availability_date}
                      onChange={(e) => setFormData({ ...formData, availability_date: e.target.value })}
                      className="input"
                      required
                    />
                  </div>
                  <div>
                    <label className="form-label">Start Time</label>
                    <input
                      type="time"
                      value={formData.start_time}
                      onChange={(e) => setFormData({ ...formData, start_time: e.target.value })}
                      className="input"
                      required
                    />
                  </div>
                  <div>
                    <label className="form-label">End Time</label>
                    <input
                      type="time"
                      value={formData.end_time}
                      onChange={(e) => setFormData({ ...formData, end_time: e.target.value })}
                      className="input"
                      required
                    />
                  </div>
                </div>
                <div>
                  <label className="form-label">Notes</label>
                  <textarea
                    value={formData.notes}
                    onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
                    className="input"
                    rows="2"
                    placeholder="Optional notes..."
                  />
                </div>
                <div className="flex gap-3">
                  <button type="submit" className="btn-primary flex items-center gap-2">
                    <Save className="w-4 h-4" />
                    {editingId ? 'Update' : 'Add'}
                  </button>
                  <button type="button" onClick={resetForm} className="btn-secondary">
                    Cancel
                  </button>
                </div>
              </form>
            </div>
          )}

          {/* Weekly Pattern Form */}
          {showWeeklyPattern && (
            <div className="mb-6 p-4 border rounded-lg bg-gray-50">
              <h4 className="font-medium text-gray-900 mb-4">Weekly Availability Pattern</h4>
              <form onSubmit={handleWeeklyPatternSubmit} className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                  {Object.entries(weeklyPattern).map(([day, config]) => (
                    <div key={day} className="p-3 border rounded-lg">
                      <div className="flex items-center gap-2 mb-3">
                        <input
                          type="checkbox"
                          checked={config.enabled}
                          onChange={(e) => setWeeklyPattern({
                            ...weeklyPattern,
                            [day]: { ...config, enabled: e.target.checked }
                          })}
                          className="rounded"
                        />
                        <label className="font-medium capitalize">{day}</label>
                      </div>
                      {config.enabled && (
                        <div className="space-y-2">
                          <div>
                            <label className="text-sm text-gray-600">Start</label>
                            <input
                              type="time"
                              value={config.startTime}
                              onChange={(e) => setWeeklyPattern({
                                ...weeklyPattern,
                                [day]: { ...config, startTime: e.target.value }
                              })}
                              className="input text-sm"
                            />
                          </div>
                          <div>
                            <label className="text-sm text-gray-600">End</label>
                            <input
                              type="time"
                              value={config.endTime}
                              onChange={(e) => setWeeklyPattern({
                                ...weeklyPattern,
                                [day]: { ...config, endTime: e.target.value }
                              })}
                              className="input text-sm"
                            />
                          </div>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
                <div className="flex gap-3">
                  <button type="submit" className="btn-primary">
                    Create Weekly Pattern
                  </button>
                  <button 
                    type="button" 
                    onClick={() => setShowWeeklyPattern(false)} 
                    className="btn-secondary"
                  >
                    Cancel
                  </button>
                </div>
              </form>
            </div>
          )}

          {/* Availability List */}
          <div>
            <h4 className="font-medium text-gray-900 mb-4">Current Availability</h4>
            {loading ? (
              <div className="text-center py-8">
                <div className="spinner w-8 h-8 mx-auto mb-4"></div>
                <p className="text-gray-600">Loading availability...</p>
              </div>
            ) : availability.length === 0 ? (
              <div className="text-center py-8 text-gray-500">
                <Calendar className="w-12 h-12 mx-auto mb-4 text-gray-300" />
                <p>No availability set</p>
                <p className="text-sm">Add availability to get started</p>
              </div>
            ) : (
              <div className="space-y-2 max-h-96 overflow-y-auto">
                {availability.map((item) => (
                  <div key={item.id} className="flex items-center justify-between p-3 border rounded-lg hover:bg-gray-50">
                    <div className="flex items-center gap-4">
                      <div className="flex items-center gap-2">
                        <Calendar className="w-4 h-4 text-gray-400" />
                        <span className="font-medium">{formatDate(item.availability_date)}</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <Clock className="w-4 h-4 text-gray-400" />
                        <span>{formatTime(item.start_time)} - {formatTime(item.end_time)}</span>
                      </div>
                      {item.notes && (
                        <span className="text-sm text-gray-600">({item.notes})</span>
                      )}
                    </div>
                    <div className="flex items-center gap-2">
                      <button
                        onClick={() => handleEdit(item)}
                        className="p-1 text-blue-600 hover:text-blue-800"
                      >
                        <Edit className="w-4 h-4" />
                      </button>
                      <button
                        onClick={() => handleDelete(item.id)}
                        className="p-1 text-red-600 hover:text-red-800"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default PractitionerAvailabilityManager; 
import React, { useState, useEffect } from 'react';
import { User, Phone, Mail, MapPin, Calendar, Shield, AlertTriangle, Edit, Save, X, Camera, Upload, Plus } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import { useAPI } from '../hooks/useAPI';

const Profile = () => {
  const { user } = useAuth();
  const { put } = useAPI();
  const [isEditing, setIsEditing] = useState(false);
  const [showInsuranceUpload, setShowInsuranceUpload] = useState(false);
  const [insuranceCards, setInsuranceCards] = useState([]);
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    phone: '',
    address: '',
    emergency_contact_name: '',
    emergency_contact_phone: ''
  });

  useEffect(() => {
    if (user) {
      setFormData({
        first_name: user.first_name || '',
        last_name: user.last_name || '',
        phone: user.phone || '',
        address: user.address || '',
        emergency_contact_name: user.emergency_contact_name || '',
        emergency_contact_phone: user.emergency_contact_phone || ''
      });
    }

    // Load mock insurance cards
    const mockInsuranceCards = [
      {
        id: 1,
        insuranceCompany: 'Blue Cross Blue Shield',
        planName: 'Premium Health Plan',
        type: 'Primary',
        policyNumber: 'BC123456789',
        memberId: 'M987654321',
        effectiveDate: '2024-01-01',
        expirationDate: '2024-12-31',
        frontImage: '/api/placeholder/300/200', // Would be actual image URL in real app
        backImage: '/api/placeholder/300/200',
        uploadDate: '2024-01-15',
        status: 'verified'
      }
    ];
    setInsuranceCards(mockInsuranceCards);
  }, [user]);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSave = async () => {
    try {
      await put('/users/me', formData);
      setIsEditing(false);
      // You might want to refresh user data here
    } catch (error) {
      console.error('Error updating profile:', error);
    }
  };

  const handleCancel = () => {
    setFormData({
      first_name: user.first_name || '',
      last_name: user.last_name || '',
      phone: user.phone || '',
      address: user.address || '',
      emergency_contact_name: user.emergency_contact_name || '',
      emergency_contact_phone: user.emergency_contact_phone || ''
    });
    setIsEditing(false);
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'Not provided';
    return new Date(dateString).toLocaleDateString();
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-gray-800">Profile</h2>
        {!isEditing ? (
          <button
            onClick={() => setIsEditing(true)}
            className="flex items-center space-x-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
          >
            <Edit className="w-4 h-4" />
            <span>Edit Profile</span>
          </button>
        ) : (
          <div className="flex space-x-2">
            <button
              onClick={handleSave}
              className="flex items-center space-x-2 bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors"
            >
              <Save className="w-4 h-4" />
              <span>Save</span>
            </button>
            <button
              onClick={handleCancel}
              className="flex items-center space-x-2 bg-gray-600 text-white px-4 py-2 rounded-lg hover:bg-gray-700 transition-colors"
            >
              <X className="w-4 h-4" />
              <span>Cancel</span>
            </button>
          </div>
        )}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Personal Information */}
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center space-x-3 mb-6">
            <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
              <User className="w-6 h-6 text-blue-600" />
            </div>
            <h3 className="text-lg font-semibold text-gray-800">Personal Information</h3>
          </div>

          <div className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">First Name</label>
                {isEditing ? (
                  <input
                    type="text"
                    name="first_name"
                    value={formData.first_name}
                    onChange={handleInputChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                ) : (
                  <p className="text-gray-900">{user?.first_name || 'Not provided'}</p>
                )}
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Last Name</label>
                {isEditing ? (
                  <input
                    type="text"
                    name="last_name"
                    value={formData.last_name}
                    onChange={handleInputChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                ) : (
                  <p className="text-gray-900">{user?.last_name || 'Not provided'}</p>
                )}
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
              <div className="flex items-center space-x-2">
                <Mail className="w-4 h-4 text-gray-400" />
                <p className="text-gray-900">{user?.email}</p>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Phone</label>
              {isEditing ? (
                <input
                  type="tel"
                  name="phone"
                  value={formData.phone}
                  onChange={handleInputChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              ) : (
                <div className="flex items-center space-x-2">
                  <Phone className="w-4 h-4 text-gray-400" />
                  <p className="text-gray-900">{user?.phone || 'Not provided'}</p>
                </div>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Address</label>
              {isEditing ? (
                <textarea
                  name="address"
                  value={formData.address}
                  onChange={handleInputChange}
                  rows="3"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              ) : (
                <div className="flex items-start space-x-2">
                  <MapPin className="w-4 h-4 text-gray-400 mt-1" />
                  <p className="text-gray-900">{user?.address || 'Not provided'}</p>
                </div>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Date of Birth</label>
              <div className="flex items-center space-x-2">
                <Calendar className="w-4 h-4 text-gray-400" />
                <p className="text-gray-900">{formatDate(user?.date_of_birth)}</p>
              </div>
            </div>
          </div>
        </div>

        {/* Insurance Cards */}
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
                <Shield className="w-6 h-6 text-blue-600" />
              </div>
              <h3 className="text-lg font-semibold text-gray-800">Insurance Cards</h3>
            </div>
            <button
              onClick={() => setShowInsuranceUpload(true)}
              className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors flex items-center"
            >
              <Plus className="w-4 h-4 mr-2" />
              Upload Card
            </button>
          </div>

          {insuranceCards.length === 0 ? (
            <div className="text-center py-8">
              <Shield className="w-12 h-12 text-gray-300 mx-auto mb-4" />
              <p className="text-gray-500 mb-4">No insurance cards uploaded yet</p>
              <button
                onClick={() => setShowInsuranceUpload(true)}
                className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                Upload Your First Insurance Card
              </button>
            </div>
          ) : (
            <div className="space-y-4">
              {insuranceCards.map(card => (
                <div key={card.id} className="border border-gray-200 rounded-lg p-4">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center space-x-2 mb-2">
                        <Shield className="w-5 h-5 text-blue-600" />
                        <h4 className="font-semibold text-gray-900">{card.insuranceCompany}</h4>
                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                          card.status === 'verified' ? 'bg-green-100 text-green-800' :
                          card.status === 'pending' ? 'bg-yellow-100 text-yellow-800' :
                          'bg-red-100 text-red-800'
                        }`}>
                          {card.status}
                        </span>
                      </div>
                      
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-sm text-gray-600">
                        <div>
                          <span className="font-medium">Plan:</span> {card.planName}
                        </div>
                        <div>
                          <span className="font-medium">Type:</span> {card.type}
                        </div>
                        <div>
                          <span className="font-medium">Policy #:</span> {card.policyNumber}
                        </div>
                        <div>
                          <span className="font-medium">Member ID:</span> {card.memberId}
                        </div>
                        <div>
                          <span className="font-medium">Valid:</span> {card.effectiveDate} - {card.expirationDate}
                        </div>
                        <div>
                          <span className="font-medium">Uploaded:</span> {card.uploadDate}
                        </div>
                      </div>
                    </div>
                    
                    <div className="flex space-x-2 ml-4">
                      <button className="p-2 text-gray-400 hover:text-blue-600" title="View Images">
                        <Camera className="w-4 h-4" />
                      </button>
                      <button className="p-2 text-gray-400 hover:text-gray-600" title="Edit">
                        <Edit className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Emergency Contact */}
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center space-x-3 mb-6">
            <div className="w-10 h-10 bg-red-100 rounded-full flex items-center justify-center">
              <AlertTriangle className="w-6 h-6 text-red-600" />
            </div>
            <h3 className="text-lg font-semibold text-gray-800">Emergency Contact</h3>
          </div>

          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Contact Name</label>
              {isEditing ? (
                <input
                  type="text"
                  name="emergency_contact_name"
                  value={formData.emergency_contact_name}
                  onChange={handleInputChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              ) : (
                <p className="text-gray-900">{user?.emergency_contact_name || 'Not provided'}</p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Contact Phone</label>
              {isEditing ? (
                <input
                  type="tel"
                  name="emergency_contact_phone"
                  value={formData.emergency_contact_phone}
                  onChange={handleInputChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              ) : (
                <div className="flex items-center space-x-2">
                  <Phone className="w-4 h-4 text-gray-400" />
                  <p className="text-gray-900">{user?.emergency_contact_phone || 'Not provided'}</p>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Account Information */}
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-800 mb-4">Account Information</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
          <div>
            <p className="text-gray-600">Member Since</p>
            <p className="font-medium text-gray-900">{formatDate(user?.created_at)}</p>
          </div>
          <div>
            <p className="text-gray-600">Account Status</p>
            <span className={`inline-flex px-2 py-1 text-xs font-medium rounded-full ${
              user?.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
            }`}>
              {user?.is_active ? 'Active' : 'Inactive'}
            </span>
          </div>
          <div>
            <p className="text-gray-600">Last Updated</p>
            <p className="font-medium text-gray-900">{formatDate(user?.updated_at)}</p>
          </div>
        </div>
      </div>

      {/* Insurance Upload Modal */}
      {showInsuranceUpload && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6 border-b border-gray-200">
              <div className="flex items-center justify-between">
                <h2 className="text-xl font-semibold text-gray-900">Upload Insurance Card</h2>
                <button 
                  onClick={() => setShowInsuranceUpload(false)}
                  className="text-gray-400 hover:text-gray-600"
                >
                  <X className="w-6 h-6" />
                </button>
              </div>
              <p className="text-gray-600 mt-2">Upload clear photos of both sides of your insurance card</p>
            </div>

            <form className="p-6 space-y-6" onSubmit={(e) => {
              e.preventDefault();
              alert('Insurance card upload functionality coming soon!');
              setShowInsuranceUpload(false);
            }}>
              {/* Basic Information */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Insurance Company *
                  </label>
                  <input
                    type="text"
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Plan Name *
                  </label>
                  <input
                    type="text"
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Policy Number *
                  </label>
                  <input
                    type="text"
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Member ID
                  </label>
                  <input
                    type="text"
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>
              </div>

              {/* Image Upload */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-4">Insurance Card Images *</label>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {/* Front of Card */}
                  <div>
                    <label className="block text-sm font-medium text-gray-600 mb-2">Front of Card</label>
                    <div className="border-2 border-dashed border-gray-300 rounded-lg p-4 text-center hover:border-blue-400 transition-colors">
                      <Camera className="mx-auto h-8 w-8 text-gray-400 mb-2" />
                      <label className="cursor-pointer">
                        <span className="text-sm font-medium text-gray-900">Upload Front</span>
                        <span className="block text-xs text-gray-500 mt-1">JPG, PNG up to 5MB</span>
                        <input type="file" className="sr-only" accept="image/*" />
                      </label>
                    </div>
                  </div>

                  {/* Back of Card */}
                  <div>
                    <label className="block text-sm font-medium text-gray-600 mb-2">Back of Card</label>
                    <div className="border-2 border-dashed border-gray-300 rounded-lg p-4 text-center hover:border-blue-400 transition-colors">
                      <Camera className="mx-auto h-8 w-8 text-gray-400 mb-2" />
                      <label className="cursor-pointer">
                        <span className="text-sm font-medium text-gray-900">Upload Back</span>
                        <span className="block text-xs text-gray-500 mt-1">JPG, PNG up to 5MB</span>
                        <input type="file" className="sr-only" accept="image/*" />
                      </label>
                    </div>
                  </div>
                </div>
              </div>

              {/* Upload Tips */}
              <div className="bg-blue-50 rounded-lg p-4">
                <div className="flex items-start space-x-2">
                  <AlertTriangle className="w-5 h-5 text-blue-600 mt-0.5" />
                  <div className="text-sm text-blue-700">
                    <p className="font-medium mb-2">Tips for clear insurance card photos:</p>
                    <ul className="list-disc list-inside space-y-1">
                      <li>Ensure all text is clearly visible and readable</li>
                      <li>Take photos in good lighting without shadows</li>
                      <li>Include the entire card in the frame</li>
                      <li>Avoid glare and reflections</li>
                      <li>Hold the camera steady to prevent blurring</li>
                    </ul>
                  </div>
                </div>
              </div>

              {/* Submit Buttons */}
              <div className="flex space-x-4 pt-6">
                <button
                  type="button"
                  onClick={() => setShowInsuranceUpload(false)}
                  className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                >
                  Upload Insurance Card
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default Profile; 
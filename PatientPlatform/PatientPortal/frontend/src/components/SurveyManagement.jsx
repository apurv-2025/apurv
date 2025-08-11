import React, { useState, useEffect } from 'react';
import { 
  BarChart3, PieChart, TrendingUp, Users, MessageSquare, Calendar, 
  Star, Download, Filter, Search, Eye, Edit, Trash2, Plus, RefreshCw
} from 'lucide-react';
import { surveyService } from '../services/surveyService';

const SurveyManagement = () => {
  const [surveys, setSurveys] = useState([]);
  const [responses, setResponses] = useState([]);
  const [analytics, setAnalytics] = useState({});
  const [loading, setLoading] = useState(true);
  const [selectedSurvey, setSelectedSurvey] = useState(null);
  const [filterType, setFilterType] = useState('all');
  const [dateRange, setDateRange] = useState('30');

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      const [surveysData, responsesData] = await Promise.all([
        surveyService.getSurveys(),
        surveyService.getSurveyResponses()
      ]);
      
      setSurveys(surveysData);
      setResponses(responsesData);
      
      // Calculate analytics
      const analyticsData = {};
      for (const survey of surveysData) {
        const surveyResponses = responsesData.filter(r => r.survey_id === survey.id);
        analyticsData[survey.id] = {
          totalResponses: surveyResponses.length,
          averageRating: surveyResponses.length > 0 
            ? surveyResponses.reduce((sum, r) => sum + (r.overall_rating || 0), 0) / surveyResponses.length
            : 0,
          responseRate: 0, // Would need total potential respondents
          recentResponses: surveyResponses.slice(-5)
        };
      }
      setAnalytics(analyticsData);
    } catch (error) {
      console.error('Error loading survey data:', error);
    } finally {
      setLoading(false);
    }
  };

  const filteredSurveys = surveys.filter(survey => {
    if (filterType !== 'all' && survey.survey_type !== filterType) return false;
    return true;
  });

  const getSurveyTypeIcon = (type) => {
    switch (type) {
      case 'visit': return Calendar;
      case 'ai_chat': return MessageSquare;
      default: return Users;
    }
  };

  const getSurveyTypeColor = (type) => {
    switch (type) {
      case 'visit': return 'bg-blue-100 text-blue-800 border-blue-200';
      case 'ai_chat': return 'bg-green-100 text-green-800 border-green-200';
      default: return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  const renderRatingStars = (rating) => {
    return (
      <div className="flex items-center space-x-1">
        {[1, 2, 3, 4, 5].map((star) => (
          <Star
            key={star}
            className={`w-4 h-4 ${star <= rating ? 'text-yellow-400 fill-current' : 'text-gray-300'}`}
          />
        ))}
        <span className="ml-1 text-sm text-gray-600">({rating.toFixed(1)})</span>
      </div>
    );
  };

  const SurveyCard = ({ survey }) => {
    const surveyAnalytics = analytics[survey.id] || {};
    const Icon = getSurveyTypeIcon(survey.survey_type);

    return (
      <div className="bg-white rounded-lg border border-gray-200 p-6 hover:shadow-md transition-shadow">
        <div className="flex justify-between items-start mb-4">
          <div className="flex items-center space-x-3">
            <div className="w-12 h-12 bg-primary-100 rounded-full flex items-center justify-center">
              <Icon className="w-6 h-6 text-primary-600" />
            </div>
            <div>
              <h3 className="font-semibold text-gray-900">{survey.title}</h3>
              <p className="text-sm text-gray-500">{survey.description}</p>
            </div>
          </div>
          <div className="flex items-center space-x-2">
            <span className={`px-2 py-1 text-xs font-medium rounded-full border ${getSurveyTypeColor(survey.survey_type)}`}>
              {survey.survey_type.replace('_', ' ')}
            </span>
            <span className={`px-2 py-1 text-xs font-medium rounded-full ${
              survey.is_active ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
            }`}>
              {survey.is_active ? 'Active' : 'Inactive'}
            </span>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
          <div className="text-center p-3 bg-blue-50 rounded-lg">
            <div className="text-2xl font-bold text-blue-600">{surveyAnalytics.totalResponses}</div>
            <div className="text-sm text-blue-600">Total Responses</div>
          </div>
          <div className="text-center p-3 bg-green-50 rounded-lg">
            <div className="text-2xl font-bold text-green-600">
              {surveyAnalytics.averageRating > 0 ? surveyAnalytics.averageRating.toFixed(1) : 'N/A'}
            </div>
            <div className="text-sm text-green-600">Avg Rating</div>
          </div>
          <div className="text-center p-3 bg-purple-50 rounded-lg">
            <div className="text-2xl font-bold text-purple-600">
              {surveyAnalytics.responseRate > 0 ? `${surveyAnalytics.responseRate}%` : 'N/A'}
            </div>
            <div className="text-sm text-purple-600">Response Rate</div>
          </div>
        </div>

        <div className="border-t border-gray-100 pt-4">
          <div className="flex justify-between items-center">
            <div className="text-sm text-gray-600">
              Created: {formatDate(survey.created_at)}
            </div>
            <div className="flex items-center space-x-2">
              <button
                onClick={() => setSelectedSurvey(survey)}
                className="flex items-center space-x-1 px-3 py-1 text-sm text-primary-600 hover:bg-primary-50 rounded-md transition-colors"
              >
                <Eye className="w-4 h-4" />
                <span>View Details</span>
              </button>
              <button className="flex items-center space-x-1 px-3 py-1 text-sm text-gray-600 hover:bg-gray-50 rounded-md transition-colors">
                <Download className="w-4 h-4" />
                <span>Export</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  };

  const SurveyDetailModal = () => {
    if (!selectedSurvey) return null;

    const surveyResponses = responses.filter(r => r.survey_id === selectedSurvey.id);
    const surveyAnalytics = analytics[selectedSurvey.id] || {};

    return (
      <div className="fixed inset-0 z-50 overflow-y-auto">
        <div className="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
          <div className="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"></div>
          <div className="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-4xl sm:w-full">
            <div className="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
              <div className="flex items-center justify-between mb-6">
                <div>
                  <h3 className="text-lg font-medium text-gray-900">{selectedSurvey.title}</h3>
                  <p className="text-sm text-gray-500">{selectedSurvey.description}</p>
                </div>
                <button
                  onClick={() => setSelectedSurvey(null)}
                  className="text-gray-400 hover:text-gray-600"
                >
                  <span className="sr-only">Close</span>
                  <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>

              {/* Analytics Overview */}
              <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
                <div className="bg-blue-50 p-4 rounded-lg">
                  <div className="flex items-center">
                    <BarChart3 className="w-8 h-8 text-blue-600" />
                    <div className="ml-3">
                      <p className="text-sm font-medium text-blue-600">Total Responses</p>
                      <p className="text-2xl font-bold text-blue-900">{surveyAnalytics.totalResponses}</p>
                    </div>
                  </div>
                </div>
                <div className="bg-green-50 p-4 rounded-lg">
                  <div className="flex items-center">
                    <Star className="w-8 h-8 text-green-600" />
                    <div className="ml-3">
                      <p className="text-sm font-medium text-green-600">Average Rating</p>
                      <p className="text-2xl font-bold text-green-900">
                        {surveyAnalytics.averageRating > 0 ? surveyAnalytics.averageRating.toFixed(1) : 'N/A'}
                      </p>
                    </div>
                  </div>
                </div>
                <div className="bg-purple-50 p-4 rounded-lg">
                  <div className="flex items-center">
                    <TrendingUp className="w-8 h-8 text-purple-600" />
                    <div className="ml-3">
                      <p className="text-sm font-medium text-purple-600">Response Rate</p>
                      <p className="text-2xl font-bold text-purple-900">
                        {surveyAnalytics.responseRate > 0 ? `${surveyAnalytics.responseRate}%` : 'N/A'}
                      </p>
                    </div>
                  </div>
                </div>
                <div className="bg-orange-50 p-4 rounded-lg">
                  <div className="flex items-center">
                    <Calendar className="w-8 h-8 text-orange-600" />
                    <div className="ml-3">
                      <p className="text-sm font-medium text-orange-600">Created</p>
                      <p className="text-sm font-bold text-orange-900">{formatDate(selectedSurvey.created_at)}</p>
                    </div>
                  </div>
                </div>
              </div>

              {/* Recent Responses */}
              <div>
                <h4 className="text-lg font-medium text-gray-900 mb-4">Recent Responses</h4>
                <div className="space-y-3 max-h-96 overflow-y-auto">
                  {surveyResponses.slice(-10).map((response) => (
                    <div key={response.id} className="border border-gray-200 rounded-lg p-4">
                      <div className="flex justify-between items-start mb-2">
                        <div className="flex items-center space-x-2">
                          <span className="text-sm font-medium text-gray-900">
                            Response #{response.id}
                          </span>
                          <span className="text-xs text-gray-500">
                            {formatDate(response.created_at)}
                          </span>
                        </div>
                        {response.overall_rating && renderRatingStars(response.overall_rating)}
                      </div>
                      {response.feedback_text && (
                        <p className="text-sm text-gray-600 mb-2">{response.feedback_text}</p>
                      )}
                      <div className="text-xs text-gray-500">
                        {response.appointment_id && `Appointment ID: ${response.appointment_id}`}
                        {response.conversation_id && `Conversation ID: ${response.conversation_id}`}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Survey Management</h1>
          <p className="text-gray-600">Monitor and analyze patient feedback</p>
        </div>
        <div className="flex items-center space-x-3">
          <button
            onClick={loadData}
            className="flex items-center space-x-2 px-3 py-2 text-sm text-gray-600 hover:text-gray-800 transition-colors"
          >
            <RefreshCw className="w-4 h-4" />
            <span>Refresh</span>
          </button>
          <button className="flex items-center space-x-2 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors">
            <Plus className="w-4 h-4" />
            <span>Create Survey</span>
          </button>
        </div>
      </div>

      {/* Filters */}
      <div className="flex flex-col sm:flex-row gap-4">
        <div className="flex-1">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
            <input
              type="text"
              placeholder="Search surveys..."
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            />
          </div>
        </div>
        <div className="sm:w-48">
          <select
            value={filterType}
            onChange={(e) => setFilterType(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          >
            <option value="all">All Types</option>
            <option value="visit">Visit Surveys</option>
            <option value="ai_chat">AI Chat Surveys</option>
            <option value="general">General Surveys</option>
          </select>
        </div>
        <div className="sm:w-48">
          <select
            value={dateRange}
            onChange={(e) => setDateRange(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          >
            <option value="7">Last 7 days</option>
            <option value="30">Last 30 days</option>
            <option value="90">Last 90 days</option>
            <option value="365">Last year</option>
          </select>
        </div>
      </div>

      {/* Summary Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-white p-6 rounded-lg border border-gray-200">
          <div className="flex items-center">
            <div className="p-2 bg-blue-100 rounded-lg">
              <BarChart3 className="w-6 h-6 text-blue-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Total Surveys</p>
              <p className="text-2xl font-bold text-gray-900">{surveys.length}</p>
            </div>
          </div>
        </div>
        <div className="bg-white p-6 rounded-lg border border-gray-200">
          <div className="flex items-center">
            <div className="p-2 bg-green-100 rounded-lg">
              <MessageSquare className="w-6 h-6 text-green-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Total Responses</p>
              <p className="text-2xl font-bold text-gray-900">{responses.length}</p>
            </div>
          </div>
        </div>
        <div className="bg-white p-6 rounded-lg border border-gray-200">
          <div className="flex items-center">
            <div className="p-2 bg-purple-100 rounded-lg">
              <Star className="w-6 h-6 text-purple-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Avg Rating</p>
              <p className="text-2xl font-bold text-gray-900">
                {responses.length > 0 
                  ? (responses.reduce((sum, r) => sum + (r.overall_rating || 0), 0) / responses.length).toFixed(1)
                  : 'N/A'
                }
              </p>
            </div>
          </div>
        </div>
        <div className="bg-white p-6 rounded-lg border border-gray-200">
          <div className="flex items-center">
            <div className="p-2 bg-orange-100 rounded-lg">
              <Users className="w-6 h-6 text-orange-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Active Surveys</p>
              <p className="text-2xl font-bold text-gray-900">
                {surveys.filter(s => s.is_active).length}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Surveys List */}
      <div className="space-y-4">
        {filteredSurveys.length === 0 ? (
          <div className="text-center py-12">
            <BarChart3 className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">No surveys found</h3>
            <p className="text-gray-600">Try adjusting your filters or create a new survey</p>
          </div>
        ) : (
          filteredSurveys.map(survey => (
            <SurveyCard key={survey.id} survey={survey} />
          ))
        )}
      </div>

      {/* Survey Detail Modal */}
      <SurveyDetailModal />
    </div>
  );
};

export default SurveyManagement; 
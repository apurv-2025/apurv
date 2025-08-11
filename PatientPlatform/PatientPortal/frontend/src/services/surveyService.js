import api from './api';

export const surveyService = {
  // Survey management
  async getSurveys(surveyType = null) {
    const params = surveyType ? `?survey_type=${surveyType}` : '';
    const response = await api.get(`/surveys${params}`);
    return response.data;
  },

  async getActiveSurveys(surveyType = null) {
    const params = surveyType ? `?survey_type=${surveyType}` : '';
    const response = await api.get(`/surveys/active${params}`);
    return response.data;
  },

  async getSurvey(surveyId) {
    const response = await api.get(`/surveys/${surveyId}`);
    return response.data;
  },

  async createSurvey(surveyData) {
    const response = await api.post('/surveys', surveyData);
    return response.data;
  },

  async updateSurvey(surveyId, surveyData) {
    const response = await api.put(`/surveys/${surveyId}`, surveyData);
    return response.data;
  },

  async deleteSurvey(surveyId) {
    const response = await api.delete(`/surveys/${surveyId}`);
    return response.data;
  },

  // Survey questions
  async getSurveyQuestions(surveyId) {
    const response = await api.get(`/surveys/${surveyId}/questions`);
    return response.data;
  },

  async createSurveyQuestion(surveyId, questionData) {
    const response = await api.post(`/surveys/${surveyId}/questions`, questionData);
    return response.data;
  },

  async updateSurveyQuestion(questionId, questionData) {
    const response = await api.put(`/surveys/questions/${questionId}`, questionData);
    return response.data;
  },

  async deleteSurveyQuestion(questionId) {
    const response = await api.delete(`/surveys/questions/${questionId}`);
    return response.data;
  },

  // Survey responses
  async submitSurveyResponse(responseData) {
    const response = await api.post('/surveys/responses', responseData);
    return response.data;
  },

  async getSurveyResponses(surveyId = null) {
    const params = surveyId ? `?survey_id=${surveyId}` : '';
    const response = await api.get(`/surveys/responses${params}`);
    return response.data;
  },

  async getSurveyResponse(responseId) {
    const response = await api.get(`/surveys/responses/${responseId}`);
    return response.data;
  },

  async updateSurveyResponse(responseId, responseData) {
    const response = await api.put(`/surveys/responses/${responseId}`, responseData);
    return response.data;
  },

  // Survey analytics
  async getSurveyAnalytics(surveyId) {
    const response = await api.get(`/surveys/${surveyId}/analytics`);
    return response.data;
  },

  // Survey triggers and eligibility
  async triggerSurvey(triggerData) {
    const response = await api.post('/surveys/trigger', triggerData);
    return response.data;
  },

  async checkSurveyEligibility(surveyType, appointmentId = null, conversationId = null) {
    const params = new URLSearchParams();
    if (appointmentId) params.append('appointment_id', appointmentId);
    if (conversationId) params.append('conversation_id', conversationId);
    
    const response = await api.get(`/surveys/eligibility/${surveyType}?${params}`);
    return response.data;
  },

  // Survey templates
  async createVisitSurveyTemplate() {
    const response = await api.post('/surveys/templates/visit');
    return response.data;
  },

  async createAiChatSurveyTemplate() {
    const response = await api.post('/surveys/templates/ai-chat');
    return response.data;
  }
}; 
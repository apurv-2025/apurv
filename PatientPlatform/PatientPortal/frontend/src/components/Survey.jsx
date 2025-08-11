import React, { useState, useEffect } from 'react';
import { Star, CheckCircle, XCircle, MessageSquare, Calendar, Clock, AlertCircle, Send, ThumbsUp, ThumbsDown } from 'lucide-react';
import { surveyService } from '../services/surveyService';

const Survey = ({ 
  surveyId, 
  surveyType = 'general', 
  appointmentId = null, 
  conversationId = null,
  onComplete = null,
  onClose = null 
}) => {
  const [survey, setSurvey] = useState(null);
  const [questions, setQuestions] = useState([]);
  const [responses, setResponses] = useState({});
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState(null);
  const [overallRating, setOverallRating] = useState(0);
  const [feedbackText, setFeedbackText] = useState('');

  useEffect(() => {
    loadSurvey();
  }, [surveyId, surveyType]);

  const loadSurvey = async () => {
    try {
      setLoading(true);
      let surveyData;

      if (surveyId) {
        // Load specific survey
        surveyData = await surveyService.getSurvey(surveyId);
        setSurvey(surveyData);
        setQuestions(surveyData.questions || []);
      } else {
        // Check eligibility and get appropriate survey
        const eligibility = await surveyService.checkSurveyEligibility(
          surveyType, 
          appointmentId, 
          conversationId
        );
        
        if (eligibility.eligible) {
          setSurvey(eligibility.survey);
          setQuestions(eligibility.questions || []);
        } else {
          setError('No survey available or you have already completed this survey.');
        }
      }
    } catch (err) {
      setError('Failed to load survey. Please try again.');
      console.error('Error loading survey:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleResponseChange = (questionId, value) => {
    setResponses(prev => ({
      ...prev,
      [questionId]: value
    }));
  };

  const handleRatingChange = (questionId, rating) => {
    handleResponseChange(questionId, rating);
  };

  const handleMultipleChoiceChange = (questionId, option) => {
    handleResponseChange(questionId, option);
  };

  const handleTextChange = (questionId, text) => {
    handleResponseChange(questionId, text);
  };

  const handleYesNoChange = (questionId, answer) => {
    handleResponseChange(questionId, answer);
  };

  const isQuestionAnswered = (question) => {
    const response = responses[question.id];
    if (question.required && !response) return false;
    if (question.question_type === 'rating' && (!response || response < 1)) return false;
    if (question.question_type === 'text' && question.required && (!response || response.trim() === '')) return false;
    return true;
  };

  const canProceed = () => {
    if (currentQuestion >= questions.length - 1) return true;
    return isQuestionAnswered(questions[currentQuestion]);
  };

  const nextQuestion = () => {
    if (currentQuestion < questions.length - 1) {
      setCurrentQuestion(prev => prev + 1);
    }
  };

  const previousQuestion = () => {
    if (currentQuestion > 0) {
      setCurrentQuestion(prev => prev - 1);
    }
  };

  const submitSurvey = async () => {
    try {
      setSubmitting(true);
      
      const responseData = {
        survey_id: survey.id,
        response_data: responses,
        overall_rating: overallRating > 0 ? overallRating : null,
        feedback_text: feedbackText.trim() || null,
        appointment_id: appointmentId,
        conversation_id: conversationId
      };

      await surveyService.submitSurveyResponse(responseData);
      
      if (onComplete) {
        onComplete();
      }
    } catch (err) {
      setError('Failed to submit survey. Please try again.');
      console.error('Error submitting survey:', err);
    } finally {
      setSubmitting(false);
    }
  };

  const renderQuestion = (question) => {
    const response = responses[question.id];

    switch (question.question_type) {
      case 'rating':
        return (
          <div className="space-y-4">
            <div className="flex justify-center space-x-2">
              {[1, 2, 3, 4, 5].map((rating) => (
                <button
                  key={rating}
                  onClick={() => handleRatingChange(question.id, rating)}
                  className={`p-2 rounded-full transition-colors ${
                    response === rating
                      ? 'bg-primary-100 text-primary-600'
                      : 'bg-gray-100 text-gray-400 hover:bg-gray-200'
                  }`}
                >
                  <Star className={`w-6 h-6 ${response === rating ? 'fill-current' : ''}`} />
                </button>
              ))}
            </div>
            <div className="text-center text-sm text-gray-600">
              {response ? `${response} star${response > 1 ? 's' : ''}` : 'Select rating'}
            </div>
          </div>
        );

      case 'multiple_choice':
        return (
          <div className="space-y-3">
            {question.options?.map((option, index) => (
              <label key={index} className="flex items-center space-x-3 cursor-pointer">
                <input
                  type="radio"
                  name={`question-${question.id}`}
                  value={option}
                  checked={response === option}
                  onChange={(e) => handleMultipleChoiceChange(question.id, e.target.value)}
                  className="w-4 h-4 text-primary-600 focus:ring-primary-500"
                />
                <span className="text-gray-700">{option}</span>
              </label>
            ))}
          </div>
        );

      case 'text':
        return (
          <div>
            <textarea
              value={response || ''}
              onChange={(e) => handleTextChange(question.id, e.target.value)}
              placeholder="Enter your response..."
              className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent resize-none"
              rows={4}
            />
          </div>
        );

      case 'yes_no':
        return (
          <div className="flex space-x-4">
            <button
              onClick={() => handleYesNoChange(question.id, true)}
              className={`flex items-center space-x-2 px-4 py-2 rounded-lg border transition-colors ${
                response === true
                  ? 'border-green-500 bg-green-50 text-green-700'
                  : 'border-gray-300 hover:border-green-300'
              }`}
            >
              <ThumbsUp className="w-4 h-4" />
              <span>Yes</span>
            </button>
            <button
              onClick={() => handleYesNoChange(question.id, false)}
              className={`flex items-center space-x-2 px-4 py-2 rounded-lg border transition-colors ${
                response === false
                  ? 'border-red-500 bg-red-50 text-red-700'
                  : 'border-gray-300 hover:border-red-300'
              }`}
            >
              <ThumbsDown className="w-4 h-4" />
              <span>No</span>
            </button>
          </div>
        );

      default:
        return <div>Unsupported question type</div>;
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center p-8">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-4">
        <div className="flex items-center space-x-3">
          <AlertCircle className="w-5 h-5 text-red-500" />
          <p className="text-red-700">{error}</p>
        </div>
      </div>
    );
  }

  if (!survey || questions.length === 0) {
    return (
      <div className="text-center p-8">
        <p className="text-gray-600">No survey available.</p>
      </div>
    );
  }

  const currentQ = questions[currentQuestion];
  const isLastQuestion = currentQuestion === questions.length - 1;
  const progress = ((currentQuestion + 1) / questions.length) * 100;

  return (
    <div className="max-w-2xl mx-auto bg-white rounded-lg shadow-lg overflow-hidden">
      {/* Header */}
      <div className="bg-gradient-to-r from-primary-600 to-primary-700 text-white p-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            {surveyType === 'visit' ? (
              <Calendar className="w-6 h-6" />
            ) : surveyType === 'ai_chat' ? (
              <MessageSquare className="w-6 h-6" />
            ) : (
              <CheckCircle className="w-6 h-6" />
            )}
            <div>
              <h2 className="text-xl font-semibold">{survey.title}</h2>
              <p className="text-primary-100 text-sm">{survey.description}</p>
            </div>
          </div>
          {onClose && (
            <button
              onClick={onClose}
              className="text-primary-100 hover:text-white transition-colors"
            >
              <XCircle className="w-6 h-6" />
            </button>
          )}
        </div>
        
        {/* Progress bar */}
        <div className="mt-4">
          <div className="flex justify-between text-sm text-primary-100 mb-2">
            <span>Question {currentQuestion + 1} of {questions.length}</span>
            <span>{Math.round(progress)}%</span>
          </div>
          <div className="w-full bg-primary-500 rounded-full h-2">
            <div
              className="bg-white h-2 rounded-full transition-all duration-300"
              style={{ width: `${progress}%` }}
            ></div>
          </div>
        </div>
      </div>

      {/* Question */}
      <div className="p-6">
        {currentQ && (
          <div className="space-y-6">
            <div>
              <h3 className="text-lg font-medium text-gray-900 mb-2">
                {currentQ.question_text}
                {currentQ.required && <span className="text-red-500 ml-1">*</span>}
              </h3>
              {!isQuestionAnswered(currentQ) && currentQ.required && (
                <p className="text-sm text-red-600">This question is required</p>
              )}
            </div>

            {renderQuestion(currentQ)}
          </div>
        )}

        {/* Overall rating for last question */}
        {isLastQuestion && (
          <div className="mt-8 pt-6 border-t border-gray-200">
            <h3 className="text-lg font-medium text-gray-900 mb-4">
              Overall Rating
            </h3>
            <div className="flex justify-center space-x-2 mb-2">
              {[1, 2, 3, 4, 5].map((rating) => (
                <button
                  key={rating}
                  onClick={() => setOverallRating(rating)}
                  className={`p-2 rounded-full transition-colors ${
                    overallRating === rating
                      ? 'bg-primary-100 text-primary-600'
                      : 'bg-gray-100 text-gray-400 hover:bg-gray-200'
                  }`}
                >
                  <Star className={`w-6 h-6 ${overallRating === rating ? 'fill-current' : ''}`} />
                </button>
              ))}
            </div>
            <div className="text-center text-sm text-gray-600 mb-4">
              {overallRating ? `${overallRating} star${overallRating > 1 ? 's' : ''}` : 'Select overall rating'}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Additional Comments (Optional)
              </label>
              <textarea
                value={feedbackText}
                onChange={(e) => setFeedbackText(e.target.value)}
                placeholder="Share any additional feedback..."
                className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent resize-none"
                rows={3}
              />
            </div>
          </div>
        )}
      </div>

      {/* Navigation */}
      <div className="bg-gray-50 px-6 py-4 flex justify-between items-center">
        <button
          onClick={previousQuestion}
          disabled={currentQuestion === 0}
          className="px-4 py-2 text-gray-600 hover:text-gray-800 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          Previous
        </button>

        <div className="flex space-x-3">
          {!isLastQuestion ? (
            <button
              onClick={nextQuestion}
              disabled={!canProceed()}
              className="px-6 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              Next
            </button>
          ) : (
            <button
              onClick={submitSurvey}
              disabled={submitting || !canProceed()}
              className="px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center space-x-2"
            >
              {submitting ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                  <span>Submitting...</span>
                </>
              ) : (
                <>
                  <Send className="w-4 h-4" />
                  <span>Submit Survey</span>
                </>
              )}
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

export default Survey; 
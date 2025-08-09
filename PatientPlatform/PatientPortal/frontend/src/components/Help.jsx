import React, { useState } from 'react';
import {
  HelpCircle, Search, MessageSquare, Phone, Mail, Clock, User,
  ChevronDown, ChevronRight, ExternalLink, FileText, Video,
  Shield, Settings, CreditCard, Calendar, Bot, Book
} from 'lucide-react';

const Help = () => {
  const [activeCategory, setActiveCategory] = useState('general');
  const [expandedFAQ, setExpandedFAQ] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');

  const helpCategories = [
    { id: 'general', label: 'General Help', icon: HelpCircle },
    { id: 'account', label: 'Account & Profile', icon: User },
    { id: 'appointments', label: 'Appointments', icon: Calendar },
    { id: 'telehealth', label: 'Telehealth', icon: Video },
    { id: 'billing', label: 'Billing & Insurance', icon: CreditCard },
    { id: 'privacy', label: 'Privacy & Security', icon: Shield },
    { id: 'technical', label: 'Technical Support', icon: Settings }
  ];

  const faqData = {
    general: [
      {
        id: 1,
        question: 'How do I get started with the Patient Portal?',
        answer: 'After logging in, start by completing your profile information and verifying your contact details. You can then schedule appointments, view your medical records, and communicate with your healthcare team.'
      },
      {
        id: 2,
        question: 'Can I access the portal on my mobile device?',
        answer: 'Yes! The Patient Portal is fully responsive and works on smartphones, tablets, and desktop computers. You can access all features from any device with an internet connection.'
      },
      {
        id: 3,
        question: 'How do I update my personal information?',
        answer: 'Go to the Profile section from the sidebar or user menu in the header. You can update your contact information, emergency contacts, and other personal details there.'
      }
    ],
    account: [
      {
        id: 4,
        question: 'How do I reset my password?',
        answer: 'Click "Forgot Password" on the login page and enter your email address. You\'ll receive instructions to reset your password within a few minutes.'
      },
      {
        id: 5,
        question: 'How do I change my notification preferences?',
        answer: 'Go to Settings and select "Notification Preferences." You can choose how you want to receive appointment reminders, test results, and other important communications.'
      },
      {
        id: 6,
        question: 'Can I add family members to my account?',
        answer: 'If you have dependent children under 18, you can request access to their records through your healthcare provider. Adult family members need their own separate accounts.'
      }
    ],
    appointments: [
      {
        id: 7,
        question: 'How do I schedule an appointment?',
        answer: 'Go to the Appointments section and click "Schedule New Appointment." Choose your provider, select an available time slot, and provide the reason for your visit.'
      },
      {
        id: 8,
        question: 'Can I cancel or reschedule an appointment?',
        answer: 'Yes, you can cancel or reschedule appointments up to 24 hours in advance. Go to Appointments, find your appointment, and use the "Reschedule" or "Cancel" options.'
      },
      {
        id: 9,
        question: 'How will I receive appointment reminders?',
        answer: 'You\'ll receive reminders via email, SMS, or app notifications based on your preferences. Reminders are sent 24 hours and 2 hours before your appointment.'
      }
    ],
    telehealth: [
      {
        id: 10,
        question: 'What do I need for a telehealth appointment?',
        answer: 'You need a device with a camera and microphone (computer, smartphone, or tablet), a stable internet connection, and a quiet, private space for your appointment.'
      },
      {
        id: 11,
        question: 'How do I test my technology before an appointment?',
        answer: 'Go to the Telehealth section and click "Tech Check" to test your camera, microphone, and internet connection. We recommend doing this 15 minutes before your appointment.'
      },
      {
        id: 12,
        question: 'What if I have technical issues during my appointment?',
        answer: 'Use the "Contact Support" button in the Telehealth section for immediate technical assistance. Our support team is available during all appointment hours.'
      }
    ],
    billing: [
      {
        id: 13,
        question: 'How do I view my billing statements?',
        answer: 'Go to the Billing section to view all your statements, payment history, and insurance information. You can download statements as PDF files for your records.'
      },
      {
        id: 14,
        question: 'How do I make a payment?',
        answer: 'In the Billing section, click "Make Payment" next to any outstanding balance. You can pay by credit card, debit card, or bank transfer through our secure payment portal.'
      },
      {
        id: 15,
        question: 'How do I update my insurance information?',
        answer: 'Go to Billing and select "Insurance Cards." You can upload photos of your insurance cards and update your coverage information there.'
      }
    ],
    privacy: [
      {
        id: 16,
        question: 'How is my health information protected?',
        answer: 'We use industry-standard encryption and security measures to protect your data. Our system is HIPAA-compliant and regularly audited for security compliance.'
      },
      {
        id: 17,
        question: 'Who can access my medical records?',
        answer: 'Only you and your authorized healthcare providers can access your medical records. You control who sees your information and can review access logs in your account.'
      },
      {
        id: 18,
        question: 'Can I delete my account and data?',
        answer: 'You can request account deletion by contacting our support team. Please note that some medical records may be retained as required by law and medical practice standards.'
      }
    ],
    technical: [
      {
        id: 19,
        question: 'What browsers are supported?',
        answer: 'We support the latest versions of Chrome, Firefox, Safari, and Edge. For the best experience, please keep your browser updated to the latest version.'
      },
      {
        id: 20,
        question: 'Why is the portal running slowly?',
        answer: 'Slow performance can be due to internet connection, browser cache, or too many open tabs. Try clearing your browser cache, closing unnecessary tabs, or switching to a faster internet connection.'
      },
      {
        id: 21,
        question: 'I\'m having trouble uploading documents. What should I do?',
        answer: 'Ensure your files are in supported formats (PDF, JPG, PNG) and under 10MB. If problems persist, try using a different browser or contact technical support for assistance.'
      }
    ]
  };

  const contactOptions = [
    {
      id: 1,
      title: 'Live Chat Support',
      description: 'Get instant help from our support team',
      icon: MessageSquare,
      action: 'Start Chat',
      hours: '24/7 Available',
      color: 'bg-blue-100 text-blue-600'
    },
    {
      id: 2,
      title: 'Phone Support',
      description: 'Speak directly with a support representative',
      icon: Phone,
      action: 'Call (555) 123-4567',
      hours: 'Mon-Fri 8AM-6PM',
      color: 'bg-green-100 text-green-600'
    },
    {
      id: 3,
      title: 'Email Support',
      description: 'Send us an email for non-urgent questions',
      icon: Mail,
      action: 'Send Email',
      hours: 'Response within 24 hours',
      color: 'bg-purple-100 text-purple-600'
    },
    {
      id: 4,
      title: 'Technical Support',
      description: 'Get help with technical issues and troubleshooting',
      icon: Settings,
      action: 'Submit Ticket',
      hours: 'Mon-Fri 8AM-8PM',
      color: 'bg-orange-100 text-orange-600'
    }
  ];

  const filteredFAQs = faqData[activeCategory]?.filter(faq =>
    faq.question.toLowerCase().includes(searchTerm.toLowerCase()) ||
    faq.answer.toLowerCase().includes(searchTerm.toLowerCase())
  ) || [];

  const toggleFAQ = (faqId) => {
    setExpandedFAQ(expandedFAQ === faqId ? null : faqId);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Help & Support</h1>
        <p className="text-gray-600">Find answers to common questions and get support when you need it</p>
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {contactOptions.map(option => {
          const IconComponent = option.icon;
          return (
            <div key={option.id} className="bg-white border border-gray-200 rounded-lg p-6">
              <div className={`w-12 h-12 rounded-lg ${option.color} flex items-center justify-center mb-4`}>
                <IconComponent className="w-6 h-6" />
              </div>
              <h3 className="font-semibold text-gray-900 mb-2">{option.title}</h3>
              <p className="text-sm text-gray-600 mb-3">{option.description}</p>
              <p className="text-xs text-gray-500 mb-4">{option.hours}</p>
              <button className="w-full px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm">
                {option.action}
              </button>
            </div>
          );
        })}
      </div>

      {/* Search */}
      <div className="bg-white border border-gray-200 rounded-lg p-6">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Search help articles and FAQs..."
            className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>
      </div>

      {/* Main Content */}
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Categories Sidebar */}
        <div className="lg:col-span-1">
          <div className="bg-white border border-gray-200 rounded-lg p-4">
            <h3 className="font-semibold text-gray-900 mb-4">Help Categories</h3>
            <nav className="space-y-1">
              {helpCategories.map(category => {
                const IconComponent = category.icon;
                return (
                  <button
                    key={category.id}
                    onClick={() => setActiveCategory(category.id)}
                    className={`w-full flex items-center space-x-3 px-3 py-2 rounded-lg text-left transition-colors ${
                      activeCategory === category.id
                        ? 'bg-blue-50 text-blue-600 border border-blue-200'
                        : 'text-gray-700 hover:bg-gray-50'
                    }`}
                  >
                    <IconComponent className="w-4 h-4" />
                    <span className="text-sm">{category.label}</span>
                  </button>
                );
              })}
            </nav>
          </div>
        </div>

        {/* FAQ Content */}
        <div className="lg:col-span-3">
          <div className="bg-white border border-gray-200 rounded-lg">
            <div className="p-6 border-b border-gray-200">
              <h2 className="text-lg font-semibold text-gray-900">
                {helpCategories.find(cat => cat.id === activeCategory)?.label} - Frequently Asked Questions
              </h2>
              <p className="text-sm text-gray-600 mt-1">
                {filteredFAQs.length} question{filteredFAQs.length !== 1 ? 's' : ''} found
              </p>
            </div>

            <div className="divide-y divide-gray-200">
              {filteredFAQs.length === 0 ? (
                <div className="p-6 text-center">
                  <HelpCircle className="w-12 h-12 text-gray-300 mx-auto mb-4" />
                  <p className="text-gray-500">No questions found matching your search.</p>
                  <p className="text-sm text-gray-400 mt-2">Try a different search term or browse other categories.</p>
                </div>
              ) : (
                filteredFAQs.map(faq => (
                  <div key={faq.id} className="p-6">
                    <button
                      onClick={() => toggleFAQ(faq.id)}
                      className="w-full flex items-center justify-between text-left"
                    >
                      <h3 className="font-medium text-gray-900 pr-4">{faq.question}</h3>
                      {expandedFAQ === faq.id ? (
                        <ChevronDown className="w-5 h-5 text-gray-500 flex-shrink-0" />
                      ) : (
                        <ChevronRight className="w-5 h-5 text-gray-500 flex-shrink-0" />
                      )}
                    </button>
                    
                    {expandedFAQ === faq.id && (
                      <div className="mt-4 text-gray-600">
                        <p>{faq.answer}</p>
                      </div>
                    )}
                  </div>
                ))
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Additional Resources */}
      <div className="bg-white border border-gray-200 rounded-lg p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Additional Resources</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="flex items-start space-x-3">
            <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
              <Book className="w-5 h-5 text-blue-600" />
            </div>
            <div>
              <h4 className="font-medium text-gray-900">User Guide</h4>
              <p className="text-sm text-gray-600 mt-1">Complete guide to using the Patient Portal</p>
              <button className="text-sm text-blue-600 hover:text-blue-700 mt-2 flex items-center">
                View Guide <ExternalLink className="w-3 h-3 ml-1" />
              </button>
            </div>
          </div>

          <div className="flex items-start space-x-3">
            <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
              <Video className="w-5 h-5 text-green-600" />
            </div>
            <div>
              <h4 className="font-medium text-gray-900">Video Tutorials</h4>
              <p className="text-sm text-gray-600 mt-1">Watch step-by-step video tutorials</p>
              <button className="text-sm text-blue-600 hover:text-blue-700 mt-2 flex items-center">
                Watch Videos <ExternalLink className="w-3 h-3 ml-1" />
              </button>
            </div>
          </div>

          <div className="flex items-start space-x-3">
            <div className="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center">
              <Bot className="w-5 h-5 text-purple-600" />
            </div>
            <div>
              <h4 className="font-medium text-gray-900">AI Assistant</h4>
              <p className="text-sm text-gray-600 mt-1">Get instant answers from our AI helper</p>
              <button className="text-sm text-blue-600 hover:text-blue-700 mt-2 flex items-center">
                Ask AI Assistant <ExternalLink className="w-3 h-3 ml-1" />
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Contact Form */}
      <div className="bg-white border border-gray-200 rounded-lg p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Still Need Help?</h3>
        <p className="text-gray-600 mb-6">Can't find what you're looking for? Send us a message and we'll get back to you within 24 hours.</p>
        
        <form className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Subject</label>
              <select className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                <option value="">Select a topic</option>
                <option value="account">Account Issues</option>
                <option value="technical">Technical Problems</option>
                <option value="billing">Billing Questions</option>
                <option value="appointments">Appointment Help</option>
                <option value="other">Other</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Priority</label>
              <select className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
                <option value="urgent">Urgent</option>
              </select>
            </div>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Message</label>
            <textarea
              rows="4"
              placeholder="Please describe your question or issue in detail..."
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            ></textarea>
          </div>
          
          <div className="flex justify-end">
            <button
              type="submit"
              className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              Send Message
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default Help;
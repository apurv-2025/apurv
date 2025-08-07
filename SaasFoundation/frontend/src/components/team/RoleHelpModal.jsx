import React from 'react';
import { XMarkIcon, InformationCircleIcon } from '@heroicons/react/24/outline';
import { Card, Button } from '../ui';
import { ROLES } from '../../utils/constants';

const RoleHelpModal = ({ isOpen, onClose }) => {
  if (!isOpen) return null;

  const roleCategories = [
    {
      title: "Management Roles",
      description: "These roles have administrative privileges and can manage team members, settings, and organizational operations.",
      roles: [
        {
          role: ROLES.OWNER,
          emoji: "👑",
          description: "Full access including billing and organization management",
          responsibilities: [
            "Manage subscription and billing",
            "Transfer ownership",
            "Delete organization",
            "All admin permissions"
          ],
          color: "bg-yellow-100 text-yellow-800"
        },
        {
          role: ROLES.ADMIN,
          emoji: "🛡️",
          description: "Can manage team members and settings",
          responsibilities: [
            "Invite and manage team members",
            "Manage organization settings",
            "View billing information",
            "All member permissions"
          ],
          color: "bg-blue-100 text-blue-800"
        },
        {
          role: ROLES.REVENUE_CYCLE_MANAGER,
          emoji: "📊",
          description: "Manages revenue cycle operations and team",
          responsibilities: [
            "Oversee revenue cycle processes",
            "Manage RCM team members",
            "Analyze financial performance",
            "Implement process improvements"
          ],
          color: "bg-blue-100 text-blue-800"
        },
        {
          role: ROLES.COMPLIANCE_OFFICER,
          emoji: "⚖️",
          description: "Ensures regulatory compliance and policies",
          responsibilities: [
            "Monitor regulatory compliance",
            "Develop compliance policies",
            "Conduct audits and training",
            "Manage risk assessments"
          ],
          color: "bg-blue-100 text-blue-800"
        },
        {
          role: ROLES.RCM_ANALYST,
          emoji: "📈",
          description: "Analyzes revenue cycle data and performance",
          responsibilities: [
            "Analyze revenue cycle metrics",
            "Generate performance reports",
            "Identify improvement opportunities",
            "Track key performance indicators"
          ],
          color: "bg-blue-100 text-blue-800"
        },
        {
          role: ROLES.RCM_SYSTEMS_ANALYST,
          emoji: "💻",
          description: "Manages RCM systems and technical processes",
          responsibilities: [
            "Manage RCM software systems",
            "Optimize technical workflows",
            "Troubleshoot system issues",
            "Implement system integrations"
          ],
          color: "bg-blue-100 text-blue-800"
        },
        {
          role: ROLES.PRACTICE_MANAGER,
          emoji: "🏢",
          description: "Manages practice operations and staff",
          responsibilities: [
            "Oversee daily practice operations",
            "Manage staff schedules and performance",
            "Coordinate with clinical teams",
            "Ensure operational efficiency"
          ],
          color: "bg-blue-100 text-blue-800"
        }
      ]
    },
    {
      title: "Specialist Roles",
      description: "These roles focus on specific areas of healthcare operations and revenue cycle management.",
      roles: [
        {
          role: ROLES.INSURANCE_VERIFICATION_SPECIALIST,
          emoji: "🏥",
          description: "Verifies insurance coverage and benefits",
          responsibilities: [
            "Verify patient insurance coverage",
            "Check benefit eligibility",
            "Obtain pre-authorization requirements",
            "Document coverage details"
          ],
          color: "bg-green-100 text-green-800"
        },
        {
          role: ROLES.PRE_AUTHORIZATION_SPECIALIST,
          emoji: "✅",
          description: "Obtains pre-authorizations for procedures",
          responsibilities: [
            "Submit pre-authorization requests",
            "Follow up on pending authorizations",
            "Document authorization details",
            "Coordinate with clinical staff"
          ],
          color: "bg-green-100 text-green-800"
        },
        {
          role: ROLES.FINANCIAL_COUNSELOR,
          emoji: "💰",
          description: "Provides financial guidance to patients",
          responsibilities: [
            "Explain patient financial responsibilities",
            "Set up payment plans",
            "Provide cost estimates",
            "Assist with financial assistance applications"
          ],
          color: "bg-green-100 text-green-800"
        },
        {
          role: ROLES.REGISTRATION_CLERK,
          emoji: "📝",
          description: "Handles patient registration and check-in",
          responsibilities: [
            "Register new patients",
            "Update patient information",
            "Verify insurance at check-in",
            "Collect patient payments"
          ],
          color: "bg-green-100 text-green-800"
        },
        {
          role: ROLES.MEDICAL_CODER,
          emoji: "🏷️",
          description: "Assigns medical codes for billing",
          responsibilities: [
            "Review clinical documentation",
            "Assign appropriate diagnosis codes",
            "Assign procedure codes",
            "Ensure coding accuracy and compliance"
          ],
          color: "bg-green-100 text-green-800"
        },
        {
          role: ROLES.CLINICAL_DOCUMENTATION_SPECIALIST,
          emoji: "📋",
          description: "Ensures accurate clinical documentation",
          responsibilities: [
            "Review clinical documentation",
            "Ensure documentation completeness",
            "Query providers for missing information",
            "Improve documentation quality"
          ],
          color: "bg-green-100 text-green-800"
        },
        {
          role: ROLES.CHARGE_ENTRY_SPECIALIST,
          emoji: "💳",
          description: "Enters charges for services provided",
          responsibilities: [
            "Enter charges from clinical encounters",
            "Verify charge accuracy",
            "Apply appropriate modifiers",
            "Ensure timely charge entry"
          ],
          color: "bg-green-100 text-green-800"
        },
        {
          role: ROLES.BILLING_SPECIALIST,
          emoji: "🧾",
          description: "Processes medical bills and claims",
          responsibilities: [
            "Submit claims to insurance companies",
            "Review claim rejections and denials",
            "Process patient statements",
            "Follow up on unpaid claims"
          ],
          color: "bg-green-100 text-green-800"
        },
        {
          role: ROLES.ACCOUNTS_RECEIVABLE_SPECIALIST,
          emoji: "📊",
          description: "Manages accounts receivable and collections",
          responsibilities: [
            "Monitor accounts receivable aging",
            "Manage collection processes",
            "Process insurance payments",
            "Reconcile payment discrepancies"
          ],
          color: "bg-green-100 text-green-800"
        },
        {
          role: ROLES.PAYMENT_POSTER,
          emoji: "📥",
          description: "Posts payments and adjustments",
          responsibilities: [
            "Post insurance payments",
            "Post patient payments",
            "Apply adjustments and write-offs",
            "Reconcile daily payments"
          ],
          color: "bg-green-100 text-green-800"
        },
        {
          role: ROLES.DENIALS_MANAGEMENT_SPECIALIST,
          emoji: "🚫",
          description: "Manages claim denials and appeals",
          responsibilities: [
            "Review claim denials",
            "Prepare and submit appeals",
            "Track appeal outcomes",
            "Identify denial trends"
          ],
          color: "bg-green-100 text-green-800"
        },
        {
          role: ROLES.PATIENT_COLLECTIONS_REPRESENTATIVE,
          emoji: "📞",
          description: "Handles patient payment collections",
          responsibilities: [
            "Contact patients for payment",
            "Set up payment arrangements",
            "Process payment plans",
            "Handle patient billing inquiries"
          ],
          color: "bg-green-100 text-green-800"
        },
        {
          role: ROLES.SCHEDULER,
          emoji: "📅",
          description: "Manages patient appointments and scheduling",
          responsibilities: [
            "Schedule patient appointments",
            "Manage provider schedules",
            "Handle appointment changes",
            "Coordinate with clinical teams"
          ],
          color: "bg-green-100 text-green-800"
        },
        {
          role: ROLES.HEALTH_INFORMATION_TECHNICIAN,
          emoji: "📋",
          description: "Manages health records and information systems",
          responsibilities: [
            "Manage electronic health records",
            "Ensure record accuracy and completeness",
            "Process record requests",
            "Maintain data integrity"
          ],
          color: "bg-green-100 text-green-800"
        }
      ]
    }
  ];

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg shadow-xl max-w-4xl w-full max-h-[90vh] overflow-hidden">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <div className="flex items-center space-x-3">
            <InformationCircleIcon className="h-6 w-6 text-blue-600" />
            <h2 className="text-xl font-semibold text-gray-900">
              Healthcare Role Guide
            </h2>
          </div>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <XMarkIcon className="h-6 w-6" />
          </button>
        </div>

        {/* Content */}
        <div className="overflow-y-auto max-h-[calc(90vh-80px)] p-6">
          <div className="space-y-8">
            {roleCategories.map((category, categoryIndex) => (
              <div key={categoryIndex} className="space-y-4">
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">
                    {category.title}
                  </h3>
                  <p className="text-gray-600 text-sm">
                    {category.description}
                  </p>
                </div>

                <div className="grid gap-4 md:grid-cols-2">
                  {category.roles.map((role, roleIndex) => (
                    <Card key={roleIndex} className="p-4">
                      <div className="flex items-start space-x-3">
                        <span className="text-2xl">{role.emoji}</span>
                        <div className="flex-1">
                          <div className="flex items-center space-x-2 mb-2">
                            <h4 className="font-medium text-gray-900">
                              {role.role}
                            </h4>
                            <span className={`px-2 py-1 text-xs font-medium rounded-full ${role.color}`}>
                              {category.title === "Management Roles" ? "Management" : "Specialist"}
                            </span>
                          </div>
                          <p className="text-sm text-gray-600 mb-3">
                            {role.description}
                          </p>
                          <div>
                            <h5 className="text-xs font-medium text-gray-700 mb-2 uppercase tracking-wide">
                              Key Responsibilities:
                            </h5>
                            <ul className="text-xs text-gray-600 space-y-1">
                              {role.responsibilities.map((responsibility, respIndex) => (
                                <li key={respIndex} className="flex items-start space-x-2">
                                  <span className="text-blue-500 mt-1">•</span>
                                  <span>{responsibility}</span>
                                </li>
                              ))}
                            </ul>
                          </div>
                        </div>
                      </div>
                    </Card>
                  ))}
                </div>
              </div>
            ))}
          </div>

          {/* Footer */}
          <div className="mt-8 pt-6 border-t border-gray-200">
            <div className="bg-blue-50 rounded-lg p-4">
              <h4 className="font-medium text-blue-900 mb-2">💡 Tips for Role Selection</h4>
              <ul className="text-sm text-blue-800 space-y-1">
                <li>• <strong>Management roles</strong> have administrative privileges and can manage team members</li>
                <li>• <strong>Specialist roles</strong> focus on specific operational areas</li>
                <li>• Consider the person's experience and responsibilities when assigning roles</li>
                <li>• You can always change roles later as team members grow</li>
              </ul>
            </div>
          </div>
        </div>

        {/* Footer Actions */}
        <div className="flex justify-end p-6 border-t border-gray-200 bg-gray-50">
          <Button
            onClick={onClose}
            variant="primary"
          >
            Got it, thanks!
          </Button>
        </div>
      </div>
    </div>
  );
};

export default RoleHelpModal; 
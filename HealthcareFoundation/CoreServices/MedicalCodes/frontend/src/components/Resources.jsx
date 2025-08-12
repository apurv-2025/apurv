import React from 'react';
import { BookOpen, ExternalLink, FileText, Code, Database, Globe, Info, AlertCircle, CheckCircle, Clock, BarChart3 } from 'lucide-react';

const Resources = () => {
  const externalReferences = [
    {
      title: "CPT Codes",
      description: "Current Procedural Terminology codes for medical procedures and services",
      url: "https://www.ama-assn.org/practice-management/cpt",
      organization: "American Medical Association (AMA)",
      icon: Code,
      color: "bg-blue-50 border-blue-200"
    },
    {
      title: "ICD-10 Codes",
      description: "International Classification of Diseases, 10th Revision for diagnosis codes",
      url: "https://www.cms.gov/medicare/coding-billing/icd-10-codes",
      organization: "Centers for Medicare & Medicaid Services (CMS)",
      icon: FileText,
      color: "bg-green-50 border-green-200"
    },
    {
      title: "HCPCS Codes",
      description: "Healthcare Common Procedure Coding System for supplies and services",
      url: "https://www.cms.gov/medicare/coding-billing/healthcare-common-procedure-system",
      organization: "Centers for Medicare & Medicaid Services (CMS)",
      icon: Database,
      color: "bg-purple-50 border-purple-200"
    }
  ];

  const codingConcepts = [
    {
      title: "CPT Codes",
      subtitle: "Current Procedural Terminology",
      description: "CPT codes are a standardized set of codes used to describe medical, surgical, and diagnostic procedures and services. They are maintained by the American Medical Association (AMA) and are used by healthcare providers for billing purposes.",
      examples: ["99213 - Office visit, established patient", "90791 - Psychiatric diagnostic evaluation", "90832 - Psychotherapy, 30 minutes"],
      category: "Procedures & Services",
      icon: Code,
      color: "bg-blue-100 text-blue-700"
    },
    {
      title: "ICD-10 Codes",
      subtitle: "International Classification of Diseases, 10th Revision",
      description: "ICD-10 codes are used to classify and code all diagnoses, symptoms, and procedures recorded in conjunction with hospital care. They provide a standardized way to describe diseases and health conditions.",
      examples: ["F32.1 - Major depressive disorder, moderate", "E11.9 - Type 2 diabetes without complications", "I10 - Essential (primary) hypertension"],
      category: "Diagnoses & Conditions",
      icon: FileText,
      color: "bg-green-100 text-green-700"
    },
    {
      title: "HCPCS Codes",
      subtitle: "Healthcare Common Procedure Coding System",
      description: "HCPCS codes are used to identify products, supplies, and services not included in the CPT codes. They are primarily used for Medicare and Medicaid billing and include durable medical equipment, drugs, and other services.",
      examples: ["H0004 - Behavioral health screening", "H0005 - Behavioral health assessment", "H0006 - Behavioral health counseling"],
      category: "Supplies & Services",
      icon: Database,
      color: "bg-purple-100 text-purple-700"
    },
    {
      title: "Modifier Codes",
      subtitle: "Code Modifiers",
      description: "Modifiers are two-digit codes that provide additional information about a procedure or service. They can indicate that a service was performed by a different provider, in a different location, or with special circumstances.",
      examples: ["25 - Separate E/M service", "59 - Distinct procedural service", "95 - Telemedicine service"],
      category: "Service Modifiers",
      icon: Code,
      color: "bg-orange-100 text-orange-700"
    }
  ];

  const billingConcepts = [
    {
      title: "Revenue Cycle",
      description: "The complete process of managing claims processing, payment, and revenue generation from patient registration to final payment collection.",
      steps: ["Patient Registration", "Insurance Verification", "Service Delivery", "Claims Submission", "Payment Processing", "Denial Management"]
    },
    {
      title: "Medical Billing",
      description: "The process of submitting and following up on claims with health insurance companies to receive payment for services rendered by healthcare providers.",
      steps: ["Code Assignment", "Claims Creation", "Insurance Submission", "Payment Posting", "Denial Appeals"]
    },
    {
      title: "Coding Compliance",
      description: "Ensuring that medical coding follows established guidelines and regulations to prevent fraud, waste, and abuse in healthcare billing.",
      steps: ["Documentation Review", "Code Validation", "Compliance Auditing", "Education & Training", "Ongoing Monitoring"]
    }
  ];

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="text-center">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">Medical Coding Resources</h1>
        <p className="text-lg text-gray-600 max-w-3xl mx-auto">
          Learn about medical coding standards, understand different code types, and access official resources for healthcare professionals and non-revenue cycle staff.
        </p>
      </div>

      {/* Medical Coding Concepts */}
      <div className="bg-white rounded-lg shadow-sm p-6">
        <h2 className="text-2xl font-semibold text-gray-900 mb-6 flex items-center gap-3">
          <BookOpen className="w-6 h-6 text-blue-600" />
          Understanding Medical Codes
        </h2>
        
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {codingConcepts.map((concept, index) => (
            <div key={index} className="border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow">
              <div className="flex items-start gap-4">
                <div className={`p-3 rounded-lg ${concept.color}`}>
                  <concept.icon className="w-6 h-6" />
                </div>
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-2">
                    <h3 className="text-xl font-semibold text-gray-900">{concept.title}</h3>
                    <span className="px-2 py-1 bg-gray-100 text-gray-600 rounded text-xs font-medium">
                      {concept.category}
                    </span>
                  </div>
                  <p className="text-sm text-gray-600 mb-2">{concept.subtitle}</p>
                  <p className="text-gray-700 mb-4 leading-relaxed">{concept.description}</p>
                  
                  <div>
                    <h4 className="font-medium text-gray-900 mb-2">Examples:</h4>
                    <ul className="space-y-1">
                      {concept.examples.map((example, idx) => (
                        <li key={idx} className="text-sm text-gray-600 font-mono bg-gray-50 px-2 py-1 rounded">
                          {example}
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Revenue Cycle Concepts */}
      <div className="bg-white rounded-lg shadow-sm p-6">
        <h2 className="text-2xl font-semibold text-gray-900 mb-6 flex items-center gap-3">
          <BarChart3 className="w-6 h-6 text-green-600" />
          Revenue Cycle & Billing Concepts
        </h2>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {billingConcepts.map((concept, index) => (
            <div key={index} className="border border-gray-200 rounded-lg p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-3">{concept.title}</h3>
              <p className="text-gray-700 mb-4 leading-relaxed">{concept.description}</p>
              
              <div>
                <h4 className="font-medium text-gray-900 mb-2">Key Steps:</h4>
                <ol className="space-y-1">
                  {concept.steps.map((step, idx) => (
                    <li key={idx} className="text-sm text-gray-600 flex items-center gap-2">
                      <span className="w-5 h-5 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center text-xs font-medium">
                        {idx + 1}
                      </span>
                      {step}
                    </li>
                  ))}
                </ol>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* External References */}
      <div className="bg-white rounded-lg shadow-sm p-6">
        <h2 className="text-2xl font-semibold text-gray-900 mb-6 flex items-center gap-3">
          <Globe className="w-6 h-6 text-purple-600" />
          Official External References
        </h2>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {externalReferences.map((reference, index) => (
            <div key={index} className={`border rounded-lg p-6 ${reference.color} hover:shadow-md transition-shadow`}>
              <div className="flex items-start gap-4">
                <div className="p-3 bg-white rounded-lg shadow-sm">
                  <reference.icon className="w-6 h-6 text-gray-600" />
                </div>
                <div className="flex-1">
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">{reference.title}</h3>
                  <p className="text-gray-700 mb-3 leading-relaxed">{reference.description}</p>
                  <p className="text-sm text-gray-600 mb-4">
                    <strong>Source:</strong> {reference.organization}
                  </p>
                  <a
                    href={reference.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center gap-2 px-4 py-2 bg-white text-gray-700 rounded-lg border border-gray-300 hover:bg-gray-50 transition-colors font-medium"
                  >
                    <ExternalLink className="w-4 h-4" />
                    Visit Official Site
                  </a>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Quick Reference Guide */}
      <div className="bg-white rounded-lg shadow-sm p-6">
        <h2 className="text-2xl font-semibold text-gray-900 mb-6 flex items-center gap-3">
          <Info className="w-6 h-6 text-orange-600" />
          Quick Reference Guide
        </h2>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Code Type Summary</h3>
            <div className="space-y-3">
              <div className="flex items-center gap-3 p-3 bg-blue-50 rounded-lg">
                <div className="w-3 h-3 bg-blue-500 rounded"></div>
                <div>
                  <span className="font-medium text-blue-900">CPT</span>
                  <span className="text-sm text-blue-700 ml-2">Procedures & Services</span>
                </div>
              </div>
              <div className="flex items-center gap-3 p-3 bg-green-50 rounded-lg">
                <div className="w-3 h-3 bg-green-500 rounded"></div>
                <div>
                  <span className="font-medium text-green-900">ICD-10</span>
                  <span className="text-sm text-green-700 ml-2">Diagnoses & Conditions</span>
                </div>
              </div>
              <div className="flex items-center gap-3 p-3 bg-purple-50 rounded-lg">
                <div className="w-3 h-3 bg-purple-500 rounded"></div>
                <div>
                  <span className="font-medium text-purple-900">HCPCS</span>
                  <span className="text-sm text-purple-700 ml-2">Supplies & Services</span>
                </div>
              </div>
              <div className="flex items-center gap-3 p-3 bg-orange-50 rounded-lg">
                <div className="w-3 h-3 bg-orange-500 rounded"></div>
                <div>
                  <span className="font-medium text-orange-900">Modifiers</span>
                  <span className="text-sm text-orange-700 ml-2">Service Modifiers</span>
                </div>
              </div>
            </div>
          </div>
          
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Key Terms</h3>
            <div className="space-y-3">
              <div className="p-3 bg-gray-50 rounded-lg">
                <span className="font-medium text-gray-900">Revenue Cycle</span>
                <p className="text-sm text-gray-600 mt-1">Complete billing process from registration to payment</p>
              </div>
              <div className="p-3 bg-gray-50 rounded-lg">
                <span className="font-medium text-gray-900">Claims Processing</span>
                <p className="text-sm text-gray-600 mt-1">Submitting and managing insurance claims</p>
              </div>
              <div className="p-3 bg-gray-50 rounded-lg">
                <span className="font-medium text-gray-900">Coding Compliance</span>
                <p className="text-sm text-gray-600 mt-1">Following coding guidelines and regulations</p>
              </div>
              <div className="p-3 bg-gray-50 rounded-lg">
                <span className="font-medium text-gray-900">Denial Management</span>
                <p className="text-sm text-gray-600 mt-1">Handling rejected or denied insurance claims</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Tips for Non-Revenue Cycle Staff */}
      <div className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg p-6">
        <h2 className="text-2xl font-semibold text-gray-900 mb-6 flex items-center gap-3">
          <AlertCircle className="w-6 h-6 text-blue-600" />
          Tips for Non-Revenue Cycle Staff
        </h2>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="space-y-4">
            <div className="flex items-start gap-3">
              <CheckCircle className="w-5 h-5 text-green-600 mt-0.5" />
              <div>
                <h4 className="font-medium text-gray-900">Understand the Basics</h4>
                <p className="text-sm text-gray-600">Learn what CPT, ICD-10, and HCPCS codes represent and their purpose in healthcare billing.</p>
              </div>
            </div>
            <div className="flex items-start gap-3">
              <CheckCircle className="w-5 h-5 text-green-600 mt-0.5" />
              <div>
                <h4 className="font-medium text-gray-900">Use Official Resources</h4>
                <p className="text-sm text-gray-600">Always refer to official sources like AMA and CMS for the most current and accurate information.</p>
              </div>
            </div>
            <div className="flex items-start gap-3">
              <CheckCircle className="w-5 h-5 text-green-600 mt-0.5" />
              <div>
                <h4 className="font-medium text-gray-900">Stay Updated</h4>
                <p className="text-sm text-gray-600">Medical codes are updated annually, so stay informed about changes and new codes.</p>
              </div>
            </div>
          </div>
          
          <div className="space-y-4">
            <div className="flex items-start gap-3">
              <CheckCircle className="w-5 h-5 text-green-600 mt-0.5" />
              <div>
                <h4 className="font-medium text-gray-900">Ask Questions</h4>
                <p className="text-sm text-gray-600">Don't hesitate to ask revenue cycle specialists for clarification on coding matters.</p>
              </div>
            </div>
            <div className="flex items-start gap-3">
              <CheckCircle className="w-5 h-5 text-green-600 mt-0.5" />
              <div>
                <h4 className="font-medium text-gray-900">Documentation Matters</h4>
                <p className="text-sm text-gray-600">Good documentation is essential for accurate coding and proper billing.</p>
              </div>
            </div>
            <div className="flex items-start gap-3">
              <CheckCircle className="w-5 h-5 text-green-600 mt-0.5" />
              <div>
                <h4 className="font-medium text-gray-900">Compliance is Key</h4>
                <p className="text-sm text-gray-600">Understanding coding compliance helps prevent billing errors and potential audits.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Resources; 
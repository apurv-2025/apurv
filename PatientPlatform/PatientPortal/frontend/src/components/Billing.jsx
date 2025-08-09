import React, { useState, useEffect } from 'react';
import { 
  CreditCard, DollarSign, FileText, Calendar, User, Search, Filter, 
  Download, Eye, Plus, Upload, Check, AlertCircle, Clock, Receipt,
  Shield, Camera, Edit, Trash2, X, ExternalLink, ChevronDown, ChevronRight
} from 'lucide-react';
import { useAPI } from '../hooks/useAPI';

const Billing = () => {
  const [activeTab, setActiveTab] = useState('overview');
  const [billingData, setBillingData] = useState({
    invoices: [],
    payments: [],
    insuranceCards: [],
    coverageDetails: [],
    statements: []
  });
  const [filteredInvoices, setFilteredInvoices] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState('all');
  const [filterDateRange, setFilterDateRange] = useState('all');
  const [loading, setLoading] = useState(true);
  const [selectedInvoice, setSelectedInvoice] = useState(null);
  const [showAddInsuranceModal, setShowAddInsuranceModal] = useState(false);
  const [showPaymentModal, setShowPaymentModal] = useState(false);
  const [selectedPaymentInvoice, setSelectedPaymentInvoice] = useState(null);

  useEffect(() => {
    // Mock comprehensive billing data
    const mockBillingData = {
      // Practice Invoices/Bills
      invoices: [
        {
          id: 1,
          invoiceNumber: 'INV-2024-001',
          date: '2024-02-15',
          dueDate: '2024-03-15',
          serviceDate: '2024-02-10',
          provider: 'Dr. Sarah Johnson',
          service: 'Annual Physical Examination',
          amount: 285.00,
          insuranceCovered: 228.00,
          patientResponsibility: 57.00,
          status: 'pending',
          description: 'Comprehensive annual physical with routine labs',
          cptCodes: [
            { code: '99213', description: 'Office visit, established patient', amount: 150.00 },
            { code: '80053', description: 'Comprehensive metabolic panel', amount: 85.00 },
            { code: '85025', description: 'Complete blood count', amount: 50.00 }
          ],
          insuranceClaim: {
            claimNumber: 'CLM-789456123',
            submittedDate: '2024-02-16',
            processedDate: '2024-02-20',
            status: 'processed',
            coveragePercentage: 80,
            deductibleApplied: 0,
            copayAmount: 25.00
          }
        },
        {
          id: 2,
          invoiceNumber: 'INV-2024-002',
          date: '2024-01-20',
          dueDate: '2024-02-20',
          serviceDate: '2024-01-15',
          provider: 'Dr. Michael Chen',
          service: 'Cardiology Consultation',
          amount: 450.00,
          insuranceCovered: 360.00,
          patientResponsibility: 90.00,
          status: 'paid',
          paidDate: '2024-02-18',
          paymentMethod: 'Credit Card',
          description: 'Follow-up consultation for hypertension management',
          cptCodes: [
            { code: '99244', description: 'Cardiology consultation', amount: 350.00 },
            { code: '93000', description: 'Electrocardiogram', amount: 100.00 }
          ],
          insuranceClaim: {
            claimNumber: 'CLM-789456124',
            submittedDate: '2024-01-21',
            processedDate: '2024-01-25',
            status: 'approved',
            coveragePercentage: 80,
            deductibleApplied: 0,
            copayAmount: 40.00
          }
        },
        {
          id: 3,
          invoiceNumber: 'INV-2024-003',
          date: '2024-02-25',
          dueDate: '2024-03-25',
          serviceDate: '2024-02-22',
          provider: 'Lab Corp',
          service: 'Laboratory Tests',
          amount: 125.00,
          insuranceCovered: 100.00,
          patientResponsibility: 25.00,
          status: 'overdue',
          description: 'Routine lab work ordered by Dr. Johnson',
          cptCodes: [
            { code: '80061', description: 'Lipid panel', amount: 75.00 },
            { code: '83036', description: 'Hemoglobin A1C', amount: 50.00 }
          ],
          insuranceClaim: {
            claimNumber: 'CLM-789456125',
            submittedDate: '2024-02-23',
            processedDate: '2024-02-27',
            status: 'processed',
            coveragePercentage: 80,
            deductibleApplied: 0,
            copayAmount: 25.00
          }
        }
      ],

      // Payment History
      payments: [
        {
          id: 1,
          date: '2024-02-18',
          amount: 90.00,
          method: 'Credit Card (**** 4532)',
          invoiceNumber: 'INV-2024-002',
          confirmationNumber: 'PAY-789123456',
          status: 'completed'
        },
        {
          id: 2,
          date: '2024-01-15',
          amount: 150.00,
          method: 'Bank Transfer',
          invoiceNumber: 'INV-2023-045',
          confirmationNumber: 'PAY-789123455',
          status: 'completed'
        }
      ],

      // Insurance Cards
      insuranceCards: [
        {
          id: 1,
          type: 'primary',
          insuranceCompany: 'Blue Cross Blue Shield',
          planName: 'PPO Select',
          policyNumber: 'BC123456789',
          groupNumber: 'GRP-001234',
          memberName: 'John Smith',
          memberId: 'BC123456789',
          effectiveDate: '2024-01-01',
          expirationDate: '2024-12-31',
          copay: {
            primaryCare: 25,
            specialist: 40,
            emergency: 150,
            urgentCare: 50
          },
          deductible: {
            individual: 1500,
            family: 3000,
            met: 250
          },
          outOfPocketMax: {
            individual: 6000,
            family: 12000,
            met: 340
          },
          cardImageUrl: '/images/insurance-card-front.jpg',
          cardBackImageUrl: '/images/insurance-card-back.jpg',
          customerServicePhone: '1-800-555-0123',
          website: 'www.bcbs.com'
        },
        {
          id: 2,
          type: 'secondary',
          insuranceCompany: 'Aetna',
          planName: 'Health Fund HDHP',
          policyNumber: 'AET987654321',
          groupNumber: 'GRP-005678',
          memberName: 'John Smith',
          memberId: 'AET987654321',
          effectiveDate: '2024-01-01',
          expirationDate: '2024-12-31',
          copay: {
            primaryCare: 0,
            specialist: 0,
            emergency: 0,
            urgentCare: 0
          },
          deductible: {
            individual: 3000,
            family: 6000,
            met: 0
          },
          outOfPocketMax: {
            individual: 5000,
            family: 10000,
            met: 0
          },
          cardImageUrl: '/images/aetna-card-front.jpg',
          cardBackImageUrl: '/images/aetna-card-back.jpg',
          customerServicePhone: '1-800-555-0456',
          website: 'www.aetna.com'
        }
      ],

      // Coverage Details
      coverageDetails: [
        {
          id: 1,
          category: 'Preventive Care',
          covered: true,
          coveragePercentage: 100,
          copayAmount: 0,
          deductibleApplies: false,
          description: 'Annual physical, mammograms, colonoscopies, vaccinations',
          limitations: 'Once per calendar year'
        },
        {
          id: 2,
          category: 'Primary Care Visits',
          covered: true,
          coveragePercentage: 80,
          copayAmount: 25,
          deductibleApplies: false,
          description: 'Routine office visits with primary care physician',
          limitations: 'Copay applies after insurance payment'
        },
        {
          id: 3,
          category: 'Specialist Visits',
          covered: true,
          coveragePercentage: 80,
          copayAmount: 40,
          deductibleApplies: true,
          description: 'Consultations with specialists',
          limitations: 'Referral may be required'
        },
        {
          id: 4,
          category: 'Laboratory Tests',
          covered: true,
          coveragePercentage: 80,
          copayAmount: 0,
          deductibleApplies: true,
          description: 'Blood work, urine tests, diagnostic labs',
          limitations: 'Must be medically necessary'
        },
        {
          id: 5,
          category: 'Prescription Drugs',
          covered: true,
          coveragePercentage: 80,
          copayAmount: 0,
          deductibleApplies: true,
          description: 'Generic and brand name medications',
          limitations: 'Formulary restrictions may apply'
        }
      ],

      // Monthly Statements
      statements: [
        {
          id: 1,
          month: 'February 2024',
          statementDate: '2024-03-01',
          totalCharges: 860.00,
          insurancePayments: 688.00,
          patientPayments: 90.00,
          adjustments: 0.00,
          balance: 82.00,
          dueDate: '2024-03-25'
        },
        {
          id: 2,
          month: 'January 2024',
          statementDate: '2024-02-01',
          totalCharges: 450.00,
          insurancePayments: 360.00,
          patientPayments: 90.00,
          adjustments: 0.00,
          balance: 0.00,
          dueDate: null
        }
      ]
    };

    setBillingData(mockBillingData);
    setFilteredInvoices(mockBillingData.invoices);
    setLoading(false);
  }, []);

  useEffect(() => {
    let filtered = billingData.invoices;

    // Filter by status
    if (filterStatus !== 'all') {
      filtered = filtered.filter(invoice => invoice.status === filterStatus);
    }

    // Filter by date range
    if (filterDateRange !== 'all') {
      const now = new Date();
      const cutoffDate = new Date();
      
      switch (filterDateRange) {
        case '30days':
          cutoffDate.setDate(now.getDate() - 30);
          break;
        case '3months':
          cutoffDate.setMonth(now.getMonth() - 3);
          break;
        case '6months':
          cutoffDate.setMonth(now.getMonth() - 6);
          break;
        case '1year':
          cutoffDate.setFullYear(now.getFullYear() - 1);
          break;
        default:
          break;
      }
      
      if (filterDateRange !== 'all') {
        filtered = filtered.filter(invoice => new Date(invoice.date) >= cutoffDate);
      }
    }

    // Filter by search term
    if (searchTerm) {
      filtered = filtered.filter(invoice =>
        invoice.invoiceNumber.toLowerCase().includes(searchTerm.toLowerCase()) ||
        invoice.provider.toLowerCase().includes(searchTerm.toLowerCase()) ||
        invoice.service.toLowerCase().includes(searchTerm.toLowerCase()) ||
        invoice.description.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    setFilteredInvoices(filtered);
  }, [billingData.invoices, filterStatus, filterDateRange, searchTerm]);

  const getStatusColor = (status) => {
    switch (status) {
      case 'paid': return 'bg-green-100 text-green-800';
      case 'pending': return 'bg-yellow-100 text-yellow-800';
      case 'overdue': return 'bg-red-100 text-red-800';
      case 'processing': return 'bg-blue-100 text-blue-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'paid': return Check;
      case 'pending': return Clock;
      case 'overdue': return AlertCircle;
      case 'processing': return Clock;
      default: return FileText;
    }
  };

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(amount);
  };

  const OverviewTab = () => {
    const totalBalance = billingData.invoices
      .filter(inv => inv.status !== 'paid')
      .reduce((sum, inv) => sum + inv.patientResponsibility, 0);
    
    const overdueBalance = billingData.invoices
      .filter(inv => inv.status === 'overdue')
      .reduce((sum, inv) => sum + inv.patientResponsibility, 0);

    return (
      <div className="space-y-6">
        {/* Account Summary */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-white p-6 rounded-lg shadow border border-gray-200">
            <div className="flex items-center space-x-3">
              <DollarSign className="w-8 h-8 text-blue-600" />
              <div>
                <p className="text-sm text-gray-600">Current Balance</p>
                <p className="text-2xl font-bold text-gray-900">{formatCurrency(totalBalance)}</p>
              </div>
            </div>
          </div>
          
          <div className="bg-white p-6 rounded-lg shadow border border-gray-200">
            <div className="flex items-center space-x-3">
              <AlertCircle className="w-8 h-8 text-red-600" />
              <div>
                <p className="text-sm text-gray-600">Overdue Balance</p>
                <p className="text-2xl font-bold text-red-900">{formatCurrency(overdueBalance)}</p>
              </div>
            </div>
          </div>
          
          <div className="bg-white p-6 rounded-lg shadow border border-gray-200">
            <div className="flex items-center space-x-3">
              <Shield className="w-8 h-8 text-green-600" />
              <div>
                <p className="text-sm text-gray-600">Insurance Coverage</p>
                <p className="text-2xl font-bold text-green-900">80%</p>
              </div>
            </div>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <button 
              onClick={() => setShowPaymentModal(true)}
              className="flex items-center space-x-3 p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
            >
              <CreditCard className="w-5 h-5 text-blue-600" />
              <span className="text-sm font-medium">Make Payment</span>
            </button>
            
            <button className="flex items-center space-x-3 p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
              <Download className="w-5 h-5 text-green-600" />
              <span className="text-sm font-medium">Download Statement</span>
            </button>
            
            <button 
              onClick={() => setShowAddInsuranceModal(true)}
              className="flex items-center space-x-3 p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
            >
              <Plus className="w-5 h-5 text-purple-600" />
              <span className="text-sm font-medium">Add Insurance</span>
            </button>
            
            <button className="flex items-center space-x-3 p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
              <FileText className="w-5 h-5 text-orange-600" />
              <span className="text-sm font-medium">View Coverage</span>
            </button>
          </div>
        </div>

        {/* Recent Invoices */}
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-900">Recent Invoices</h3>
            <button 
              onClick={() => setActiveTab('invoices')}
              className="text-blue-600 hover:text-blue-800 text-sm flex items-center"
            >
              View All <ChevronRight className="w-4 h-4 ml-1" />
            </button>
          </div>
          
          <div className="space-y-3">
            {billingData.invoices.slice(0, 3).map(invoice => (
              <div key={invoice.id} className="flex items-center justify-between p-3 border border-gray-200 rounded-lg">
                <div className="flex-1">
                  <div className="flex items-center space-x-3">
                    <span className="font-medium text-gray-900">{invoice.invoiceNumber}</span>
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(invoice.status)}`}>
                      {invoice.status}
                    </span>
                  </div>
                  <p className="text-sm text-gray-600">{invoice.service} - {invoice.date}</p>
                </div>
                <div className="text-right">
                  <p className="font-medium text-gray-900">{formatCurrency(invoice.patientResponsibility)}</p>
                  <p className="text-xs text-gray-500">Due: {invoice.dueDate}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  };

  const InvoicesTab = () => (
    <div className="space-y-6">
      {/* Search and Filters */}
      <div className="bg-white rounded-lg shadow p-6">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
            <input
              type="text"
              placeholder="Search invoices..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10 pr-4 py-2 w-full border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          
          <select
            value={filterStatus}
            onChange={(e) => setFilterStatus(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="all">All Status</option>
            <option value="pending">Pending</option>
            <option value="paid">Paid</option>
            <option value="overdue">Overdue</option>
            <option value="processing">Processing</option>
          </select>

          <select
            value={filterDateRange}
            onChange={(e) => setFilterDateRange(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="all">All Time</option>
            <option value="30days">Last 30 Days</option>
            <option value="3months">Last 3 Months</option>
            <option value="6months">Last 6 Months</option>
            <option value="1year">Last Year</option>
          </select>
        </div>
      </div>

      {/* Invoices List */}
      <div className="space-y-4">
        {filteredInvoices.map(invoice => {
          const StatusIcon = getStatusIcon(invoice.status);
          
          return (
            <div key={invoice.id} className="bg-white border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center space-x-3 mb-2">
                    <StatusIcon className="w-5 h-5 text-gray-400" />
                    <h3 className="text-lg font-semibold text-gray-900">{invoice.invoiceNumber}</h3>
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(invoice.status)}`}>
                      {invoice.status}
                    </span>
                  </div>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-4 text-sm text-gray-600">
                    <div className="flex items-center space-x-2">
                      <Calendar className="w-4 h-4" />
                      <span>Service: {invoice.serviceDate}</span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <User className="w-4 h-4" />
                      <span>{invoice.provider}</span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <FileText className="w-4 h-4" />
                      <span>{invoice.service}</span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <Clock className="w-4 h-4" />
                      <span>Due: {invoice.dueDate}</span>
                    </div>
                  </div>

                  <p className="text-sm text-gray-600 mb-4">{invoice.description}</p>

                  {/* Billing Breakdown */}
                  <div className="bg-gray-50 p-4 rounded-lg">
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                      <div>
                        <span className="text-gray-600">Total Amount:</span>
                        <span className="ml-2 font-medium">{formatCurrency(invoice.amount)}</span>
                      </div>
                      <div>
                        <span className="text-gray-600">Insurance Covered:</span>
                        <span className="ml-2 font-medium text-green-600">{formatCurrency(invoice.insuranceCovered)}</span>
                      </div>
                      <div>
                        <span className="text-gray-600">Your Responsibility:</span>
                        <span className="ml-2 font-medium text-orange-600">{formatCurrency(invoice.patientResponsibility)}</span>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="flex flex-col space-y-2 ml-4">
                  {invoice.status !== 'paid' && (
                    <button
                      onClick={() => {
                        setSelectedPaymentInvoice(invoice);
                        setShowPaymentModal(true);
                      }}
                      className="px-3 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm"
                    >
                      Pay Now
                    </button>
                  )}
                  
                  <button
                    onClick={() => setSelectedInvoice(invoice)}
                    className="px-3 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors text-sm"
                  >
                    View Details
                  </button>
                  
                  <button className="px-3 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors text-sm flex items-center">
                    <Download className="w-4 h-4 mr-1" />
                    PDF
                  </button>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );

  const InsuranceTab = () => (
    <div className="space-y-6">
      {/* Insurance Cards */}
      <div className="bg-white rounded-lg shadow p-6">
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-lg font-semibold text-gray-900">Insurance Cards</h3>
          <button
            onClick={() => setShowAddInsuranceModal(true)}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors flex items-center"
          >
            <Plus className="w-4 h-4 mr-2" />
            Add Insurance
          </button>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {billingData.insuranceCards.map(card => (
            <div key={card.id} className="border border-gray-200 rounded-lg p-6">
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center space-x-3">
                  <Shield className="w-6 h-6 text-blue-600" />
                  <div>
                    <h4 className="font-semibold text-gray-900">{card.insuranceCompany}</h4>
                    <p className="text-sm text-gray-600">{card.planName} ({card.type})</p>
                  </div>
                </div>
                <div className="flex space-x-2">
                  <button className="p-2 text-gray-400 hover:text-gray-600">
                    <Edit className="w-4 h-4" />
                  </button>
                  <button className="p-2 text-gray-400 hover:text-red-600">
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              </div>

              <div className="space-y-3 text-sm">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <span className="text-gray-600">Member ID:</span>
                    <span className="ml-2 font-medium">{card.memberId}</span>
                  </div>
                  <div>
                    <span className="text-gray-600">Group:</span>
                    <span className="ml-2 font-medium">{card.groupNumber}</span>
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <span className="text-gray-600">Effective:</span>
                    <span className="ml-2 font-medium">{card.effectiveDate}</span>
                  </div>
                  <div>
                    <span className="text-gray-600">Expires:</span>
                    <span className="ml-2 font-medium">{card.expirationDate}</span>
                  </div>
                </div>

                <div className="mt-4 p-3 bg-gray-50 rounded-lg">
                  <h5 className="font-medium text-gray-900 mb-2">Copays</h5>
                  <div className="grid grid-cols-2 gap-2 text-xs">
                    <div>Primary Care: ${card.copay.primaryCare}</div>
                    <div>Specialist: ${card.copay.specialist}</div>
                    <div>Emergency: ${card.copay.emergency}</div>
                    <div>Urgent Care: ${card.copay.urgentCare}</div>
                  </div>
                </div>

                <div className="mt-3 p-3 bg-blue-50 rounded-lg">
                  <h5 className="font-medium text-gray-900 mb-2">Deductible Progress</h5>
                  <div className="text-xs">
                    <div className="flex justify-between">
                      <span>Individual: ${card.deductible.met} / ${card.deductible.individual}</span>
                      <span>{Math.round((card.deductible.met / card.deductible.individual) * 100)}%</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2 mt-1">
                      <div 
                        className="bg-blue-600 h-2 rounded-full" 
                        style={{ width: `${(card.deductible.met / card.deductible.individual) * 100}%` }}
                      ></div>
                    </div>
                  </div>
                </div>
              </div>

              <div className="mt-4 flex space-x-2">
                <button className="flex-1 px-3 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors text-sm flex items-center justify-center">
                  <Camera className="w-4 h-4 mr-1" />
                  View Card
                </button>
                <button className="flex-1 px-3 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors text-sm flex items-center justify-center">
                  <ExternalLink className="w-4 h-4 mr-1" />
                  Portal
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Coverage Details */}
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-6">Coverage Details</h3>
        
        <div className="space-y-4">
          {billingData.coverageDetails.map(coverage => (
            <div key={coverage.id} className="border border-gray-200 rounded-lg p-4">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center space-x-3 mb-2">
                    <h4 className="font-medium text-gray-900">{coverage.category}</h4>
                    {coverage.covered ? (
                      <Check className="w-5 h-5 text-green-600" />
                    ) : (
                      <X className="w-5 h-5 text-red-600" />
                    )}
                  </div>
                  
                  <p className="text-sm text-gray-600 mb-3">{coverage.description}</p>
                  
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                    <div>
                      <span className="text-gray-600">Coverage:</span>
                      <span className="ml-2 font-medium">{coverage.coveragePercentage}%</span>
                    </div>
                    <div>
                      <span className="text-gray-600">Copay:</span>
                      <span className="ml-2 font-medium">${coverage.copayAmount}</span>
                    </div>
                    <div>
                      <span className="text-gray-600">Deductible:</span>
                      <span className="ml-2 font-medium">{coverage.deductibleApplies ? 'Applies' : 'No'}</span>
                    </div>
                  </div>
                  
                  {coverage.limitations && (
                    <div className="mt-3 p-2 bg-yellow-50 border border-yellow-200 rounded text-sm">
                      <strong>Limitations:</strong> {coverage.limitations}
                    </div>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );

  const PaymentModal = () => {
    const [paymentData, setPaymentData] = useState({
      amount: selectedPaymentInvoice?.patientResponsibility || '',
      method: 'credit_card',
      cardNumber: '',
      expiryDate: '',
      cvv: '',
      nameOnCard: '',
      saveCard: false
    });

    const handleSubmit = (e) => {
      e.preventDefault();
      console.log('Processing payment:', paymentData);
      alert('Payment would be processed here');
      setShowPaymentModal(false);
      setSelectedPaymentInvoice(null);
    };

    if (!showPaymentModal) return null;

    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
        <div className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
          <div className="p-6 border-b border-gray-200">
            <div className="flex items-center justify-between">
              <h2 className="text-xl font-semibold text-gray-900">Make Payment</h2>
              <button 
                onClick={() => setShowPaymentModal(false)}
                className="text-gray-400 hover:text-gray-600"
              >
                <X className="w-6 h-6" />
              </button>
            </div>
          </div>

          <form onSubmit={handleSubmit} className="p-6 space-y-6">
            {selectedPaymentInvoice && (
              <div className="bg-gray-50 p-4 rounded-lg">
                <h3 className="font-medium text-gray-900 mb-2">Payment Details</h3>
                <div className="text-sm text-gray-600">
                  <p>Invoice: {selectedPaymentInvoice.invoiceNumber}</p>
                  <p>Service: {selectedPaymentInvoice.service}</p>
                  <p>Amount Due: {formatCurrency(selectedPaymentInvoice.patientResponsibility)}</p>
                </div>
              </div>
            )}

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Payment Amount
              </label>
              <input
                type="number"
                step="0.01"
                value={paymentData.amount}
                onChange={(e) => setPaymentData({...paymentData, amount: e.target.value})}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Payment Method
              </label>
              <select
                value={paymentData.method}
                onChange={(e) => setPaymentData({...paymentData, method: e.target.value})}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="credit_card">Credit Card</option>
                <option value="debit_card">Debit Card</option>
                <option value="bank_transfer">Bank Transfer</option>
              </select>
            </div>

            {(paymentData.method === 'credit_card' || paymentData.method === 'debit_card') && (
              <>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Card Number
                  </label>
                  <input
                    type="text"
                    value={paymentData.cardNumber}
                    onChange={(e) => setPaymentData({...paymentData, cardNumber: e.target.value})}
                    placeholder="1234 5678 9012 3456"
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    required
                  />
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Expiry Date
                    </label>
                    <input
                      type="text"
                      value={paymentData.expiryDate}
                      onChange={(e) => setPaymentData({...paymentData, expiryDate: e.target.value})}
                      placeholder="MM/YY"
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      required
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      CVV
                    </label>
                    <input
                      type="text"
                      value={paymentData.cvv}
                      onChange={(e) => setPaymentData({...paymentData, cvv: e.target.value})}
                      placeholder="123"
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      required
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Name on Card
                  </label>
                  <input
                    type="text"
                    value={paymentData.nameOnCard}
                    onChange={(e) => setPaymentData({...paymentData, nameOnCard: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    required
                  />
                </div>
              </>
            )}

            <div className="flex space-x-4 pt-6">
              <button
                type="button"
                onClick={() => setShowPaymentModal(false)}
                className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
              >
                Cancel
              </button>
              <button
                type="submit"
                className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                Process Payment
              </button>
            </div>
          </form>
        </div>
      </div>
    );
  };

  const AddInsuranceModal = () => {
    const [insuranceData, setInsuranceData] = useState({
      company: '',
      planName: '',
      policyNumber: '',
      groupNumber: '',
      memberId: '',
      effectiveDate: '',
      expirationDate: '',
      type: 'primary'
    });

    const handleSubmit = (e) => {
      e.preventDefault();
      console.log('Adding insurance:', insuranceData);
      alert('Insurance card would be added here');
      setShowAddInsuranceModal(false);
    };

    if (!showAddInsuranceModal) return null;

    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
        <div className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
          <div className="p-6 border-b border-gray-200">
            <div className="flex items-center justify-between">
              <h2 className="text-xl font-semibold text-gray-900">Add Insurance Card</h2>
              <button 
                onClick={() => setShowAddInsuranceModal(false)}
                className="text-gray-400 hover:text-gray-600"
              >
                <X className="w-6 h-6" />
              </button>
            </div>
          </div>

          <form onSubmit={handleSubmit} className="p-6 space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Insurance Company
                </label>
                <input
                  type="text"
                  value={insuranceData.company}
                  onChange={(e) => setInsuranceData({...insuranceData, company: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Plan Name
                </label>
                <input
                  type="text"
                  value={insuranceData.planName}
                  onChange={(e) => setInsuranceData({...insuranceData, planName: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Policy Number
                </label>
                <input
                  type="text"
                  value={insuranceData.policyNumber}
                  onChange={(e) => setInsuranceData({...insuranceData, policyNumber: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Group Number
                </label>
                <input
                  type="text"
                  value={insuranceData.groupNumber}
                  onChange={(e) => setInsuranceData({...insuranceData, groupNumber: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Member ID
                </label>
                <input
                  type="text"
                  value={insuranceData.memberId}
                  onChange={(e) => setInsuranceData({...insuranceData, memberId: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Insurance Type
                </label>
                <select
                  value={insuranceData.type}
                  onChange={(e) => setInsuranceData({...insuranceData, type: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="primary">Primary</option>
                  <option value="secondary">Secondary</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Effective Date
                </label>
                <input
                  type="date"
                  value={insuranceData.effectiveDate}
                  onChange={(e) => setInsuranceData({...insuranceData, effectiveDate: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Expiration Date
                </label>
                <input
                  type="date"
                  value={insuranceData.expirationDate}
                  onChange={(e) => setInsuranceData({...insuranceData, expirationDate: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  required
                />
              </div>
            </div>

            <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
              <Upload className="mx-auto h-12 w-12 text-gray-400" />
              <div className="mt-4">
                <label className="cursor-pointer">
                  <span className="mt-2 block text-sm font-medium text-gray-900">
                    Upload Insurance Card Images
                  </span>
                  <span className="mt-1 block text-sm text-gray-500">
                    Front and back of your insurance card
                  </span>
                  <input type="file" className="sr-only" multiple accept="image/*" />
                </label>
              </div>
            </div>

            <div className="flex space-x-4 pt-6">
              <button
                type="button"
                onClick={() => setShowAddInsuranceModal(false)}
                className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
              >
                Cancel
              </button>
              <button
                type="submit"
                className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                Add Insurance
              </button>
            </div>
          </form>
        </div>
      </div>
    );
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Billing & Insurance</h1>
        <p className="text-gray-600">Manage your medical bills, insurance coverage, and payments</p>
      </div>

      {/* Tabs */}
      <div className="bg-white rounded-lg shadow">
        <div className="border-b border-gray-200">
          <nav className="flex space-x-8 px-6">
            {[
              { id: 'overview', label: 'Overview' },
              { id: 'invoices', label: 'Invoices' },
              { id: 'insurance', label: 'Insurance' },
              { id: 'payments', label: 'Payment History' }
            ].map(tab => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`py-4 px-1 border-b-2 font-medium text-sm ${
                  activeTab === tab.id
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                {tab.label}
              </button>
            ))}
          </nav>
        </div>

        <div className="p-6">
          {activeTab === 'overview' && <OverviewTab />}
          {activeTab === 'invoices' && <InvoicesTab />}
          {activeTab === 'insurance' && <InsuranceTab />}
          {activeTab === 'payments' && (
            <div className="text-center py-12">
              <Receipt className="mx-auto h-12 w-12 text-gray-400" />
              <h3 className="mt-2 text-sm font-medium text-gray-900">Payment History</h3>
              <p className="mt-1 text-sm text-gray-500">
                View your payment history and transaction details.
              </p>
            </div>
          )}
        </div>
      </div>

      {/* Modals */}
      <PaymentModal />
      <AddInsuranceModal />
    </div>
  );
};

export default Billing;
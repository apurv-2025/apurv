import React, { useState, useEffect } from 'react';
import { 
  Folder, FileText, Calendar, User, Search, Filter, Download, Eye, 
  Clock, Stethoscope, Shield, Pill, TestTube, Heart, Activity,
  ChevronDown, ChevronRight, ArrowRight, ExternalLink, X, AlertTriangle
} from 'lucide-react';
import { useAPI } from '../hooks/useAPI';
import { recordsAPI } from '../services/api';

const Records = () => {
  const [activeTab, setActiveTab] = useState('all');
  const [records, setRecords] = useState([]);
  const [filteredRecords, setFilteredRecords] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterType, setFilterType] = useState('all');
  const [filterProvider, setFilterProvider] = useState('all');
  const [dateRange, setDateRange] = useState('all');
  const [loading, setLoading] = useState(true);
  const [selectedRecord, setSelectedRecord] = useState(null);
  const [expandedRecords, setExpandedRecords] = useState(new Set());

  const { data: recordsData, error } = useAPI(() => recordsAPI.getRecords(), []);

  useEffect(() => {
    if (recordsData && recordsData.length > 0) {
      setRecords(recordsData.sort((a, b) => new Date(b.date) - new Date(a.date)));
      setFilteredRecords(recordsData.sort((a, b) => new Date(b.date) - new Date(a.date)));
      setLoading(false);
      return;
    }

    // Mock comprehensive health records data from EHR systems (fallback)
    const mockRecords = [
      // Visit Summaries
      {
        id: 1,
        type: 'visit',
        category: 'Office Visit',
        title: 'Annual Physical Examination',
        date: '2024-02-15',
        provider: 'Dr. Sarah Johnson',
        specialty: 'Internal Medicine',
        facility: 'Main Medical Center',
        status: 'Final',
        summary: 'Comprehensive annual physical examination with routine preventive care.',
        chiefComplaint: 'Annual wellness exam',
        diagnosis: [
          { code: 'Z00.00', description: 'Encounter for general adult medical examination without abnormal findings' }
        ],
        vitals: {
          bloodPressure: '118/76',
          heartRate: '68',
          temperature: '98.4°F',
          weight: '165 lbs',
          height: '5\'8"',
          bmi: '25.1'
        },
        assessment: 'Patient is in good health overall. Continue current exercise routine and healthy diet.',
        plan: [
          'Continue current medications',
          'Return in 1 year for routine follow-up',
          'Annual mammogram recommended',
          'Colonoscopy due in 2 years'
        ],
        medications: ['Lisinopril 10mg daily', 'Metformin 500mg twice daily'],
        allergies: ['Penicillin - Rash'],
        notes: 'Patient reports feeling well. No acute concerns. Discussed preventive care measures.',
        downloadUrl: '/records/visit-2024-02-15.pdf'
      },
      {
        id: 2,
        type: 'visit',
        category: 'Cardiology Consultation',
        title: 'Hypertension Follow-up',
        date: '2024-01-20',
        provider: 'Dr. Sarah Johnson',
        specialty: 'Cardiology',
        facility: 'Cardiology Associates',
        status: 'Final',
        summary: 'Follow-up visit for blood pressure management.',
        chiefComplaint: 'Blood pressure check',
        diagnosis: [
          { code: 'I10', description: 'Essential hypertension' }
        ],
        vitals: {
          bloodPressure: '128/82',
          heartRate: '72',
          weight: '167 lbs'
        },
        assessment: 'Blood pressure well controlled on current regimen.',
        plan: [
          'Continue Lisinopril 10mg daily',
          'Follow-up in 3 months',
          'Home blood pressure monitoring'
        ],
        medications: ['Lisinopril 10mg daily'],
        allergies: ['Penicillin - Rash'],
        downloadUrl: '/records/visit-2024-01-20.pdf'
      },
      // Immunizations
      {
        id: 3,
        type: 'immunization',
        category: 'Vaccination',
        title: 'COVID-19 Vaccine (Booster)',
        date: '2024-01-15',
        provider: 'Dr. Michael Chen',
        specialty: 'Internal Medicine',
        facility: 'Vaccination Clinic',
        status: 'Administered',
        vaccine: {
          name: 'COVID-19 mRNA Vaccine',
          manufacturer: 'Pfizer-BioNTech',
          lotNumber: 'FF9899',
          dose: 'Booster (3rd dose)',
          site: 'Left deltoid',
          route: 'Intramuscular'
        },
        nextDue: '2024-07-15',
        reactions: 'None reported',
        notes: 'Patient tolerated vaccine well. No immediate adverse reactions observed.',
        downloadUrl: '/records/immunization-2024-01-15.pdf'
      },
      {
        id: 4,
        type: 'immunization',
        category: 'Vaccination',
        title: 'Influenza Vaccine',
        date: '2023-10-01',
        provider: 'Dr. Michael Chen',
        specialty: 'Internal Medicine',
        facility: 'Main Medical Center',
        status: 'Administered',
        vaccine: {
          name: 'Influenza Vaccine (Quadrivalent)',
          manufacturer: 'Sanofi Pasteur',
          lotNumber: 'UJ015AA',
          dose: 'Annual dose',
          site: 'Right deltoid',
          route: 'Intramuscular'
        },
        nextDue: '2024-09-01',
        reactions: 'Mild soreness at injection site',
        notes: 'Annual influenza vaccination. Patient advised to expect mild local reaction.',
        downloadUrl: '/records/immunization-2023-10-01.pdf'
      },
      // Lab Results (Additional)
      {
        id: 5,
        type: 'lab',
        category: 'Laboratory',
        title: 'Hemoglobin A1C',
        date: '2024-02-10',
        provider: 'Dr. Michael Chen',
        specialty: 'Endocrinology',
        facility: 'Lab Corp',
        status: 'Final',
        results: [
          { test: 'Hemoglobin A1C', value: '6.8', unit: '%', range: '<7.0', status: 'normal' }
        ],
        interpretation: 'Good diabetes control. Continue current management.',
        notes: 'Patient continues to show excellent diabetes management.',
        downloadUrl: '/records/lab-2024-02-10.pdf'
      },
      // Allergies & Medical Conditions
      {
        id: 6,
        type: 'allergy',
        category: 'Allergy',
        title: 'Drug Allergy - Penicillin',
        date: '2020-03-15',
        provider: 'Dr. Emily Davis',
        specialty: 'Allergy & Immunology',
        facility: 'Allergy Center',
        status: 'Active',
        allergen: 'Penicillin',
        reaction: 'Skin rash, hives',
        severity: 'Moderate',
        onset: 'Childhood',
        notes: 'Patient developed rash and hives after taking penicillin as a child. Avoid all penicillin-based antibiotics.',
        alternatives: ['Cephalexin', 'Azithromycin', 'Ciprofloxacin'],
        downloadUrl: '/records/allergy-penicillin.pdf'
      },
      {
        id: 7,
        type: 'condition',
        category: 'Medical Condition',
        title: 'Type 2 Diabetes Mellitus',
        date: '2022-06-10',
        provider: 'Dr. Michael Chen',
        specialty: 'Endocrinology',
        facility: 'Diabetes Center',
        status: 'Active',
        condition: 'Type 2 Diabetes Mellitus',
        icd10: 'E11.9',
        severity: 'Mild to Moderate',
        onset: '2022-06-10',
        management: 'Diet, exercise, and medication',
        currentMedications: ['Metformin 500mg twice daily'],
        monitoring: 'Quarterly HbA1c, annual eye exam, annual foot exam',
        notes: 'Well-controlled diabetes with lifestyle modifications and metformin.',
        downloadUrl: '/records/condition-diabetes.pdf'
      },
      // Imaging
      {
        id: 8,
        type: 'imaging',
        category: 'Radiology',
        title: 'Mammogram Screening',
        date: '2024-01-25',
        provider: 'Dr. Jennifer Wilson',
        specialty: 'Radiology',
        facility: 'Imaging Center',
        status: 'Final',
        procedure: 'Bilateral Diagnostic Mammography',
        findings: 'No suspicious masses or calcifications identified.',
        impression: 'BIRADS Category 1 - Negative',
        recommendation: 'Continue routine annual screening',
        notes: 'Normal screening mammogram. Next screening due in 12 months.',
        downloadUrl: '/records/imaging-2024-01-25.pdf'
      },
      // Procedures
      {
        id: 9,
        type: 'procedure',
        category: 'Procedure',
        title: 'Colonoscopy Screening',
        date: '2023-08-15',
        provider: 'Dr. Robert Smith',
        specialty: 'Gastroenterology',
        facility: 'Endoscopy Center',
        status: 'Complete',
        procedure: 'Screening Colonoscopy',
        indication: 'Routine screening - age 50+',
        findings: 'Two small polyps removed from sigmoid colon',
        pathology: 'Benign adenomatous polyps',
        complications: 'None',
        recommendation: 'Repeat colonoscopy in 5 years',
        postOpInstructions: 'Resume normal diet, follow-up if any concerning symptoms',
        downloadUrl: '/records/procedure-2023-08-15.pdf'
      }
    ];

    setRecords(mockRecords.sort((a, b) => new Date(b.date) - new Date(a.date)));
    setFilteredRecords(mockRecords.sort((a, b) => new Date(b.date) - new Date(a.date)));
    setLoading(false);
  }, []);

  useEffect(() => {
    let filtered = records;

    // Filter by tab/type
    if (activeTab !== 'all') {
      filtered = filtered.filter(record => record.type === activeTab);
    }

    // Filter by record type
    if (filterType !== 'all') {
      filtered = filtered.filter(record => record.type === filterType);
    }

    // Filter by provider
    if (filterProvider !== 'all') {
      filtered = filtered.filter(record => record.provider === filterProvider);
    }

    // Filter by date range
    if (dateRange !== 'all') {
      const now = new Date();
      const cutoffDate = new Date();
      
      switch (dateRange) {
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
      
      if (dateRange !== 'all') {
        filtered = filtered.filter(record => new Date(record.date) >= cutoffDate);
      }
    }

    // Filter by search term
    if (searchTerm) {
      filtered = filtered.filter(record =>
        record.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        record.category.toLowerCase().includes(searchTerm.toLowerCase()) ||
        record.provider.toLowerCase().includes(searchTerm.toLowerCase()) ||
        record.specialty.toLowerCase().includes(searchTerm.toLowerCase()) ||
        (record.summary && record.summary.toLowerCase().includes(searchTerm.toLowerCase())) ||
        (record.notes && record.notes.toLowerCase().includes(searchTerm.toLowerCase()))
      );
    }

    setFilteredRecords(filtered);
  }, [records, activeTab, filterType, filterProvider, dateRange, searchTerm]);

  const getRecordIcon = (type) => {
    switch (type) {
      case 'visit': return Stethoscope;
      case 'immunization': return Shield;
      case 'lab': return TestTube;
      case 'imaging': return Eye;
      case 'procedure': return Activity;
      case 'allergy': return AlertTriangle;
      case 'condition': return Heart;
      default: return FileText;
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'Final': return 'bg-green-100 text-green-800';
      case 'Administered': return 'bg-blue-100 text-blue-800';
      case 'Active': return 'bg-orange-100 text-orange-800';
      case 'Complete': return 'bg-purple-100 text-purple-800';
      case 'Pending': return 'bg-yellow-100 text-yellow-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const toggleRecordExpansion = (recordId) => {
    const newExpanded = new Set(expandedRecords);
    if (newExpanded.has(recordId)) {
      newExpanded.delete(recordId);
    } else {
      newExpanded.add(recordId);
    }
    setExpandedRecords(newExpanded);
  };

  const downloadRecord = (record) => {
    console.log(`Downloading record: ${record.title}`);
    alert(`PDF download for ${record.title} would start here`);
  };

  const downloadAllRecords = () => {
    console.log('Downloading all records');
    alert('Complete health record PDF compilation would start here');
  };

  const RecordCard = ({ record }) => {
    const RecordIcon = getRecordIcon(record.type);
    const isExpanded = expandedRecords.has(record.id);

    return (
      <div className="bg-white border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow">
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <div className="flex items-center space-x-3 mb-2">
              <RecordIcon className="w-5 h-5 text-blue-600" />
              <h3 className="text-lg font-semibold text-gray-900">{record.title}</h3>
              <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(record.status)}`}>
                {record.status}
              </span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4 text-sm text-gray-600">
              <div className="flex items-center space-x-2">
                <Calendar className="w-4 h-4" />
                <span>{record.date}</span>
              </div>
              <div className="flex items-center space-x-2">
                <User className="w-4 h-4" />
                <span>{record.provider}</span>
              </div>
              <div className="flex items-center space-x-2">
                <FileText className="w-4 h-4" />
                <span>{record.category}</span>
              </div>
            </div>

            {record.summary && (
              <p className="text-sm text-gray-600 mb-4">{record.summary}</p>
            )}

            {/* Expanded Details */}
            {isExpanded && (
              <div className="mt-4 space-y-4 bg-gray-50 p-4 rounded-lg">
                {/* Visit Details */}
                {record.type === 'visit' && (
                  <>
                    {record.chiefComplaint && (
                      <div>
                        <h4 className="font-medium text-gray-900 mb-1">Chief Complaint:</h4>
                        <p className="text-sm text-gray-600">{record.chiefComplaint}</p>
                      </div>
                    )}
                    
                    {record.vitals && (
                      <div>
                        <h4 className="font-medium text-gray-900 mb-2">Vital Signs:</h4>
                        <div className="grid grid-cols-2 md:grid-cols-3 gap-2 text-sm">
                          {Object.entries(record.vitals).map(([key, value]) => (
                            <div key={key} className="flex justify-between">
                              <span className="text-gray-600 capitalize">{key.replace(/([A-Z])/g, ' $1')}:</span>
                              <span className="text-gray-900">{value}</span>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {record.diagnosis && (
                      <div>
                        <h4 className="font-medium text-gray-900 mb-1">Diagnosis:</h4>
                        <ul className="text-sm text-gray-600">
                          {record.diagnosis.map((dx, index) => (
                            <li key={index}>{dx.code} - {dx.description}</li>
                          ))}
                        </ul>
                      </div>
                    )}

                    {record.assessment && (
                      <div>
                        <h4 className="font-medium text-gray-900 mb-1">Assessment:</h4>
                        <p className="text-sm text-gray-600">{record.assessment}</p>
                      </div>
                    )}

                    {record.plan && (
                      <div>
                        <h4 className="font-medium text-gray-900 mb-1">Plan:</h4>
                        <ul className="text-sm text-gray-600 list-disc list-inside">
                          {record.plan.map((item, index) => (
                            <li key={index}>{item}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </>
                )}

                {/* Immunization Details */}
                {record.type === 'immunization' && record.vaccine && (
                  <div>
                    <h4 className="font-medium text-gray-900 mb-2">Vaccine Details:</h4>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-sm">
                      <div className="flex justify-between">
                        <span className="text-gray-600">Vaccine:</span>
                        <span className="text-gray-900">{record.vaccine.name}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600">Manufacturer:</span>
                        <span className="text-gray-900">{record.vaccine.manufacturer}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600">Lot Number:</span>
                        <span className="text-gray-900">{record.vaccine.lotNumber}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600">Site:</span>
                        <span className="text-gray-900">{record.vaccine.site}</span>
                      </div>
                    </div>
                    {record.nextDue && (
                      <p className="text-sm text-blue-600 mt-2">Next dose due: {record.nextDue}</p>
                    )}
                  </div>
                )}

                {/* Allergy Details */}
                {record.type === 'allergy' && (
                  <div>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <h4 className="font-medium text-gray-900 mb-1">Allergen:</h4>
                        <p className="text-sm text-gray-600">{record.allergen}</p>
                      </div>
                      <div>
                        <h4 className="font-medium text-gray-900 mb-1">Reaction:</h4>
                        <p className="text-sm text-gray-600">{record.reaction}</p>
                      </div>
                      <div>
                        <h4 className="font-medium text-gray-900 mb-1">Severity:</h4>
                        <span className={`text-sm px-2 py-1 rounded-full ${
                          record.severity === 'Severe' ? 'bg-red-100 text-red-800' :
                          record.severity === 'Moderate' ? 'bg-orange-100 text-orange-800' :
                          'bg-yellow-100 text-yellow-800'
                        }`}>
                          {record.severity}
                        </span>
                      </div>
                    </div>
                    {record.alternatives && (
                      <div className="mt-4">
                        <h4 className="font-medium text-gray-900 mb-1">Safe Alternatives:</h4>
                        <p className="text-sm text-gray-600">{record.alternatives.join(', ')}</p>
                      </div>
                    )}
                  </div>
                )}

                {/* Medical Condition Details */}
                {record.type === 'condition' && (
                  <div>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <h4 className="font-medium text-gray-900 mb-1">Condition:</h4>
                        <p className="text-sm text-gray-600">{record.condition}</p>
                      </div>
                      <div>
                        <h4 className="font-medium text-gray-900 mb-1">ICD-10 Code:</h4>
                        <p className="text-sm text-gray-600">{record.icd10}</p>
                      </div>
                      <div>
                        <h4 className="font-medium text-gray-900 mb-1">Onset:</h4>
                        <p className="text-sm text-gray-600">{record.onset}</p>
                      </div>
                      <div>
                        <h4 className="font-medium text-gray-900 mb-1">Severity:</h4>
                        <p className="text-sm text-gray-600">{record.severity}</p>
                      </div>
                    </div>
                    {record.currentMedications && (
                      <div className="mt-4">
                        <h4 className="font-medium text-gray-900 mb-1">Current Medications:</h4>
                        <ul className="text-sm text-gray-600 list-disc list-inside">
                          {record.currentMedications.map((med, index) => (
                            <li key={index}>{med}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                )}

                {record.notes && (
                  <div className="mt-4 p-3 bg-blue-50 border border-blue-200 rounded-lg">
                    <h4 className="font-medium text-blue-800 mb-1">Provider Notes:</h4>
                    <p className="text-sm text-blue-700">{record.notes}</p>
                  </div>
                )}
              </div>
            )}
          </div>

          <div className="flex flex-col space-y-2 ml-4">
            <button
              onClick={() => toggleRecordExpansion(record.id)}
              className="px-3 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors text-sm flex items-center"
            >
              {isExpanded ? <ChevronDown className="w-4 h-4 mr-1" /> : <ChevronRight className="w-4 h-4 mr-1" />}
              {isExpanded ? 'Less' : 'Details'}
            </button>
            
            <button
              onClick={() => downloadRecord(record)}
              className="px-3 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm flex items-center"
            >
              <Download className="w-4 h-4 mr-1" />
              PDF
            </button>

            <button
              onClick={() => setSelectedRecord(record)}
              className="px-3 py-2 border border-blue-600 text-blue-600 rounded-lg hover:bg-blue-50 transition-colors text-sm flex items-center"
            >
              <Eye className="w-4 h-4 mr-1" />
              View
            </button>
          </div>
        </div>
      </div>
    );
  };

  const RecordDetailModal = () => {
    if (!selectedRecord) return null;

    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
        <div className="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-y-auto">
          <div className="p-6 border-b border-gray-200">
            <div className="flex items-center justify-between">
              <h2 className="text-xl font-semibold text-gray-900">{selectedRecord.title}</h2>
              <button 
                onClick={() => setSelectedRecord(null)}
                className="text-gray-400 hover:text-gray-600"
              >
                <X className="w-6 h-6" />
              </button>
            </div>
          </div>

          <div className="p-6">
            <RecordCard record={selectedRecord} />
          </div>
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

  const uniqueProviders = [...new Set(records.map(record => record.provider))];
  const recordTypes = [
    { value: 'all', label: 'All Records' },
    { value: 'visit', label: 'Visit Summaries' },
    { value: 'immunization', label: 'Immunizations' },
    { value: 'lab', label: 'Lab Results' },
    { value: 'imaging', label: 'Imaging' },
    { value: 'procedure', label: 'Procedures' },
    { value: 'allergy', label: 'Allergies' },
    { value: 'condition', label: 'Conditions' }
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Health Records</h1>
          <p className="text-gray-600">Complete medical history from electronic health records</p>
        </div>
        <button
          onClick={downloadAllRecords}
          className="mt-4 sm:mt-0 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors flex items-center"
        >
          <Download className="w-5 h-5 mr-2" />
          Download All Records
        </button>
      </div>

      {/* Search and Filters */}
      <div className="bg-white rounded-lg shadow p-6">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-4">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
            <input
              type="text"
              placeholder="Search records..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10 pr-4 py-2 w-full border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          
          <select
            value={filterType}
            onChange={(e) => setFilterType(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            {recordTypes.map(type => (
              <option key={type.value} value={type.value}>{type.label}</option>
            ))}
          </select>

          <select
            value={filterProvider}
            onChange={(e) => setFilterProvider(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="all">All Providers</option>
            {uniqueProviders.map((provider, index) => (
              <option key={index} value={provider}>{provider}</option>
            ))}
          </select>

          <select
            value={dateRange}
            onChange={(e) => setDateRange(e.target.value)}
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

      {/* Summary Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-white p-4 rounded-lg shadow">
          <div className="flex items-center space-x-3">
            <Stethoscope className="w-8 h-8 text-blue-600" />
            <div>
              <p className="text-sm text-gray-600">Total Visits</p>
              <p className="text-2xl font-bold text-gray-900">
                {records.filter(r => r.type === 'visit').length}
              </p>
            </div>
          </div>
        </div>
        
        <div className="bg-white p-4 rounded-lg shadow">
          <div className="flex items-center space-x-3">
            <Shield className="w-8 h-8 text-green-600" />
            <div>
              <p className="text-sm text-gray-600">Immunizations</p>
              <p className="text-2xl font-bold text-gray-900">
                {records.filter(r => r.type === 'immunization').length}
              </p>
            </div>
          </div>
        </div>
        
        <div className="bg-white p-4 rounded-lg shadow">
          <div className="flex items-center space-x-3">
            <AlertTriangle className="w-8 h-8 text-orange-600" />
            <div>
              <p className="text-sm text-gray-600">Active Allergies</p>
              <p className="text-2xl font-bold text-gray-900">
                {records.filter(r => r.type === 'allergy' && r.status === 'Active').length}
              </p>
            </div>
          </div>
        </div>
        
        <div className="bg-white p-4 rounded-lg shadow">
          <div className="flex items-center space-x-3">
            <Heart className="w-8 h-8 text-red-600" />
            <div>
              <p className="text-sm text-gray-600">Conditions</p>
              <p className="text-2xl font-bold text-gray-900">
                {records.filter(r => r.type === 'condition').length}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="bg-white rounded-lg shadow">
        <div className="border-b border-gray-200">
          <nav className="flex space-x-8 px-6">
            {[
              { id: 'all', label: 'All Records', count: records.length },
              { id: 'visit', label: 'Visits', count: records.filter(r => r.type === 'visit').length },
              { id: 'immunization', label: 'Immunizations', count: records.filter(r => r.type === 'immunization').length },
              { id: 'allergy', label: 'Allergies', count: records.filter(r => r.type === 'allergy').length },
              { id: 'condition', label: 'Conditions', count: records.filter(r => r.type === 'condition').length }
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
                {tab.label} ({tab.count})
              </button>
            ))}
          </nav>
        </div>

        {/* Records List */}
        <div className="p-6">
          {filteredRecords.length === 0 ? (
            <div className="text-center py-12">
              <Folder className="mx-auto h-12 w-12 text-gray-400" />
              <h3 className="mt-2 text-sm font-medium text-gray-900">No records found</h3>
              <p className="mt-1 text-sm text-gray-500">
                No health records match your current filters.
              </p>
            </div>
          ) : (
            <div className="space-y-4">
              <div className="mb-4 text-sm text-gray-600">
                Showing {filteredRecords.length} records in chronological order (newest first)
              </div>
              {filteredRecords.map(record => (
                <RecordCard key={record.id} record={record} />
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Detail Modal */}
      <RecordDetailModal />
    </div>
  );
};

export default Records;
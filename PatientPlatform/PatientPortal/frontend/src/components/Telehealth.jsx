import React, { useState, useEffect, useRef } from 'react';
import {
  Video, VideoOff, Mic, MicOff, Phone, PhoneOff, Settings, Users,
  Monitor, MonitorSpeaker, Camera, CameraOff, Volume2, VolumeX,
  MessageSquare, Share, Download, Upload, Clock, AlertCircle,
  CheckCircle, HelpCircle, Wifi, WifiOff, Signal, Battery,
  Maximize2, Minimize2, RotateCcw, Pause, Play, Circle,
  Calendar, User, FileText, Link, ExternalLink, Smartphone,
  Laptop, Tablet, Globe, Shield, Zap, Activity, Heart
} from 'lucide-react';
import { useAPI } from '../hooks/useAPI';

const Telehealth = () => {
  const [activeTab, setActiveTab] = useState('appointments');
  const [telehealthData, setTelehealthData] = useState({
    upcomingAppointments: [],
    completedSessions: [],
    systemStatus: {},
    deviceChecks: {},
    supportResources: []
  });
  const [loading, setLoading] = useState(true);
  const [isInCall, setIsInCall] = useState(false);
  const [callSettings, setCallSettings] = useState({
    video: true,
    audio: true,
    screen: false,
    recording: false
  });
  const [connectionStatus, setConnectionStatus] = useState('checking');
  const [showTechCheck, setShowTechCheck] = useState(false);
  const [showJoinModal, setShowJoinModal] = useState(false);
  const [selectedAppointment, setSelectedAppointment] = useState(null);

  // Refs for video elements
  const localVideoRef = useRef(null);
  const remoteVideoRef = useRef(null);
  const localStreamRef = useRef(null);

  useEffect(() => {
    // Mock comprehensive telehealth data
    const mockData = {
      // Upcoming Telehealth Appointments
      upcomingAppointments: [
        {
          id: 1,
          appointmentId: 'TH-2024-001',
          type: 'video',
          patientName: 'John Smith',
          providerName: 'Dr. Sarah Johnson',
          specialty: 'Primary Care',
          scheduledDate: '2024-02-20',
          scheduledTime: '2:00 PM',
          duration: 30,
          status: 'scheduled',
          meetingUrl: 'https://telehealth.clinic.com/room/th-001',
          joinAvailable: true,
          joinTime: '1:50 PM',
          preVisitCompleted: true,
          techCheckPassed: true,
          appointmentNotes: 'Follow-up for blood pressure monitoring',
          insuranceVerified: true,
          consentSigned: true,
          prescriptionsReady: false,
          documentsToReview: ['Lab Results - Feb 15', 'Previous Visit Summary']
        },
        {
          id: 2,
          appointmentId: 'TH-2024-002',
          type: 'audio',
          patientName: 'John Smith',
          providerName: 'Dr. Michael Chen',
          specialty: 'Cardiology',
          scheduledDate: '2024-02-25',
          scheduledTime: '10:30 AM',
          duration: 45,
          status: 'confirmed',
          meetingUrl: 'https://telehealth.clinic.com/room/th-002',
          joinAvailable: false,
          joinTime: '10:20 AM',
          preVisitCompleted: false,
          techCheckPassed: false,
          appointmentNotes: 'Consultation for cardiac stress test results',
          insuranceVerified: true,
          consentSigned: false,
          prescriptionsReady: true,
          documentsToReview: ['Stress Test Results', 'EKG Report', 'Medication History']
        },
        {
          id: 3,
          appointmentId: 'TH-2024-003',
          type: 'video',
          patientName: 'John Smith',
          providerName: 'Dr. Emily Rodriguez',
          specialty: 'Dermatology',
          scheduledDate: '2024-03-05',
          scheduledTime: '3:15 PM',
          duration: 20,
          status: 'pending-confirmation',
          meetingUrl: null,
          joinAvailable: false,
          joinTime: null,
          preVisitCompleted: false,
          techCheckPassed: false,
          appointmentNotes: 'Skin lesion evaluation with photo documentation',
          insuranceVerified: false,
          consentSigned: false,
          prescriptionsReady: false,
          documentsToReview: ['Previous Dermatology Photos', 'Treatment History']
        }
      ],

      // Completed Telehealth Sessions
      completedSessions: [
        {
          id: 101,
          appointmentId: 'TH-2024-050',
          patientName: 'John Smith',
          providerName: 'Dr. Sarah Johnson',
          specialty: 'Primary Care',
          sessionDate: '2024-02-01',
          sessionTime: '2:00 PM',
          duration: 28,
          actualDuration: 28,
          type: 'video',
          status: 'completed',
          quality: 'excellent',
          issuesReported: false,
          summary: 'Routine follow-up completed successfully. Blood pressure stable.',
          prescriptionsIssued: 2,
          followUpScheduled: true,
          nextAppointment: '2024-03-01',
          patientSatisfaction: 5,
          technicalIssues: 'None',
          recordingAvailable: true,
          transcriptAvailable: true
        },
        {
          id: 102,
          appointmentId: 'TH-2024-049',
          patientName: 'John Smith',
          providerName: 'Dr. Lisa Park',
          specialty: 'Mental Health',
          sessionDate: '2024-01-28',
          sessionTime: '11:00 AM',
          duration: 50,
          actualDuration: 52,
          type: 'video',
          status: 'completed',
          quality: 'good',
          issuesReported: true,
          summary: 'Therapy session focused on anxiety management techniques.',
          prescriptionsIssued: 0,
          followUpScheduled: true,
          nextAppointment: '2024-02-25',
          patientSatisfaction: 4,
          technicalIssues: 'Minor audio delay in first 5 minutes',
          recordingAvailable: false,
          transcriptAvailable: false
        }
      ],

      // System Status and Requirements
      systemStatus: {
        serverStatus: 'operational',
        lastCheck: '2024-02-16 14:30:00',
        uptime: '99.97%',
        activeUsers: 1247,
        systemLoad: 'low',
        maintenanceScheduled: false,
        maintenanceWindow: null,
        supportedBrowsers: ['Chrome 90+', 'Firefox 88+', 'Safari 14+', 'Edge 90+'],
        minimumBandwidth: '1 Mbps upload / 1 Mbps download',
        recommendedBandwidth: '2 Mbps upload / 2 Mbps download',
        systemRequirements: {
          os: ['Windows 10+', 'macOS 10.15+', 'iOS 14+', 'Android 8+'],
          browser: ['Chrome', 'Firefox', 'Safari', 'Edge'],
          camera: 'HD Camera (720p minimum)',
          microphone: 'Built-in or external microphone',
          speakers: 'Built-in speakers or headphones recommended'
        }
      },

      // Device and Connection Checks
      deviceChecks: {
        camera: { status: 'working', resolution: '1080p', framerate: '30fps' },
        microphone: { status: 'working', level: 85, quality: 'good' },
        speakers: { status: 'working', volume: 75, quality: 'excellent' },
        connection: { 
          status: 'excellent', 
          speed: '45.2 Mbps', 
          latency: '23ms', 
          packetLoss: '0.1%',
          jitter: '2ms'
        },
        browser: { 
          name: 'Chrome', 
          version: '121.0.6167.184', 
          supported: true, 
          webrtc: true,
          permissions: {
            camera: 'granted',
            microphone: 'granted',
            notifications: 'granted'
          }
        },
        lastChecked: '2024-02-16 14:25:00'
      },

      // Support Resources and Guides
      supportResources: [
        {
          id: 1,
          category: 'Getting Started',
          title: 'First-Time Telehealth Setup Guide',
          description: 'Complete guide for setting up your device for telehealth visits',
          type: 'guide',
          estimatedTime: '5 minutes',
          steps: [
            'Download and install required software',
            'Test your camera and microphone',
            'Check your internet connection',
            'Complete practice session',
            'Review appointment details'
          ],
          popular: true,
          lastUpdated: '2024-02-10'
        },
        {
          id: 2,
          category: 'Troubleshooting',
          title: 'Audio and Video Issues',
          description: 'Solve common audio and video problems during telehealth calls',
          type: 'troubleshooting',
          estimatedTime: '3 minutes',
          commonIssues: [
            'No video appearing',
            'Audio not working',
            'Poor video quality',
            'Echo or feedback',
            'Connection dropping'
          ],
          popular: true,
          lastUpdated: '2024-02-12'
        },
        {
          id: 3,
          category: 'Privacy & Security',
          title: 'Telehealth Privacy and Security',
          description: 'Understanding how your privacy is protected during virtual visits',
          type: 'information',
          estimatedTime: '4 minutes',
          topics: [
            'HIPAA compliance',
            'End-to-end encryption',
            'Recording policies',
            'Data storage and retention',
            'Patient rights and consent'
          ],
          popular: false,
          lastUpdated: '2024-02-08'
        },
        {
          id: 4,
          category: 'Device Support',
          title: 'Supported Devices and Browsers',
          description: 'Complete list of compatible devices and system requirements',
          type: 'reference',
          estimatedTime: '2 minutes',
          devices: [
            'Desktop computers (Windows, Mac, Linux)',
            'Smartphones (iOS, Android)',
            'Tablets (iPad, Android tablets)',
            'Smart TVs with camera (limited support)'
          ],
          popular: false,
          lastUpdated: '2024-02-05'
        },
        {
          id: 5,
          category: 'Best Practices',
          title: 'Tips for a Successful Telehealth Visit',
          description: 'Best practices to ensure a smooth and productive virtual appointment',
          type: 'tips',
          estimatedTime: '3 minutes',
          tips: [
            'Choose a quiet, private location',
            'Test technology 15 minutes before appointment',
            'Have good lighting facing you',
            'Prepare questions and documents in advance',
            'Use headphones for better audio quality'
          ],
          popular: true,
          lastUpdated: '2024-02-14'
        }
      ]
    };

    setTelehealthData(mockData);
    setLoading(false);

    // Simulate connection check
    setTimeout(() => {
      setConnectionStatus('excellent');
    }, 2000);
  }, []);

  const getStatusColor = (status) => {
    switch (status) {
      case 'scheduled': case 'confirmed': case 'completed': case 'excellent': case 'working': return 'text-green-600 bg-green-100';
      case 'pending-confirmation': case 'good': return 'text-yellow-600 bg-yellow-100';
      case 'cancelled': case 'failed': case 'poor': return 'text-red-600 bg-red-100';
      case 'checking': case 'in-progress': return 'text-blue-600 bg-blue-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  const getConnectionIcon = (status) => {
    switch (status) {
      case 'excellent': return <Wifi className="w-5 h-5 text-green-600" />;
      case 'good': return <Signal className="w-5 h-5 text-yellow-600" />;
      case 'poor': return <WifiOff className="w-5 h-5 text-red-600" />;
      case 'checking': return <Activity className="w-5 h-5 text-blue-600 animate-pulse" />;
      default: return <WifiOff className="w-5 h-5 text-gray-600" />;
    }
  };

  const startTechCheck = async () => {
    setShowTechCheck(true);
    // Simulate tech check process
    const checks = ['camera', 'microphone', 'speakers', 'connection'];
    for (let check of checks) {
      await new Promise(resolve => setTimeout(resolve, 1000));
      console.log(`${check} check completed`);
    }
  };

  const joinAppointment = (appointment) => {
    setSelectedAppointment(appointment);
    setShowJoinModal(true);
  };

  const startVideoCall = async () => {
    try {
      // Request user media (camera and microphone)
      const stream = await navigator.mediaDevices.getUserMedia({
        video: callSettings.video,
        audio: callSettings.audio
      });
      
      localStreamRef.current = stream;
      if (localVideoRef.current) {
        localVideoRef.current.srcObject = stream;
      }
      
      setIsInCall(true);
      setShowJoinModal(false);
      
      // In real implementation, this would establish WebRTC connection
      console.log('Video call started with settings:', callSettings);
    } catch (error) {
      console.error('Error starting video call:', error);
      alert('Error accessing camera/microphone. Please check permissions.');
    }
  };

  const endCall = () => {
    if (localStreamRef.current) {
      localStreamRef.current.getTracks().forEach(track => track.stop());
    }
    setIsInCall(false);
    setSelectedAppointment(null);
  };

  const toggleSetting = (setting) => {
    setCallSettings(prev => ({
      ...prev,
      [setting]: !prev[setting]
    }));
  };

  const UpcomingAppointmentsTab = () => (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold text-gray-900">Upcoming Telehealth Appointments</h3>
        <button
          onClick={startTechCheck}
          className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors flex items-center"
        >
          <Settings className="w-4 h-4 mr-2" />
          Tech Check
        </button>
      </div>

      <div className="space-y-4">
        {telehealthData.upcomingAppointments.map(appointment => (
          <div key={appointment.id} className="bg-white border border-gray-200 rounded-lg p-6">
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <div className="flex items-center space-x-3 mb-3">
                  {appointment.type === 'video' ? (
                    <Video className="w-6 h-6 text-blue-600" />
                  ) : (
                    <Phone className="w-6 h-6 text-green-600" />
                  )}
                  <div>
                    <h4 className="font-semibold text-gray-900">
                      {appointment.providerName} - {appointment.specialty}
                    </h4>
                    <p className="text-sm text-gray-600">{appointment.appointmentNotes}</p>
                  </div>
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(appointment.status)}`}>
                    {appointment.status}
                  </span>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-4 gap-4 text-sm text-gray-600 mb-4">
                  <div className="flex items-center space-x-2">
                    <Calendar className="w-4 h-4" />
                    <span>{appointment.scheduledDate} at {appointment.scheduledTime}</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <Clock className="w-4 h-4" />
                    <span>{appointment.duration} minutes</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <User className="w-4 h-4" />
                    <span>ID: {appointment.appointmentId}</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    {appointment.joinAvailable ? (
                      <CheckCircle className="w-4 h-4 text-green-600" />
                    ) : (
                      <Clock className="w-4 h-4 text-yellow-600" />
                    )}
                    <span>
                      {appointment.joinAvailable ? `Join at ${appointment.joinTime}` : 'Join not available yet'}
                    </span>
                  </div>
                </div>

                {/* Pre-visit Checklist */}
                <div className="bg-gray-50 rounded-lg p-4 mb-4">
                  <h5 className="font-medium text-gray-900 mb-3">Pre-Visit Checklist</h5>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                    <div className="flex items-center space-x-2">
                      {appointment.preVisitCompleted ? (
                        <CheckCircle className="w-4 h-4 text-green-600" />
                      ) : (
                        <AlertCircle className="w-4 h-4 text-yellow-600" />
                      )}
                      <span className="text-sm">Pre-visit forms completed</span>
                    </div>
                    <div className="flex items-center space-x-2">
                      {appointment.techCheckPassed ? (
                        <CheckCircle className="w-4 h-4 text-green-600" />
                      ) : (
                        <AlertCircle className="w-4 h-4 text-yellow-600" />
                      )}
                      <span className="text-sm">Technology check passed</span>
                    </div>
                    <div className="flex items-center space-x-2">
                      {appointment.insuranceVerified ? (
                        <CheckCircle className="w-4 h-4 text-green-600" />
                      ) : (
                        <AlertCircle className="w-4 h-4 text-yellow-600" />
                      )}
                      <span className="text-sm">Insurance verified</span>
                    </div>
                    <div className="flex items-center space-x-2">
                      {appointment.consentSigned ? (
                        <CheckCircle className="w-4 h-4 text-green-600" />
                      ) : (
                        <AlertCircle className="w-4 h-4 text-red-600" />
                      )}
                      <span className="text-sm">Telehealth consent signed</span>
                    </div>
                  </div>
                </div>

                {/* Documents to Review */}
                {appointment.documentsToReview.length > 0 && (
                  <div className="mb-4">
                    <h5 className="font-medium text-gray-900 mb-2">Documents to Review</h5>
                    <div className="flex flex-wrap gap-2">
                      {appointment.documentsToReview.map((doc, index) => (
                        <span key={index} className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded">
                          <FileText className="w-3 h-3 inline mr-1" />
                          {doc}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>

              <div className="flex flex-col space-y-2 ml-4">
                {appointment.joinAvailable ? (
                  <button
                    onClick={() => joinAppointment(appointment)}
                    className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors flex items-center"
                  >
                    <Video className="w-4 h-4 mr-2" />
                    Join Visit
                  </button>
                ) : (
                  <button
                    disabled
                    className="px-4 py-2 bg-gray-300 text-gray-500 rounded-lg cursor-not-allowed flex items-center"
                  >
                    <Clock className="w-4 h-4 mr-2" />
                    Not Available
                  </button>
                )}
                
                <button className="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors text-sm">
                  <Settings className="w-4 h-4 mr-2 inline" />
                  Tech Check
                </button>
                
                {appointment.meetingUrl && (
                  <button className="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors text-sm">
                    <Link className="w-4 h-4 mr-2 inline" />
                    Copy Link
                  </button>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  const CompletedSessionsTab = () => (
    <div className="space-y-6">
      <h3 className="text-lg font-semibold text-gray-900">Completed Telehealth Sessions</h3>
      
      <div className="space-y-4">
        {telehealthData.completedSessions.map(session => (
          <div key={session.id} className="bg-white border border-gray-200 rounded-lg p-6">
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <div className="flex items-center space-x-3 mb-3">
                  {session.type === 'video' ? (
                    <Video className="w-6 h-6 text-blue-600" />
                  ) : (
                    <Phone className="w-6 h-6 text-green-600" />
                  )}
                  <div>
                    <h4 className="font-semibold text-gray-900">
                      {session.providerName} - {session.specialty}
                    </h4>
                    <p className="text-sm text-gray-600">{session.summary}</p>
                  </div>
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(session.quality)}`}>
                    {session.quality} quality
                  </span>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-4 gap-4 text-sm text-gray-600 mb-4">
                  <div className="flex items-center space-x-2">
                    <Calendar className="w-4 h-4" />
                    <span>{session.sessionDate} at {session.sessionTime}</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <Clock className="w-4 h-4" />
                    <span>{session.actualDuration} minutes</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <User className="w-4 h-4" />
                    <span>ID: {session.appointmentId}</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <Heart className="w-4 h-4" />
                    <span>Rating: {session.patientSatisfaction}/5</span>
                  </div>
                </div>

                {/* Session Details */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                  <div>
                    <span className="font-medium text-gray-700">Prescriptions Issued:</span>
                    <span className="ml-2 text-gray-600">{session.prescriptionsIssued}</span>
                  </div>
                  <div>
                    <span className="font-medium text-gray-700">Follow-up Scheduled:</span>
                    <span className="ml-2 text-gray-600">
                      {session.followUpScheduled ? session.nextAppointment : 'No'}
                    </span>
                  </div>
                  <div>
                    <span className="font-medium text-gray-700">Technical Issues:</span>
                    <span className="ml-2 text-gray-600">{session.technicalIssues}</span>
                  </div>
                </div>
              </div>

              <div className="flex flex-col space-y-2 ml-4">
                <button className="px-3 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors text-sm">
                  <FileText className="w-4 h-4 mr-2 inline" />
                  View Summary
                </button>
                
                {session.recordingAvailable && (
                  <button className="px-3 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors text-sm">
                    <Play className="w-4 h-4 mr-2 inline" />
                    Recording
                  </button>
                )}
                
                {session.transcriptAvailable && (
                  <button className="px-3 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors text-sm">
                    <Download className="w-4 h-4 mr-2 inline" />
                    Transcript
                  </button>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  const SystemStatusTab = () => (
    <div className="space-y-6">
      <h3 className="text-lg font-semibold text-gray-900">System Status & Requirements</h3>

      {/* Current System Status */}
      <div className="bg-white border border-gray-200 rounded-lg p-6">
        <h4 className="font-semibold text-gray-900 mb-4">Current System Status</h4>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="flex items-center space-x-3">
            {getConnectionIcon(telehealthData.systemStatus.serverStatus)}
            <div>
              <p className="font-medium text-gray-900">Server Status</p>
              <p className="text-sm text-gray-600 capitalize">{telehealthData.systemStatus.serverStatus}</p>
            </div>
          </div>
          <div className="flex items-center space-x-3">
            <Activity className="w-5 h-5 text-green-600" />
            <div>
              <p className="font-medium text-gray-900">Uptime</p>
              <p className="text-sm text-gray-600">{telehealthData.systemStatus.uptime}</p>
            </div>
          </div>
          <div className="flex items-center space-x-3">
            <Users className="w-5 h-5 text-blue-600" />
            <div>
              <p className="font-medium text-gray-900">Active Users</p>
              <p className="text-sm text-gray-600">{telehealthData.systemStatus.activeUsers.toLocaleString()}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Device Check Results */}
      <div className="bg-white border border-gray-200 rounded-lg p-6">
        <div className="flex items-center justify-between mb-4">
          <h4 className="font-semibold text-gray-900">Your Device Status</h4>
          <button
            onClick={startTechCheck}
            className="px-3 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm"
          >
            Run Check
          </button>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div className="flex items-center space-x-3">
            <Camera className={`w-5 h-5 ${telehealthData.deviceChecks.camera.status === 'working' ? 'text-green-600' : 'text-red-600'}`} />
            <div>
              <p className="font-medium text-gray-900">Camera</p>
              <p className="text-sm text-gray-600">{telehealthData.deviceChecks.camera.resolution}</p>
            </div>
          </div>
          
          <div className="flex items-center space-x-3">
            <Mic className={`w-5 h-5 ${telehealthData.deviceChecks.microphone.status === 'working' ? 'text-green-600' : 'text-red-600'}`} />
            <div>
              <p className="font-medium text-gray-900">Microphone</p>
              <p className="text-sm text-gray-600">Level: {telehealthData.deviceChecks.microphone.level}%</p>
            </div>
          </div>
          
          <div className="flex items-center space-x-3">
            <Volume2 className={`w-5 h-5 ${telehealthData.deviceChecks.speakers.status === 'working' ? 'text-green-600' : 'text-red-600'}`} />
            <div>
              <p className="font-medium text-gray-900">Speakers</p>
              <p className="text-sm text-gray-600">{telehealthData.deviceChecks.speakers.quality}</p>
            </div>
          </div>
          
          <div className="flex items-center space-x-3">
            {getConnectionIcon(telehealthData.deviceChecks.connection.status)}
            <div>
              <p className="font-medium text-gray-900">Connection</p>
              <p className="text-sm text-gray-600">{telehealthData.deviceChecks.connection.speed}</p>
            </div>
          </div>
        </div>

        <div className="mt-6 pt-6 border-t border-gray-200">
          <h5 className="font-medium text-gray-900 mb-3">Connection Details</h5>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 text-sm">
            <div>
              <span className="font-medium text-gray-700">Speed:</span>
              <span className="ml-2 text-gray-600">{telehealthData.deviceChecks.connection.speed}</span>
            </div>
            <div>
              <span className="font-medium text-gray-700">Latency:</span>
              <span className="ml-2 text-gray-600">{telehealthData.deviceChecks.connection.latency}</span>
            </div>
            <div>
              <span className="font-medium text-gray-700">Packet Loss:</span>
              <span className="ml-2 text-gray-600">{telehealthData.deviceChecks.connection.packetLoss}</span>
            </div>
            <div>
              <span className="font-medium text-gray-700">Jitter:</span>
              <span className="ml-2 text-gray-600">{telehealthData.deviceChecks.connection.jitter}</span>
            </div>
          </div>
        </div>
      </div>

      {/* System Requirements */}
      <div className="bg-white border border-gray-200 rounded-lg p-6">
        <h4 className="font-semibold text-gray-900 mb-4">System Requirements</h4>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h5 className="font-medium text-gray-900 mb-3">Minimum Requirements</h5>
            <ul className="space-y-2 text-sm text-gray-600">
              <li className="flex items-center space-x-2">
                <Laptop className="w-4 h-4" />
                <span>Operating System: Windows 10+, macOS 10.15+</span>
              </li>
              <li className="flex items-center space-x-2">
                <Globe className="w-4 h-4" />
                <span>Browser: Chrome 90+, Firefox 88+, Safari 14+</span>
              </li>
              <li className="flex items-center space-x-2">
                <Wifi className="w-4 h-4" />
                <span>Internet: {telehealthData.systemStatus.minimumBandwidth}</span>
              </li>
              <li className="flex items-center space-x-2">
                <Camera className="w-4 h-4" />
                <span>Camera: HD Camera (720p minimum)</span>
              </li>
              <li className="flex items-center space-x-2">
                <Mic className="w-4 h-4" />
                <span>Audio: Built-in or external microphone</span>
              </li>
            </ul>
          </div>
          
          <div>
            <h5 className="font-medium text-gray-900 mb-3">Recommended for Best Experience</h5>
            <ul className="space-y-2 text-sm text-gray-600">
              <li className="flex items-center space-x-2">
                <Zap className="w-4 h-4" />
                <span>Internet: {telehealthData.systemStatus.recommendedBandwidth}</span>
              </li>
              <li className="flex items-center space-x-2">
                <Camera className="w-4 h-4" />
                <span>Camera: Full HD Camera (1080p)</span>
              </li>
              <li className="flex items-center space-x-2">
                <Volume2 className="w-4 h-4" />
                <span>Audio: Headphones or dedicated speakers</span>
              </li>
              <li className="flex items-center space-x-2">
                <Monitor className="w-4 h-4" />
                <span>Display: Large screen for better visibility</span>
              </li>
              <li className="flex items-center space-x-2">
                <Shield className="w-4 h-4" />
                <span>Environment: Quiet, private space</span>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );

  const TechSupportTab = () => (
    <div className="space-y-6">
      <h3 className="text-lg font-semibold text-gray-900">Technical Support & Guides</h3>

      {/* Quick Help Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <div className="flex items-center space-x-3 mb-3">
            <HelpCircle className="w-6 h-6 text-blue-600" />
            <h4 className="font-semibold text-blue-900">Need Help Now?</h4>
          </div>
          <p className="text-sm text-blue-700 mb-3">Get immediate assistance during your appointment</p>
          <button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm">
            Contact Support
          </button>
        </div>

        <div className="bg-green-50 border border-green-200 rounded-lg p-4">
          <div className="flex items-center space-x-3 mb-3">
            <Settings className="w-6 h-6 text-green-600" />
            <h4 className="font-semibold text-green-900">Test Your Setup</h4>
          </div>
          <p className="text-sm text-green-700 mb-3">Run a complete system check before your appointment</p>
          <button
            onClick={startTechCheck}
            className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors text-sm"
          >
            Run Test
          </button>
        </div>

        <div className="bg-purple-50 border border-purple-200 rounded-lg p-4">
          <div className="flex items-center space-x-3 mb-3">
            <Play className="w-6 h-6 text-purple-600" />
            <h4 className="font-semibold text-purple-900">Practice Session</h4>
          </div>
          <p className="text-sm text-purple-700 mb-3">Try a practice video call to get comfortable</p>
          <button className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors text-sm">
            Start Practice
          </button>
        </div>
      </div>

      {/* Support Resources */}
      <div className="space-y-4">
        {telehealthData.supportResources.map(resource => (
          <div key={resource.id} className="bg-white border border-gray-200 rounded-lg p-6">
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <div className="flex items-center space-x-3 mb-3">
                  <FileText className="w-6 h-6 text-blue-600" />
                  <div>
                    <h4 className="font-semibold text-gray-900">{resource.title}</h4>
                    <p className="text-sm text-gray-600">{resource.category}</p>
                  </div>
                  {resource.popular && (
                    <span className="px-2 py-1 bg-yellow-100 text-yellow-800 text-xs rounded-full font-medium">
                      Popular
                    </span>
                  )}
                </div>

                <p className="text-sm text-gray-600 mb-4">{resource.description}</p>

                <div className="flex items-center space-x-4 text-sm text-gray-500 mb-4">
                  <span>📚 {resource.type}</span>
                  <span>⏱️ {resource.estimatedTime}</span>
                  <span>📅 Updated {resource.lastUpdated}</span>
                </div>

                {/* Resource Content Preview */}
                {resource.steps && (
                  <div className="bg-gray-50 rounded-lg p-4">
                    <h5 className="font-medium text-gray-900 mb-2">Steps:</h5>
                    <ol className="list-decimal list-inside space-y-1 text-sm text-gray-600">
                      {resource.steps.map((step, index) => (
                        <li key={index}>{step}</li>
                      ))}
                    </ol>
                  </div>
                )}

                {resource.commonIssues && (
                  <div className="bg-gray-50 rounded-lg p-4">
                    <h5 className="font-medium text-gray-900 mb-2">Common Issues:</h5>
                    <ul className="list-disc list-inside space-y-1 text-sm text-gray-600">
                      {resource.commonIssues.map((issue, index) => (
                        <li key={index}>{issue}</li>
                      ))}
                    </ul>
                  </div>
                )}

                {resource.tips && (
                  <div className="bg-gray-50 rounded-lg p-4">
                    <h5 className="font-medium text-gray-900 mb-2">Tips:</h5>
                    <ul className="list-disc list-inside space-y-1 text-sm text-gray-600">
                      {resource.tips.map((tip, index) => (
                        <li key={index}>{tip}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>

              <div className="flex flex-col space-y-2 ml-4">
                <button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm">
                  View Guide
                </button>
                <button className="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors text-sm">
                  <Download className="w-4 h-4 mr-2 inline" />
                  Download
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  // Video Call Interface
  const VideoCallInterface = () => {
    if (!isInCall) return null;

    return (
      <div className="fixed inset-0 bg-black z-50 flex flex-col">
        {/* Video Area */}
        <div className="flex-1 relative">
          {/* Remote Video (Main) */}
          <video
            ref={remoteVideoRef}
            className="w-full h-full object-cover"
            autoPlay
            playsInline
          />
          
          {/* Local Video (Picture-in-Picture) */}
          <div className="absolute top-4 right-4 w-48 h-36 bg-gray-800 rounded-lg overflow-hidden">
            <video
              ref={localVideoRef}
              className="w-full h-full object-cover"
              autoPlay
              playsInline
              muted
            />
          </div>

          {/* Connection Status */}
          <div className="absolute top-4 left-4 flex items-center space-x-2 bg-black bg-opacity-50 text-white px-3 py-2 rounded-lg">
            {getConnectionIcon(connectionStatus)}
            <span className="text-sm">Connection: {connectionStatus}</span>
          </div>

          {/* Call Info */}
          <div className="absolute top-4 left-1/2 transform -translate-x-1/2 bg-black bg-opacity-50 text-white px-4 py-2 rounded-lg">
            <div className="text-center">
              <p className="font-medium">{selectedAppointment?.providerName}</p>
              <p className="text-sm">{selectedAppointment?.specialty}</p>
            </div>
          </div>
        </div>

        {/* Control Bar */}
        <div className="bg-gray-900 p-4">
          <div className="flex items-center justify-center space-x-4">
            <button
              onClick={() => toggleSetting('audio')}
              className={`p-3 rounded-full ${callSettings.audio ? 'bg-gray-700 text-white' : 'bg-red-600 text-white'}`}
            >
              {callSettings.audio ? <Mic className="w-6 h-6" /> : <MicOff className="w-6 h-6" />}
            </button>

            <button
              onClick={() => toggleSetting('video')}
              className={`p-3 rounded-full ${callSettings.video ? 'bg-gray-700 text-white' : 'bg-red-600 text-white'}`}
            >
              {callSettings.video ? <Video className="w-6 h-6" /> : <VideoOff className="w-6 h-6" />}
            </button>

            <button
              onClick={() => toggleSetting('screen')}
              className={`p-3 rounded-full ${callSettings.screen ? 'bg-blue-600 text-white' : 'bg-gray-700 text-white'}`}
            >
              <Monitor className="w-6 h-6" />
            </button>

            <button className="p-3 rounded-full bg-gray-700 text-white">
              <MessageSquare className="w-6 h-6" />
            </button>

            <button
              onClick={() => toggleSetting('recording')}
              className={`p-3 rounded-full ${callSettings.recording ? 'bg-red-600 text-white' : 'bg-gray-700 text-white'}`}
            >
              <Circle className="w-6 h-6" />
            </button>

            <button
              onClick={endCall}
              className="p-3 rounded-full bg-red-600 text-white"
            >
              <PhoneOff className="w-6 h-6" />
            </button>
          </div>
        </div>
      </div>
    );
  };

  // Join Appointment Modal
  const JoinAppointmentModal = () => {
    if (!showJoinModal || !selectedAppointment) return null;

    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
        <div className="bg-white rounded-lg max-w-2xl w-full">
          <div className="p-6 border-b border-gray-200">
            <h2 className="text-xl font-semibold text-gray-900">Join Telehealth Appointment</h2>
            <p className="text-gray-600">{selectedAppointment.providerName} - {selectedAppointment.specialty}</p>
          </div>

          <div className="p-6 space-y-6">
            {/* Pre-join Checklist */}
            <div>
              <h3 className="font-medium text-gray-900 mb-3">Pre-Join Checklist</h3>
              <div className="space-y-2">
                <div className="flex items-center space-x-2">
                  <CheckCircle className="w-5 h-5 text-green-600" />
                  <span className="text-sm">Camera and microphone permissions granted</span>
                </div>
                <div className="flex items-center space-x-2">
                  <CheckCircle className="w-5 h-5 text-green-600" />
                  <span className="text-sm">Internet connection stable</span>
                </div>
                <div className="flex items-center space-x-2">
                  <CheckCircle className="w-5 h-5 text-green-600" />
                  <span className="text-sm">Quiet, private environment ready</span>
                </div>
              </div>
            </div>

            {/* Video Preview */}
            <div>
              <h3 className="font-medium text-gray-900 mb-3">Video Preview</h3>
              <div className="bg-gray-900 rounded-lg aspect-video flex items-center justify-center">
                <video
                  ref={localVideoRef}
                  className="w-full h-full object-cover rounded-lg"
                  autoPlay
                  playsInline
                  muted
                />
              </div>
            </div>

            {/* Controls */}
            <div>
              <h3 className="font-medium text-gray-900 mb-3">Call Settings</h3>
              <div className="flex items-center space-x-4">
                <button
                  onClick={() => toggleSetting('video')}
                  className={`flex items-center space-x-2 px-4 py-2 rounded-lg ${
                    callSettings.video ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                  }`}
                >
                  {callSettings.video ? <Video className="w-4 h-4" /> : <VideoOff className="w-4 h-4" />}
                  <span>Camera {callSettings.video ? 'On' : 'Off'}</span>
                </button>

                <button
                  onClick={() => toggleSetting('audio')}
                  className={`flex items-center space-x-2 px-4 py-2 rounded-lg ${
                    callSettings.audio ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                  }`}
                >
                  {callSettings.audio ? <Mic className="w-4 h-4" /> : <MicOff className="w-4 h-4" />}
                  <span>Microphone {callSettings.audio ? 'On' : 'Off'}</span>
                </button>
              </div>
            </div>
          </div>

          <div className="flex justify-between p-6 bg-gray-50">
            <button
              onClick={() => setShowJoinModal(false)}
              className="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
            >
              Cancel
            </button>
            <button
              onClick={startVideoCall}
              className="px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors flex items-center"
            >
              <Video className="w-4 h-4 mr-2" />
              Join Appointment
            </button>
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

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Telehealth</h1>
        <p className="text-gray-600">Secure virtual healthcare appointments and support</p>
      </div>

      {/* Quick Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-white p-4 rounded-lg shadow border border-gray-200">
          <div className="flex items-center space-x-3">
            <Video className="w-8 h-8 text-blue-600" />
            <div>
              <p className="text-sm text-gray-600">Upcoming Visits</p>
              <p className="text-2xl font-bold text-gray-900">{telehealthData.upcomingAppointments.length}</p>
            </div>
          </div>
        </div>
        
        <div className="bg-white p-4 rounded-lg shadow border border-gray-200">
          <div className="flex items-center space-x-3">
            <CheckCircle className="w-8 h-8 text-green-600" />
            <div>
              <p className="text-sm text-gray-600">Completed Sessions</p>
              <p className="text-2xl font-bold text-gray-900">{telehealthData.completedSessions.length}</p>
            </div>
          </div>
        </div>
        
        <div className="bg-white p-4 rounded-lg shadow border border-gray-200">
          <div className="flex items-center space-x-3">
            {getConnectionIcon(connectionStatus)}
            <div>
              <p className="text-sm text-gray-600">Connection</p>
              <p className="text-2xl font-bold text-gray-900 capitalize">{connectionStatus}</p>
            </div>
          </div>
        </div>
        
        <div className="bg-white p-4 rounded-lg shadow border border-gray-200">
          <div className="flex items-center space-x-3">
            <Activity className="w-8 h-8 text-purple-600" />
            <div>
              <p className="text-sm text-gray-600">System Status</p>
              <p className="text-2xl font-bold text-gray-900 capitalize">{telehealthData.systemStatus.serverStatus}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="bg-white rounded-lg shadow">
        <div className="border-b border-gray-200">
          <nav className="flex space-x-8 px-6">
            {[
              { id: 'appointments', label: 'Appointments', count: telehealthData.upcomingAppointments.length },
              { id: 'completed', label: 'Completed', count: telehealthData.completedSessions.length },
              { id: 'status', label: 'System Status' },
              { id: 'support', label: 'Tech Support' }
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
                {tab.label} {tab.count !== undefined && `(${tab.count})`}
              </button>
            ))}
          </nav>
        </div>

        <div className="p-6">
          {activeTab === 'appointments' && <UpcomingAppointmentsTab />}
          {activeTab === 'completed' && <CompletedSessionsTab />}
          {activeTab === 'status' && <SystemStatusTab />}
          {activeTab === 'support' && <TechSupportTab />}
        </div>
      </div>

      {/* Modals and Overlays */}
      <VideoCallInterface />
      <JoinAppointmentModal />
    </div>
  );
};

export default Telehealth;
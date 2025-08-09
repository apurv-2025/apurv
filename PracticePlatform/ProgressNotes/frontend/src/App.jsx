import React, { useState, useEffect } from 'react';
import { AuthProvider } from './contexts/AuthContext';
import { useAuth } from './hooks/useAuth';
import { NotificationProvider } from './components/common/Notification/NotificationProvider';
import Header from './components/common/Header';
import LoginForm from './components/auth/LoginForm';
import Loading from './components/common/Loading';
import Dashboard from './pages/Dashboard';
import EnhancedNotesList from './components/notes/EnhancedNotesList';
import NoteEditor from './components/notes/NoteEditor';
import PatientsPage from './pages/PatientsPage';
import APIService from './services/api';
import { ArrowLeft } from 'lucide-react';

const AppContent = () => {
  const { user, loading, logout } = useAuth();
  const [currentView, setCurrentView] = useState('dashboard');
  const [selectedNote, setSelectedNote] = useState(null);
  const [patients, setPatients] = useState([]);

  useEffect(() => {
    if (user) {
      fetchPatients();
    }
  }, [user]);

  const fetchPatients = async () => {
    try {
      const data = await APIService.getPatients();
      setPatients(data);
    } catch (error) {
      console.error('Error fetching patients:', error);
    }
  };

  const handleCreateNote = async (noteData) => {
    await APIService.createNote(noteData);
    setCurrentView('notes');
  };

  const handleUpdateNote = async (noteData) => {
    await APIService.updateNote(selectedNote.id, noteData);
    setCurrentView('notes');
    setSelectedNote(null);
  };

  const handleSelectNote = (note) => {
    setSelectedNote(note);
    setCurrentView('note-detail');
  };

  const handleEditNote = (note) => {
    setSelectedNote(note);
    setCurrentView('note-editor');
  };

  const handleCreatePatient = async (patientData) => {
    await APIService.createPatient(patientData);
    await fetchPatients();
  };

  const handleUpdatePatient = async (patientId, patientData) => {
    await APIService.updatePatient(patientId, patientData);
    await fetchPatients();
  };

  const handleLogout = () => {
    logout();
    setCurrentView('dashboard');
    setSelectedNote(null);
  };

  if (loading) {
    return <Loading />;
  }

  if (!user) {
    return <LoginForm />;
  }

  const renderCurrentView = () => {
    switch (currentView) {
      case 'dashboard':
        return <Dashboard />;
      case 'notes':
        return (
          <EnhancedNotesList
            onSelectNote={handleSelectNote}
            onCreateNote={() => {
              setSelectedNote(null);
              setCurrentView('note-editor');
            }}
            onEditNote={handleEditNote}
          />
        );
      case 'note-editor':
        return (
          <div>
            <div className="p-6">
              <button
                onClick={() => {
                  setCurrentView('notes');
                  setSelectedNote(null);
                }}
                className="mb-4 text-blue-600 hover:text-blue-800 flex items-center"
              >
                <ArrowLeft className="h-4 w-4 mr-1" />
                Back to Notes
              </button>
            </div>
            <NoteEditor
              note={selectedNote}
              patients={patients}
              onSave={selectedNote ? handleUpdateNote : handleCreateNote}
              onCancel={() => {
                setCurrentView('notes');
                setSelectedNote(null);
              }}
              mode={selectedNote ? 'edit' : 'create'}
            />
          </div>
        );
      case 'note-detail':
        return (
          <div className="p-6">
            <button
              onClick={() => setCurrentView('notes')}
              className="mb-4 text-blue-600 hover:text-blue-800 flex items-center"
            >
              <ArrowLeft className="h-4 w-4 mr-1" />
              Back to Notes
            </button>
            <div className="bg-white rounded-lg shadow p-6">
              <h1 className="text-xl font-bold mb-4">Note Details</h1>
              <p>Note detail view would be implemented here with FileAttachments and AuditLogViewer components.</p>
            </div>
          </div>
        );
      case 'patients':
        return (
          <PatientsPage
            onCreatePatient={handleCreatePatient}
            onUpdatePatient={handleUpdatePatient}
          />
        );
      default:
        return <Dashboard />;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Header
        currentView={currentView}
        setCurrentView={setCurrentView}
        onLogout={handleLogout}
      />
      <main className="max-w-7xl mx-auto">
        {renderCurrentView()}
      </main>
    </div>
  );
};

const App = () => {
  return (
    <AuthProvider>
      <NotificationProvider>
        <AppContent />
      </NotificationProvider>
    </AuthProvider>
  );
};

export default App;

// src/pages/NotesPage.jsx
import React, { useState, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import NotesList from '../components/NotesList';
import NoteViewer from '../components/NoteViewer';
import NoteEditor from '../components/NoteEditor';
import FileAttachments from '../components/FileAttachments';
import AuditLogViewer from '../components/AuditLogViewer';
import NotificationSystem from '../components/NotificationSystem';
import LoadingSpinner from '../components/ui/LoadingSpinner';
import Modal from '../components/ui/Modal';
import NotesService from '../services/notesService';
import NotificationService from '../services/notificationService';
import { useNotes } from '../hooks/useNotes';
import { useNotifications } from '../hooks/useNotifications';

const NotesPage = () => {
  const navigate = useNavigate();
  const [searchParams, setSearchParams] = useSearchParams();
  const [currentView, setCurrentView] = useState('list'); // 'list', 'view', 'edit', 'create'
  const [selectedNote, setSelectedNote] = useState(null);
  const [showAuditLog, setShowAuditLog] = useState(false);
  const [showAttachments, setShowAttachments] = useState(false);
  const [loading, setLoading] = useState(false);

  const {
    notes,
    totalPages,
    loading: notesLoading,
    filters,
    sortBy,
    sortOrder,
    selectedNotes,
    refreshNotes,
    updateFilters,
    updateSort,
    toggleNoteSelection,
    selectAllNotes,
    clearSelection
  } = useNotes();

  const notifications = useNotifications();

  // Handle URL parameters
  useEffect(() => {
    const noteId = searchParams.get('noteId');
    const view = searchParams.get('view') || 'list';
    
    if (noteId && (view === 'view' || view === 'edit')) {
      handleSelectNote(noteId, view);
    } else {
      setCurrentView('list');
      setSelectedNote(null);
    }
  }, [searchParams]);

  const handleSelectNote = async (noteIdOrNote, view = 'view') => {
    setLoading(true);
    try {
      let note;
      if (typeof noteIdOrNote === 'string') {
        const result = await NotesService.getNoteById(noteIdOrNote);
        if (!result.success) {
          NotificationService.error(result.error);
          return;
        }
        note = result.data;
      } else {
        note = noteIdOrNote;
      }

      setSelectedNote(note);
      setCurrentView(view);
      setSearchParams({ noteId: note.id, view });
    } catch (error) {
      NotificationService.error('Failed to load note');
      console.error('Error selecting note:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateNote = () => {
    setSelectedNote(null);
    setCurrentView('create');
    setSearchParams({ view: 'create' });
  };

  const handleEditNote = (note) => {
    if (note.is_signed && !note.can_unlock) {
      NotificationService.warning('Cannot edit signed note without proper permissions');
      return;
    }
    handleSelectNote(note, 'edit');
  };

  const handleSaveNote = async (noteData, isEdit = false) => {
    setLoading(true);
    try {
      let result;
      if (isEdit) {
        result = await NotesService.updateNote(selectedNote.id, noteData);
        if (result.success) {
          NotificationService.noteSaved(result.data.patient?.first_name + ' ' + result.data.patient?.last_name);
        }
      } else {
        result = await NotesService.createNote(noteData);
        if (result.success) {
          NotificationService.success('Note created successfully');
        }
      }

      if (result.success) {
        await refreshNotes();
        setSelectedNote(result.data);
        setCurrentView('view');
        setSearchParams({ noteId: result.data.id, view: 'view' });
      } else {
        NotificationService.error(result.error);
      }
    } catch (error) {
      NotificationService.error('Failed to save note');
      console.error('Error saving note:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteNote = async (noteId) => {
    if (!window.confirm('Are you sure you want to delete this note?')) {
      return;
    }

    setLoading(true);
    try {
      const result = await NotesService.deleteNote(noteId);
      if (result.success) {
        NotificationService.success('Note deleted successfully');
        await refreshNotes();
        setCurrentView('list');
        setSelectedNote(null);
        setSearchParams({});
      } else {
        NotificationService.error(result.error);
      }
    } catch (error) {
      NotificationService.error('Failed to delete note');
      console.error('Error deleting note:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSignNote = async (noteId) => {
    if (!window.confirm('Are you sure you want to sign this note? This action cannot be undone.')) {
      return;
    }

    setLoading(true);
    try {
      const result = await NotesService.signNote(noteId);
      if (result.success) {
        NotificationService.noteSigned('Note');
        await refreshNotes();
        if (selectedNote?.id === noteId) {
          setSelectedNote(result.data);
        }
      } else {
        NotificationService.error(result.error);
      }
    } catch (error) {
      NotificationService.error('Failed to sign note');
      console.error('Error signing note:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleBulkAction = async (action) => {
    if (selectedNotes.length === 0) {
      NotificationService.warning('No notes selected');
      return;
    }

    const progress = NotificationService.startProgress(`Processing ${selectedNotes.length} notes`);

    try {
      let result;
      switch (action) {
        case 'archive':
          result = await NotesService.bulkArchiveNotes(selectedNotes);
          break;
        case 'export':
          result = await NotesService.bulkExportNotes(selectedNotes);
          break;
        case 'delete':
          if (!window.confirm(`Delete ${selectedNotes.length} notes?`)) {
            progress.complete();
            return;
          }
          // Implement bulk delete
          break;
        default:
          throw new Error('Unknown bulk action');
      }

      if (result.success) {
        progress.complete(`${action} completed successfully`);
        await refreshNotes();
        clearSelection();
      } else {
        progress.error(result.error);
      }
    } catch (error) {
      progress.error(`Failed to ${action} notes`);
      console.error(`Error in bulk ${action}:`, error);
    }
  };

  const handleBackToList = () => {
    setCurrentView('list');
    setSelectedNote(null);
    setSearchParams({});
  };

  const renderContent = () => {
    if (loading || notesLoading) {
      return <LoadingSpinner message="Loading..." />;
    }

    switch (currentView) {
      case 'list':
        return (
          <NotesList
            notes={notes}
            totalPages={totalPages}
            filters={filters}
            sortBy={sortBy}
            sortOrder={sortOrder}
            selectedNotes={selectedNotes}
            onSelectNote={handleSelectNote}
            onEditNote={handleEditNote}
            onCreateNote={handleCreateNote}
            onDeleteNote={handleDeleteNote}
            onSignNote={handleSignNote}
            onFilterChange={updateFilters}
            onSortChange={updateSort}
            onToggleSelection={toggleNoteSelection}
            onSelectAll={selectAllNotes}
            onBulkAction={handleBulkAction}
          />
        );

      case 'view':
        return selectedNote ? (
          <NoteViewer
            note={selectedNote}
            onEdit={() => handleEditNote(selectedNote)}
            onDelete={() => handleDeleteNote(selectedNote.id)}
            onSign={() => handleSignNote(selectedNote.id)}
            onBack={handleBackToList}
            onShowAuditLog={() => setShowAuditLog(true)}
            onShowAttachments={() => setShowAttachments(true)}
          />
        ) : (
          <div className="text-center py-8">Note not found</div>
        );

      case 'edit':
        return selectedNote ? (
          <NoteEditor
            note={selectedNote}
            mode="edit"
            onSave={(data) => handleSaveNote(data, true)}
            onCancel={handleBackToList}
          />
        ) : (
          <div className="text-center py-8">Note not found</div>
        );

      case 'create':
        return (
          <NoteEditor
            mode="create"
            onSave={(data) => handleSaveNote(data, false)}
            onCancel={handleBackToList}
          />
        );

      default:
        return <div className="text-center py-8">Unknown view</div>;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto">
        {renderContent()}
      </div>

      {/* Modals */}
      {showAuditLog && selectedNote && (
        <Modal
          title="Audit Log"
          onClose={() => setShowAuditLog(false)}
          size="large"
        >
          <AuditLogViewer
            resourceId={selectedNote.id}
            resourceType="note"
          />
        </Modal>
      )}

      {showAttachments && selectedNote && (
        <Modal
          title="File Attachments"
          onClose={() => setShowAttachments(false)}
          size="large"
        >
          <FileAttachments
            noteId={selectedNote.id}
            attachments={selectedNote.attachments || []}
            onAttachmentsChange={(attachments) => {
              setSelectedNote(prev => ({ ...prev, attachments }));
            }}
          />
        </Modal>
      )}

      {/* Notification System */}
      <NotificationSystem notifications={notifications} />
    </div>
  );
};

export default NotesPage;

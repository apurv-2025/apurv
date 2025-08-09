import { useState, useEffect, useCallback } from 'react';
import NotesService from '../services/notesService';
import NotificationService from '../services/notificationService';

export const useNotes = (initialFilters = {}) => {
  const [notes, setNotes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [totalPages, setTotalPages] = useState(1);
  const [totalCount, setTotalCount] = useState(0);
  const [selectedNotes, setSelectedNotes] = useState([]);
  
  const [filters, setFilters] = useState({
    search_query: '',
    note_type: '',
    is_draft: '',
    is_signed: '',
    date_from: '',
    date_to: '',
    patient_id: '',
    clinician_id: '',
    page: 1,
    page_size: 20,
    ...initialFilters
  });

  const [sortBy, setSortBy] = useState('session_date');
  const [sortOrder, setSortOrder] = useState('desc');

  const fetchNotes = useCallback(async () => {
    setLoading(true);
    setError(null);
    
    try {
      const searchParams = {
        ...filters,
        sort_by: sortBy,
        sort_order: sortOrder
      };
      
      const result = await NotesService.getNotes(searchParams);


      
      if (result.success) {
        const formattedNotes = result.items.map(note => 
          NotesService.formatNoteForDisplay(note)
        );
        
        setNotes(formattedNotes);
        setTotalPages(result.totalPages);
        setTotalCount(result.totalCount);
      } else {
        setError(result.error);
        NotificationService.error(result.error);
      }
    } catch (err) {
      const errorMessage = 'Failed to fetch notes';
      setError(errorMessage);
      NotificationService.error(errorMessage);
      console.error('useNotes fetchNotes error:', err);
    } finally {
      setLoading(false);
    }
  }, [filters, sortBy, sortOrder]);

  // Fetch notes when dependencies change
  useEffect(() => {
    fetchNotes();
  }, [fetchNotes]);

  // Clear selection when notes change
  useEffect(() => {
    setSelectedNotes([]);
  }, [notes]);

  const updateFilters = useCallback((key, value) => {
    setFilters(prev => ({
      ...prev,
      [key]: value,
      page: key === 'page' ? value : 1 // Reset to page 1 unless updating page directly
    }));
  }, []);

  const updateSort = useCallback((field, order) => {
    setSortBy(field);
    setSortOrder(order);
  }, []);

  const toggleNoteSelection = useCallback((noteId) => {
    setSelectedNotes(prev => 
      prev.includes(noteId)
        ? prev.filter(id => id !== noteId)
        : [...prev, noteId]
    );
  }, []);

  const selectAllNotes = useCallback(() => {
    if (selectedNotes.length === notes.length) {
      setSelectedNotes([]);
    } else {
      setSelectedNotes(notes.map(note => note.id));
    }
  }, [notes, selectedNotes]);

  const clearSelection = useCallback(() => {
    setSelectedNotes([]);
  }, []);

  const resetFilters = useCallback(() => {
    setFilters({
      search_query: '',
      note_type: '',
      is_draft: '',
      is_signed: '',
      date_from: '',
      date_to: '',
      patient_id: '',
      clinician_id: '',
      page: 1,
      page_size: 20
    });
  }, []);

  const refreshNotes = useCallback(async () => {
    await fetchNotes();
  }, [fetchNotes]);

  // Helper methods
  const getFilteredNotesCount = useCallback(() => {
    return notes.length;
  }, [notes]);

  const hasActiveFilters = useCallback(() => {
    return Object.entries(filters).some(([key, value]) => {
      if (key === 'page' || key === 'page_size') return false;
      return value !== '' && value !== null && value !== undefined;
    });
  }, [filters]);

  const getNoteById = useCallback((noteId) => {
    return notes.find(note => note.id === noteId);
  }, [notes]);

  const updateNoteInList = useCallback((updatedNote) => {
    setNotes(prev => prev.map(note => 
      note.id === updatedNote.id 
        ? NotesService.formatNoteForDisplay(updatedNote)
        : note
    ));
  }, []);

  const removeNoteFromList = useCallback((noteId) => {
    setNotes(prev => prev.filter(note => note.id !== noteId));
    setSelectedNotes(prev => prev.filter(id => id !== noteId));
  }, []);

  const addNoteToList = useCallback((newNote) => {
    const formattedNote = NotesService.formatNoteForDisplay(newNote);
    setNotes(prev => [formattedNote, ...prev]);
  }, []);

  // Search utilities
  const searchNotes = useCallback((query) => {
    updateFilters('search_query', query);
  }, [updateFilters]);

  const filterByType = useCallback((noteType) => {
    updateFilters('note_type', noteType);
  }, [updateFilters]);

  const filterByStatus = useCallback((status) => {
    switch (status) {
      case 'draft':
        updateFilters('is_draft', 'true');
        break;
      case 'signed':
        updateFilters('is_signed', 'true');
        break;
      case 'final':
        updateFilters('is_draft', 'false');
        updateFilters('is_signed', '');
        break;
      default:
        updateFilters('is_draft', '');
        updateFilters('is_signed', '');
    }
  }, [updateFilters]);

  const filterByDateRange = useCallback((fromDate, toDate) => {
    updateFilters('date_from', fromDate);
    updateFilters('date_to', toDate);
  }, [updateFilters]);

  const filterByPatient = useCallback((patientId) => {
    updateFilters('patient_id', patientId);
  }, [updateFilters]);

  return {
    // Data
    notes,
    totalPages,
    totalCount,
    loading,
    error,
    selectedNotes,
    filters,
    sortBy,
    sortOrder,

    // Actions
    refreshNotes,
    updateFilters,
    updateSort,
    toggleNoteSelection,
    selectAllNotes,
    clearSelection,
    resetFilters,

    // Utilities
    getFilteredNotesCount,
    hasActiveFilters,
    getNoteById,
    updateNoteInList,
    removeNoteFromList,
    addNoteToList,

    // Search utilities
    searchNotes,
    filterByType,
    filterByStatus,
    filterByDateRange,
    filterByPatient
  };
};

export default useNotes;

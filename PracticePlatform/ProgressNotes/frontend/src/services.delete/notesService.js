// src/services/notesService.js
import NotesAPI from '../api/notes';
import AuditAPI from '../api/audit';

class NotesService {
  static async getNotes(filters = {}) {
    try {
      const data = await NotesAPI.getNotes(filters);
      return {
        success: true,
        data: data.items || [],
        totalPages: data.total_pages || 1,
        totalCount: data.total_count || 0
      };
    } catch (error) {
      console.error('NotesService.getNotes error:', error);
      return {
        success: false,
        error: error.message,
        data: [],
        totalPages: 1,
        totalCount: 0
      };
    }
  }

  static async getNoteById(noteId) {
    try {
      const data = await NotesAPI.getNoteById(noteId);
      
      // Log audit entry for viewing note
      await this.logAuditAction(noteId, 'read');
      
      return {
        success: true,
        data
      };
    } catch (error) {
      console.error('NotesService.getNoteById error:', error);
      return {
        success: false,
        error: error.message,
        data: null
      };
    }
  }

  static async createNote(noteData) {
    try {
      // Validate note data
      const validationResult = this.validateNoteData(noteData);
      if (!validationResult.isValid) {
        return {
          success: false,
          error: validationResult.errors.join(', '),
          data: null
        };
      }

      const data = await NotesAPI.createNote(noteData);
      
      // Log audit entry for creating note
      await this.logAuditAction(data.id, 'create', null, noteData);
      
      return {
        success: true,
        data
      };
    } catch (error) {
      console.error('NotesService.createNote error:', error);
      return {
        success: false,
        error: error.message,
        data: null
      };
    }
  }

  static async updateNote(noteId, noteData) {
    try {
      // Get current note data for audit trail
      const currentNote = await NotesAPI.getNoteById(noteId);
      
      // Validate note data
      const validationResult = this.validateNoteData(noteData);
      if (!validationResult.isValid) {
        return {
          success: false,
          error: validationResult.errors.join(', '),
          data: null
        };
      }

      // Check if note is locked/signed
      if (currentNote.is_signed && !noteData.unlock_reason) {
        return {
          success: false,
          error: 'Cannot modify signed note without unlock reason',
          data: null
        };
      }

      const data = await NotesAPI.updateNote(noteId, noteData);
      
      // Log audit entry for updating note
      await this.logAuditAction(noteId, 'update', currentNote, noteData);
      
      return {
        success: true,
        data
      };
    } catch (error) {
      console.error('NotesService.updateNote error:', error);
      return {
        success: false,
        error: error.message,
        data: null
      };
    }
  }

  static async deleteNote(noteId) {
    try {
      const success = await NotesAPI.deleteNote(noteId);
      
      if (success) {
        // Log audit entry for deleting note
        await this.logAuditAction(noteId, 'delete');
      }
      
      return {
        success,
        error: success ? null : 'Failed to delete note'
      };
    } catch (error) {
      console.error('NotesService.deleteNote error:', error);
      return {
        success: false,
        error: error.message
      };
    }
  }

  static async signNote(noteId) {
    try {
      const data = await NotesAPI.signNote(noteId);
      
      // Log audit entry for signing note
      await this.logAuditAction(noteId, 'sign', { is_signed: false }, { is_signed: true });
      
      return {
        success: true,
        data
      };
    } catch (error) {
      console.error('NotesService.signNote error:', error);
      return {
        success: false,
        error: error.message,
        data: null
      };
    }
  }

  static async bulkArchiveNotes(noteIds) {
    try {
      const data = await NotesAPI.bulkArchiveNotes(noteIds);
      
      // Log audit entries for bulk archive
      await Promise.all(
        noteIds.map(noteId => this.logAuditAction(noteId, 'archive'))
      );
      
      return {
        success: true,
        data
      };
    } catch (error) {
      console.error('NotesService.bulkArchiveNotes error:', error);
      return {
        success: false,
        error: error.message,
        data: null
      };
    }
  }

  static async bulkExportNotes(noteIds) {
    try {
      const blob = await NotesAPI.bulkExportNotes(noteIds);
      
      // Create download link
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `notes_export_${new Date().toISOString().split('T')[0]}.zip`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
      
      // Log audit entries for bulk export
      await Promise.all(
        noteIds.map(noteId => this.logAuditAction(noteId, 'export'))
      );
      
      return {
        success: true
      };
    } catch (error) {
      console.error('NotesService.bulkExportNotes error:', error);
      return {
        success: false,
        error: error.message
      };
    }
  }

  static validateNoteData(noteData) {
    const errors = [];

    if (!noteData.patient_id) {
      errors.push('Patient ID is required');
    }

    if (!noteData.note_type) {
      errors.push('Note type is required');
    }

    if (!noteData.session_date) {
      errors.push('Session date is required');
    }

    if (!noteData.content || Object.keys(noteData.content).length === 0) {
      errors.push('Note content is required');
    }

    // Validate note type specific requirements
    if (noteData.note_type === 'SOAP') {
      const requiredFields = ['subjective', 'objective', 'assessment', 'plan'];
      const missingFields = requiredFields.filter(field => !noteData.content[field]);
      if (missingFields.length > 0) {
        errors.push(`SOAP note missing required fields: ${missingFields.join(', ')}`);
      }
    }

    return {
      isValid: errors.length === 0,
      errors
    };
  }

  static async logAuditAction(noteId, action, oldValues = null, newValues = null) {
    try {
      await AuditAPI.createAuditLog({
        resource_id: noteId,
        resource_type: 'note',
        action,
        old_values: oldValues,
        new_values: newValues,
        ip_address: await this.getClientIP()
      });
    } catch (error) {
      console.error('Failed to log audit action:', error);
      // Don't throw error to avoid breaking main functionality
    }
  }

  static async getClientIP() {
    try {
      const response = await fetch('https://api.ipify.org?format=json');
      const data = await response.json();
      return data.ip;
    } catch (error) {
      return 'unknown';
    }
  }

  static formatNoteForDisplay(note) {
    return {
      ...note,
      patientName: `${note.patient?.first_name || ''} ${note.patient?.last_name || ''}`.trim(),
      clinicianName: `${note.clinician?.first_name || ''} ${note.clinician?.last_name || ''}`.trim(),
      formattedSessionDate: new Date(note.session_date).toLocaleDateString(),
      formattedCreatedAt: new Date(note.created_at).toLocaleDateString(),
      statusBadges: this.getNoteStatusBadges(note)
    };
  }

  static getNoteStatusBadges(note) {
    const badges = [];
    
    if (note.is_draft) {
      badges.push({ text: 'Draft', color: 'yellow' });
    }
    
    if (note.is_signed) {
      badges.push({ text: 'Signed', color: 'green' });
    }
    
    if (note.is_locked) {
      badges.push({ text: 'Locked', color: 'red' });
    }

    return badges;
  }
}

export default NotesService;

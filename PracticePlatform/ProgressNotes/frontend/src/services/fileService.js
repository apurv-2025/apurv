// src/services/fileService.js
import APIService from './api';

class FileService extends APIService {
  static async uploadFiles(noteId, files) {
    const formData = new FormData();
    Array.from(files).forEach(file => {
      formData.append('files', file);
    });

    return this.request(`/notes/${noteId}/attachments`, {
      method: 'POST',
      body: formData,
      headers: {} // Remove Content-Type header for FormData
    });
  }

  static async getAttachments(noteId) {
    return this.request(`/notes/${noteId}/attachments`);
  }

  static async deleteAttachment(noteId, attachmentId) {
    return this.request(`/notes/${noteId}/attachments/${attachmentId}`, {
      method: 'DELETE'
    });
  }

  static async downloadAttachment(noteId, attachmentId) {
    const response = await fetch(`${this.API_BASE_URL}/notes/${noteId}/attachments/${attachmentId}/download`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('access_token')}`
      }
    });
    
    if (!response.ok) {
      throw new Error('Download failed');
    }
    
    return response.blob();
  }
}

export default FileService;

// src/services/fileService.js
import FilesAPI from '../api/files';
import AuditAPI from '../api/audit';

class FileService {
  static async uploadFiles(noteId, files) {
    try {
      // Validate all files before uploading
      const validationResults = Array.from(files).map(file => {
        try {
          FilesAPI.validateFile(file);
          return { file, isValid: true, error: null };
        } catch (error) {
          return { file, isValid: false, error: error.message };
        }
      });

      const invalidFiles = validationResults.filter(result => !result.isValid);
      if (invalidFiles.length > 0) {
        return {
          success: false,
          error: `Invalid files: ${invalidFiles.map(f => `${f.file.name}: ${f.error}`).join(', ')}`,
          data: null
        };
      }

      const data = await FilesAPI.uploadFiles(noteId, files);
      
      // Log audit entry for file upload
      await this.logAuditAction(noteId, 'file_upload', null, {
        files: Array.from(files).map(f => ({ name: f.name, size: f.size, type: f.type }))
      });
      
      return {
        success: true,
        data
      };
    } catch (error) {
      console.error('FileService.uploadFiles error:', error);
      return {
        success: false,
        error: error.message,
        data: null
      };
    }
  }

  static async getAttachments(noteId) {
    try {
      const data = await FilesAPI.getAttachments(noteId);
      return {
        success: true,
        data: data.map(attachment => this.formatAttachmentForDisplay(attachment))
      };
    } catch (error) {
      console.error('FileService.getAttachments error:', error);
      return {
        success: false,
        error: error.message,
        data: []
      };
    }
  }

  static async downloadFile(attachmentId, fileName) {
    try {
      const blob = await FilesAPI.downloadFile(attachmentId);
      
      // Create download link
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = fileName;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
      
      // Log audit entry for file download
      await this.logAuditAction(attachmentId, 'file_download', null, { file_name: fileName });
      
      return {
        success: true
      };
    } catch (error) {
      console.error('FileService.downloadFile error:', error);
      return {
        success: false,
        error: error.message
      };
    }
  }

  static async deleteAttachment(attachmentId, fileName) {
    try {
      const success = await FilesAPI.deleteAttachment(attachmentId);
      
      if (success) {
        // Log audit entry for file deletion
        await this.logAuditAction(attachmentId, 'file_delete', { file_name: fileName }, null);
      }
      
      return {
        success,
        error: success ? null : 'Failed to delete attachment'
      };
    } catch (error) {
      console.error('FileService.deleteAttachment error:', error);
      return {
        success: false,
        error: error.message
      };
    }
  }

  static formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  }

  static getFileIcon(mimeType) {
    if (mimeType.includes('image')) return '🖼️';
    if (mimeType.includes('pdf')) return '📄';
    if (mimeType.includes('word')) return '📝';
    if (mimeType.includes('excel') || mimeType.includes('spreadsheet')) return '📊';
    if (mimeType.includes('powerpoint') || mimeType.includes('presentation')) return '📊';
    if (mimeType.includes('text')) return '📄';
    if (mimeType.includes('audio')) return '🎵';
    if (mimeType.includes('video')) return '🎥';
    return '📎';
  }

  static getFileCategory(mimeType) {
    if (mimeType.includes('image')) return 'image';
    if (mimeType.includes('pdf')) return 'document';
    if (mimeType.includes('word') || mimeType.includes('text')) return 'document';
    if (mimeType.includes('excel') || mimeType.includes('spreadsheet')) return 'spreadsheet';
    if (mimeType.includes('powerpoint') || mimeType.includes('presentation')) return 'presentation';
    if (mimeType.includes('audio')) return 'audio';
    if (mimeType.includes('video')) return 'video';
    return 'other';
  }

  static formatAttachmentForDisplay(attachment) {
    return {
      ...attachment,
      formattedSize: this.formatFileSize(attachment.file_size),
      formattedDate: new Date(attachment.uploaded_at).toLocaleDateString(),
      icon: this.getFileIcon(attachment.mime_type),
      category: this.getFileCategory(attachment.mime_type),
      isImage: attachment.mime_type.includes('image'),
      isPdf: attachment.mime_type.includes('pdf'),
      canPreview: attachment.mime_type.includes('image') || attachment.mime_type.includes('pdf')
    };
  }

  static async logAuditAction(resourceId, action, oldValues = null, newValues = null) {
    try {
      await AuditAPI.createAuditLog({
        resource_id: resourceId,
        resource_type: 'file',
        action,
        old_values: oldValues,
        new_values: newValues
      });
    } catch (error) {
      console.error('Failed to log file audit action:', error);
    }
  }

  static validateFileType(file) {
    const allowedTypes = [
      'application/pdf',
      'application/msword',
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
      'image/jpeg',
      'image/jpg',
      'image/png',
      'image/gif',
      'text/plain'
    ];

    return allowedTypes.includes(file.type);
  }

  static validateFileSize(file, maxSizeMB = 10) {
    const maxSize = maxSizeMB * 1024 * 1024;
    return file.size <= maxSize;
  }

  static createFilePreview(file) {
    return new Promise((resolve) => {
      if (file.type.startsWith('image/')) {
        const reader = new FileReader();
        reader.onload = (e) => resolve(e.target.result);
        reader.readAsDataURL(file);
      } else {
        resolve(null);
      }
    });
  }
}

export default FileService;

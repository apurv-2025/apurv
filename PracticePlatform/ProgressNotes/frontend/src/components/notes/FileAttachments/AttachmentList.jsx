import React from 'react';
import { Download, Trash2 } from 'lucide-react';
import { formatFileSize, getFileIcon } from '../../../utils/fileUtils';
import FileService from '../../../services/fileService';
import { useNotificationContext } from '../../common/Notification/NotificationProvider';

const AttachmentList = ({ noteId, attachments, onAttachmentRemoved }) => {
  const { showSuccess, showError } = useNotificationContext();

  const handleDownload = async (attachment) => {
    try {
      const blob = await FileService.downloadAttachment(noteId, attachment.id);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = attachment.file_name;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (error) {
      showError(`Download failed: ${error.message}`);
    }
  };

  const handleRemove = async (attachment) => {
    if (!window.confirm(`Remove ${attachment.file_name}?`)) return;

    try {
      await FileService.deleteAttachment(noteId, attachment.id);
      showSuccess('Attachment removed successfully');
      onAttachmentRemoved?.(attachment.id);
    } catch (error) {
      showError(`Remove failed: ${error.message}`);
    }
  };

  if (!attachments || attachments.length === 0) {
    return (
      <div className="text-center py-4 text-gray-500">
        No attachments yet.
      </div>
    );
  }

  return (
    <div className="space-y-2">
      {attachments.map((attachment) => (
        <div
          key={attachment.id}
          className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
        >
          <div className="flex items-center space-x-3">
            <span className="text-lg">{getFileIcon(attachment.mime_type)}</span>
            <div>
              <p className="text-sm font-medium text-gray-900">
                {attachment.file_name}
              </p>
              <p className="text-xs text-gray-500">
                {formatFileSize(attachment.file_size)} • {new Date(attachment.uploaded_at).toLocaleDateString()}
              </p>
            </div>
          </div>
          <div className="flex items-center space-x-2">
            <button
              onClick={() => handleDownload(attachment)}
              className="p-2 text-gray-400 hover:text-blue-600"
              title="Download"
            >
              <Download className="h-4 w-4" />
            </button>
            <button
              onClick={() => handleRemove(attachment)}
              className="p-2 text-gray-400 hover:text-red-600"
              title="Remove"
            >
              <Trash2 className="h-4 w-4" />
            </button>
          </div>
        </div>
      ))}
    </div>
  );
};

export default AttachmentList;

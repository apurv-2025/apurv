// src/components/notes/FileAttachments/index.jsx
import React, { useState, useEffect } from 'react';
import FileUploadZone from './FileUploadZone';
import AttachmentList from './AttachmentList';
import FileService from '../../../services/fileService';

const FileAttachments = ({ noteId }) => {
  const [attachments, setAttachments] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAttachments();
  }, [noteId]);

  const fetchAttachments = async () => {
    if (!noteId) return;
    
    setLoading(true);
    try {
      const data = await FileService.getAttachments(noteId);
      setAttachments(data);
    } catch (error) {
      console.error('Error fetching attachments:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleFilesUploaded = (newAttachments) => {
    setAttachments(prev => [...prev, ...newAttachments]);
  };

  const handleAttachmentRemoved = (attachmentId) => {
    setAttachments(prev => prev.filter(att => att.id !== attachmentId));
  };

  return (
    <div className="space-y-6">
      <FileUploadZone 
        noteId={noteId} 
        onFilesUploaded={handleFilesUploaded} 
      />
      
      {loading ? (
        <div className="text-center py-4">Loading attachments...</div>
      ) : (
        <AttachmentList
          noteId={noteId}
          attachments={attachments}
          onAttachmentRemoved={handleAttachmentRemoved}
        />
      )}
    </div>
  );
};

export default FileAttachments;

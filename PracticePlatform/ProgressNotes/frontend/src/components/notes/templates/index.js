import SOAPNoteTemplate from './SOAPNoteTemplate';
import DAPNoteTemplate from './DAPNoteTemplate';
import { NOTE_TYPES } from '../../../utils/constants';

export const NoteTemplates = {
  [NOTE_TYPES.SOAP]: SOAPNoteTemplate,
  [NOTE_TYPES.DAP]: DAPNoteTemplate,
  // Add other templates as needed
  [NOTE_TYPES.BIRP]: SOAPNoteTemplate, // Fallback to SOAP for now
  [NOTE_TYPES.PAIP]: SOAPNoteTemplate, // Fallback to SOAP for now
};

export { SOAPNoteTemplate, DAPNoteTemplate };


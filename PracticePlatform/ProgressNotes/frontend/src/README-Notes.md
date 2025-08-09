# Refactored Notes Application Structure

## Directory Structure

```
src/
├── api/                    # API layer - HTTP requests
│   ├── notes.js           # Notes CRUD operations
│   ├── files.js           # File upload/download
│   └── audit.js           # Audit log operations
│
├── services/              # Business logic layer
│   ├── notesService.js    # Notes business logic & validation
│   ├── fileService.js     # File handling & validation
│   └── notificationService.js  # Notification management
│
├── components/            # Reusable UI components
│   ├── ui/                # Basic UI components
│   │   ├── NoteCard.jsx   # Note card for grid view
│   │   ├── NoteListItem.jsx # Note item for list view
│   │   ├── SearchFilters.jsx # Search and filter controls
│   │   ├── BulkActions.jsx # Bulk operation controls
│   │   ├── Pagination.jsx # Pagination component
│   │   ├── Modal.jsx      # Modal dialog
│   │   └── LoadingSpinner.jsx # Loading indicator
│   │
│   ├── NotesList.jsx      # Main notes list component
│   ├── NoteViewer.jsx     # Note viewing component
│   ├── NoteEditor.jsx     # Note editing component
│   ├── FileAttachments.jsx # File attachment management
│   ├── AuditLogViewer.jsx # Audit log display
│   └── NotificationSystem.jsx # Toast notifications
│
├── pages/                 # Page components
│   └── NotesPage.jsx      # Main notes page
│
├── hooks/                 # Custom React hooks
│   ├── useNotes.js        # Notes state management
│   ├── useFileUpload.js   # File upload logic
│   └── useNotifications.js # Notification management
│
└── utils/                 # Utility functions
    ├── constants.js       # App constants
    ├── validators.js      # Validation functions
    └── formatters.js      # Data formatting utilities
```

## Key Architecture Decisions

### 1. Separation of Concerns

- **API Layer**: Pure HTTP requests without business logic
- **Services Layer**: Business logic, validation, and data transformation
- **Components**: UI rendering and user interactions
- **Hooks**: State management and side effects

### 2. API Layer (`/api`)

Each API module handles a specific domain:

```javascript
// Example usage
import NotesAPI from '../api/notes';

const notes = await NotesAPI.getNotes({ page: 1, limit: 20 });
```

Features:
- Centralized error handling
- Consistent request/response format
- Authentication token management
- Type validation

### 3. Services Layer (`/services`)

Business logic and data processing:

```javascript
// Example usage
import NotesService from '../services/notesService';

const result = await NotesService.createNote(noteData);
if (result.success) {
  // Handle success
} else {
  // Handle error
}
```

Features:
- Data validation
- Business rules enforcement
- Audit logging
- Error handling and user feedback
- Data formatting for display

### 4. Component Architecture

#### Smart Components (Pages)
- `NotesPage.jsx`: Main orchestrator component
- Handles routing and high-level state
- Coordinates between multiple components

#### Presentational Components
- Pure UI components with props
- No direct API calls or business logic
- Highly reusable and testable

#### UI Components
- Basic building blocks (buttons, modals, etc.)
- Consistent styling and behavior
- Accessibility features built-in

### 5. State Management with Hooks

Custom hooks encapsulate complex state logic:

```javascript
const {
  notes,
  loading,
  filters,
  updateFilters,
  refreshNotes
} = useNotes();
```

Benefits:
- Reusable state logic
- Separation of concerns
- Easy testing
- Clean component code

### 6. Notification System

Centralized notification management:

```javascript
// From components
NotificationService.success('Note saved successfully');
NotificationService.error('Failed to save note');

// With actions
NotificationService.confirmAction(
  'Delete this note?',
  () => handleDelete(),
  () => console.log('Cancelled')
);
```

## Data Flow

1. **User Action** → Component event handler
2. **Component** → Service method call
3. **Service** → API request + business logic
4. **API** → HTTP request to backend
5. **Response** → Service processes response
6. **Service** → Updates UI via hooks/state
7. **Notification** → User feedback (success/error)

## Benefits of This Structure

### Maintainability
- Clear separation of concerns
- Easy to locate and modify code
- Consistent patterns across the app

### Testability
- Services can be unit tested independently
- Components can be tested with mock services
- API layer can be mocked for integration tests

### Reusability
- Services can be reused across different components
- UI components are framework-agnostic
- Hooks can be shared between pages

### Scalability
- Easy to add new features following established patterns
- Services can be extended without affecting UI
- New API endpoints follow consistent structure

### Error Handling
- Centralized error handling in services
- Consistent user feedback via notifications
- Graceful degradation for network issues

## Migration Steps

1. **Extract API calls** from components into API modules
2. **Create service layer** to handle business logic
3. **Refactor components** to use services instead of direct API calls
4. **Implement hooks** for state management
5. **Add notification system** for user feedback
6. **Create reusable UI components** from existing code
7. **Add comprehensive error handling**

## Future Enhancements

- Add Redux/Zustand for global state management
- Implement React Query for caching and synchronization
- Add comprehensive TypeScript types
- Implement lazy loading for components
- Add comprehensive test suite
- Implement service workers for offline functionality

// File: README.md for Frontend
# Health Insurance Verification System - Frontend

A modern React application for health insurance eligibility verification with EDI 270/271 support.

## Features

- **Modern UI/UX**: Clean, responsive design with Tailwind CSS
- **File Upload**: Drag-and-drop interface with OCR processing
- **Real-time Updates**: Live status updates and notifications
- **Modular Architecture**: Well-organized components and services
- **Type Safety**: Comprehensive validation and error handling
- **Accessibility**: WCAG compliant interface design

## Technology Stack

- **React 18**: Latest React with hooks and context
- **React Router 6**: Client-side routing
- **Tailwind CSS**: Utility-first CSS framework
- **Lucide React**: Beautiful icon library
- **React Dropzone**: File upload functionality

## Project Structure

```
src/
├── components/           # Reusable UI components
│   ├── common/          # Generic components (Button, Card, Modal, etc.)
│   ├── layout/          # Layout components (Header, Navigation, etc.)
│   ├── upload/          # File upload related components
│   └── eligibility/     # Eligibility form and result components
├── pages/               # Page components
│   ├── Dashboard.js     # Main dashboard
│   ├── UploadPage.js    # File upload page
│   ├── EligibilityPage.js # Eligibility verification page
│   └── HistoryPage.js   # Request history page
├── services/            # API and utility services
│   ├── apiService.js    # API communication
│   ├── storageService.js # Local storage utilities
│   └── fileService.js   # File handling utilities
├── contexts/            # React contexts for state management
│   ├── AppContext.js    # Main application state
│   └── ToastContext.js  # Toast notification system
├── hooks/               # Custom React hooks
│   ├── useFileUpload.js # File upload functionality
│   └── useEligibilityCheck.js # Eligibility verification
├── utils/               # Utility functions
│   ├── formatters.js    # Data formatting utilities
│   └── validation.js    # Input validation functions
└── constants/           # Application constants
    └── index.js         # API endpoints, service types, etc.
```

## Getting Started

### Prerequisites

- Node.js 18 or higher
- npm or yarn package manager

### Installation

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your API URL
   ```

3. **Start development server:**
   ```bash
   npm start
   ```

4. **Build for production:**
   ```bash
   npm run build
   ```

## Key Components

### Layout Components
- **Header**: Application header with branding
- **Navigation**: Tab-based navigation system
- **StatusBar**: Real-time connection and status display

### Common Components
- **Button**: Customizable button with loading states
- **Card**: Container component for content sections
- **Modal**: Popup modal for detailed views
- **LoadingSpinner**: Loading indicator component
- **Toast**: Notification system for user feedback

### Specialized Components
- **FileUpload**: Drag-and-drop file upload with validation
- **EligibilityForm**: Form for submitting verification requests
- **EligibilityResult**: Display verification results and EDI responses
- **ExtractedDataDisplay**: Show OCR extracted insurance card data

## State Management

The application uses React Context for state management:

- **AppContext**: Manages application-wide state (requests, extracted data, etc.)
- **ToastContext**: Handles notification system

## Custom Hooks

- **useFileUpload**: Encapsulates file upload logic and state
- **useEligibilityCheck**: Manages eligibility verification workflow

## Styling

The application uses Tailwind CSS with custom configuration:

- **Design System**: Consistent colors, spacing, and typography
- **Responsive Design**: Mobile-first approach
- **Custom Components**: Styled component variants
- **Animations**: Smooth transitions and loading states

## API Integration

All API communication is handled through the `apiService`:

- **RESTful API**: JSON-based communication
- **Error Handling**: Comprehensive error management
- **Loading States**: User feedback during operations
- **Toast Notifications**: Success and error messages

## Development Guidelines

### Component Structure
```javascript
// Standard component template
import React from 'react';
import PropTypes from 'prop-types';

const ComponentName = ({ prop1, prop2 }) => {
  // Component logic
  
  return (
    <div className="component-styles">
      {/* Component JSX */}
    </div>
  );
};

ComponentName.propTypes = {
  prop1: PropTypes.string.isRequired,
  prop2: PropTypes.number
};

export default ComponentName;
```

### Styling Guidelines
- Use Tailwind utility classes
- Create custom components for repeated patterns
- Maintain consistent spacing and colors
- Ensure responsive design for all components

### State Management
- Use Context for global state
- Keep component state local when possible
- Use custom hooks for complex logic
- Implement proper error boundaries

## Testing

```bash
# Run tests
npm test

# Run tests with coverage
npm test -- --coverage

# Run tests in watch mode
npm test -- --watch
```

## Deployment

### Development
```bash
npm start
```

### Production Build
```bash
npm run build
npm install -g serve
serve -s build
```

### Docker Deployment
```bash
docker build -t health-insurance-frontend .
docker run -p 3000:3000 health-insurance-frontend
```

## Performance Optimization

- **Code Splitting**: Automatic route-based splitting
- **Lazy Loading**: Components loaded on demand
- **Memoization**: React.memo for expensive components
- **Bundle Analysis**: Use webpack-bundle-analyzer

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Contributing

1. Follow the established file structure
2. Use TypeScript for new features (optional)
3. Write tests for new components
4. Follow the existing code style
5. Update documentation as needed

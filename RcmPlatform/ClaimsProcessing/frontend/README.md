# EDI Claims Processing Application

A React-based application for processing Electronic Data Interchange (EDI) claims with support for 837D (Dental), 837P (Professional), and 837I (Institutional) claim types.

## Project Structure

```
src/
├── components/
│   ├── ui/
│   │   ├── StatusBadge.jsx          # Reusable status badge component
│   │   ├── ClaimTypeBadge.jsx       # Claim type badge component
│   │   └── LoadingSpinner.jsx       # Loading spinner component
│   └── layout/
│       ├── Header.jsx               # Application header
│       └── Navigation.jsx           # Main navigation tabs
├── pages/
│   ├── Dashboard.jsx                # Dashboard with statistics and charts
│   ├── ClaimsList.jsx               # Claims listing and filtering
│   └── Upload.jsx                   # File upload functionality
├── services/
│   └── claimsService.js             # Business logic and API abstraction
├── api/
│   └── mockApi.js                   # Mock API implementation
├── utils/
│   ├── constants.js                 # Application constants and configurations
│   └── helpers.js                   # Utility functions
├── styles/
│   └── globals.css                  # Global CSS styles and custom utilities
├── App.jsx                          # Main application component
└── index.js                         # Application entry point
```

## Features

### Dashboard
- Real-time statistics for claims processing
- Financial summary with collection rates
- Claims distribution by status and type
- Visual charts and metrics

### Claims Management
- Comprehensive claims listing
- Advanced search and filtering
- Status tracking and validation error display
- Action buttons for viewing and downloading claims

### File Upload
- Drag-and-drop EDI file upload
- Support for .edi, .txt, and .x12 formats
- Payer selection and validation
- Real-time upload progress and feedback

## Architecture Highlights

### Component Organization
- **UI Components**: Reusable, presentational components in `components/ui/`
- **Layout Components**: Application structure components in `components/layout/`
- **Page Components**: Route-level components in `pages/`

### Service Layer
- **claimsService.js**: Centralizes business logic and API interactions
- Provides error handling and data transformation
- Abstracts API implementation details from components

### API Layer
- **mockApi.js**: Simulates backend API with realistic data and delays
- Easily replaceable with real API calls
- Includes error simulation for testing

### Utilities
- **constants.js**: Centralized configuration and mappings
- **helpers.js**: Pure utility functions for formatting and validation
- Promotes code reusability and maintainability

### Styling Strategy
- **Tailwind CSS**: Utility-first CSS framework for rapid development
- **globals.css**: Custom styles for animations, hover effects, and accessibility
- Responsive design with mobile-first approach

## Key Components

### StatusBadge
Displays claim status with appropriate colors and icons:
- Validated (green)
- Sent (blue)
- Paid (emerald)
- Rejected (red)
- Queued (yellow)

### ClaimTypeBadge
Shows claim types with descriptive labels:
- 837D (Dental)
- 837P (Professional)
- 837I (Institutional)

### LoadingSpinner
Configurable loading component with:
- Multiple size options
- Optional text display
- Full-page and inline variants

## Data Flow

1. **Components** call methods on **claimsService**
2. **claimsService** validates inputs and calls **mockApi**
3. **mockApi** simulates server responses with realistic delays
4. **claimsService** handles errors and transforms data
5. **Components** receive clean, formatted data for display

## Error Handling

- Service-level error catching and transformation
- User-friendly error messages
- Retry mechanisms for failed operations
- Input validation before API calls

## Performance Considerations

- Efficient state management with React hooks
- Memoization opportunities for expensive calculations
- Lazy loading potential for large datasets
- Optimized re-renders through proper component structure

## Accessibility Features

- Semantic HTML structure
- Proper ARIA labels and roles
- Keyboard navigation support
- High contrast color schemes
- Screen reader compatibility

## Getting Started

1. Install dependencies:
   ```bash
   npm install react react-dom lucide-react
   ```

2. Install Tailwind CSS:
   ```bash
   npm install -D tailwindcss postcss autoprefixer
   npx tailwindcss init -p
   ```

3. Configure Tailwind (tailwind.config.js):
   ```javascript
   module.exports = {
     content: ["./src/**/*.{js,jsx,ts,tsx}"],
     theme: {
       extend: {},
     },
     plugins: [],
   }
   ```

4. Start the development server:
   ```bash
   npm start
   ```

## Future Enhancements

- Real API integration
- User authentication and authorization
- Advanced filtering and sorting options
- Bulk operations for claims
- Export functionality (PDF, Excel)
- Real-time notifications
- Audit trail and logging
- Integration with external payer systems

## Testing Strategy

- Unit tests for utility functions
- Component testing with React Testing Library
- Integration tests for service layer
- End-to-end testing for user workflows
- Mock data validation for API contracts

## Browser Support

- Modern browsers (Chrome, Firefox, Safari, Edge)
- Mobile responsive design
- Progressive enhancement approach
- Graceful degradation for older browsers

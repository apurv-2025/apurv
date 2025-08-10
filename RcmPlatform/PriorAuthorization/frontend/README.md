A modern React application for healthcare prior authorization (EDI 278) and patient information management (EDI 275).

## 🏥 Features

- **Prior Authorization (EDI 278)**: Submit and track prior authorization requests
- **Patient Information (EDI 275)**: Manage patient demographics and medical information
- **Real-time Dashboard**: Track statistics and recent activity
- **Request History**: View and filter authorization requests and patient records
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Modern UI/UX**: Clean, healthcare-appropriate interface

## 🏗️ Architecture

### **Modular Structure**
```
src/
├── components/           # Reusable UI components
│   ├── common/          # Generic components (Card, Button, FormField)
│   ├── forms/           # Specialized forms
│   ├── layout/          # Layout components
│   └── notifications/   # Notification system
├── contexts/            # React contexts for state management
├── hooks/               # Custom React hooks
├── pages/               # Route-based page components
├── services/            # API and utility services
└── App.js              # Main application component
```

### **Key Components**
- **Layout System**: Header, Navigation, StatusBar
- **Form Components**: PriorAuthorizationForm, PatientInformationForm
- **Common Components**: Card, Button, FormField, NotificationSystem
- **Pages**: Dashboard, PriorAuthorizationPage, PatientInformationPage, HistoryPage

### **State Management**
- **AuthorizationContext**: Main application state (requests, patients)
- **NotificationContext**: Toast notification system
- **Custom Hooks**: usePriorAuthorization, usePatientInformation

## 🚀 Getting Started

### **Prerequisites**
- Node.js 18 or higher
- npm or yarn package manager

### **Installation**
1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your API configuration
   ```

3. **Start development server:**
   ```bash
   npm start
   ```

4. **Build for production:**
   ```bash
   npm run build
   ```

## 🔧 Configuration

### **Environment Variables**
- `REACT_APP_API_URL`: Backend API base URL
- `REACT_APP_NAME`: Application name
- `REACT_APP_VERSION`: Application version

### **API Integration**
The application uses a service layer (`authorizationService`) to communicate with the backend API. Update the service methods to match your actual API endpoints.

## 📱 Usage

### **Dashboard**
- View system statistics and recent activity
- Quick access to create new requests or add patients
- Real-time updates of authorization status

### **Prior Authorization (EDI 278)**
- Complete patient and provider information forms
- Submit authorization requests with medical necessity
- Track request status and approval decisions

### **Patient Information (EDI 275)**
- Manage patient demographics and contact information
- Handle insurance information and HIPAA authorization
- Generate EDI 275 transactions

### **History**
- View all authorization requests with filtering
- Browse patient records with search functionality
- Track processing status and outcomes

## 🎨 Design System

### **Color Scheme**
- Primary: Purple (`#7c3aed`)
- Success: Green (`#10b981`)
- Warning: Yellow (`#f59e0b`)
- Error: Red (`#ef4444`)

### **Components**
- **Cards**: Consistent container design
- **Buttons**: Multiple variants and sizes
- **Forms**: Standardized field components with validation
- **Notifications**: Toast system for user feedback

## 🔒 Security

- Input validation with comprehensive error handling
- Secure API communication with proper error handling
- HIPAA compliance considerations built into the design
- No sensitive data stored in browser storage

## 📊 Performance

- React 18 with concurrent features
- Optimized component rendering with proper state management
- Lazy loading for better initial load times
- Responsive design for all device sizes

## 🧪 Testing

```bash
# Run tests
npm test

# Run tests with coverage
npm test -- --coverage
```

## 🚢 Deployment

### **Development**
```bash
npm start
```

### **Production Build**
```bash
npm run build
```

### **Docker Deployment**
```bash
docker build -t edi-278-275-frontend .
docker run -p 3000:3000 edi-278-275-frontend
```

## 🤝 Contributing

1. Follow the established component structure
2. Use TypeScript for new features (optional migration)
3. Write tests for new components
4. Follow the existing code style and patterns
5. Update documentation as needed

## 📋 Component Guidelines

### **Creating New Components**
```javascript
// Standard component template
import React from 'react';

const ComponentName = ({ prop1, prop2 }) => {
  return (
    <div className="component-styles">
      {/* Component content */}
    </div>
  );
};

export default ComponentName;
```

### **Using Contexts**
```javascript
import { useAuthorization } from '../contexts/AuthorizationContext';
import { useNotification } from '../contexts/NotificationContext';

const MyComponent = () => {
  const { requests, patients, dispatch } = useAuthorization();
  const { showSuccess, showError } = useNotification();
  
  // Component logic
};
```

## 🔗 Integration

The frontend is designed to work with the EDI 278/275 backend system. Ensure your backend implements the following endpoints:

- `POST /api/v1/prior-authorization/request`
- `GET /api/v1/prior-authorization/response/{id}`
- `POST /api/v1/patient-information/`
- `GET /api/v1/patient-information/edi-275/{id}`


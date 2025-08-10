# 🎨 React Frontend for Claims Anomaly Detection System

A modern, responsive React application with Tailwind CSS for managing the entire claims anomaly detection pipeline.

## 🚀 Features

### 📊 Dashboard
- **Real-time System Status**: Monitor API health and system performance
- **Key Metrics**: View total claims, anomalies detected, model accuracy, and response times
- **Performance Charts**: Interactive charts showing model performance over time
- **Activity Timeline**: Recent system activities and events

### 🔧 Data Pipeline Management
- **Configuration Forms**: Comprehensive forms for data generation settings
- **Real-time Generation**: Live progress tracking during data generation
- **Statistics Dashboard**: View data statistics and anomaly distribution
- **Data Export**: Download generated data in various formats

### 🤖 Model Training & Management
- **Training Configuration**: Configure ensemble models (Isolation Forest + Random Forest)
- **Real-time Training**: Monitor training progress with live updates
- **Model Comparison**: Compare different model versions
- **Performance Metrics**: View accuracy, precision, recall, and AUC scores

### 🌐 API Service Management
- **Service Configuration**: Configure API settings, rate limits, and security
- **Endpoint Testing**: Test API endpoints directly from the UI
- **Service Monitoring**: Monitor API performance and health
- **Documentation**: Access interactive API documentation

### 📈 Monitoring & Analytics
- **System Health**: Real-time system health monitoring
- **Performance Metrics**: Track model and API performance
- **Request Analytics**: Analyze API request patterns
- **Alert Management**: Configure and manage system alerts

### ⚙️ Settings & Configuration
- **Global Settings**: Configure system-wide settings
- **User Preferences**: Manage user-specific preferences
- **Security Settings**: Configure authentication and authorization
- **Integration Settings**: Manage external service integrations

## 🛠️ Technology Stack

### Frontend
- **React 18**: Modern React with hooks and functional components
- **Tailwind CSS**: Utility-first CSS framework for rapid UI development
- **React Router**: Client-side routing
- **React Hook Form**: Form handling with validation
- **Zustand**: Lightweight state management
- **Axios**: HTTP client for API communication
- **Recharts**: Beautiful charts and data visualization
- **React Hot Toast**: Toast notifications
- **Heroicons**: Beautiful SVG icons

### Development Tools
- **Vite**: Fast build tool and development server
- **ESLint**: Code linting
- **Prettier**: Code formatting
- **PostCSS**: CSS processing
- **Autoprefixer**: CSS vendor prefixing

## 📦 Installation

### Prerequisites
- Node.js 18+ 
- npm or yarn
- Docker (for full-stack deployment)

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ClaimsAnamoly/frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start development server**
   ```bash
   npm start
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - API: http://localhost:8000

### Docker Deployment

1. **Build and start the full stack**
   ```bash
   ./docker-run.sh start
   ```

2. **Access the application**
   - Frontend: http://localhost:3000
   - API: http://localhost:8000

## 🏗️ Project Structure

```
frontend/
├── public/                 # Static assets
│   ├── index.html         # Main HTML file
│   └── manifest.json      # PWA manifest
├── src/
│   ├── components/        # Reusable components
│   │   ├── Sidebar.js     # Navigation sidebar
│   │   └── ...           # Other components
│   ├── pages/            # Page components
│   │   ├── Dashboard.js   # Main dashboard
│   │   ├── DataPipeline.js # Data pipeline management
│   │   ├── ModelTraining.js # Model training interface
│   │   ├── ModelManagement.js # Model management
│   │   ├── APIService.js  # API service management
│   │   ├── Monitoring.js  # Monitoring dashboard
│   │   └── Settings.js    # Settings page
│   ├── services/         # API services
│   │   └── apiService.js # API communication layer
│   ├── store/           # State management
│   │   └── appStore.js  # Zustand store
│   ├── utils/           # Utility functions
│   ├── App.js           # Main app component
│   ├── index.js         # App entry point
│   └── index.css        # Global styles
├── package.json         # Dependencies and scripts
├── tailwind.config.js   # Tailwind configuration
├── Dockerfile           # Docker configuration
└── nginx.conf          # Nginx configuration
```

## 🎨 UI Components

### Design System
- **Color Palette**: Primary blue, success green, warning yellow, danger red
- **Typography**: Clean, readable fonts with proper hierarchy
- **Spacing**: Consistent spacing using Tailwind's spacing scale
- **Shadows**: Subtle shadows for depth and elevation
- **Animations**: Smooth transitions and micro-interactions

### Responsive Design
- **Mobile First**: Designed for mobile devices first
- **Breakpoints**: Responsive breakpoints for tablet and desktop
- **Touch Friendly**: Optimized for touch interactions
- **Accessibility**: WCAG compliant with proper ARIA labels

## 🔌 API Integration

### API Service Layer
The frontend communicates with the backend through a comprehensive API service layer:

```javascript
// Example API calls
import { apiService } from '../services/apiService';

// Health check
const health = await apiService.getHealth();

// Generate data
const result = await apiService.generateData(config);

// Train model
const training = await apiService.trainModel(config);

// Score claims
const score = await apiService.scoreClaim(claimData);
```

### Real-time Updates
- **WebSocket Support**: Real-time updates for training progress
- **Polling**: Automatic polling for system status
- **Event-driven**: Reactive updates based on system events

## 🧪 Testing

### Unit Tests
```bash
npm test
```

### Integration Tests
```bash
npm run test:integration
```

### E2E Tests
```bash
npm run test:e2e
```

## 📊 Performance

### Optimization Techniques
- **Code Splitting**: Lazy loading of components and routes
- **Bundle Optimization**: Tree shaking and dead code elimination
- **Image Optimization**: Compressed images and lazy loading
- **Caching**: Browser caching and service worker support

### Monitoring
- **Performance Metrics**: Core Web Vitals monitoring
- **Error Tracking**: Error boundary and error reporting
- **Analytics**: User behavior and performance analytics

## 🔒 Security

### Security Features
- **Input Validation**: Client-side and server-side validation
- **XSS Protection**: Sanitized inputs and outputs
- **CSRF Protection**: CSRF tokens for API requests
- **Content Security Policy**: CSP headers for XSS prevention

### Authentication
- **JWT Tokens**: Secure token-based authentication
- **Role-based Access**: Role-based access control
- **Session Management**: Secure session handling

## 🚀 Deployment

### Production Build
```bash
npm run build
```

### Docker Deployment
```bash
# Build frontend image
docker build -t claims-anomaly-frontend ./frontend

# Run with docker-compose
docker-compose up -d
```

### Environment Variables
```bash
REACT_APP_API_URL=http://localhost:8000
REACT_APP_ENVIRONMENT=production
REACT_APP_VERSION=1.0.0
```

## 📈 Monitoring & Analytics

### Application Monitoring
- **Error Tracking**: Automatic error reporting
- **Performance Monitoring**: Real-time performance metrics
- **User Analytics**: User behavior and usage patterns
- **System Health**: API and service health monitoring

### Logging
- **Structured Logging**: JSON formatted logs
- **Log Levels**: Debug, info, warn, error levels
- **Log Aggregation**: Centralized log collection

## 🔧 Configuration

### Tailwind Configuration
```javascript
// tailwind.config.js
module.exports = {
  content: ['./src/**/*.{js,jsx,ts,tsx}'],
  theme: {
    extend: {
      colors: {
        primary: { /* custom colors */ },
        success: { /* success colors */ },
        warning: { /* warning colors */ },
        danger: { /* danger colors */ }
      }
    }
  },
  plugins: [require('@tailwindcss/forms')]
}
```

### State Management
```javascript
// store/appStore.js
export const useAppStore = create(
  persist(
    (set, get) => ({
      // State
      dataConfig: { /* data configuration */ },
      modelConfig: { /* model configuration */ },
      trainingState: { /* training state */ },
      
      // Actions
      updateDataConfig: (config) => set(/* update logic */),
      updateModelConfig: (config) => set(/* update logic */),
      setTrainingState: (state) => set(/* update logic */)
    }),
    { name: 'claims-anomaly-store' }
  )
);
```

## 🤝 Contributing

### Development Workflow
1. **Fork the repository**
2. **Create a feature branch**
3. **Make your changes**
4. **Add tests**
5. **Submit a pull request**

### Code Style
- **ESLint**: Follow ESLint rules
- **Prettier**: Use Prettier for formatting
- **Conventional Commits**: Use conventional commit messages
- **TypeScript**: Consider using TypeScript for new features

## 📚 Documentation

### API Documentation
- **Interactive Docs**: Available at `/docs` when API is running
- **OpenAPI Spec**: Generated from FastAPI backend
- **Examples**: Code examples for all endpoints

### Component Documentation
- **Storybook**: Component documentation and examples
- **Props Documentation**: Detailed prop descriptions
- **Usage Examples**: Real-world usage examples

## 🆘 Support

### Getting Help
- **Documentation**: Check this README and API docs
- **Issues**: Report bugs and feature requests
- **Discussions**: Ask questions and share ideas

### Troubleshooting
- **Common Issues**: Check the troubleshooting guide
- **Debug Mode**: Enable debug mode for detailed logs
- **Health Checks**: Use health check endpoints

---

**Happy Coding! 🎉** 
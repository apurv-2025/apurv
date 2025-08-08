// README.md (Frontend specific)
# Task Management System - Frontend

A modern React frontend for the Task Management System built with Tailwind CSS.

## 🚀 Features

- **Modern React** - Built with React 18 and functional components
- **Tailwind CSS** - Utility-first CSS framework for rapid UI development
- **Responsive Design** - Mobile-first approach with responsive layouts
- **Real-time Updates** - WebSocket integration for live notifications
- **File Upload** - Drag & drop file upload with progress indicators
- **Search & Filter** - Advanced filtering and search capabilities
- **Toast Notifications** - User-friendly notification system
- **Accessibility** - WCAG compliant components

## 📋 Prerequisites

- Node.js 16+ and npm 8+
- Backend API running on http://localhost:8000

## 🛠️ Quick Start

```bash
# Install dependencies
npm install

# Start development server
npm start

# Build for production
npm run build

# Run tests
npm test
```

## 📁 Project Structure

```
src/
├── components/           # Reusable UI components
│   ├── Layout/          # Layout components (Header, Sidebar)
│   ├── Tasks/           # Task-related components
│   ├── Clients/         # Client management components
│   └── UI/              # Basic UI components (Button, Input, etc.)
├── hooks/               # Custom React hooks
├── services/            # API services
├── utils/               # Utility functions
├── config/              # Configuration files
├── styles/              # CSS and styling
└── App.js               # Main application component
```

## 🎨 Styling

This project uses Tailwind CSS for styling. Custom styles are defined in:

- `src/index.css` - Global styles and Tailwind imports
- `tailwind.config.js` - Tailwind configuration
- `postcss.config.js` - PostCSS configuration

## 🔧 Configuration

Environment variables can be set in `.env` file:

```bash
REACT_APP_API_URL=http://localhost:8000/api/v1
REACT_APP_WS_URL=ws://localhost:8000/ws
```

## 🧪 Testing

```bash
# Run tests
npm test

# Run tests with coverage
npm test -- --coverage

# Run tests in watch mode
npm test -- --watch
```

## 📦 Building for Production

```bash
# Create production build
npm run build

# Preview production build
npm run preview
```

## 🚀 Deployment

The build folder is ready to be deployed. You can deploy it to:

- **Netlify** - Drag and drop the build folder
- **Vercel** - Connect your GitHub repository
- **AWS S3** - Upload build folder to S3 bucket
- **Nginx** - Serve static files from build folder

## 🔧 Development Tools

- **ESLint** - Code linting
- **Prettier** - Code formatting
- **React DevTools** - React debugging
- **Tailwind CSS IntelliSense** - VSCode extension for Tailwind

## 📱 Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

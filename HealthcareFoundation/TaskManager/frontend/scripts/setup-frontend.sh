// scripts/setup-frontend.sh
#!/bin/bash

# Frontend setup script

echo "🚀 Setting up Task Management Frontend..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first."
    exit 1
fi

# Check Node.js version
NODE_VERSION=$(node -v | cut -d'v' -f2)
REQUIRED_VERSION="16.0.0"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$NODE_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "❌ Node.js version $NODE_VERSION is too old. Please install Node.js 16 or higher."
    exit 1
fi

echo "✅ Node.js version $NODE_VERSION detected"

# Install dependencies
echo "📦 Installing dependencies..."
npm install

# Copy environment file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "🔧 Creating .env file..."
    cp .env.example .env
    echo "✅ Created .env file (please update with your values)"
fi

# Build Tailwind CSS
echo "🎨 Building Tailwind CSS..."
npx tailwindcss -i ./src/index.css -o ./src/styles/tailwind.css --watch &

echo "✅ Frontend setup complete!"
echo ""
echo "🌐 Available commands:"
echo "  npm start     - Start development server"
echo "  npm test      - Run tests"
echo "  npm run build - Build for production"
echo "  npm run lint  - Run ESLint"
echo ""
echo "📚 Open http://localhost:3000 in your browser"

# Scheduling2.0 - Frontend Dockerfile
# Merged from both MBH-Scheduling and Scheduling projects

FROM node:18-alpine

# Set work directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy project files
COPY . .

# Debug: Check what's installed
RUN ls -la node_modules/.bin/ | grep react-scripts || echo "react-scripts not found in .bin"
RUN npm list react-scripts || echo "react-scripts not in package.json dependencies"

# Create non-root user (commented out for debugging)
# RUN addgroup -g 1001 -S nodejs
# RUN adduser -S nextjs -u 1001
# RUN chown -R nextjs:nodejs /app
# USER nextjs

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:3000 || exit 1

# Start the app
CMD ["sh", "-c", "cd /app && node node_modules/.bin/react-scripts start"] 
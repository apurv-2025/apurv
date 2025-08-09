FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 3000

# Set environment variable to allow React dev server to bind to all interfaces
ENV HOST=0.0.0.0

CMD ["npm", "start"]

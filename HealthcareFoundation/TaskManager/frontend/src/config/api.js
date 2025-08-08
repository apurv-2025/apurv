const API_CONFIG = {
  BASE_URL: process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1',
  TIMEOUT: 10000,
  MAX_FILE_SIZE: 50 * 1024 * 1024, // 50MB
  WEBSOCKET_URL: process.env.REACT_APP_WS_URL || 'ws://localhost:8000/ws',
};

export default API_CONFIG;


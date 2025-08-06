const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

class ApiService {
  constructor() {
    this.baseURL = API_BASE_URL;
    this.authToken = null;
    this.defaultHeaders = {
      'Content-Type': 'application/json'
    };
  }

  // Set authentication token
  setAuthToken(token) {
    this.authToken = token;
  }

  // Clear authentication token
  clearAuthToken() {
    this.authToken = null;
  }

  // Get headers with auth token
  getHeaders(customHeaders = {}) {
    const headers = { ...this.defaultHeaders, ...customHeaders };
    
    if (this.authToken) {
      headers.Authorization = `Bearer ${this.authToken}`;
    }
    
    return headers;
  }

  // Build full URL
  buildUrl(endpoint) {
    // Handle absolute URLs
    if (endpoint.startsWith('http')) {
      return endpoint;
    }
    
    // Remove leading slash if present
    const cleanEndpoint = endpoint.startsWith('/') ? endpoint.slice(1) : endpoint;
    
    return `${this.baseURL}/${cleanEndpoint}`;
  }

  // Handle response
  async handleResponse(response) {
    const contentType = response.headers.get('content-type');
    let data;

    // Handle different content types
    if (contentType && contentType.includes('application/json')) {
      data = await response.json();
    } else if (contentType && contentType.includes('text/')) {
      data = await response.text();
    } else {
      data = await response.blob();
    }

    // Handle successful responses
    if (response.ok) {
      return {
        success: true,
        data: data,
        status: response.status,
        statusText: response.statusText
      };
    }

    // Handle error responses
    const errorMessage = data?.message || data?.error || response.statusText || 'Request failed';
    
    // Handle specific error status codes
    if (response.status === 401) {
      // Unauthorized - clear auth token and redirect to login
      this.clearAuthToken();
      if (typeof window !== 'undefined') {
        window.location.href = '/login';
      }
    }

    throw new Error(errorMessage);
  }

  // Generic request method
  async request(endpoint, options = {}) {
    const url = this.buildUrl(endpoint);
    const config = {
      headers: this.getHeaders(options.headers),
      ...options
    };

    // Handle request body
    if (config.body && typeof config.body === 'object' && !(config.body instanceof FormData)) {
      config.body = JSON.stringify(config.body);
    }

    try {
      const response = await fetch(url, config);
      return await this.handleResponse(response);
    } catch (error) {
      // Network or other fetch errors
      if (error.name === 'TypeError' && error.message.includes('fetch')) {
        throw new Error('Network error. Please check your internet connection.');
      }
      
      // Re-throw API errors
      throw error;
    }
  }

  // GET request
  async get(endpoint, params = {}, options = {}) {
    // Build query string from params
    const queryString = Object.keys(params).length > 0 
      ? '?' + new URLSearchParams(params).toString()
      : '';
    
    const urlWithParams = endpoint + queryString;
    
    return this.request(urlWithParams, {
      method: 'GET',
      ...options
    });
  }

  // POST request
  async post(endpoint, data = null, options = {}) {
    return this.request(endpoint, {
      method: 'POST',
      body: data,
      ...options
    });
  }

  // PUT request
  async put(endpoint, data = null, options = {}) {
    return this.request(endpoint, {
      method: 'PUT',
      body: data,
      ...options
    });
  }

  // PATCH request
  async patch(endpoint, data = null, options = {}) {
    return this.request(endpoint, {
      method: 'PATCH',
      body: data,
      ...options
    });
  }

  // DELETE request
  async delete(endpoint, options = {}) {
    return this.request(endpoint, {
      method: 'DELETE',
      ...options
    });
  }

  // File upload with FormData
  async uploadFile(endpoint, file, additionalData = {}, options = {}) {
    const formData = new FormData();
    formData.append('file', file);
    
    // Add additional data to FormData
    Object.keys(additionalData).forEach(key => {
      formData.append(key, additionalData[key]);
    });

    return this.request(endpoint, {
      method: 'POST',
      body: formData,
      headers: {
        // Don't set Content-Type header for FormData
        // Browser will set it automatically with boundary
        ...options.headers
      },
      ...options
    });
  }

  // Download file
  async downloadFile(endpoint, filename = null, options = {}) {
    const response = await this.request(endpoint, {
      ...options,
      headers: {
        ...options.headers
      }
    });

    // Create download link
    const blob = new Blob([response.data]);
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename || 'download';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);

    return response;
  }

  // Health check
  async healthCheck() {
    try {
      return await this.get('/health');
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }

  // Get API configuration
  getConfig() {
    return {
      baseURL: this.baseURL,
      hasAuthToken: !!this.authToken
    };
  }

  // Set base URL (useful for environment switching)
  setBaseURL(url) {
    this.baseURL = url;
  }

  // Retry mechanism for failed requests
  async retryRequest(endpoint, options = {}, maxRetries = 3, delay = 1000) {
    let lastError;
    
    for (let attempt = 1; attempt <= maxRetries; attempt++) {
      try {
        return await this.request(endpoint, options);
      } catch (error) {
        lastError = error;
        
        // Don't retry on 4xx errors (client errors)
        if (error.status >= 400 && error.status < 500) {
          throw error;
        }
        
        // Wait before retrying
        if (attempt < maxRetries) {
          await new Promise(resolve => setTimeout(resolve, delay * attempt));
        }
      }
    }
    
    throw lastError;
  }
}

// Create singleton instance
const apiService = new ApiService();

// Export both named and default exports for flexibility
export { apiService as api };
export default apiService;

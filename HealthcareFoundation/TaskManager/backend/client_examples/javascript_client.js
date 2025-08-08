# client_examples/javascript_client.js
/**
 * JavaScript client example for Task Management API
 */
class TaskManagerClient {
    constructor(baseUrl = 'http://localhost:8000', apiKey = null) {
        this.baseUrl = baseUrl.replace(/\/$/, '');
        this.apiBase = `${this.baseUrl}/api/v1`;
        this.headers = {
            'Content-Type': 'application/json'
        };
        
        if (apiKey) {
            this.headers['Authorization'] = `Bearer ${apiKey}`;
        }
    }
    
    async login(username, password) {
        const formData = new FormData();
        formData.append('username', username);
        formData.append('password', password);
        
        const response = await fetch(`${this.apiBase}/auth/login`, {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            throw new Error(`Login failed: ${response.statusText}`);
        }
        
        const tokenData = await response.json();
        const accessToken = tokenData.access_token;
        
        // Update headers
        this.headers['Authorization'] = `Bearer ${accessToken}`;
        
        return accessToken;
    }
    
    async request(endpoint, options = {}) {
        const url = `${this.apiBase}${endpoint}`;
        const config = {
            headers: this.headers,
            ...options
        };
        
        const response = await fetch(url, config);
        
        if (!response.ok) {
            throw new Error(`API request failed: ${response.statusText}`);
        }
        
        return response.json();
    }
    
    // Task methods
    async createTask(taskData) {
        return this.request('/tasks/', {
            method: 'POST',
            body: JSON.stringify(taskData)
        });
    }
    
    async getTasks(filters = {}) {
        const queryString = new URLSearchParams(filters).toString();
        const endpoint = queryString ? `/tasks/?${queryString}` : '/tasks/';
        return this.request(endpoint);
    }
    
    async getTask(taskId) {
        return this.request(`/tasks/${taskId}`);
    }
    
    async updateTask(taskId, taskData) {
        return this.request(`/tasks/${taskId}`, {
            method: 'PUT',
            body: JSON.stringify(taskData)
        });
    }
    
    async deleteTask(taskId) {
        return this.request(`/tasks/${taskId}`, {
            method: 'DELETE'
        });
    }
    
    // Client methods
    async createClient(clientData) {
        return this.request('/clients/', {
            method: 'POST',
            body: JSON.stringify(clientData)
        });
    }
    
    async getClients(filters = {}) {
        const queryString = new URLSearchParams(filters).toString();
        const endpoint = queryString ? `/clients/?${queryString}` : '/clients/';
        return this.request(endpoint);
    }
    
    // File upload
    async uploadFile(file, taskId = null) {
        const formData = new FormData();
        formData.append('file', file);
        if (taskId) {
            formData.append('task_id', taskId);
        }
        
        const headers = { ...this.headers };
        delete headers['Content-Type']; // Let browser set content type for FormData
        
        const response = await fetch(`${this.apiBase}/attachments/upload`, {
            method: 'POST',
            headers,
            body: formData
        });
        
        if (!response.ok) {
            throw new Error(`File upload failed: ${response.statusText}`);
        }
        
        return response.json();
    }
    
    // Statistics
    async getTaskStats() {
        return this.request('/tasks/stats/overview');
    }
    
    // WebSocket connection
    connectWebSocket(userId) {
        const wsUrl = `ws://localhost:8000/ws/notifications/${userId}`;
        const socket = new WebSocket(wsUrl);
        
        socket.onopen = (event) => {
            console.log('WebSocket connected');
        };
        
        socket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            console.log('WebSocket message:', data);
            
            // Handle different message types
            if (data.type === 'task_notification') {
                this.handleTaskNotification(data);
            } else if (data.type === 'system_notification') {
                this.handleSystemNotification(data);
            }
        };
        
        socket.onclose = (event) => {
            console.log('WebSocket disconnected');
        };
        
        socket.onerror = (error) => {
            console.error('WebSocket error:', error);
        };
        
        return socket;
    }
    
    handleTaskNotification(data) {
        // Override this method to handle task notifications
        console.log('Task notification:', data);
    }
    
    handleSystemNotification(data) {
        // Override this method to handle system notifications
        console.log('System notification:', data);
    }
}

// Example usage
async function example() {
    const client = new TaskManagerClient();
    
    try {
        // Create a client
        const newClient = await client.createClient({
            name: 'Jane Smith',
            email: 'jane@example.com',
            company: 'Tech Solutions'
        });
        console.log('Created client:', newClient);
        
        // Create a task
        const newTask = await client.createTask({
            name: 'Review API documentation',
            description: 'Review and update API documentation',
            priority: 'medium',
            client_id: newClient.id
        });
        console.log('Created task:', newTask);
        
        // Get tasks with filters
        const tasks = await client.getTasks({ status: 'todo', priority: 'high' });
        console.log('Filtered tasks:', tasks);
        
        // Get statistics
        const stats = await client.getTaskStats();
        console.log('Task statistics:', stats);
        
        // Connect to WebSocket
        const socket = client.connectWebSocket(1);
        
    } catch (error) {
        console.error('API error:', error);
    }
}


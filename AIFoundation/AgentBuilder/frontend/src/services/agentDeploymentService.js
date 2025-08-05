// Agent Deployment Service
class AgentDeploymentService {
  constructor() {
    this.baseUrl = 'http://localhost:8000';
  }

  // Mock agents data
  getAgents() {
    return [
      {
        id: 1,
        name: "Billing Support Bot",
        template: "billing",
        status: "ready",
        deploymentStatus: "deployed",
        version: "v1.2",
        lastTested: "2025-01-28",
        accuracy: 94,
        cloudVendor: "aws",
        endpoint: "https://api.billing-bot.com",
        region: "us-east-1"
      },
      {
        id: 2,
        name: "Front Desk Assistant",
        template: "reception",
        status: "ready",
        deploymentStatus: "staging",
        version: "v2.0",
        lastTested: "2025-01-27",
        accuracy: 98,
        cloudVendor: "azure",
        endpoint: "https://staging.frontdesk-bot.com",
        region: "east-us"
      },
      {
        id: 3,
        name: "Sales Consultant",
        template: "sales",
        status: "testing",
        deploymentStatus: "not_deployed",
        version: "v1.0",
        lastTested: "2025-01-26",
        accuracy: 87,
        cloudVendor: "",
        endpoint: "",
        region: ""
      }
    ];
  }

  // Cloud vendor options
  getCloudVendors() {
    return [
      {
        id: 'aws',
        name: 'Amazon Web Services',
        logo: '🔶',
        regions: [
          { id: 'us-east-1', name: 'US East (N. Virginia)', latency: '12ms' },
          { id: 'us-west-2', name: 'US West (Oregon)', latency: '45ms' },
          { id: 'eu-west-1', name: 'Europe (Ireland)', latency: '89ms' },
          { id: 'ap-southeast-1', name: 'Asia Pacific (Singapore)', latency: '156ms' }
        ],
        instanceTypes: [
          { id: 't3.micro', name: 't3.micro', cpu: '2 vCPUs', memory: '1GB', cost: '$8.76/month' },
          { id: 't3.small', name: 't3.small', cpu: '2 vCPUs', memory: '2GB', cost: '$17.52/month' },
          { id: 't3.medium', name: 't3.medium', cpu: '2 vCPUs', memory: '4GB', cost: '$35.04/month' },
          { id: 'c5.large', name: 'c5.large', cpu: '2 vCPUs', memory: '4GB', cost: '$62.56/month' }
        ],
        features: ['Auto Scaling', 'Load Balancing', 'CloudWatch Monitoring', 'S3 Storage']
      },
      {
        id: 'azure',
        name: 'Microsoft Azure',
        logo: '🔷',
        regions: [
          { id: 'east-us', name: 'East US', latency: '15ms' },
          { id: 'west-us-2', name: 'West US 2', latency: '42ms' },
          { id: 'west-europe', name: 'West Europe', latency: '92ms' },
          { id: 'southeast-asia', name: 'Southeast Asia', latency: '162ms' }
        ],
        instanceTypes: [
          { id: 'B1s', name: 'B1s', cpu: '1 vCPU', memory: '1GB', cost: '$7.59/month' },
          { id: 'B2s', name: 'B2s', cpu: '2 vCPUs', memory: '4GB', cost: '$30.37/month' },
          { id: 'D2s_v3', name: 'D2s v3', cpu: '2 vCPUs', memory: '8GB', cost: '$70.08/month' },
          { id: 'F2s_v2', name: 'F2s v2', cpu: '2 vCPUs', memory: '4GB', cost: '$60.74/month' }
        ],
        features: ['Auto Scaling', 'Application Gateway', 'Azure Monitor', 'Blob Storage']
      },
      {
        id: 'gcp',
        name: 'Google Cloud Platform',
        logo: '🟡',
        regions: [
          { id: 'us-central1', name: 'US Central (Iowa)', latency: '18ms' },
          { id: 'us-west1', name: 'US West (Oregon)', latency: '48ms' },
          { id: 'europe-west1', name: 'Europe West (Belgium)', latency: '95ms' },
          { id: 'asia-southeast1', name: 'Asia Southeast (Singapore)', latency: '168ms' }
        ],
        instanceTypes: [
          { id: 'e2-micro', name: 'e2-micro', cpu: '2 vCPUs', memory: '1GB', cost: '$6.11/month' },
          { id: 'e2-small', name: 'e2-small', cpu: '2 vCPUs', memory: '2GB', cost: '$12.23/month' },
          { id: 'e2-medium', name: 'e2-medium', cpu: '2 vCPUs', memory: '4GB', cost: '$24.46/month' },
          { id: 'n2-standard-2', name: 'n2-standard-2', cpu: '2 vCPUs', memory: '8GB', cost: '$63.74/month' }
        ],
        features: ['Auto Scaling', 'Load Balancing', 'Cloud Monitoring', 'Cloud Storage']
      }
    ];
  }

  // Simulate agent testing
  async testAgent(agentId, message) {
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, Math.random() * 2000 + 1000));
    
    return {
      type: 'agent',
      content: `Hello! I'm the agent. I understand you said: "${message}". How can I help you with that?`,
      timestamp: new Date(),
      confidence: Math.random() * 0.3 + 0.7, // 70-100% confidence
      processingTime: Math.random() * 2000 + 500 // 500-2500ms
    };
  }

  // Simulate deployment
  async deployAgent(agentId, deploymentConfig) {
    return new Promise((resolve) => {
      let progress = 0;
      const interval = setInterval(() => {
        progress += Math.random() * 20;
        if (progress >= 100) {
          clearInterval(interval);
          resolve({
            success: true,
            endpoint: `https://api.agent-${agentId}.com`,
            deploymentId: `deploy-${Date.now()}`
          });
        }
      }, 1500);
    });
  }

  // Get deployment status
  getDeploymentStatuses() {
    return {
      'not_deployed': { color: 'text-gray-600 bg-gray-100', label: 'Not Deployed' },
      'deploying': { color: 'text-blue-600 bg-blue-100', label: 'Deploying' },
      'staging': { color: 'text-yellow-600 bg-yellow-100', label: 'Staging' },
      'deployed': { color: 'text-green-600 bg-green-100', label: 'Production' },
      'failed': { color: 'text-red-600 bg-red-100', label: 'Failed' }
    };
  }
}

export default new AgentDeploymentService(); 
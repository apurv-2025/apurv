import { mockApi } from '../api/mockApi';
import { validateFile } from '../utils/helpers';
import { UPLOAD_CONFIG } from '../utils/constants';

class ClaimsService {
  async getClaims(filters = {}) {
    try {
      return await mockApi.getClaims(filters);
    } catch (error) {
      console.error('Error fetching claims:', error);
      throw new Error('Failed to fetch claims. Please try again.');
    }
  }

  async getDashboardStats() {
    try {
      return await mockApi.getDashboardStats();
    } catch (error) {
      console.error('Error fetching dashboard stats:', error);
      throw new Error('Failed to fetch dashboard statistics. Please try again.');
    }
  }

  async uploadClaim(file, payerId) {
    // Validate file before upload
    const validation = validateFile(
      file,
      UPLOAD_CONFIG.acceptedExtensions,
      UPLOAD_CONFIG.maxFileSize
    );

    if (!validation.valid) {
      throw new Error(validation.error);
    }

    try {
      return await mockApi.uploadClaim(file, payerId);
    } catch (error) {
      console.error('Error uploading claim:', error);
      throw new Error(error.message || 'Failed to upload claim. Please try again.');
    }
  }

  async getClaimById(id) {
    try {
      const claim = await mockApi.getClaimById(id);
      if (!claim) {
        throw new Error('Claim not found');
      }
      return claim;
    } catch (error) {
      console.error('Error fetching claim:', error);
      throw new Error('Failed to fetch claim details. Please try again.');
    }
  }

  async updateClaimStatus(id, status) {
    try {
      return await mockApi.updateClaimStatus(id, status);
    } catch (error) {
      console.error('Error updating claim status:', error);
      throw new Error('Failed to update claim status. Please try again.');
    }
  }

  // Additional business logic methods
  calculateCollectionRate(totalCharged, totalPaid) {
    if (!totalCharged || totalCharged === 0) return 0;
    return ((totalPaid / totalCharged) * 100).toFixed(1);
  }

  getClaimStatusSummary(claims) {
    const summary = {};
    claims.forEach(claim => {
      summary[claim.status] = (summary[claim.status] || 0) + 1;
    });
    return summary;
  }

  getClaimTypeSummary(claims) {
    const summary = {};
    claims.forEach(claim => {
      summary[claim.claim_type] = (summary[claim.claim_type] || 0) + 1;
    });
    return summary;
  }

  // Work Queue Methods
  async getWorkQueue(filters = {}) {
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL || 'http://localhost:8000'}/api/claims/work-queue/?${new URLSearchParams(filters)}`);
      if (!response.ok) {
        throw new Error('Failed to fetch work queue');
      }
      return await response.json();
    } catch (error) {
      console.error('Error fetching work queue:', error);
      throw new Error('Failed to fetch work queue. Please try again.');
    }
  }

  async getWorkQueueSummary() {
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL || 'http://localhost:8000'}/api/claims/work-queue/summary`);
      if (!response.ok) {
        throw new Error('Failed to fetch work queue summary');
      }
      return await response.json();
    } catch (error) {
      console.error('Error fetching work queue summary:', error);
      throw new Error('Failed to fetch work queue summary. Please try again.');
    }
  }

  async assignClaimToWorkQueue(claimId, assignment) {
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL || 'http://localhost:8000'}/api/claims/${claimId}/assign`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(assignment),
      });
      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to assign claim to work queue');
      }
      return await response.json();
    } catch (error) {
      console.error('Error assigning claim to work queue:', error);
      throw new Error('Failed to assign claim to work queue. Please try again.');
    }
  }

  async updateWorkQueueItem(workQueueId, update) {
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL || 'http://localhost:8000'}/api/claims/work-queue/${workQueueId}`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(update),
      });
      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to update work queue item');
      }
      return await response.json();
    } catch (error) {
      console.error('Error updating work queue item:', error);
      throw new Error('Failed to update work queue item. Please try again.');
    }
  }

  async assignWorkQueueToAgent(workQueueId, agentId, taskType = 'process_claim') {
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL || 'http://localhost:8000'}/api/claims/work-queue/${workQueueId}/assign-to-agent`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ agent_id: agentId, task_type: taskType }),
      });
      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to assign to agent');
      }
      return await response.json();
    } catch (error) {
      console.error('Error assigning to agent:', error);
      throw new Error('Failed to assign to agent. Please try again.');
    }
  }

  async getAvailableAgents() {
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL || 'http://localhost:8000'}/api/claims/work-queue/available-agents`);
      if (!response.ok) {
        throw new Error('Failed to fetch available agents');
      }
      return await response.json();
    } catch (error) {
      console.error('Error fetching available agents:', error);
      throw new Error('Failed to fetch available agents. Please try again.');
    }
  }
}

export const claimsService = new ClaimsService();

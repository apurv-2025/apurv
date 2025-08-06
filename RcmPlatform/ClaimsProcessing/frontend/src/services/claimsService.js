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
}

export const claimsService = new ClaimsService();

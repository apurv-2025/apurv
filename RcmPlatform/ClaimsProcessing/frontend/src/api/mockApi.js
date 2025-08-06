import { generateClaimNumber } from '../utils/helpers';

// Mock data
const MOCK_CLAIMS = [
  {
    id: 1,
    claim_number: 'CLM12345678',
    claim_type: '837D',
    status: 'validated',
    patient_first_name: 'John',
    patient_last_name: 'Doe',
    provider_name: 'Smile Dental Care',
    provider_npi: '1234567890',
    total_charge: 450.00,
    paid_amount: 360.00,
    created_at: '2024-01-15T10:30:00Z',
    payer: { name: 'Delta Dental' }
  },
  {
    id: 2,
    claim_number: 'CLM87654321',
    claim_type: '837P',
    status: 'sent',
    patient_first_name: 'Jane',
    patient_last_name: 'Smith',
    provider_name: 'Family Health Center',
    provider_npi: '0987654321',
    total_charge: 250.00,
    paid_amount: null,
    created_at: '2024-01-14T14:20:00Z',
    payer: { name: 'Blue Cross Blue Shield' }
  },
  {
    id: 3,
    claim_number: 'CLM11223344',
    claim_type: '837I',
    status: 'rejected',
    patient_first_name: 'Bob',
    patient_last_name: 'Johnson',
    provider_name: 'City Hospital',
    provider_npi: '1122334455',
    total_charge: 1250.00,
    paid_amount: null,
    created_at: '2024-01-13T09:15:00Z',
    payer: { name: 'Medicare' },
    validation_errors: {
      errors: ['Invalid NPI format', 'Missing diagnosis code']
    }
  }
];

const MOCK_DASHBOARD_STATS = {
  status_distribution: [
    { status: 'validated', count: 45 },
    { status: 'sent', count: 32 },
    { status: 'paid', count: 28 },
    { status: 'rejected', count: 8 }
  ],
  type_distribution: [
    { type: '837D', count: 52 },
    { type: '837P', count: 38 },
    { type: '837I', count: 23 }
  ],
  recent_claims_30_days: 113,
  financial_summary: {
    total_charged: 45680.50,
    total_allowed: 38920.25,
    total_paid: 35240.80
  }
};

// Simulate network delay
const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));

// Mock API functions
export const mockApi = {
  async getClaims(filters = {}) {
    await delay(500);
    return MOCK_CLAIMS;
  },

  async getDashboardStats() {
    await delay(300);
    return MOCK_DASHBOARD_STATS;
  },

  async uploadClaim(file, payerId) {
    await delay(1500);
    
    // Simulate 90% success rate
    if (Math.random() > 0.1) {
      return {
        id: Math.floor(Math.random() * 1000),
        claim_number: generateClaimNumber(),
        status: 'queued',
        message: 'Claim uploaded successfully'
      };
    } else {
      throw new Error('Failed to parse EDI file');
    }
  },

  async getClaimById(id) {
    await delay(200);
    return MOCK_CLAIMS.find(claim => claim.id === parseInt(id));
  },

  async updateClaimStatus(id, status) {
    await delay(400);
    const claim = MOCK_CLAIMS.find(claim => claim.id === parseInt(id));
    if (claim) {
      claim.status = status;
      return claim;
    }
    throw new Error('Claim not found');
  }
};

export const DEFAULT_CONFIG = {
  apiUrl: 'http://localhost:8000',
  model: 'gpt-4',
  theme: 'light' as const,
  position: 'bottom-right' as const,
  showQuickActions: true,
  enableHistory: true,
  enableMetrics: true,
};

export const SUPPORTED_MODELS = [
  { name: 'GPT-4', value: 'gpt-4', provider: 'openai' },
  { name: 'GPT-3.5 Turbo', value: 'gpt-3.5-turbo', provider: 'openai' },
  { name: 'Claude 3 Sonnet', value: 'claude-3-sonnet', provider: 'anthropic' },
  { name: 'Claude 3 Haiku', value: 'claude-3-haiku', provider: 'anthropic' },
];

export const QUICK_ACTIONS = [
  { label: 'Analyze Claim', action: 'analyze_claim', icon: 'FileText' },
  { label: 'Process Rejection', action: 'process_rejection', icon: 'AlertCircle' },
  { label: 'Generate Report', action: 'generate_report', icon: 'BarChart3' },
  { label: 'Search Claims', action: 'search_claims', icon: 'Search' },
]; 
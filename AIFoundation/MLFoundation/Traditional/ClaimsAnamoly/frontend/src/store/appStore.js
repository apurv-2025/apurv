import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export const useAppStore = create(
  persist(
    (set, get) => ({
      // UI State
      sidebarOpen: false,
      loading: false,
      notifications: [],

      // Data Pipeline Configuration
      dataConfig: {
        numClaims: 5000,
        anomalyRate: 0.08,
        dateRange: {
          start: '2023-01-01',
          end: '2025-12-31'
        },
        providers: {
          count: 100,
          specialties: ['Internal Medicine', 'Cardiology', 'Orthopedics', 'Neurology', 'Oncology']
        },
        amounts: {
          min: 50,
          max: 2000,
          mean: 300
        }
      },

      // Model Configuration
      modelConfig: {
        ensemble: {
          isolationForest: {
            enabled: true,
            contamination: 0.08,
            randomState: 42
          },
          randomForest: {
            enabled: true,
            nEstimators: 100,
            maxDepth: 10,
            randomState: 42
          },
          weights: {
            isolationForest: 0.3,
            randomForest: 0.7
          }
        },
        features: {
          includeDateFeatures: true,
          includeProviderFeatures: true,
          includeAmountFeatures: true,
          includeCategoricalFeatures: true
        },
        preprocessing: {
          normalizeNumerical: true,
          encodeCategorical: true,
          handleMissingValues: true
        }
      },

      // Training State
      trainingState: {
        isTraining: false,
        progress: 0,
        currentStep: '',
        metrics: null,
        history: []
      },

      // Model Management
      models: [],
      activeModel: null,

      // API Service Configuration
      apiConfig: {
        port: 8000,
        host: '0.0.0.0',
        debug: true,
        cors: true,
        rateLimit: {
          enabled: true,
          requestsPerMinute: 100
        }
      },

      // Monitoring Data
      monitoringData: {
        apiRequests: [],
        modelPerformance: [],
        systemHealth: {
          status: 'healthy',
          uptime: 0,
          memoryUsage: 0,
          cpuUsage: 0
        }
      },

      // Actions
      setSidebarOpen: (open) => set({ sidebarOpen: open }),
      setLoading: (loading) => set({ loading }),
      
      addNotification: (notification) => 
        set((state) => ({
          notifications: [...state.notifications, { ...notification, id: Date.now() }]
        })),
      
      removeNotification: (id) =>
        set((state) => ({
          notifications: state.notifications.filter(n => n.id !== id)
        })),

      updateDataConfig: (config) =>
        set((state) => ({
          dataConfig: { ...state.dataConfig, ...config }
        })),

      updateModelConfig: (config) =>
        set((state) => ({
          modelConfig: { ...state.modelConfig, ...config }
        })),

      setTrainingState: (state) => set({ trainingState: state }),
      
      updateTrainingProgress: (progress, step) =>
        set((state) => ({
          trainingState: {
            ...state.trainingState,
            progress,
            currentStep: step
          }
        })),

      addModel: (model) =>
        set((state) => ({
          models: [...state.models, model],
          activeModel: model
        })),

      setActiveModel: (modelId) =>
        set((state) => ({
          activeModel: state.models.find(m => m.id === modelId)
        })),

      updateApiConfig: (config) =>
        set((state) => ({
          apiConfig: { ...state.apiConfig, ...config }
        })),

      updateMonitoringData: (data) =>
        set((state) => ({
          monitoringData: { ...state.monitoringData, ...data }
        })),

      // Reset functions
      resetTrainingState: () =>
        set({
          trainingState: {
            isTraining: false,
            progress: 0,
            currentStep: '',
            metrics: null,
            history: []
          }
        }),

      resetDataConfig: () =>
        set({
          dataConfig: {
            numClaims: 5000,
            anomalyRate: 0.08,
            dateRange: {
              start: '2023-01-01',
              end: '2025-12-31'
            },
            providers: {
              count: 100,
              specialties: ['Internal Medicine', 'Cardiology', 'Orthopedics', 'Neurology', 'Oncology']
            },
            amounts: {
              min: 50,
              max: 2000,
              mean: 300
            }
          }
        }),

      resetModelConfig: () =>
        set({
          modelConfig: {
            ensemble: {
              isolationForest: {
                enabled: true,
                contamination: 0.08,
                randomState: 42
              },
              randomForest: {
                enabled: true,
                nEstimators: 100,
                maxDepth: 10,
                randomState: 42
              },
              weights: {
                isolationForest: 0.3,
                randomForest: 0.7
              }
            },
            features: {
              includeDateFeatures: true,
              includeProviderFeatures: true,
              includeAmountFeatures: true,
              includeCategoricalFeatures: true
            },
            preprocessing: {
              normalizeNumerical: true,
              encodeCategorical: true,
              handleMissingValues: true
            }
          }
        })
    }),
    {
      name: 'claims-anomaly-store',
      partialize: (state) => ({
        dataConfig: state.dataConfig,
        modelConfig: state.modelConfig,
        apiConfig: state.apiConfig,
        models: state.models,
        activeModel: state.activeModel
      })
    }
  )
); 
import React, { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { 
  CircleStackIcon, 
  PlayIcon, 
  StopIcon, 
  DocumentArrowDownIcon,
  ChartBarIcon,
  CogIcon
} from '@heroicons/react/24/outline';
import { useAppStore } from '../store/appStore';
import { apiService } from '../services/apiService';
import toast from 'react-hot-toast';

function DataPipeline() {
  const { dataConfig, updateDataConfig, addNotification } = useAppStore();
  const [isGenerating, setIsGenerating] = useState(false);
  const [dataStats, setDataStats] = useState(null);
  const [generationProgress, setGenerationProgress] = useState(0);

  const { register, handleSubmit, watch, setValue, formState: { errors } } = useForm({
    defaultValues: dataConfig
  });

  const watchedValues = watch();

  useEffect(() => {
    loadDataStats();
  }, []);

  const loadDataStats = async () => {
    try {
      const stats = await apiService.getDataStats();
      setDataStats(stats);
    } catch (error) {
      console.error('Failed to load data stats:', error);
    }
  };

  const onSubmit = async (data) => {
    try {
      updateDataConfig(data);
      toast.success('Data configuration updated successfully');
    } catch (error) {
      toast.error('Failed to update configuration');
    }
  };

  const generateData = async () => {
    setIsGenerating(true);
    setGenerationProgress(0);

    try {
      const config = watchedValues;
      
      // Simulate progress updates
      const progressInterval = setInterval(() => {
        setGenerationProgress(prev => {
          if (prev >= 90) {
            clearInterval(progressInterval);
            return prev;
          }
          return prev + Math.random() * 10;
        });
      }, 500);

      const result = await apiService.generateData(config);
      
      clearInterval(progressInterval);
      setGenerationProgress(100);
      
      toast.success(`Generated ${result.total_claims} claims with ${result.anomalies} anomalies`);
      loadDataStats();
      
      addNotification({
        type: 'success',
        title: 'Data Generation Complete',
        message: `Successfully generated ${result.total_claims} claims`
      });

    } catch (error) {
      toast.error('Failed to generate data');
      addNotification({
        type: 'error',
        title: 'Data Generation Failed',
        message: error.message || 'An error occurred during data generation'
      });
    } finally {
      setIsGenerating(false);
      setTimeout(() => setGenerationProgress(0), 1000);
    }
  };

  const downloadData = async () => {
    try {
      const response = await fetch(`${apiService.baseURL}/api/v1/data/download`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      
      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'claims_data.csv';
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        toast.success('Data downloaded successfully');
      } else {
        throw new Error('Download failed');
      }
    } catch (error) {
      toast.error('Failed to download data');
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="md:flex md:items-center md:justify-between">
        <div className="min-w-0 flex-1">
          <h2 className="text-2xl font-bold leading-7 text-gray-900 sm:truncate sm:text-3xl sm:tracking-tight">
            Data Pipeline
          </h2>
          <p className="mt-1 text-sm text-gray-500">
            Configure and manage synthetic data generation for claims anomaly detection
          </p>
        </div>
        <div className="mt-4 flex md:ml-4 md:mt-0 space-x-3">
          <button
            type="button"
            onClick={downloadData}
            className="inline-flex items-center rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50"
          >
            <DocumentArrowDownIcon className="h-5 w-5 mr-2" />
            Download Data
          </button>
          <button
            type="button"
            onClick={generateData}
            disabled={isGenerating}
            className="inline-flex items-center rounded-md bg-primary-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-primary-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary-600 disabled:opacity-50"
          >
            {isGenerating ? (
              <>
                <StopIcon className="h-5 w-5 mr-2" />
                Generating...
              </>
            ) : (
              <>
                <PlayIcon className="h-5 w-5 mr-2" />
                Generate Data
              </>
            )}
          </button>
        </div>
      </div>

      {/* Progress Bar */}
      {isGenerating && (
        <div className="bg-white shadow rounded-lg p-6">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-medium text-gray-700">Generating Data...</span>
            <span className="text-sm font-medium text-gray-700">{Math.round(generationProgress)}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div 
              className="bg-primary-600 h-2 rounded-full transition-all duration-300"
              style={{ width: `${generationProgress}%` }}
            ></div>
          </div>
        </div>
      )}

      {/* Data Statistics */}
      {dataStats && (
        <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="p-5">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <CircleStackIcon className="h-6 w-6 text-gray-400" />
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">Total Claims</dt>
                    <dd className="text-lg font-medium text-gray-900">{dataStats.total_claims?.toLocaleString() || 0}</dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>

          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="p-5">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <ChartBarIcon className="h-6 w-6 text-gray-400" />
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">Anomalies</dt>
                    <dd className="text-lg font-medium text-gray-900">{dataStats.anomalies?.toLocaleString() || 0}</dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>

          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="p-5">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <CogIcon className="h-6 w-6 text-gray-400" />
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">Anomaly Rate</dt>
                    <dd className="text-lg font-medium text-gray-900">
                      {dataStats.anomaly_rate ? `${(dataStats.anomaly_rate * 100).toFixed(1)}%` : '0%'}
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>

          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="p-5">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <CircleStackIcon className="h-6 w-6 text-gray-400" />
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">Last Generated</dt>
                    <dd className="text-sm font-medium text-gray-900">
                      {dataStats.last_generated ? new Date(dataStats.last_generated).toLocaleDateString() : 'Never'}
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Configuration Form */}
      <div className="bg-white shadow rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <h3 className="text-lg font-medium text-gray-900 mb-6">Data Generation Configuration</h3>
          
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
            {/* Basic Settings */}
            <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Number of Claims
                </label>
                <input
                  type="number"
                  {...register('numClaims', { 
                    required: 'Number of claims is required',
                    min: { value: 100, message: 'Minimum 100 claims required' },
                    max: { value: 100000, message: 'Maximum 100,000 claims allowed' }
                  })}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                />
                {errors.numClaims && (
                  <p className="mt-1 text-sm text-red-600">{errors.numClaims.message}</p>
                )}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Anomaly Rate (%)
                </label>
                <input
                  type="number"
                  step="0.01"
                  {...register('anomalyRate', { 
                    required: 'Anomaly rate is required',
                    min: { value: 0, message: 'Anomaly rate must be positive' },
                    max: { value: 1, message: 'Anomaly rate cannot exceed 100%' }
                  })}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                />
                {errors.anomalyRate && (
                  <p className="mt-1 text-sm text-red-600">{errors.anomalyRate.message}</p>
                )}
              </div>
            </div>

            {/* Date Range */}
            <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Start Date
                </label>
                <input
                  type="date"
                  {...register('dateRange.start', { required: 'Start date is required' })}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                />
                {errors.dateRange?.start && (
                  <p className="mt-1 text-sm text-red-600">{errors.dateRange.start.message}</p>
                )}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700">
                  End Date
                </label>
                <input
                  type="date"
                  {...register('dateRange.end', { required: 'End date is required' })}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                />
                {errors.dateRange?.end && (
                  <p className="mt-1 text-sm text-red-600">{errors.dateRange.end.message}</p>
                )}
              </div>
            </div>

            {/* Provider Settings */}
            <div>
              <h4 className="text-md font-medium text-gray-900 mb-4">Provider Configuration</h4>
              <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
                <div>
                  <label className="block text-sm font-medium text-gray-700">
                    Number of Providers
                  </label>
                  <input
                    type="number"
                    {...register('providers.count', { 
                      required: 'Provider count is required',
                      min: { value: 1, message: 'At least 1 provider required' },
                      max: { value: 1000, message: 'Maximum 1,000 providers allowed' }
                    })}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                  />
                  {errors.providers?.count && (
                    <p className="mt-1 text-sm text-red-600">{errors.providers.count.message}</p>
                  )}
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700">
                    Provider Specialties
                  </label>
                  <select
                    multiple
                    {...register('providers.specialties')}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                  >
                    <option value="Internal Medicine">Internal Medicine</option>
                    <option value="Cardiology">Cardiology</option>
                    <option value="Orthopedics">Orthopedics</option>
                    <option value="Neurology">Neurology</option>
                    <option value="Oncology">Oncology</option>
                    <option value="Dermatology">Dermatology</option>
                    <option value="Psychiatry">Psychiatry</option>
                    <option value="Pediatrics">Pediatrics</option>
                  </select>
                </div>
              </div>
            </div>

            {/* Amount Settings */}
            <div>
              <h4 className="text-md font-medium text-gray-900 mb-4">Amount Configuration</h4>
              <div className="grid grid-cols-1 gap-6 sm:grid-cols-3">
                <div>
                  <label className="block text-sm font-medium text-gray-700">
                    Minimum Amount ($)
                  </label>
                  <input
                    type="number"
                    step="0.01"
                    {...register('amounts.min', { 
                      required: 'Minimum amount is required',
                      min: { value: 0, message: 'Minimum amount must be positive' }
                    })}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                  />
                  {errors.amounts?.min && (
                    <p className="mt-1 text-sm text-red-600">{errors.amounts.min.message}</p>
                  )}
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700">
                    Maximum Amount ($)
                  </label>
                  <input
                    type="number"
                    step="0.01"
                    {...register('amounts.max', { 
                      required: 'Maximum amount is required',
                      min: { value: 0, message: 'Maximum amount must be positive' }
                    })}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                  />
                  {errors.amounts?.max && (
                    <p className="mt-1 text-sm text-red-600">{errors.amounts.max.message}</p>
                  )}
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700">
                    Mean Amount ($)
                  </label>
                  <input
                    type="number"
                    step="0.01"
                    {...register('amounts.mean', { 
                      required: 'Mean amount is required',
                      min: { value: 0, message: 'Mean amount must be positive' }
                    })}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                  />
                  {errors.amounts?.mean && (
                    <p className="mt-1 text-sm text-red-600">{errors.amounts.mean.message}</p>
                  )}
                </div>
              </div>
            </div>

            {/* Form Actions */}
            <div className="flex justify-end space-x-3">
              <button
                type="button"
                onClick={() => {
                  setValue('numClaims', 5000);
                  setValue('anomalyRate', 0.08);
                  setValue('dateRange.start', '2023-01-01');
                  setValue('dateRange.end', '2025-12-31');
                  setValue('providers.count', 100);
                  setValue('amounts.min', 50);
                  setValue('amounts.max', 2000);
                  setValue('amounts.mean', 300);
                }}
                className="rounded-md border border-gray-300 bg-white py-2 px-4 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2"
              >
                Reset to Defaults
              </button>
              <button
                type="submit"
                className="rounded-md border border-transparent bg-primary-600 py-2 px-4 text-sm font-medium text-white shadow-sm hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2"
              >
                Save Configuration
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}

export default DataPipeline; 
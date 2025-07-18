import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 300000, // 5 minutes - increased for long-running operations
  retries: 3,
  retryDelay: 1000,
});

export const classificationAPI = {
  startClassification: async (config) => {
    const response = await api.post('/classify', config);
    return response.data;
  },

  getJobStatus: async (jobId) => {
    const response = await api.get(`/jobs/${jobId}`);
    return response.data;
  },

  getResults: async (jobId) => {
    const response = await api.get(`/results/${jobId}`);
    return response.data;
  },

  listJobs: async () => {
    const response = await api.get('/jobs');
    return response.data;
  },

  deleteJob: async (jobId) => {
    const response = await api.delete(`/jobs/${jobId}`);
    return response.data;
  },

  healthCheck: async () => {
    const response = await api.get('/health');
    return response.data;
  },
};

// Add request interceptor for retry logic
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const config = error.config;
    
    if (!config || !config.retries) {
      return Promise.reject(error);
    }
    
    config.retryCount = config.retryCount || 0;
    
    if (config.retryCount >= config.retries) {
      return Promise.reject(error);
    }
    
    config.retryCount += 1;
    
    const delay = new Promise((resolve) => {
      setTimeout(() => {
        resolve();
      }, config.retryDelay || 1000);
    });
    
    await delay;
    return api(config);
  }
);

export default api;
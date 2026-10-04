import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '';

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getHealth = async () => {
  const response = await api.get('/api/health');
  return response.data;
};

export const getDashboard = async () => {
  const response = await api.get('/api/dashboard');
  return response.data;
};

export const getFindings = async (params = {}) => {
  const response = await api.get('/api/findings', { params });
  return response.data;
};

export const getFindingByUid = async (uid) => {
  const response = await api.get(`/api/findings/${uid}`);
  return response.data;
};

export const updateFindingStatus = async (uid, status) => {
  const response = await api.patch(`/api/findings/${uid}`, { status });
  return response.data;
};

export const triggerAssessment = async (targetUrl = 'http://localhost:5001', includeDemo = false) => {
  const response = await api.post('/api/assessment/run', {
    target_url: targetUrl,
    include_demo: includeDemo,
  });
  return response.data;
};

export const resetAssessment = async () => {
  const response = await api.post('/api/assessment/reset');
  return response.data;
};

export const getReportUrl = () => {
  return `${API_BASE_URL}/api/report`;
};

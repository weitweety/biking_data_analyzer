import axios from 'axios';

// Use /api prefix for production (nginx proxy) or full URL for development
// Default to /api/ for Docker/production, can override with VITE_API_URL for local dev
const API_URL = import.meta.env.VITE_API_URL || '/api/';

const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getTripDurationStats = async () => {
  try {
    const response = await apiClient.get('/trip-duration-stats');
    return response.data;
  } catch (error) {
    console.error('Error fetching trip duration stats:', error);
    throw error;
  }
};

export default apiClient;


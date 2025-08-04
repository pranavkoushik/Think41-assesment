import axios from 'axios';

const API_URL = '/api'; // Using proxy from Vite config

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add a request interceptor to handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      // The request was made and the server responded with a status code
      // that falls out of the range of 2xx
      console.error('API Error:', error.response.data);
      return Promise.reject({
        message: error.response.data.detail || 'An error occurred',
        status: error.response.status,
      });
    } else if (error.request) {
      // The request was made but no response was received
      console.error('API Error: No response received', error.request);
      return Promise.reject({ message: 'No response from server' });
    } else {
      // Something happened in setting up the request that triggered an Error
      console.error('API Error:', error.message);
      return Promise.reject({ message: error.message });
    }
  }
);

export const getCustomers = async (params = {}) => {
  const response = await api.get('/customers', { params });
  return response.data;
};

export const getCustomer = async (id: string | number) => {
  const response = await api.get(`/customers/${id}`);
  return response.data;
};

export const getCustomerOrders = async (customerId: string | number, params = {}) => {
  const response = await api.get(`/customers/${customerId}/orders`, { params });
  return response.data;
};

export const getOrder = async (orderId: string | number) => {
  const response = await api.get(`/orders/${orderId}`);
  return response.data;
};

export default api;

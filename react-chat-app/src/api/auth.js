import axios from 'axios';

const API_BASE_URL = "http://localhost:8000";

export const login = async (email, password) => {
  const response = await axios.post(`${API_BASE_URL}/users/login`, { email, password });
  return response.data;
};

export const register = async (userData) => {
  const response = await axios.post(`${API_BASE_URL}/users/register`, userData);
  return response.data;
};

export const refreshAccessToken = async (refreshToken) => {
  const response = await axios.post(`${API_BASE_URL}/users/refresh`, { refresh_token: refreshToken });
  return response.data;
};

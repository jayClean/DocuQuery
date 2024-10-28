// src/api/axiosConfig.js
import axios from 'axios';

const API_BASE_URL = "http://localhost:8000";

// Create an instance of Axios
const axiosInstance = axios.create({
  baseURL: API_BASE_URL,
});

// Function to refresh the access token
const refreshAccessToken = async () => {
  const refreshToken = localStorage.getItem("refresh_token");
  if (!refreshToken) return null;

  try {
    const response = await axiosInstance.post('/users/refresh', { refresh_token: refreshToken });
    const newAccessToken = response.data.access_token;

    // Store the new access token
    localStorage.setItem("token", newAccessToken);
    return newAccessToken;
  } catch (error) {
    console.error("Refresh token failed:", error);
    // If refresh fails, clear tokens and logout
    localStorage.removeItem("token");
    localStorage.removeItem("refresh_token");
    return null;
  }
};

axiosInstance.interceptors.response.use(
    response => response,
    async error => {
      const originalRequest = error.config;
  
      if (error.response) {
        if (error.response.status === 401 && !originalRequest._retry) {
          originalRequest._retry = true; // Prevent infinite loops
          const newAccessToken = await refreshAccessToken();
          if (newAccessToken) {
            originalRequest.headers['Authorization'] = `Bearer ${newAccessToken}`;
            return axiosInstance(originalRequest);
          }
        } else if (error.response.status === 422) {
          console.error("Unprocessable Entity (422): Check the request data format.", error.response.data);
          alert("There was an issue with the data sent to the server. Please check your input and try again.");
          // You may also handle specific 422-related recovery here if needed.
        } else {
          console.error(`Unhandled status code: ${error.response.status}`, error.response.data);
        }
      }
      
      return Promise.reject(error);
    }
  );
  

export default axiosInstance;

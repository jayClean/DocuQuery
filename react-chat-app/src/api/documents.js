

// src/api/documents.js
import axiosInstance from './axiosConfig';

export const uploadDocument = async (file) => {
  const token = localStorage.getItem("token");
  const formData = new FormData();
  formData.append('file', file);

  const response = await axiosInstance.post(`/documents/upload`, formData, {
    headers: {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'multipart/form-data'
    }
  });

  return response.data;
};
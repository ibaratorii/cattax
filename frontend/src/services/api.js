import axios from 'axios';

const API_URL = process.env.VUE_APP_API_URL || 'http://localhost:8000/api';

export const uploadVideo = async (file) => {
  const formData = new FormData();
  formData.append('video', file);

  const response = await axios.post(`${API_URL}/analysis/upload_video/`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });

  return response.data;
};

export const getAnalysisStatus = async (id) => {
  const response = await axios.get(`${API_URL}/analysis/${id}/status/`);
  return response.data;
}; 
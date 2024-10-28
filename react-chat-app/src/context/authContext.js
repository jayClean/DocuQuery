// src/context/AuthContext.js
import React, { createContext, useState, useEffect } from 'react';
import { loginUser, refreshAccessToken, getUserProfile } from '../api/authService';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [accessToken, setAccessToken] = useState(localStorage.getItem('accessToken') || null);

  useEffect(() => {
    if (accessToken) {
      getUserProfile(accessToken).then(setUser).catch(() => setAccessToken(null));
    }
  }, [accessToken]);

  const login = async (loginData) => {
    const { access_token, refresh_token } = await loginUser(loginData);
    setAccessToken(access_token);
    localStorage.setItem('accessToken', access_token);
    localStorage.setItem('refreshToken', refresh_token);
    const profile = await getUserProfile(access_token);
    setUser(profile);
  };

  const logout = () => {
    setAccessToken(null);
    setUser(null);
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
  };

  const refresh = async () => {
    const refreshToken = localStorage.getItem('refreshToken');
    if (refreshToken) {
      const { access_token } = await refreshAccessToken(refreshToken);
      setAccessToken(access_token);
      localStorage.setItem('accessToken', access_token);
    }
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, refresh, accessToken }}>
      {children}
    </AuthContext.Provider>
  );
};

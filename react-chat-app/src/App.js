// src/App.js
import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import NavBar from './components/NavBar';
import Chat from './pages/Chat';
import Login from './pages/Login';
import Register from './pages/Register';

const ProtectedRoute = ({ token, children }) => {
  if (!token) {
    return <Navigate to="/login" />;
  }
  return children;
};

const App = () => {
  const [token, setToken] = useState(localStorage.getItem("token"));

  useEffect(() => {
    if (token) {
      localStorage.setItem("token", token);
    } else {
      localStorage.removeItem("token");
    }
  }, [token]);

  const handleLogout = () => {
    setToken(null);
    localStorage.removeItem("token");
    localStorage.removeItem("refresh_token"); // Clear refresh token
  };

  return (
    <Router>
      <NavBar token={token} onLogout={handleLogout} />
      <Routes>
        <Route path="/" element={<h1>Welcome to DocuQuery!</h1>} />
        <Route path="/login" element={<Login setToken={setToken} />} />
        <Route path="/register" element={<Register />} />
        <Route
          path="/chat"
          element={
            <ProtectedRoute token={token}>
              <Chat token={token} />
            </ProtectedRoute>
          }
        />
      </Routes>
    </Router>
  );
};

export default App;

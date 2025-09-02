import React, { useState } from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import { ThemeProvider } from './context/ThemeContext'
import Navigation from './components/Navigation'
import HomePage from './pages/HomePage'
import Login from './pages/Login'
import Register from './pages/Register'
import PriceEstimator from './pages/PriceEstimator'
import LocationAnalyzer from './pages/LocationAnalyzer'
import DealEvaluator from './pages/DealEvaluator'
import Dashboard from './pages/Dashboard'

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [user, setUser] = useState(null)

  const handleLogin = (userData) => {
    setUser(userData)
    setIsAuthenticated(true)
  }

  const handleLogout = () => {
    setUser(null)
    setIsAuthenticated(false)
  }

  return (
    <ThemeProvider>
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors duration-200">
        {isAuthenticated && <Navigation onLogout={handleLogout} user={user} />}
        <div className={isAuthenticated ? 'pt-16' : ''}>
          <Routes>
            <Route 
              path="/" 
              element={<HomePage />}
            />
            <Route 
              path="/login" 
              element={
                !isAuthenticated ? (
                  <Login onLogin={handleLogin} />
                ) : (
                  <Navigate to="/dashboard" replace />
                )
              } 
            />
            <Route 
              path="/register" 
              element={
                !isAuthenticated ? (
                  <Register onLogin={handleLogin} />
                ) : (
                  <Navigate to="/dashboard" replace />
                )
              } 
            />
            <Route 
              path="/dashboard" 
              element={
                isAuthenticated ? (
                  <Dashboard user={user} />
                ) : (
                  <Navigate to="/login" replace />
                )
              } 
            />
            <Route 
              path="/price-estimator" 
              element={
                isAuthenticated ? (
                  <PriceEstimator />
                ) : (
                  <Navigate to="/login" replace />
                )
              } 
            />
            <Route 
              path="/location-analyzer" 
              element={
                isAuthenticated ? (
                  <LocationAnalyzer />
                ) : (
                  <Navigate to="/login" replace />
                )
              } 
            />
            <Route 
              path="/deal-evaluator" 
              element={
                isAuthenticated ? (
                  <DealEvaluator />
                ) : (
                  <Navigate to="/login" replace />
                )
              } 
            />
          </Routes>
        </div>
      </div>
    </ThemeProvider>
  )
}

export default App

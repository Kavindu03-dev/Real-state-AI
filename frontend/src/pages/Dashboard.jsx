import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import axios from 'axios'

const Dashboard = ({ user }) => {
  const [searchHistory, setSearchHistory] = useState([])
  const [generatedReports, setGeneratedReports] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const [activeTab, setActiveTab] = useState('overview')

  const features = [
    {
      title: 'Price Estimator',
      description: 'Get accurate property price estimates using AI-powered analysis',
      path: '/price-estimator',
      icon: (
        <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1" />
        </svg>
      ),
      color: 'bg-blue-500',
    },
    {
      title: 'Location Analyzer',
      description: 'Analyze neighborhood data and market trends for informed decisions',
      path: '/location-analyzer',
      icon: (
        <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
        </svg>
      ),
      color: 'bg-green-500',
    },
    {
      title: 'Deal Evaluator',
      description: 'Evaluate investment opportunities and calculate potential returns',
      path: '/deal-evaluator',
      icon: (
        <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
        </svg>
      ),
      color: 'bg-purple-500',
    },
  ]

  const stats = [
    { label: 'Properties Analyzed', value: searchHistory.length.toString(), change: '+12%', changeType: 'positive' },
    { label: 'Reports Generated', value: generatedReports.length.toString(), change: '+8%', changeType: 'positive' },
    { label: 'Deals Evaluated', value: '432', change: '+15%', changeType: 'positive' },
    { label: 'Accuracy Rate', value: '94.2%', change: '+2.1%', changeType: 'positive' },
  ]

  useEffect(() => {
    // Load user data on component mount
    loadUserData()
  }, [])

  const loadUserData = async () => {
    try {
      // Simulate loading user data from API
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      // Mock search history data
      const mockSearchHistory = [
        {
          id: 1,
          type: 'Price Estimator',
          location: 'San Francisco, CA',
          propertyType: 'House',
          bedrooms: 3,
          bathrooms: 2,
          area: 2000,
          estimatedPrice: 850000,
          date: '2024-01-15T10:30:00Z',
          status: 'completed'
        },
        {
          id: 2,
          type: 'Location Analyzer',
          location: 'Downtown Seattle, WA',
          safetyRating: 'A+',
          nearbySchools: 5,
          transportOptions: 4,
          date: '2024-01-14T14:20:00Z',
          status: 'completed'
        },
        {
          id: 3,
          type: 'Deal Evaluator',
          location: 'Austin, TX',
          propertyPrice: 450000,
          marketValue: 500000,
          dealScore: 'Buy',
          confidenceLevel: 85,
          date: '2024-01-13T09:15:00Z',
          status: 'completed'
        },
        {
          id: 4,
          type: 'Price Estimator',
          location: 'Miami, FL',
          propertyType: 'Apartment',
          bedrooms: 2,
          bathrooms: 1,
          area: 1200,
          estimatedPrice: 320000,
          date: '2024-01-12T16:45:00Z',
          status: 'completed'
        }
      ]

      // Mock generated reports data
      const mockGeneratedReports = [
        {
          id: 1,
          title: 'San Francisco Property Analysis',
          type: 'Price Estimator',
          date: '2024-01-15T10:30:00Z',
          summary: '3-bedroom house in San Francisco estimated at $850,000',
          status: 'completed',
          downloadUrl: '#'
        },
        {
          id: 2,
          title: 'Seattle Neighborhood Report',
          type: 'Location Analyzer',
          date: '2024-01-14T14:20:00Z',
          summary: 'Downtown Seattle analysis with A+ safety rating',
          status: 'completed',
          downloadUrl: '#'
        },
        {
          id: 3,
          title: 'Austin Investment Evaluation',
          type: 'Deal Evaluator',
          date: '2024-01-13T09:15:00Z',
          summary: 'Property deal scored as "Buy" with 85% confidence',
          status: 'completed',
          downloadUrl: '#'
        }
      ]

      setSearchHistory(mockSearchHistory)
      setGeneratedReports(mockGeneratedReports)
    } catch (error) {
      console.error('Error loading user data:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const exportToPDF = async (reportId) => {
    try {
      // Simulate PDF generation
      console.log(`Generating PDF for report ${reportId}...`)
      await new Promise(resolve => setTimeout(resolve, 2000))
      
      // In a real implementation, this would call an API endpoint
      // const response = await axios.post(`/api/reports/${reportId}/export-pdf`)
      
      alert('PDF report generated successfully! Download will start shortly.')
    } catch (error) {
      console.error('Error generating PDF:', error)
      alert('Error generating PDF. Please try again.')
    }
  }

  const formatDate = (dateString) => {
    const date = new Date(dateString)
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  const getTypeIcon = (type) => {
    switch (type) {
      case 'Price Estimator':
        return (
          <svg className="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1" />
          </svg>
        )
      case 'Location Analyzer':
        return (
          <svg className="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
          </svg>
        )
      case 'Deal Evaluator':
        return (
          <svg className="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
          </svg>
        )
      default:
        return null
    }
  }

  const getTypeColor = (type) => {
    switch (type) {
      case 'Price Estimator':
        return 'bg-blue-100'
      case 'Location Analyzer':
        return 'bg-green-100'
      case 'Deal Evaluator':
        return 'bg-purple-100'
      default:
        return 'bg-gray-100'
    }
  }

  if (isLoading) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex items-center justify-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
        </div>
      </div>
    )
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Welcome Section */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
          Welcome back, {user?.name || 'User'}!
        </h1>
        <p className="mt-2 text-gray-600 dark:text-gray-400">
          Here's what's happening with your real estate analysis today.
        </p>
      </div>

      {/* Tab Navigation */}
      <div className="mb-8">
        <nav className="flex space-x-8">
          <button
            onClick={() => setActiveTab('overview')}
            className={`py-2 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'overview'
                ? 'border-primary-500 text-primary-600 dark:text-primary-400'
                : 'border-transparent text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300 hover:border-gray-300 dark:hover:border-gray-600'
            }`}
          >
            Overview
          </button>
          <button
            onClick={() => setActiveTab('history')}
            className={`py-2 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'history'
                ? 'border-primary-500 text-primary-600 dark:text-primary-400'
                : 'border-transparent text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300 hover:border-gray-300 dark:hover:border-gray-600'
            }`}
          >
            Search History
          </button>
          <button
            onClick={() => setActiveTab('reports')}
            className={`py-2 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'reports'
                ? 'border-primary-500 text-primary-600 dark:text-primary-400'
                : 'border-transparent text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300 hover:border-gray-300 dark:hover:border-gray-600'
            }`}
          >
            Generated Reports
          </button>
        </nav>
      </div>

      {/* Overview Tab */}
      {activeTab === 'overview' && (
        <>
          {/* Stats Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            {stats.map((stat, index) => (
              <div key={index} className="card">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">{stat.label}</p>
                    <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
                  </div>
                  <div className={`text-sm font-medium ${
                    stat.changeType === 'positive' ? 'text-green-600' : 'text-red-600'
                  }`}>
                    {stat.change}
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* Features Grid */}
          <div className="mb-8">
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">Quick Access</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {features.map((feature, index) => (
                <Link
                  key={index}
                  to={feature.path}
                  className="card hover:shadow-lg dark:hover:shadow-gray-900/30 transition-shadow duration-200 group"
                >
                  <div className="flex items-start space-x-4">
                    <div className={`${feature.color} text-white p-3 rounded-lg group-hover:scale-105 transition-transform duration-200`}>
                      {feature.icon}
                    </div>
                    <div className="flex-1">
                      <h3 className="text-lg font-semibold text-gray-900 dark:text-white group-hover:text-primary-600 dark:group-hover:text-primary-400 transition-colors duration-200">
                        {feature.title}
                      </h3>
                      <p className="text-gray-600 dark:text-gray-400 mt-2">{feature.description}</p>
                    </div>
                  </div>
                </Link>
              ))}
            </div>
          </div>

          {/* Recent Activity */}
          <div className="card">
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">Recent Activity</h2>
            <div className="space-y-4">
              {searchHistory.slice(0, 3).map((search) => (
                <div key={search.id} className="flex items-center space-x-4 p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                  <div className={`${getTypeColor(search.type)} p-2 rounded-lg`}>
                    {getTypeIcon(search.type)}
                  </div>
                  <div className="flex-1">
                    <p className="text-sm font-medium text-gray-900 dark:text-white">
                      {search.type} completed
                    </p>
                    <p className="text-sm text-gray-600 dark:text-gray-400">
                      {search.location} - {search.type === 'Price Estimator' ? `$${search.estimatedPrice?.toLocaleString()}` : 
                        search.type === 'Location Analyzer' ? `${search.safetyRating} rating` : 
                        `${search.dealScore} recommendation`}
                    </p>
                  </div>
                  <span className="text-sm text-gray-500 dark:text-gray-400">{formatDate(search.date)}</span>
                </div>
              ))}
            </div>
          </div>
        </>
      )}

      {/* Search History Tab */}
      {activeTab === 'history' && (
        <div className="space-y-6">
          <div className="flex justify-between items-center">
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Search History</h2>
            <button className="btn-secondary">
              Clear History
            </button>
          </div>
          
          <div className="card">
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
                <thead className="bg-gray-50 dark:bg-gray-700">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                      Type
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                      Location
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                      Details
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                      Date
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                      Status
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                  {searchHistory.map((search) => (
                    <tr key={search.id} className="hover:bg-gray-50 dark:hover:bg-gray-700">
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="flex items-center">
                          <div className={`${getTypeColor(search.type)} p-2 rounded-lg mr-3`}>
                            {getTypeIcon(search.type)}
                          </div>
                          <span className="text-sm font-medium text-gray-900 dark:text-white">{search.type}</span>
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                        {search.location}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600 dark:text-gray-400">
                        {search.type === 'Price Estimator' ? 
                          `${search.propertyType}, ${search.bedrooms}BR/${search.bathrooms}BA, ${search.area}sqft` :
                          search.type === 'Location Analyzer' ?
                          `${search.safetyRating} safety, ${search.nearbySchools} schools, ${search.transportOptions} transport` :
                          `$${search.propertyPrice?.toLocaleString()} vs $${search.marketValue?.toLocaleString()}`
                        }
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                        {formatDate(search.date)}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className="inline-flex px-2 py-1 text-xs font-semibold rounded-full bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200">
                          {search.status}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* Generated Reports Tab */}
      {activeTab === 'reports' && (
        <div className="space-y-6">
          <div className="flex justify-between items-center">
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Generated Reports</h2>
            <button className="btn-primary">
              Generate New Report
            </button>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {generatedReports.map((report) => (
              <div key={report.id} className="card">
                <div className="flex items-start justify-between mb-4">
                  <div className={`${getTypeColor(report.type)} p-2 rounded-lg`}>
                    {getTypeIcon(report.type)}
                  </div>
                  <span className="inline-flex px-2 py-1 text-xs font-semibold rounded-full bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200">
                    {report.status}
                  </span>
                </div>
                
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                  {report.title}
                </h3>
                
                <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
                  {report.summary}
                </p>
                
                <div className="flex items-center justify-between">
                  <span className="text-xs text-gray-500 dark:text-gray-400">
                    {formatDate(report.date)}
                  </span>
                  
                  <div className="flex space-x-2">
                    <button
                      onClick={() => exportToPDF(report.id)}
                      className="inline-flex items-center px-3 py-1 border border-gray-300 dark:border-gray-600 shadow-sm text-xs font-medium rounded text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700"
                    >
                      <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                      </svg>
                      Export PDF
                    </button>
                    
                    <button className="inline-flex items-center px-3 py-1 border border-gray-300 dark:border-gray-600 shadow-sm text-xs font-medium rounded text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700">
                      <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                      </svg>
                      View
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default Dashboard

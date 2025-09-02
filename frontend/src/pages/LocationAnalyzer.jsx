import React, { useState } from 'react'
import axios from 'axios'

const LocationAnalyzer = () => {
  const [location, setLocation] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [analysis, setAnalysis] = useState(null)
  const [error, setError] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!location.trim()) return

    setIsLoading(true)
    setError('')
    setAnalysis(null)

    try {
      // Call the dummy API endpoint
      const response = await axios.post('/api/location-analyzer', { location })
      
      setAnalysis({
        safetyRating: response.data.safetyRating || 'A+',
        nearbySchools: response.data.nearbySchools || [
          'Lincoln Elementary School (0.5 miles)',
          'Riverside Middle School (1.2 miles)',
          'Central High School (1.8 miles)',
          'St. Mary\'s Academy (2.1 miles)'
        ],
        transportAccess: response.data.transportAccess || [
          'Metro Station - 0.3 miles',
          'Bus Stop #15 - 0.1 miles',
          'Bus Stop #23 - 0.4 miles',
          'Train Station - 1.5 miles'
        ],
        summary: response.data.summary || {
          overallScore: 85,
          rating: 'Excellent',
          description: 'This location offers excellent amenities, good schools, and convenient transportation access.'
        }
      })
    } catch (err) {
      // Fallback to mock data if API fails
      console.log('API call failed, using mock data:', err.message)
      
      setAnalysis({
        safetyRating: 'A+',
        nearbySchools: [
          'Lincoln Elementary School (0.5 miles)',
          'Riverside Middle School (1.2 miles)',
          'Central High School (1.8 miles)',
          'St. Mary\'s Academy (2.1 miles)',
          'Oakwood Charter School (2.5 miles)'
        ],
        transportAccess: [
          'Metro Station - 0.3 miles',
          'Bus Stop #15 - 0.1 miles',
          'Bus Stop #23 - 0.4 miles',
          'Train Station - 1.5 miles',
          'Bike Path Access - 0.2 miles'
        ],
        summary: {
          overallScore: 85,
          rating: 'Excellent',
          description: 'This location offers excellent amenities, good schools, and convenient transportation access.'
        }
      })
    } finally {
      setIsLoading(false)
    }
  }

  const getRatingColor = (rating) => {
    if (rating === 'A+' || rating === 'A') return 'bg-green-100 text-green-800'
    if (rating === 'B+' || rating === 'B') return 'bg-blue-100 text-blue-800'
    if (rating === 'C+' || rating === 'C') return 'bg-yellow-100 text-yellow-800'
    return 'bg-red-100 text-red-800'
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Location Analyzer</h1>
        <p className="mt-2 text-gray-600">
          Analyze neighborhood safety, nearby schools, and transportation access for any location.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Form Section */}
        <div className="card">
          <h2 className="text-xl font-semibold text-gray-900 mb-6">Location Analysis</h2>
          
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label htmlFor="location" className="block text-sm font-medium text-gray-700">
                Enter Location/Address
              </label>
              <input
                type="text"
                id="location"
                value={location}
                onChange={(e) => setLocation(e.target.value)}
                className="input-field mt-1"
                placeholder="Enter city, state or specific address"
                required
              />
            </div>

            <button
              type="submit"
              disabled={isLoading || !location.trim()}
              className="btn-primary w-full flex justify-center items-center"
            >
              {isLoading ? (
                <>
                  <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Analyzing...
                </>
              ) : (
                'Analyze Location'
              )}
            </button>
          </form>
        </div>

        {/* Results Section */}
        <div className="space-y-6">
          {error && (
            <div className="card bg-red-50 border border-red-200">
              <div className="text-red-700">
                <h3 className="font-medium">Error</h3>
                <p className="mt-1">{error}</p>
              </div>
            </div>
          )}

          {analysis && (
            <>
              {/* Safety Rating */}
              <div className="card">
                <h2 className="text-xl font-semibold text-gray-900 mb-6">Safety Rating</h2>
                <div className="text-center">
                  <div className="text-6xl font-bold text-green-600 mb-2">
                    {analysis.safetyRating}
                  </div>
                  <div className={`inline-flex px-4 py-2 rounded-full text-lg font-medium ${getRatingColor(analysis.safetyRating)}`}>
                    Safe Neighborhood
                  </div>
                </div>
              </div>

              {/* Nearby Schools */}
              <div className="card">
                <h2 className="text-xl font-semibold text-gray-900 mb-6">Nearby Schools</h2>
                <div className="space-y-3">
                  {analysis.nearbySchools.map((school, index) => (
                    <div key={index} className="flex items-center p-3 bg-gray-50 rounded-lg">
                      <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center mr-3">
                        <svg className="w-4 h-4 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 14l9-5-9-5-9 5 9 5z" />
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 14l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z" />
                        </svg>
                      </div>
                      <span className="text-gray-900">{school}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Transport Access */}
              <div className="card">
                <h2 className="text-xl font-semibold text-gray-900 mb-6">Transport Access</h2>
                <div className="space-y-3">
                  {analysis.transportAccess.map((transport, index) => (
                    <div key={index} className="flex items-center p-3 bg-gray-50 rounded-lg">
                      <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center mr-3">
                        <svg className="w-4 h-4 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4" />
                        </svg>
                      </div>
                      <span className="text-gray-900">{transport}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Summary Card */}
              <div className="card">
                <h2 className="text-xl font-semibold text-gray-900 mb-6">Summary</h2>
                <div className="text-center mb-4">
                  <div className="text-3xl font-bold text-primary-600 mb-2">
                    {analysis.summary.overallScore}/100
                  </div>
                  <div className={`inline-flex px-3 py-1 rounded-full text-sm font-medium ${getRatingColor(analysis.summary.rating)}`}>
                    {analysis.summary.rating} Rating
                  </div>
                </div>
                <p className="text-gray-600 text-center">
                  {analysis.summary.description}
                </p>
              </div>
            </>
          )}

          {!analysis && !error && (
            <div className="card">
              <div className="text-center py-12">
                <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <svg className="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                  </svg>
                </div>
                <h3 className="text-lg font-medium text-gray-900 mb-2">Ready to analyze?</h3>
                <p className="text-gray-600">
                  Enter a location to get comprehensive neighborhood analysis including safety, schools, and transportation.
                </p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default LocationAnalyzer

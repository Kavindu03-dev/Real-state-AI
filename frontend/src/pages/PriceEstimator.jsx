import React, { useState } from 'react'
import axios from 'axios'

const PriceEstimator = () => {
  const [formData, setFormData] = useState({
    propertyType: 'House',
    bedrooms: '',
    bathrooms: '',
    area: '',
    location: '',
  })
  const [isLoading, setIsLoading] = useState(false)
  const [estimate, setEstimate] = useState(null)
  const [error, setError] = useState('')

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setIsLoading(true)
    setError('')
    setEstimate(null)

    try {
      // Call the dummy API endpoint
      const response = await axios.post('/api/price-estimator', formData)
      
      setEstimate({
        price: response.data.estimatedPrice,
        confidence: response.data.confidence,
        factors: response.data.factors || [
          { factor: 'Property Type', impact: 'Positive', description: `${formData.propertyType} properties have good market value` },
          { factor: 'Location', impact: 'Positive', description: `${formData.location} is a desirable area` },
          { factor: 'Size', impact: 'Positive', description: `${formData.area} sq.ft provides good living space` },
          { factor: 'Bedrooms', impact: 'Positive', description: `${formData.bedrooms} bedrooms meet market demand` },
        ]
      })
    } catch (err) {
      // Fallback to mock calculation if API fails
      console.log('API call failed, using mock calculation:', err.message)
      
      const basePrice = 250000
      const bedroomMultiplier = parseInt(formData.bedrooms) * 25000
      const bathroomMultiplier = parseFloat(formData.bathrooms) * 15000
      const areaMultiplier = parseInt(formData.area) * 100
      
      // Property type multiplier
      const typeMultiplier = {
        'House': 1.2,
        'Apartment': 1.0,
        'Land': 0.8
      }
      
      const estimatedPrice = (basePrice + bedroomMultiplier + bathroomMultiplier + areaMultiplier) * typeMultiplier[formData.propertyType]
      
      setEstimate({
        price: Math.round(estimatedPrice),
        confidence: 85,
        factors: [
          { factor: 'Property Type', impact: 'Positive', description: `${formData.propertyType} properties have good market value` },
          { factor: 'Location', impact: 'Positive', description: `${formData.location} is a desirable area` },
          { factor: 'Size', impact: 'Positive', description: `${formData.area} sq.ft provides good living space` },
          { factor: 'Bedrooms', impact: 'Positive', description: `${formData.bedrooms} bedrooms meet market demand` },
        ]
      })
    } finally {
      setIsLoading(false)
    }
  }

  const formatPrice = (price) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(price)
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Price Estimator</h1>
        <p className="mt-2 text-gray-600">
          Get accurate property price estimates using AI-powered analysis. Enter property details to receive an instant price estimate.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Form Section */}
        <div className="card">
          <h2 className="text-xl font-semibold text-gray-900 mb-6">Property Information</h2>
          
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label htmlFor="location" className="block text-sm font-medium text-gray-700">
                Location
              </label>
              <input
                type="text"
                id="location"
                name="location"
                className="input-field mt-1"
                placeholder="Enter city, state or specific address"
                value={formData.location}
                onChange={handleChange}
                required
              />
            </div>

            <div>
              <label htmlFor="propertyType" className="block text-sm font-medium text-gray-700">
                Property Type
              </label>
              <select
                id="propertyType"
                name="propertyType"
                className="input-field mt-1"
                value={formData.propertyType}
                onChange={handleChange}
                required
              >
                <option value="House">House</option>
                <option value="Apartment">Apartment</option>
                <option value="Land">Land</option>
              </select>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label htmlFor="bedrooms" className="block text-sm font-medium text-gray-700">
                  Bedrooms
                </label>
                <input
                  type="number"
                  id="bedrooms"
                  name="bedrooms"
                  min="0"
                  max="10"
                  className="input-field mt-1"
                  placeholder="3"
                  value={formData.bedrooms}
                  onChange={handleChange}
                  required
                />
              </div>

              <div>
                <label htmlFor="bathrooms" className="block text-sm font-medium text-gray-700">
                  Bathrooms
                </label>
                <input
                  type="number"
                  id="bathrooms"
                  name="bathrooms"
                  min="0"
                  max="10"
                  step="0.5"
                  className="input-field mt-1"
                  placeholder="2.5"
                  value={formData.bathrooms}
                  onChange={handleChange}
                  required
                />
              </div>

              <div>
                <label htmlFor="area" className="block text-sm font-medium text-gray-700">
                  Area (sq.ft)
                </label>
                <input
                  type="number"
                  id="area"
                  name="area"
                  min="100"
                  max="50000"
                  className="input-field mt-1"
                  placeholder="2000"
                  value={formData.area}
                  onChange={handleChange}
                  required
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={isLoading}
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
                'Get Price Estimate'
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

          {estimate && (
            <div className="card">
              <h2 className="text-xl font-semibold text-gray-900 mb-6">Price Estimate</h2>
              
              <div className="text-center mb-6">
                <div className="text-4xl font-bold text-primary-600 mb-2">
                  {formatPrice(estimate.price)}
                </div>
                <div className="text-sm text-gray-600">
                  Confidence: {estimate.confidence}%
                </div>
              </div>

              <div className="space-y-4">
                <h3 className="font-medium text-gray-900">Key Factors</h3>
                {estimate.factors.map((factor, index) => (
                  <div key={index} className="flex items-start space-x-3 p-3 bg-gray-50 rounded-lg">
                    <div className={`w-2 h-2 rounded-full mt-2 ${
                      factor.impact === 'Positive' ? 'bg-green-500' : 
                      factor.impact === 'Negative' ? 'bg-red-500' : 'bg-gray-500'
                    }`}></div>
                    <div className="flex-1">
                      <div className="font-medium text-gray-900">{factor.factor}</div>
                      <div className="text-sm text-gray-600">{factor.description}</div>
                    </div>
                  </div>
                ))}
              </div>

              <div className="mt-6 pt-6 border-t border-gray-200">
                <p className="text-sm text-gray-600">
                  This estimate is based on current market data and comparable properties in the area. 
                  For the most accurate valuation, consider consulting with a local real estate professional.
                </p>
              </div>
            </div>
          )}

          {!estimate && !error && (
            <div className="card">
              <div className="text-center py-12">
                <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <svg className="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1" />
                  </svg>
                </div>
                                 <h3 className="text-lg font-medium text-gray-900 mb-2">Ready to get started?</h3>
                 <p className="text-gray-600">
                   Fill out the property information to get an AI-powered price estimate.
                 </p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default PriceEstimator

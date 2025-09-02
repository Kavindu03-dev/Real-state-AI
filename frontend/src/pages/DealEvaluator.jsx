import React, { useState } from 'react'
import axios from 'axios'

const DealEvaluator = () => {
  const [formData, setFormData] = useState({
    propertyPrice: '',
    estimatedMarketValue: '',
    location: '',
  })
  const [isLoading, setIsLoading] = useState(false)
  const [evaluation, setEvaluation] = useState(null)
  const [error, setError] = useState('')

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!formData.propertyPrice || !formData.estimatedMarketValue || !formData.location) return

    setIsLoading(true)
    setError('')
    setEvaluation(null)

    try {
      // Call the dummy API endpoint
      const response = await axios.post('/api/deal-evaluator', formData)
      
      setEvaluation({
        dealScore: response.data.dealScore || 'Buy',
        confidenceLevel: response.data.confidenceLevel || 85,
        aiExplanation: response.data.aiExplanation || 'This appears to be a good investment opportunity based on the price-to-value ratio and market conditions.'
      })
    } catch (err) {
      // Fallback to mock calculation if API fails
      console.log('API call failed, using mock calculation:', err.message)
      
      const propertyPrice = parseFloat(formData.propertyPrice)
      const marketValue = parseFloat(formData.estimatedMarketValue)
      const priceRatio = propertyPrice / marketValue
      
      // Determine deal score based on price ratio
      let dealScore = 'Avoid'
      let confidenceLevel = 70
      let aiExplanation = ''
      
      if (priceRatio <= 0.85) {
        dealScore = 'Buy'
        confidenceLevel = 90
        aiExplanation = `This is an excellent buying opportunity. The property is priced at ${(priceRatio * 100).toFixed(1)}% of its estimated market value, representing a ${((1 - priceRatio) * 100).toFixed(1)}% discount. This suggests strong potential for appreciation and good value for your investment.`
      } else if (priceRatio <= 0.95) {
        dealScore = 'Buy'
        confidenceLevel = 80
        aiExplanation = `This is a good buying opportunity. The property is priced at ${(priceRatio * 100).toFixed(1)}% of its estimated market value, offering a reasonable discount. The location and market conditions support this investment decision.`
      } else if (priceRatio <= 1.05) {
        dealScore = 'Hold'
        confidenceLevel = 75
        aiExplanation = `This property is priced close to its estimated market value (${(priceRatio * 100).toFixed(1)}%). While not a bargain, it may be worth considering if you're looking for a stable investment in a good location. Monitor for price changes.`
      } else if (priceRatio <= 1.15) {
        dealScore = 'Hold'
        confidenceLevel = 70
        aiExplanation = `This property is priced above its estimated market value (${(priceRatio * 100).toFixed(1)}%). Consider waiting for a price reduction or negotiating better terms. The premium may be justified by unique features or location benefits.`
      } else {
        dealScore = 'Avoid'
        confidenceLevel = 85
        aiExplanation = `This property is significantly overpriced at ${(priceRatio * 100).toFixed(1)}% of its estimated market value. The ${((priceRatio - 1) * 100).toFixed(1)}% premium is too high for a sound investment. Consider other options or wait for price adjustments.`
      }
      
      setEvaluation({
        dealScore,
        confidenceLevel,
        aiExplanation
      })
    } finally {
      setIsLoading(false)
    }
  }

  const getDealScoreColor = (score) => {
    if (score === 'Buy') return 'text-green-600'
    if (score === 'Hold') return 'text-yellow-600'
    return 'text-red-600'
  }

  const getDealScoreBgColor = (score) => {
    if (score === 'Buy') return 'bg-green-100 text-green-800'
    if (score === 'Hold') return 'bg-yellow-100 text-yellow-800'
    return 'bg-red-100 text-red-800'
  }

  const getConfidenceColor = (level) => {
    if (level >= 85) return 'text-green-600'
    if (level >= 70) return 'text-blue-600'
    return 'text-yellow-600'
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Deal Evaluator</h1>
        <p className="mt-2 text-gray-600">
          Evaluate property deals by comparing asking price to estimated market value with AI-powered analysis.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Form Section */}
        <div className="card">
          <h2 className="text-xl font-semibold text-gray-900 mb-6">Deal Analysis</h2>
          
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label htmlFor="propertyPrice" className="block text-sm font-medium text-gray-700">
                Property Price
              </label>
              <input
                type="number"
                id="propertyPrice"
                name="propertyPrice"
                className="input-field mt-1"
                placeholder="Enter asking price"
                value={formData.propertyPrice}
                onChange={handleChange}
                required
              />
            </div>

            <div>
              <label htmlFor="estimatedMarketValue" className="block text-sm font-medium text-gray-700">
                Estimated Market Value
              </label>
              <input
                type="number"
                id="estimatedMarketValue"
                name="estimatedMarketValue"
                className="input-field mt-1"
                placeholder="Enter estimated market value"
                value={formData.estimatedMarketValue}
                onChange={handleChange}
                required
              />
            </div>

            <div>
              <label htmlFor="location" className="block text-sm font-medium text-gray-700">
                Location
              </label>
              <input
                type="text"
                id="location"
                name="location"
                className="input-field mt-1"
                placeholder="Enter city, state or address"
                value={formData.location}
                onChange={handleChange}
                required
              />
            </div>

            <button
              type="submit"
              disabled={isLoading || !formData.propertyPrice || !formData.estimatedMarketValue || !formData.location}
              className="btn-primary w-full flex justify-center items-center"
            >
              {isLoading ? (
                <>
                  <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Evaluating...
                </>
              ) : (
                'Evaluate Deal'
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

          {evaluation && (
            <>
              {/* Deal Score */}
              <div className="card">
                <h2 className="text-xl font-semibold text-gray-900 mb-6">Deal Score</h2>
                <div className="text-center">
                  <div className={`text-6xl font-bold mb-4 ${getDealScoreColor(evaluation.dealScore)}`}>
                    {evaluation.dealScore}
                  </div>
                  <div className={`inline-flex px-4 py-2 rounded-full text-lg font-medium ${getDealScoreBgColor(evaluation.dealScore)}`}>
                    {evaluation.dealScore === 'Buy' ? 'Recommended Purchase' : 
                     evaluation.dealScore === 'Hold' ? 'Consider Carefully' : 'Not Recommended'}
                  </div>
                </div>
              </div>

              {/* Confidence Level */}
              <div className="card">
                <h2 className="text-xl font-semibold text-gray-900 mb-6">Confidence Level</h2>
                <div className="text-center">
                  <div className={`text-4xl font-bold mb-2 ${getConfidenceColor(evaluation.confidenceLevel)}`}>
                    {evaluation.confidenceLevel}%
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-3">
                    <div 
                      className={`h-3 rounded-full ${
                        evaluation.confidenceLevel >= 85 ? 'bg-green-500' :
                        evaluation.confidenceLevel >= 70 ? 'bg-blue-500' : 'bg-yellow-500'
                      }`}
                      style={{ width: `${evaluation.confidenceLevel}%` }}
                    ></div>
                  </div>
                  <p className="text-sm text-gray-600 mt-2">
                    {evaluation.confidenceLevel >= 85 ? 'High Confidence' :
                     evaluation.confidenceLevel >= 70 ? 'Moderate Confidence' : 'Low Confidence'}
                  </p>
                </div>
              </div>

              {/* AI Explanation */}
              <div className="card">
                <h2 className="text-xl font-semibold text-gray-900 mb-6">AI Explanation</h2>
                <div className="bg-gray-50 p-4 rounded-lg">
                  <div className="flex items-start space-x-3">
                    <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center flex-shrink-0">
                      <svg className="w-4 h-4 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                      </svg>
                    </div>
                    <div className="flex-1">
                      <p className="text-gray-700 leading-relaxed">
                        {evaluation.aiExplanation}
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </>
          )}

          {!evaluation && !error && (
            <div className="card">
              <div className="text-center py-12">
                <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <svg className="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                  </svg>
                </div>
                <h3 className="text-lg font-medium text-gray-900 mb-2">Ready to evaluate?</h3>
                <p className="text-gray-600">
                  Enter the property price, estimated market value, and location to get an AI-powered deal analysis.
                </p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default DealEvaluator

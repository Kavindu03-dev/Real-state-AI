const express = require('express')
const cors = require('cors')

const app = express()
const PORT = 8000

// Middleware
app.use(cors())
app.use(express.json())

// Mock price estimator endpoint
app.post('/api/price-estimator', (req, res) => {
  const { propertyType, bedrooms, bathrooms, area, location } = req.body
  
  // Simulate processing delay
  setTimeout(() => {
    // Calculate estimated price based on inputs
    const basePrice = 250000
    const bedroomMultiplier = parseInt(bedrooms) * 25000
    const bathroomMultiplier = parseFloat(bathrooms) * 15000
    const areaMultiplier = parseInt(area) * 100
    
    // Property type multiplier
    const typeMultiplier = {
      'House': 1.2,
      'Apartment': 1.0,
      'Land': 0.8
    }
    
    const estimatedPrice = Math.round((basePrice + bedroomMultiplier + bathroomMultiplier + areaMultiplier) * typeMultiplier[propertyType])
    
    // Generate confidence score based on data completeness
    const confidence = Math.min(95, 70 + (bedrooms * 2) + (bathrooms * 3) + (area / 100))
    
    // Generate factors based on inputs
    const factors = [
      {
        factor: 'Property Type',
        impact: 'Positive',
        description: `${propertyType} properties have good market value in this area`
      },
      {
        factor: 'Location',
        impact: 'Positive',
        description: `${location} is a desirable location with good amenities`
      },
      {
        factor: 'Size',
        impact: 'Positive',
        description: `${area} sq.ft provides adequate living space for the market`
      },
      {
        factor: 'Bedrooms',
        impact: bedrooms >= 3 ? 'Positive' : 'Neutral',
        description: `${bedrooms} bedrooms ${bedrooms >= 3 ? 'meet strong market demand' : 'are adequate for the area'}`
      }
    ]
    
    res.json({
      estimatedPrice,
      confidence: Math.round(confidence),
      factors,
      message: 'Price estimate generated successfully'
    })
  }, 1500) // 1.5 second delay to simulate processing
})

// Mock location analyzer endpoint
app.post('/api/location-analyzer', (req, res) => {
  const { location } = req.body
  
  // Simulate processing delay
  setTimeout(() => {
    // Generate safety rating based on location
    const safetyRatings = ['A+', 'A', 'B+', 'B', 'C+']
    const safetyRating = safetyRatings[Math.floor(Math.random() * safetyRatings.length)]
    
    // Generate nearby schools
    const nearbySchools = [
      'Lincoln Elementary School (0.5 miles)',
      'Riverside Middle School (1.2 miles)',
      'Central High School (1.8 miles)',
      'St. Mary\'s Academy (2.1 miles)',
      'Oakwood Charter School (2.5 miles)',
      'Maple Elementary School (1.0 miles)',
      'Valley Middle School (1.5 miles)',
      'Riverside High School (2.0 miles)'
    ]
    
    // Generate transport access
    const transportAccess = [
      'Metro Station - 0.3 miles',
      'Bus Stop #15 - 0.1 miles',
      'Bus Stop #23 - 0.4 miles',
      'Train Station - 1.5 miles',
      'Bike Path Access - 0.2 miles',
      'Express Bus Route - 0.6 miles',
      'Park & Ride - 2.0 miles',
      'Light Rail Station - 1.8 miles'
    ]
    
    // Generate summary
    const summaries = [
      {
        overallScore: 85,
        rating: 'Excellent',
        description: 'This location offers excellent amenities, good schools, and convenient transportation access.'
      },
      {
        overallScore: 78,
        rating: 'Good',
        description: 'A solid neighborhood with good schools and decent transportation options.'
      },
      {
        overallScore: 92,
        rating: 'Excellent',
        description: 'Premium location with top-rated schools and excellent transport connectivity.'
      }
    ]
    
    const summary = summaries[Math.floor(Math.random() * summaries.length)]
    
    res.json({
      safetyRating,
      nearbySchools: nearbySchools.slice(0, 5), // Return 5 schools
      transportAccess: transportAccess.slice(0, 5), // Return 5 transport options
      summary,
      message: 'Location analysis completed successfully'
    })
  }, 2000) // 2 second delay to simulate processing
})

// Mock deal evaluator endpoint
app.post('/api/deal-evaluator', (req, res) => {
  const { propertyPrice, estimatedMarketValue, location } = req.body
  
  // Simulate processing delay
  setTimeout(() => {
    const priceRatio = propertyPrice / estimatedMarketValue
    
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
    
    res.json({
      dealScore,
      confidenceLevel,
      aiExplanation,
      message: 'Deal evaluation completed successfully'
    })
  }, 1800) // 1.8 second delay to simulate processing
})

// Mock dashboard endpoints
app.get('/api/dashboard/search-history', (req, res) => {
  // Simulate processing delay
  setTimeout(() => {
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
    
    res.json({
      searchHistory: mockSearchHistory,
      message: 'Search history retrieved successfully'
    })
  }, 500)
})

app.get('/api/dashboard/generated-reports', (req, res) => {
  // Simulate processing delay
  setTimeout(() => {
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
    
    res.json({
      generatedReports: mockGeneratedReports,
      message: 'Generated reports retrieved successfully'
    })
  }, 500)
})

app.post('/api/reports/:reportId/export-pdf', (req, res) => {
  const { reportId } = req.params
  
  // Simulate PDF generation delay
  setTimeout(() => {
    res.json({
      success: true,
      downloadUrl: `/api/reports/${reportId}/download-pdf`,
      message: 'PDF report generated successfully'
    })
  }, 2000)
})

// Health check endpoint
app.get('/api/health', (req, res) => {
  res.json({ status: 'OK', message: 'Mock API server is running' })
})

app.listen(PORT, () => {
  console.log(`Mock API server running on http://localhost:${PORT}`)
  console.log(`Price estimator endpoint: POST http://localhost:${PORT}/api/price-estimator`)
})

# Price Estimator Feature

## Overview
The Price Estimator page provides a comprehensive form for property price estimation with AI-powered analysis.

## Form Fields

### Required Fields:
1. **Location** (text input)
   - Enter city, state, or specific address
   - Used for market analysis and location-based pricing

2. **Property Type** (dropdown)
   - House
   - Apartment  
   - Land
   - Each type has different pricing multipliers

3. **Bedrooms** (number input)
   - Range: 0-10
   - Affects base price calculation

4. **Bathrooms** (number input)
   - Range: 0-10 (supports decimals like 2.5)
   - Influences property value

5. **Area** (number input)
   - Range: 100-50,000 sq.ft
   - Square footage multiplier for price calculation

## API Integration

### Endpoint: `/api/price-estimator`
- **Method**: POST
- **Content-Type**: application/json

### Request Body:
```json
{
  "propertyType": "House",
  "bedrooms": 3,
  "bathrooms": 2.5,
  "area": 2000,
  "location": "New York, NY"
}
```

### Response:
```json
{
  "estimatedPrice": 450000,
  "confidence": 85,
  "factors": [
    {
      "factor": "Property Type",
      "impact": "Positive",
      "description": "House properties have good market value in this area"
    },
    {
      "factor": "Location", 
      "impact": "Positive",
      "description": "New York, NY is a desirable location with good amenities"
    }
  ],
  "message": "Price estimate generated successfully"
}
```

## Price Calculation Logic

### Base Formula:
```
Estimated Price = (Base Price + Bedroom Multiplier + Bathroom Multiplier + Area Multiplier) × Property Type Multiplier
```

### Multipliers:
- **Base Price**: $250,000
- **Bedroom Multiplier**: $25,000 per bedroom
- **Bathroom Multiplier**: $15,000 per bathroom
- **Area Multiplier**: $100 per sq.ft
- **Property Type Multipliers**:
  - House: 1.2x
  - Apartment: 1.0x
  - Land: 0.8x

### Confidence Score:
- Based on data completeness and market factors
- Range: 70-95%
- Higher scores for more complete data

## Features

### ✅ Form Validation
- All fields are required
- Number inputs have appropriate ranges
- Real-time validation feedback

### ✅ Loading States
- Shows loading spinner during API calls
- Disables form during processing

### ✅ Error Handling
- Graceful fallback to mock calculation if API fails
- User-friendly error messages

### ✅ Responsive Design
- Works on desktop, tablet, and mobile
- Clean, professional UI with Tailwind CSS

### ✅ Results Display
- Large, prominent price display
- Confidence score indicator
- Detailed factor analysis
- Color-coded impact indicators

## Testing

### Mock API Server
Run the mock API server for testing:
```bash
npm run mock-api
```

This starts a server on `http://localhost:8000` with the `/api/price-estimator` endpoint.

### Frontend Development
Start the React development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

## Example Usage

1. Navigate to the Price Estimator page
2. Fill out the form:
   - Location: "San Francisco, CA"
   - Property Type: "House"
   - Bedrooms: 4
   - Bathrooms: 3
   - Area: 2500
3. Click "Get Price Estimate"
4. View the estimated price and analysis

## Integration Notes

- The frontend is configured to proxy API calls to `http://localhost:8000`
- Update the proxy configuration in `vite.config.js` if needed
- The component includes fallback logic for when the API is unavailable
- All calculations are performed server-side for security and consistency

# Deal Evaluator Feature

## Overview
The Deal Evaluator page provides AI-powered analysis of property deals by comparing asking prices to estimated market values, helping investors make informed decisions.

## Form Fields

### Required Fields:
1. **Property Price** (number input)
   - Enter the asking price of the property
   - Used for comparison against market value

2. **Estimated Market Value** (number input)
   - Enter the estimated market value of the property
   - Used as the benchmark for deal evaluation

3. **Location** (text input)
   - Enter city, state, or specific address
   - Used for market context and analysis

## API Integration

### Endpoint: `/api/deal-evaluator`
- **Method**: POST
- **Content-Type**: application/json

### Request Body:
```json
{
  "propertyPrice": 350000,
  "estimatedMarketValue": 400000,
  "location": "San Francisco, CA"
}
```

### Response:
```json
{
  "dealScore": "Buy",
  "confidenceLevel": 90,
  "aiExplanation": "This is an excellent buying opportunity. The property is priced at 87.5% of its estimated market value, representing a 12.5% discount. This suggests strong potential for appreciation and good value for your investment.",
  "message": "Deal evaluation completed successfully"
}
```

## Display Sections

### 1. Deal Score
- **Display**: Large text (Buy / Hold / Avoid)
- **Color Coding**: 
  - Buy: Green (Recommended Purchase)
  - Hold: Yellow (Consider Carefully)
  - Avoid: Red (Not Recommended)
- **Badge**: Descriptive text based on score

### 2. Confidence Level
- **Display**: Percentage with progress bar
- **Range**: 0-100%
- **Color Coding**:
  - 85%+: Green (High Confidence)
  - 70-84%: Blue (Moderate Confidence)
  - <70%: Yellow (Low Confidence)
- **Progress Bar**: Visual representation of confidence

### 3. AI Explanation
- **Format**: Detailed text explanation
- **Icon**: Lightbulb icon for AI insights
- **Background**: Light gray with rounded corners
- **Content**: Contextual analysis based on price ratio

## Deal Score Logic

### Price Ratio Calculation:
```
Price Ratio = Property Price / Estimated Market Value
```

### Scoring System:
- **Buy** (≤85%): Excellent discount, strong buying opportunity
- **Buy** (85-95%): Good discount, reasonable buying opportunity
- **Hold** (95-105%): Fair price, close to market value
- **Hold** (105-115%): Slightly overpriced, consider negotiating
- **Avoid** (>115%): Significantly overpriced, not recommended

### Confidence Levels:
- **90%**: Excellent deals with clear value
- **80%**: Good deals with reasonable value
- **75%**: Fair deals requiring consideration
- **70%**: Marginal deals needing caution
- **85%**: Clear avoidance recommendations

## Features

### ✅ Form Validation
- All fields are required
- Number inputs for prices
- Real-time validation feedback
- Prevents empty submissions

### ✅ Loading States
- Shows loading spinner during API calls
- Disables form during processing
- "Evaluating..." text during processing

### ✅ Error Handling
- Graceful fallback to mock calculation if API fails
- User-friendly error messages
- Console logging for debugging

### ✅ Responsive Design
- Works on desktop, tablet, and mobile
- Clean, professional UI with Tailwind CSS
- Card-based layout for easy scanning

### ✅ Visual Indicators
- Color-coded deal scores
- Progress bar for confidence level
- AI explanation with icon
- Professional typography and spacing

## Testing

### Mock API Server
The mock API server includes the deal evaluator endpoint:
```bash
npm run mock-api
```

This starts a server on `http://localhost:8000` with the `/api/deal-evaluator` endpoint.

### Frontend Development
Start the React development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

## Example Usage

1. Navigate to the Deal Evaluator page
2. Fill out the form:
   - Property Price: $350,000
   - Estimated Market Value: $400,000
   - Location: "San Francisco, CA"
3. Click "Evaluate Deal"
4. View the results:
   - Deal Score: Buy
   - Confidence Level: 90%
   - AI Explanation: Detailed analysis

## Data Structure

### Deal Score
- **Type**: String
- **Values**: Buy, Hold, Avoid
- **Logic**: Based on price ratio analysis

### Confidence Level
- **Type**: Number
- **Range**: 0-100
- **Logic**: Based on deal quality and market conditions

### AI Explanation
- **Type**: String
- **Content**: Detailed analysis with specific percentages
- **Logic**: Contextual explanation based on price ratio

## Price Ratio Analysis

### Buy Recommendations:
- **≤85%**: Excellent discount (12.5%+ below market)
- **85-95%**: Good discount (5-15% below market)

### Hold Recommendations:
- **95-105%**: Fair price (within 5% of market value)
- **105-115%**: Slightly overpriced (5-15% above market)

### Avoid Recommendations:
- **>115%**: Significantly overpriced (15%+ above market)

## Integration Notes

- The frontend is configured to proxy API calls to `http://localhost:8000`
- Update the proxy configuration in `vite.config.js` if needed
- The component includes fallback logic for when the API is unavailable
- All calculations are performed server-side for consistency
- Price ratio analysis ensures consistent evaluation criteria

## Future Enhancements

- Market trend integration
- Comparable property analysis
- Investment timeline recommendations
- Risk assessment factors
- Market condition analysis
- Historical price data integration
- Neighborhood appreciation rates
- Investment strategy suggestions

# Location Analyzer Feature

## Overview
The Location Analyzer page provides comprehensive neighborhood analysis including safety ratings, nearby schools, and transportation access for any location.

## Form Fields

### Required Fields:
1. **Location/Address** (text input)
   - Enter city, state, or specific address
   - Used for neighborhood analysis and data retrieval

## API Integration

### Endpoint: `/api/location-analyzer`
- **Method**: POST
- **Content-Type**: application/json

### Request Body:
```json
{
  "location": "San Francisco, CA"
}
```

### Response:
```json
{
  "safetyRating": "A+",
  "nearbySchools": [
    "Lincoln Elementary School (0.5 miles)",
    "Riverside Middle School (1.2 miles)",
    "Central High School (1.8 miles)",
    "St. Mary's Academy (2.1 miles)",
    "Oakwood Charter School (2.5 miles)"
  ],
  "transportAccess": [
    "Metro Station - 0.3 miles",
    "Bus Stop #15 - 0.1 miles",
    "Bus Stop #23 - 0.4 miles",
    "Train Station - 1.5 miles",
    "Bike Path Access - 0.2 miles"
  ],
  "summary": {
    "overallScore": 85,
    "rating": "Excellent",
    "description": "This location offers excellent amenities, good schools, and convenient transportation access."
  },
  "message": "Location analysis completed successfully"
}
```

## Display Sections

### 1. Safety Rating
- **Display**: Large letter grade (A+, A, B+, B, C+)
- **Color Coding**: 
  - A+/A: Green (Safe)
  - B+/B: Blue (Good)
  - C+/C: Yellow (Fair)
  - D/F: Red (Poor)
- **Badge**: "Safe Neighborhood" indicator

### 2. Nearby Schools
- **Format**: School name with distance
- **Icon**: Graduation cap icon
- **Background**: Light blue with rounded corners
- **Example**: "Lincoln Elementary School (0.5 miles)"

### 3. Transport Access
- **Format**: Transport type with distance
- **Icon**: Arrow icon
- **Background**: Light green with rounded corners
- **Examples**: 
  - "Metro Station - 0.3 miles"
  - "Bus Stop #15 - 0.1 miles"
  - "Train Station - 1.5 miles"

### 4. Summary Card
- **Overall Score**: Numerical score out of 100
- **Rating**: Text rating (Excellent, Good, Fair, Poor)
- **Description**: Detailed neighborhood summary
- **Color Coding**: Matches safety rating colors

## Features

### ✅ Form Validation
- Location field is required
- Real-time validation feedback
- Prevents empty submissions

### ✅ Loading States
- Shows loading spinner during API calls
- Disables form during processing
- "Analyzing..." text during processing

### ✅ Error Handling
- Graceful fallback to mock data if API fails
- User-friendly error messages
- Console logging for debugging

### ✅ Responsive Design
- Works on desktop, tablet, and mobile
- Clean, professional UI with Tailwind CSS
- Card-based layout for easy scanning

### ✅ Visual Indicators
- Color-coded safety ratings
- Icons for schools and transport
- Rating badges with appropriate colors
- Professional typography and spacing

## Testing

### Mock API Server
The mock API server includes the location analyzer endpoint:
```bash
npm run mock-api
```

This starts a server on `http://localhost:8000` with the `/api/location-analyzer` endpoint.

### Frontend Development
Start the React development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

## Example Usage

1. Navigate to the Location Analyzer page
2. Enter a location: "San Francisco, CA"
3. Click "Analyze Location"
4. View the results:
   - Safety Rating: A+
   - Nearby Schools list
   - Transport Access list
   - Summary with overall score

## Data Structure

### Safety Rating
- **Type**: String
- **Values**: A+, A, B+, B, C+, C, D, F
- **Logic**: Random selection from predefined ratings

### Nearby Schools
- **Type**: Array of strings
- **Format**: "School Name (distance miles)"
- **Count**: 5 schools per analysis
- **Logic**: Random selection from predefined list

### Transport Access
- **Type**: Array of strings
- **Format**: "Transport Type - distance miles"
- **Count**: 5 transport options per analysis
- **Logic**: Random selection from predefined list

### Summary
- **Type**: Object
- **Properties**:
  - `overallScore`: Number (0-100)
  - `rating`: String (Excellent, Good, Fair, Poor)
  - `description`: String (detailed summary)

## Integration Notes

- The frontend is configured to proxy API calls to `http://localhost:8000`
- Update the proxy configuration in `vite.config.js` if needed
- The component includes fallback logic for when the API is unavailable
- All analysis data is generated server-side for consistency
- Random data generation ensures varied results for testing

## Future Enhancements

- Real school data integration
- Actual crime statistics
- Public transport API integration
- Map visualization
- User reviews and ratings
- Historical data trends

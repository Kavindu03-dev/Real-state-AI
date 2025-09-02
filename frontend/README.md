# Real Estate AI Frontend

A modern React frontend for the Real Estate AI application, built with Vite and Tailwind CSS.

## Features

- **Authentication System**: Login and registration forms with demo functionality
- **Price Estimator**: AI-powered property price estimation with detailed analysis
- **Location Analyzer**: Comprehensive neighborhood and market analysis
- **Deal Evaluator**: Investment opportunity evaluation with ROI calculations
- **Responsive Design**: Mobile-first design that works on all devices
- **Modern UI**: Clean, professional interface with Tailwind CSS

## Tech Stack

- **React 18**: Modern React with hooks and functional components
- **Vite**: Fast build tool and development server
- **Tailwind CSS**: Utility-first CSS framework
- **React Router**: Client-side routing
- **Axios**: HTTP client for API calls

## Getting Started

### Prerequisites

- Node.js (version 16 or higher)
- npm or yarn

### Installation

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

4. Open your browser and visit `http://localhost:3000`

### Build for Production

```bash
npm run build
```

The built files will be in the `dist` directory.

## Project Structure

```
frontend/
├── public/                 # Static assets
├── src/
│   ├── components/         # Reusable React components
│   │   └── Navigation.jsx  # Main navigation component
│   ├── pages/              # Page components
│   │   ├── Dashboard.jsx   # Main dashboard
│   │   ├── Login.jsx       # Login page
│   │   ├── Register.jsx    # Registration page
│   │   ├── PriceEstimator.jsx
│   │   ├── LocationAnalyzer.jsx
│   │   └── DealEvaluator.jsx
│   ├── App.jsx             # Main app component with routing
│   ├── main.jsx           # React entry point
│   └── index.css          # Global styles with Tailwind
├── package.json           # Dependencies and scripts
├── vite.config.js         # Vite configuration
├── tailwind.config.js     # Tailwind CSS configuration
└── postcss.config.js      # PostCSS configuration
```

## Features Overview

### Authentication
- Login and registration forms
- Form validation and error handling
- Demo authentication (no backend required)
- Protected routes

### Price Estimator
- Property details input form
- AI-powered price estimation
- Confidence scoring
- Key factors analysis
- Market comparison data

### Location Analyzer
- Location-based analysis
- Neighborhood scoring
- Market trends
- School ratings and crime data
- Recent sales comparison

### Deal Evaluator
- Investment property analysis
- Cash flow calculations
- ROI metrics (Cash-on-Cash, Cap Rate)
- Expense breakdown
- Investment recommendations

## API Integration

The frontend is configured to proxy API calls to the backend server running on port 8000. Update the proxy configuration in `vite.config.js` if your backend runs on a different port.

## Customization

### Styling
- Modify `tailwind.config.js` to customize the design system
- Update color schemes in the configuration
- Add custom components in `src/index.css`

### Components
- All components are modular and reusable
- Follow the existing patterns for consistency
- Use the provided CSS classes for styling

## Development

### Available Scripts

- `npm run dev`: Start development server
- `npm run build`: Build for production
- `npm run preview`: Preview production build
- `npm run lint`: Run ESLint

### Code Style

- Use functional components with hooks
- Follow React best practices
- Use Tailwind CSS for styling
- Keep components small and focused

## Demo Credentials

For testing purposes, you can use any email and password combination. The authentication is currently mocked for demonstration.

## Contributing

1. Follow the existing code structure
2. Use meaningful component and variable names
3. Add proper error handling
4. Test on different screen sizes
5. Update documentation as needed

## License

This project is part of the Real Estate AI application.

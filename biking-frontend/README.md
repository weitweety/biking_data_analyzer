# Biking Data Analyzer Frontend

A React + Vite frontend application for visualizing biking trip data.

## Features

- Trip duration statistics visualization using Recharts
- Real-time data fetching from the backend API
- Responsive design

## Prerequisites

- Node.js (v18 or higher)
- npm or yarn

## Installation

1. Install dependencies:
```bash
npm install
```

## Development

Start the development server:
```bash
npm run dev
```

The application will be available at `http://localhost:3000`

## Configuration

The API URL can be configured via environment variables. Create a `.env` file:

```
VITE_API_URL=http://localhost:8000
```

## Build

Build for production:
```bash
npm run build
```

The built files will be in the `dist` directory.

## Project Structure

```
biking-frontend/
├── src/
│   ├── components/
│   │   └── TripDurationChart.jsx
│   ├── api/
│   │   └── client.js
│   ├── App.jsx
│   ├── App.css
│   ├── main.jsx
│   └── index.css
├── index.html
├── package.json
├── vite.config.js
└── README.md
```


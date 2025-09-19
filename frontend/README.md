# Customer Calls Manager - Frontend

A modern React TypeScript frontend for the Customer Calls API, built with Vite and styled with Tailwind CSS.

## Features

- **Add Call Records**: Create new customer call records with sentiment analysis and AI insights
- **Search Calls**: Search and view call records by phone number
- **Modern UI**: Clean, responsive design with Tailwind CSS
- **TypeScript**: Full type safety with TypeScript
- **Real-time Feedback**: Loading states, error handling, and success messages

## Tech Stack

- **React 18** with TypeScript
- **Vite** for fast development and building
- **Tailwind CSS** for styling
- **Axios** for API communication
- **Lucide React** for icons

## Getting Started

### Prerequisites

- Node.js 16+ and npm
- Backend API running on `http://localhost:8000`

### Installation

1. Install dependencies:

```bash
npm install
```

2. Start the development server:

```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

### Building for Production

```bash
npm run build
```

The built files will be in the `dist` directory.

## API Integration

The frontend communicates with the FastAPI backend through the following endpoints:

- `POST /get_calls` - Retrieve calls by phone number
- `POST /save_call` - Save a new call record
- `GET /` - Health check

## Project Structure

```
src/
├── components/          # React components
│   ├── CallCard.tsx    # Individual call record display
│   ├── CallForm.tsx    # Form for adding new calls
│   ├── CallList.tsx    # Search and list calls
│   └── Header.tsx      # Navigation header
├── services/           # API service layer
│   └── api.ts         # Axios configuration and API calls
├── types/             # TypeScript type definitions
│   └── api.ts         # API response types
├── App.tsx            # Main application component
└── index.css          # Global styles with Tailwind
```

## Usage

1. **Adding a Call Record**:

   - Click on "Add Call" tab
   - Fill in the phone number, transcript, sentiment score, insights, and resolution status
   - Click "Save Call Record"

2. **Searching Calls**:
   - Click on "Search Calls" tab
   - Enter a phone number to search for existing call records
   - View detailed call information including sentiment analysis and AI insights

## Development

The project uses Vite for fast development with hot module replacement. The development server includes a proxy to the backend API running on port 8000.

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## Styling

The project uses Tailwind CSS for styling with a custom color palette:

- Primary colors: Blue theme (`primary-50` to `primary-900`)
- Semantic colors: Green for success, red for errors, yellow for warnings
- Responsive design with mobile-first approach

## Error Handling

The application includes comprehensive error handling:

- API connection errors
- Form validation errors
- Network timeout handling
- User-friendly error messages

## Contributing

1. Follow TypeScript best practices
2. Use Tailwind CSS for styling
3. Maintain component reusability
4. Add proper error handling
5. Include loading states for async operations

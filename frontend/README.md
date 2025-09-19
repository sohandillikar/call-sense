# AI Business Assistant - Frontend

A modern React frontend for the AI Business Assistant application, built with Vite, TypeScript, and Tailwind CSS.

## Features

- **Dashboard**: Overview of business metrics and quick actions
- **Call Analysis**: Transcribe and analyze customer calls
- **Review Monitoring**: Scrape and analyze customer reviews
- **Competitor Tracking**: Monitor competitor activities and alerts
- **Analytics**: Comprehensive business analytics with charts
- **AI Insights**: AI-powered business recommendations

## Tech Stack

- **React 19** - Modern React with hooks
- **TypeScript** - Type-safe development
- **Vite** - Fast build tool and dev server
- **Tailwind CSS** - Utility-first CSS framework
- **React Router** - Client-side routing
- **Axios** - HTTP client for API calls
- **Recharts** - Data visualization
- **Lucide React** - Beautiful icons

## Getting Started

### Prerequisites

- Node.js 18+
- npm or yarn
- Backend API running on http://localhost:8000

### Installation

1. Install dependencies:

```bash
npm install
```

2. Copy environment file:

```bash
cp env.example .env
```

3. Update `.env` with your configuration:

```env
VITE_API_URL=http://localhost:8000
VITE_APP_NAME=AI Business Assistant
VITE_APP_VERSION=1.0.0
```

4. Start the development server:

```bash
npm run dev
```

The application will be available at http://localhost:5173

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## Project Structure

```
src/
├── components/          # Reusable UI components
│   └── Layout.tsx      # Main layout with navigation
├── pages/              # Page components
│   ├── Dashboard.tsx   # Main dashboard
│   ├── Calls.tsx       # Call analysis page
│   ├── Reviews.tsx     # Review monitoring page
│   ├── Competitors.tsx # Competitor tracking page
│   ├── Analytics.tsx   # Analytics dashboard
│   └── Insights.tsx    # AI insights page
├── services/           # API services
│   └── api.ts         # API client and types
├── App.tsx            # Main app component
├── main.tsx           # App entry point
└── index.css          # Global styles
```

## API Integration

The frontend communicates with the backend API through the `services/api.ts` file. All API calls are centralized and include:

- Error handling
- Request/response logging
- TypeScript types
- Axios interceptors

## Styling

The application uses Tailwind CSS for styling with a custom design system:

- **Primary Colors**: Blue palette for main actions
- **Secondary Colors**: Gray palette for neutral elements
- **Components**: Reusable button, card, and input styles
- **Responsive**: Mobile-first responsive design

## Development

### Adding New Pages

1. Create a new component in `src/pages/`
2. Add the route to `src/App.tsx`
3. Add navigation item to `src/components/Layout.tsx`

### Adding New API Endpoints

1. Add the endpoint function to `src/services/api.ts`
2. Add TypeScript types for request/response
3. Use the function in your components

### Styling Guidelines

- Use Tailwind utility classes
- Follow the established color palette
- Use the predefined component classes (`.btn`, `.card`, `.input`)
- Maintain consistent spacing and typography

## Production Build

To build for production:

```bash
npm run build
```

The built files will be in the `dist/` directory.

## Contributing

1. Follow the existing code style
2. Use TypeScript for all new code
3. Add proper error handling
4. Test your changes thoroughly
5. Update documentation as needed

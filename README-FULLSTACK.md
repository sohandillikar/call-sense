# AI Business Assistant - Full-Stack Application

A comprehensive AI-powered business assistant with both backend API and modern React frontend.

## 🏗️ Architecture

### Backend (FastAPI + Python)

- **FastAPI** - Modern, fast web framework for building APIs
- **PostgreSQL** - Primary database for business data
- **Redis** - Vector search and caching
- **TigerData** - Time-series analytics database
- **Docker** - Containerized deployment

### Frontend (React + TypeScript)

- **React 19** - Modern React with hooks
- **TypeScript** - Type-safe development
- **Vite** - Fast build tool and dev server
- **Tailwind CSS** - Utility-first CSS framework
- **React Router** - Client-side routing
- **Recharts** - Data visualization

## 🚀 Quick Start

### Option 1: Full-Stack Script (Recommended)

```bash
# Start both backend and frontend
./start-fullstack.sh
```

### Option 2: Manual Setup

#### Backend

```bash
# Start backend services
docker compose up -d

# Check health
curl http://localhost:8000/health
```

#### Frontend

```bash
# Install dependencies
cd frontend
npm install

# Start development server
npm run dev
```

## 📱 Application URLs

- **Frontend UI**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 🎯 Features

### Dashboard

- Real-time business metrics
- Quick action buttons
- System status overview
- Recent activity feed

### Call Analysis

- Upload audio files for transcription
- Manual call transcription
- Sentiment analysis
- Action item extraction
- Priority scoring
- Similar call suggestions

### Review Monitoring

- Scrape company reviews from multiple platforms
- Competitor review analysis
- Sentiment analysis and theme extraction
- Platform distribution charts

### Competitor Tracking

- Monitor competitor activities
- Price change alerts
- Alert management system
- Competitor analysis insights

### Analytics Dashboard

- Interactive charts and graphs
- Sentiment trend analysis
- Call volume tracking
- Review platform distribution
- Business recommendations

### AI Insights

- AI-powered business recommendations
- Customer satisfaction analysis
- Market trend insights
- Operational efficiency suggestions

## 🛠️ Development

### Backend Development

```bash
# View logs
docker compose logs app

# Access database
docker compose exec postgres psql -U postgres -d ai_business_assistant

# Run migrations
docker compose exec app alembic upgrade head
```

### Frontend Development

```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## 🔧 Configuration

### Backend Environment Variables

Copy `env.example` to `.env` and configure:

```env
# Database Configuration
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/ai_business_assistant
TIGERDATA_SERVICE_URL=your_tigerdata_url

# Redis Configuration
REDIS_URL=redis://redis:6379

# API Keys
GLADIA_API_KEY=your_gladia_key
OPENAI_API_KEY=your_openai_key
BRIGHT_DATA_API_KEY=your_bright_data_key

# Application Settings
DEBUG=True
SECRET_KEY=your-secret-key
```

### Frontend Environment Variables

Copy `frontend/env.example` to `frontend/.env`:

```env
VITE_API_URL=http://localhost:8000
VITE_APP_NAME=AI Business Assistant
VITE_APP_VERSION=1.0.0
```

## 📊 API Endpoints

### Health & Status

- `GET /health` - Health check
- `GET /` - API information

### Call Analysis

- `GET /api/v1/calls/` - List all calls
- `POST /api/v1/calls/transcribe` - Transcribe call text
- `POST /api/v1/calls/upload` - Upload and transcribe audio

### Review Monitoring

- `GET /api/v1/reviews/company` - Get company reviews
- `GET /api/v1/reviews/competitor` - Get competitor reviews
- `POST /api/v1/reviews/scrape-company` - Scrape company reviews
- `POST /api/v1/reviews/scrape-competitor` - Scrape competitor reviews

### Competitor Tracking

- `GET /api/v1/competitors/alerts` - Get competitor alerts
- `PATCH /api/v1/competitors/alerts/{id}/read` - Mark alert as read
- `POST /api/v1/competitors/monitor` - Start monitoring competitor

### Analytics

- `GET /api/v1/analytics/trends/overview` - Get analytics overview
- `GET /api/v1/analytics/metrics/summary` - Get metrics summary
- `GET /api/v1/analytics/widgets` - Get dashboard widgets

### AI Insights

- `GET /api/v1/insights/` - Get business insights
- `POST /api/v1/insights/generate` - Generate new insights

## 🧪 Testing

### Backend API Testing

```bash
# Health check
curl http://localhost:8000/health

# Get calls
curl http://localhost:8000/api/v1/calls/

# Get analytics overview
curl http://localhost:8000/api/v1/analytics/trends/overview
```

### Frontend Testing

Open http://localhost:5173 in your browser and test the UI components.

## 🐳 Docker Commands

```bash
# Start all services
docker compose up -d

# View logs
docker compose logs -f

# Stop services
docker compose down

# Rebuild and start
docker compose up -d --build

# Access app container
docker compose exec app bash

# Access database
docker compose exec postgres psql -U postgres -d ai_business_assistant
```

## 📁 Project Structure

```
ai-agents-hackathon/
├── app/                    # Backend FastAPI application
│   ├── api/               # API routes and endpoints
│   ├── core/              # Core configuration and database
│   ├── models/            # SQLAlchemy models
│   └── services/          # Business logic services
├── frontend/              # React frontend application
│   ├── src/
│   │   ├── components/    # Reusable UI components
│   │   ├── pages/         # Page components
│   │   ├── services/      # API client
│   │   └── App.tsx        # Main app component
│   └── package.json
├── scripts/               # Utility scripts
├── docker-compose.yml     # Docker services configuration
├── Dockerfile            # Backend container definition
└── start-fullstack.sh    # Full-stack startup script
```

## 🔒 Security

- Environment variables for sensitive data
- API key management
- CORS configuration
- Input validation and sanitization
- SQL injection prevention
- XSS protection

## 🚀 Deployment

### Production Build

```bash
# Build frontend
cd frontend
npm run build

# Start production backend
docker compose -f docker-compose.prod.yml up -d
```

### Environment Setup

1. Configure production environment variables
2. Set up SSL certificates
3. Configure reverse proxy (nginx)
4. Set up monitoring and logging

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions:

- Check the API documentation at http://localhost:8000/docs
- Review the frontend README in `frontend/README.md`
- Check Docker logs for backend issues
- Review browser console for frontend issues

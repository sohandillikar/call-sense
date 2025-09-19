# AI Business Assistant

An all-in-one AI business assistant that acts as a virtual employee handling multiple business functions for small businesses.

## Features

- **Gladia Integration**: Transcribes customer calls and voicemails into actionable insights
- **Redis Vector Search**: Finds similar past issues and solutions instantly
- **Bright Data MCP**: Monitors competitor pricing, competitor reviews, AND your own company's reviews
- **TigerData**: Stores and analyzes time-series data (competitor pricing trends, review sentiment over time)

## Quick Start (Docker)

### Prerequisites

- Docker and Docker Compose installed
- API keys for Gladia, Bright Data, and TigerData

### One-Command Setup

```bash
# Clone the repository
git clone <repository-url>
cd ai-agents-hackathon

# Run the setup script (creates .env, builds, and starts everything)
./scripts/setup.sh
```

**That's it!** The application will be available at `http://localhost:8000`

### Manual Setup

1. **Clone and setup environment**:

```bash
git clone <repository-url>
cd ai-agents-hackathon
cp env.example .env
# Edit .env with your API keys
```

2. **Start all services**:

```bash
docker compose up -d
```

3. **Access the application**:

- API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

## API Keys Setup

You'll need API keys from these services:

### Required API Keys:

1. **Gladia** (Call Transcription) - https://gladia.io/
2. **Bright Data** (Web Scraping) - https://brightdata.com/
3. **TigerData** (Time-Series Analytics) - https://tigerdata.com/

### Optional API Keys:

- **OpenAI** (AI Analysis) - https://openai.com/

### Setting API Keys:

Edit the `.env` file created by setup:

```bash
# Edit the .env file
nano .env

# Add your API keys:
GLADIA_API_KEY=your_actual_key_here
BRIGHT_DATA_API_KEY=your_actual_key_here
TIGERDATA_API_KEY=your_actual_key_here
OPENAI_API_KEY=your_actual_key_here
```

## Development Commands

Use the helper script for common tasks:

```bash
# Start services
./scripts/dev.sh start

# Stop services
./scripts/dev.sh stop

# View logs
./scripts/dev.sh logs

# Access app shell
./scripts/dev.sh shell

# Run database migrations
./scripts/dev.sh migrate

# Create new migration
./scripts/dev.sh migrate-new "Add new field"

# Start management tools (pgAdmin, Redis Commander)
./scripts/dev.sh tools

# Check service status
./scripts/dev.sh status
```

## Management Tools

Start optional management tools:

```bash
./scripts/dev.sh tools
```

Access:

- **pgAdmin** (Database): http://localhost:5050 (admin@ai-business-assistant.com / admin)
- **Redis Commander** (Cache): http://localhost:8081

## API Endpoints

### Calls

- `POST /api/v1/calls/transcribe` - Transcribe audio from URL
- `POST /api/v1/calls/upload` - Upload and transcribe audio file
- `GET /api/v1/calls/{call_id}` - Get call details
- `GET /api/v1/calls/` - List all calls

### Reviews

- `POST /api/v1/reviews/scrape-company` - Scrape company reviews
- `POST /api/v1/reviews/scrape-competitor` - Scrape competitor reviews
- `POST /api/v1/reviews/analyze-competitive` - Analyze competitive position
- `GET /api/v1/reviews/company/{company_name}` - Get company reviews

### Competitors

- `POST /api/v1/competitors/add` - Add competitor to monitor
- `POST /api/v1/competitors/scrape-pricing` - Scrape competitor pricing
- `GET /api/v1/competitors/` - List competitors
- `GET /api/v1/competitors/pricing/{competitor_name}` - Get competitor pricing

### Insights

- `POST /api/v1/insights/vector-search` - Perform vector search
- `POST /api/v1/insights/store-issue-solution` - Store issue-solution pair
- `GET /api/v1/insights/similar-issues/{query_text}` - Find similar issues

### Analytics

- `GET /api/v1/analytics/sentiment-trends/{company_name}` - Get sentiment trends
- `GET /api/v1/analytics/pricing-trends/{competitor_name}` - Get pricing trends
- `POST /api/v1/analytics/create-dashboard` - Create analytics dashboard

## Testing the API

### Quick API Test:

```bash
# Test health endpoint
curl http://localhost:8000/health

# Test API documentation
open http://localhost:8000/docs
```

### Example API Calls:

**1. Transcribe a call:**

```bash
curl -X POST "http://localhost:8000/api/v1/calls/transcribe" \
  -H "Content-Type: application/json" \
  -d '{
    "audio_url": "https://example.com/audio.wav",
    "language": "en",
    "customer_phone": "+1234567890",
    "call_type": "incoming"
  }'
```

**2. Scrape company reviews:**

```bash
curl -X POST "http://localhost:8000/api/v1/reviews/scrape-company" \
  -H "Content-Type: application/json" \
  -d '{
    "business_name": "Your Company",
    "location": "Your City",
    "platforms": ["google", "yelp"]
  }'
```

**3. Add a competitor:**

```bash
curl -X POST "http://localhost:8000/api/v1/competitors/add" \
  -H "Content-Type: application/json" \
  -d '{
    "competitor_name": "Competitor Inc",
    "website_url": "https://competitor.com",
    "industry": "Technology",
    "market_position": "competitive"
  }'
```

## Troubleshooting

### Common Issues:

**1. Port already in use:**

```bash
./scripts/dev.sh stop
```

**2. Database connection issues:**

```bash
./scripts/dev.sh restart
```

**3. API key issues:**

```bash
# Check environment variables
docker compose exec app env | grep API_KEY

# Restart after adding keys
./scripts/dev.sh restart
```

**4. Permission issues:**

```bash
chmod +x scripts/*.sh
```

## Tech Stack

### Backend Framework

- **FastAPI** - Modern, fast web framework for building APIs
- **Uvicorn** - ASGI server for running FastAPI applications
- **Pydantic** - Data validation and settings management

### Database & Storage

- **PostgreSQL** - Primary relational database for structured data
- **Redis** - In-memory data store for vector search and caching
- **SQLAlchemy** - Python ORM for database operations
- **Alembic** - Database migration tool

### AI & Machine Learning

- **Sentence Transformers** - For generating text embeddings
- **scikit-learn** - Machine learning utilities
- **NumPy & Pandas** - Data processing and analysis

### External APIs

- **Gladia** - Call transcription and voicemail processing
- **Bright Data** - Web scraping for competitor monitoring
- **TigerData** - Time-series data storage and analytics
- **OpenAI** - AI analysis and insights (optional)

### Infrastructure

- **Docker & Docker Compose** - Containerization and orchestration
- **pgAdmin** - Database management interface
- **Redis Commander** - Redis management interface

### Development Tools

- **Alembic** - Database migrations
- **httpx** - Async HTTP client for API calls
- **python-multipart** - File upload handling

## Code Structure

```
app/
├── __init__.py           # Package initialization
├── main.py              # FastAPI application entry point
├── api/                 # API layer
│   ├── __init__.py
│   ├── routes.py        # Main API router
│   └── endpoints/       # Individual endpoint modules
│       ├── __init__.py
│       ├── calls.py     # Call transcription endpoints
│       ├── reviews.py   # Review monitoring endpoints
│       ├── competitors.py # Competitor analysis endpoints
│       ├── insights.py  # Business insights endpoints
│       └── analytics.py # Analytics and trends endpoints
├── core/                # Core functionality
│   ├── __init__.py
│   ├── config.py        # Application configuration
│   ├── database.py      # Database setup and session management
│   └── redis_client.py  # Redis client for vector search
├── models/              # Database models (SQLAlchemy)
│   ├── __init__.py
│   ├── customer_call.py # Call and voicemail models
│   ├── review.py        # Review models
│   ├── competitor_data.py # Competitor monitoring models
│   └── business_insight.py # Business insights models
└── services/            # Business logic services
    ├── __init__.py
    ├── gladia_client.py      # Call transcription service
    ├── bright_data_client.py # Web scraping service
    ├── tigerdata_client.py   # Time-series analytics service
    └── vector_search.py      # Vector similarity search service
```

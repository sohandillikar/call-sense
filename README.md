# Customer Calls Manager

A full-stack application for managing customer call records with AI-powered sentiment analysis and insights. Built with FastAPI (Python) backend and React TypeScript frontend.

## 🚀 Features

- **Call Management**: Add and search customer call records
- **Sentiment Analysis**: Track customer sentiment with numerical scores
- **AI Insights**: Generate and store AI-powered insights from call transcripts
- **Modern UI**: Clean, responsive interface built with React and Tailwind CSS
- **Real-time Feedback**: Loading states, error handling, and success notifications
- **Type Safety**: Full TypeScript support for both frontend and backend

## 🏗️ Architecture

```
├── backend/           # FastAPI Python backend
│   ├── server.py     # Main API server
│   ├── requirements.txt
│   └── credentials/  # Database credentials
├── frontend/         # React TypeScript frontend
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── services/    # API service layer
│   │   ├── types/       # TypeScript definitions
│   │   └── App.tsx      # Main app component
│   ├── package.json
│   └── vite.config.ts
└── start-dev.sh      # Development startup script
```

## 🛠️ Tech Stack

### Backend

- **FastAPI** - Modern Python web framework
- **PostgreSQL** - Database (via TimescaleDB)
- **Pydantic** - Data validation and serialization
- **psycopg2** - PostgreSQL adapter

### Frontend

- **React 18** with TypeScript
- **Vite** - Fast build tool and dev server
- **Tailwind CSS** - Utility-first CSS framework
- **Axios** - HTTP client
- **Lucide React** - Icon library

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- PostgreSQL database (TimescaleDB)

### 1. Clone and Setup

```bash
git clone <repository-url>
cd ai-agents-hackathon
```

### 2. Backend Setup

```bash
cd backend
pip install -r requirements.txt
```

Configure your database credentials in `backend/credentials/tiger-cloud-db-89754-credentials.env`

### 3. Frontend Setup

```bash
cd frontend
npm install
```

### 4. Start Development Servers

**Option A: Use the startup script (recommended)**

```bash
./start-dev.sh
```

**Option B: Start manually**

```bash
# Terminal 1 - Backend
cd backend
python server.py

# Terminal 2 - Frontend
cd frontend
npm run dev
```

### 5. Access the Application

- **Frontend UI**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 📖 API Endpoints

### POST /get_calls

Retrieve all call records for a specific phone number.

**Request:**

```json
{
  "phone": "+1234567890"
}
```

**Response:**

```json
{
  "calls": [
    {
      "id": 1,
      "created_at": "2024-01-15T10:30:00Z",
      "phone": "+1234567890",
      "transcript": "Customer called about billing issue...",
      "sentiments": -0.8,
      "insights": "Customer is experiencing billing problems...",
      "solved": false
    }
  ]
}
```

### POST /save_call

Save a new call record.

**Request:**

```json
{
  "phone": "+1234567890",
  "transcript": "Customer called about billing issue...",
  "sentiment": -0.8,
  "insight": "Customer is experiencing billing problems...",
  "solved": false
}
```

**Response:**

```json
{
  "success": true,
  "call_id": 1,
  "message": "Call saved successfully"
}
```

## 🎨 Frontend Features

### Add Call Record

- Form validation with real-time feedback
- Sentiment score slider (-1 to 1)
- AI insights text area
- Resolution status toggle
- Success/error notifications

### Search Calls

- Search by phone number
- Display call history with sentiment analysis
- Visual indicators for solved/unsolved issues
- Responsive card layout

### UI Components

- **CallCard**: Displays individual call records
- **CallForm**: Form for adding new calls
- **CallList**: Search and display call history
- **Header**: Navigation and branding

## 🗄️ Database Schema

The application uses a `customer_calls` table with the following structure:

```sql
CREATE TABLE customer_calls (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    phone TEXT NOT NULL,
    transcript TEXT NOT NULL,
    sentiment DECIMAL(5,2),
    insight TEXT NOT NULL,
    solved BOOLEAN DEFAULT FALSE
);
```

## 🔧 Development

### Backend Development

```bash
cd backend
python server.py
```

The backend runs on port 8000 with auto-reload enabled.

### Frontend Development

```bash
cd frontend
npm run dev
```

The frontend runs on port 3000 with hot module replacement.

### Building for Production

**Frontend:**

```bash
cd frontend
npm run build
```

**Backend:**
The backend is ready for production deployment with any WSGI/ASGI server.

## 🧪 Testing

### Backend API Testing

```bash
cd backend
python -c "
import requests
response = requests.post('http://localhost:8000/get_calls', json={'phone': '+1234567890'})
print(response.json())
"
```

### Frontend Testing

```bash
cd frontend
npm run build  # Test build process
```

## 📝 Environment Variables

### Backend

Create `backend/credentials/tiger-cloud-db-89754-credentials.env`:

```
TIMESCALE_SERVICE_URL=postgresql://user:password@host:port/database
```

### Frontend

The frontend is configured to connect to `http://localhost:8000` by default. Update `src/services/api.ts` to change the API base URL.

## 🚀 Deployment

### Backend Deployment

1. Set up PostgreSQL database
2. Configure environment variables
3. Deploy with any ASGI server (e.g., Gunicorn + Uvicorn)

### Frontend Deployment

1. Build the frontend: `npm run build`
2. Serve the `dist` folder with any static file server
3. Update API base URL for production

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Troubleshooting

### Common Issues

**Backend won't start:**

- Check database connection credentials
- Ensure PostgreSQL is running
- Verify all dependencies are installed

**Frontend build fails:**

- Clear node_modules and reinstall: `rm -rf node_modules && npm install`
- Check Node.js version (16+ required)

**API connection errors:**

- Verify backend is running on port 8000
- Check CORS settings if needed
- Ensure API base URL is correct

### Getting Help

1. Check the logs for error messages
2. Verify all prerequisites are installed
3. Ensure ports 3000 and 8000 are available
4. Check database connectivity

---

**Happy coding! 🎉**

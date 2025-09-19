# Customer Calls API

A FastAPI server for managing customer call records in TigerData database.

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Start the server:

```bash
python server.py
```

The server will run on `http://localhost:8000`

## API Endpoints

### 1. POST /get_calls

Get all calls for a specific phone number.

**Request Body:**

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
      "insights": "Customer is experiencing billing problems..."
    }
  ]
}
```

### 2. POST /save_call

Save a new call record.

**Request Body:**

```json
{
  "phone": "+1234567890",
  "transcript": "Customer called about billing issue. Very frustrated with the service.",
  "sentiment": -0.8,
  "insight": "Customer is experiencing billing problems and is highly dissatisfied"
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

## Testing

Run the test script to verify the API:

```bash
python test_api.py
```

## Database Schema

The API works with the `customer_calls` table:

- `id` (SERIAL PRIMARY KEY)
- `created_at` (TIMESTAMP WITH TIME ZONE)
- `phone` (TEXT)
- `transcript` (TEXT)
- `sentiments` (DECIMAL(5,2))
- `insights` (TEXT)

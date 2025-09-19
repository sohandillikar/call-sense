from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
import os
from dotenv import load_dotenv
from typing import List, Optional
from datetime import datetime

load_dotenv('./credentials/tiger-cloud-db-89754-credentials.env')

app = FastAPI(title="Customer Calls API", version="1.0.0")

class GetCallsRequest(BaseModel):
    phone: str

class CallRecord(BaseModel):
    id: int
    created_at: datetime
    phone: str
    transcript: str
    sentiments: Optional[float]
    insights: str
    solved: bool

class GetCallsResponse(BaseModel):
    calls: List[CallRecord]

class SaveCallRequest(BaseModel):
    phone: str
    transcript: str
    sentiment: float
    insight: str
    solved: bool

class SaveCallResponse(BaseModel):
    success: bool
    call_id: int
    message: str

def get_db_connection():
    """Get database connection using environment variables"""
    service_url = os.environ.get('TIMESCALE_SERVICE_URL')
    if not service_url:
        raise HTTPException(status_code=500, detail="Database connection string not found")
    
    try:
        conn = psycopg2.connect(service_url)
        return conn
    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")

@app.get("/")
async def root():
    return {"message": "Customer Calls API is running"}

@app.post("/get_calls", response_model=GetCallsResponse)
async def get_calls(request: GetCallsRequest):
    """
    Get all calls for a specific phone number
    """
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Query to get calls by phone number
        query = """
        SELECT id, created_at, phone, transcript, sentiment, insight, solved
        FROM customer_calls 
        WHERE phone = %s
        ORDER BY created_at DESC
        """
        
        cursor.execute(query, (request.phone,))
        rows = cursor.fetchall()
        
        calls = []
        for row in rows:
            call = CallRecord(
                id=row[0],
                created_at=row[1],
                phone=row[2],
                transcript=row[3],
                sentiments=float(row[4]) if row[4] is not None else None,
                insights=row[5],
                solved=row[6]
            )
            calls.append(call)
        
        return GetCallsResponse(calls=calls)
        
    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        if conn:
            conn.close()

@app.post("/save_call", response_model=SaveCallResponse)
async def save_call(request: SaveCallRequest):
    """
    Save a new call record
    """
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Insert new call record
        insert_query = """
        INSERT INTO customer_calls (phone, transcript, sentiment, insight, solved)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id
        """
        
        cursor.execute(insert_query, (
            request.phone,
            request.transcript,
            request.sentiment,
            request.insight,
            request.solved
        ))
        
        call_id = cursor.fetchone()[0]
        conn.commit()
        
        return SaveCallResponse(
            success=True,
            call_id=call_id,
            message="Call saved successfully"
        )
        
    except psycopg2.Error as e:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

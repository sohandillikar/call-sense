"""
API endpoints for call transcription and analysis
"""
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from pydantic import BaseModel
from datetime import datetime

from app.core.database import get_db
from app.services.gladia_client import gladia_client, call_analysis_service
from app.services.vector_search import vector_search_service
from app.services.tigerdata_client import time_series_analysis_service
from app.models.customer_call import CustomerCall, CallInsight

router = APIRouter()


async def _process_call_transcription(transcription_text: str, customer_phone: str, call_type: str, db: Session):
    """Helper function to process call transcription and generate insights"""
    # Analyze sentiment
    sentiment_analysis = await call_analysis_service.analyze_call_sentiment(transcription_text)
    
    # Extract key topics
    key_topics = await call_analysis_service.extract_key_topics(transcription_text)
    
    # Generate action items
    action_items = await call_analysis_service.generate_action_items(transcription_text, sentiment_analysis)
    
    # Calculate priority score
    priority_score = await call_analysis_service.calculate_priority_score(sentiment_analysis, action_items)
    
    # Find similar calls using vector search
    similar_calls = await vector_search_service.find_similar_calls(transcription_text, limit=3)
    
    # Store call data in database
    import uuid
    call_id = str(uuid.uuid4())
    
    call_record = CustomerCall(
        call_id=call_id,
        customer_phone=customer_phone,
        call_type=call_type,
        transcription=transcription_text,
        sentiment_score=sentiment_analysis["sentiment_score"],
        sentiment_label=sentiment_analysis["sentiment_label"],
        key_topics=key_topics,
        action_items=action_items,
        priority_score=priority_score
    )
    
    db.add(call_record)
    db.commit()
    
    # Store call insights in vector search
    call_metadata = {
        "call_id": call_id,
        "customer_phone": customer_phone,
        "call_type": call_type,
        "created_at": datetime.now().isoformat()
    }
    
    call_insights = {
        "sentiment_analysis": sentiment_analysis,
        "key_topics": key_topics,
        "action_items": action_items,
        "priority_score": priority_score
    }
    
    await vector_search_service.store_call_insight(
        transcription_text, call_insights, call_metadata
    )
    
    # Store in time-series data
    await time_series_analysis_service.store_customer_satisfaction_trends([{
        "created_at": datetime.now().isoformat(),
        "sentiment_score": sentiment_analysis["sentiment_score"],
        "call_type": call_type,
        "priority_score": priority_score
    }])
    
    return CallTranscriptionResponse(
        call_id=call_id,
        transcription=transcription_text,
        sentiment_analysis=sentiment_analysis,
        key_topics=key_topics,
        action_items=action_items,
        priority_score=priority_score,
        similar_calls=similar_calls
    )


class CallTranscriptionRequest(BaseModel):
    audio_url: str
    language: str = "en"
    customer_phone: str = ""
    call_type: str = "incoming"


class CallTranscriptionResponse(BaseModel):
    call_id: str
    transcription: str
    sentiment_analysis: Dict[str, Any]
    key_topics: List[str]
    action_items: List[Dict[str, Any]]
    priority_score: float
    similar_calls: List[Dict[str, Any]]


class CallInsightRequest(BaseModel):
    call_id: str
    insight_type: str
    insight_text: str
    confidence_score: float
    suggested_actions: List[str]


@router.post("/transcribe", response_model=CallTranscriptionResponse)
async def transcribe_call(
    request: CallTranscriptionRequest,
    db: Session = Depends(get_db)
):
    """Transcribe a call and generate insights"""
    try:
        # Transcribe audio using Gladia
        transcription_result = await gladia_client.transcribe_audio(
            request.audio_url, request.language
        )
        
        if "error" in transcription_result:
            raise HTTPException(status_code=400, detail=f"Transcription failed: {transcription_result['error']}")
        
        # Extract transcription text
        transcription_text = gladia_client.extract_transcription_text(transcription_result)
        
        if not transcription_text:
            raise HTTPException(status_code=400, detail="No transcription text found")
        
        # Process transcription using helper function
        return await _process_call_transcription(
            transcription_text, request.customer_phone, request.call_type, db
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/upload", response_model=CallTranscriptionResponse)
async def upload_and_transcribe_call(
    file: UploadFile = File(...),
    customer_phone: str = "",
    call_type: str = "incoming",
    language: str = "en",
    db: Session = Depends(get_db)
):
    """Upload and transcribe an audio file"""
    try:
        # Save uploaded file temporarily
        import tempfile
        import os
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        try:
            # Transcribe file using Gladia
            transcription_result = await gladia_client.transcribe_file(
                temp_file_path, language
            )
            
            if "error" in transcription_result:
                raise HTTPException(status_code=400, detail=f"Transcription failed: {transcription_result['error']}")
            
            # Extract transcription text
            transcription_text = gladia_client.extract_transcription_text(transcription_result)
            
            if not transcription_text:
                raise HTTPException(status_code=400, detail="No transcription text found")
            
            # Process transcription using helper function
            return await _process_call_transcription(
                transcription_text, customer_phone, call_type, db
            )
            
        finally:
            # Clean up temporary file
            os.unlink(temp_file_path)
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{call_id}")
async def get_call_details(call_id: str, db: Session = Depends(get_db)):
    """Get details of a specific call"""
    try:
        call = db.query(CustomerCall).filter(CustomerCall.call_id == call_id).first()
        
        if not call:
            raise HTTPException(status_code=404, detail="Call not found")
        
        return {
            "call_id": call.call_id,
            "customer_phone": call.customer_phone,
            "call_type": call.call_type,
            "transcription": call.transcription,
            "sentiment_score": call.sentiment_score,
            "sentiment_label": call.sentiment_label,
            "key_topics": call.key_topics,
            "action_items": call.action_items,
            "priority_score": call.priority_score,
            "created_at": call.created_at
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/")
async def list_calls(
    skip: int = 0,
    limit: int = 100,
    call_type: str = None,
    db: Session = Depends(get_db)
):
    """List all calls with optional filtering"""
    try:
        query = db.query(CustomerCall)
        
        if call_type:
            query = query.filter(CustomerCall.call_type == call_type)
        
        calls = query.offset(skip).limit(limit).all()
        
        return [
            {
                "call_id": call.call_id,
                "customer_phone": call.customer_phone,
                "call_type": call.call_type,
                "sentiment_score": call.sentiment_score,
                "sentiment_label": call.sentiment_label,
                "priority_score": call.priority_score,
                "created_at": call.created_at
            }
            for call in calls
        ]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/insights")
async def create_call_insight(
    request: CallInsightRequest,
    db: Session = Depends(get_db)
):
    """Create a new call insight"""
    try:
        insight = CallInsight(
            call_id=request.call_id,
            insight_type=request.insight_type,
            insight_text=request.insight_text,
            confidence_score=request.confidence_score,
            suggested_actions=request.suggested_actions
        )
        
        db.add(insight)
        db.commit()
        
        return {"message": "Call insight created successfully", "insight_id": insight.id}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/insights/{call_id}")
async def get_call_insights(call_id: str, db: Session = Depends(get_db)):
    """Get insights for a specific call"""
    try:
        insights = db.query(CallInsight).filter(CallInsight.call_id == call_id).all()
        
        return [
            {
                "id": insight.id,
                "insight_type": insight.insight_type,
                "insight_text": insight.insight_text,
                "confidence_score": insight.confidence_score,
                "suggested_actions": insight.suggested_actions,
                "created_at": insight.created_at
            }
            for insight in insights
        ]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# app.py
from flask import Flask, render_template, request, jsonify, redirect, url_for
import os
from datetime import datetime
from dotenv import load_dotenv

# Import our custom modules
from src.models.strategy_engine import StrategyEngine
from src.api.gladia_client import GladiaClient
from src.data.database import store_customer_call, get_recent_calls

load_dotenv()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize our AI components
strategy_engine = StrategyEngine()
gladia_client = GladiaClient()

@app.route('/')
def index():
    """Main dashboard page"""
    dashboard_data = strategy_engine.get_business_dashboard()
    return render_template('dashboard.html', data=dashboard_data)

@app.route('/analyze-call', methods=['GET', 'POST'])
def analyze_call():
    """Analyze customer call page"""
    if request.method == 'POST':
        # Handle audio file upload
        if 'audio_file' in request.files:
            audio_file = request.files['audio_file']
            if audio_file.filename:
                # Save uploaded file
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], audio_file.filename)
                audio_file.save(file_path)
                
                try:
                    # Transcribe with Gladia
                    transcription_result = gladia_client.transcribe_audio(file_path)
                    transcription = transcription_result['transcription']
                    
                    # Extract issues
                    issues = gladia_client.extract_customer_issue(transcription)
                    
                    # Analyze with strategy engine
                    analysis = strategy_engine.analyze_customer_issue(
                        ', '.join(issues), transcription
                    )
                    
                    # Store in database
                    store_customer_call(transcription, issues, analysis['priority_level'])
                    
                    return render_template('call_analysis.html', 
                                         transcription=transcription,
                                         analysis=analysis)
                except Exception as e:
                    return render_template('call_analysis.html', error=str(e))
        
        # Handle text input
        elif request.form.get('issue_text'):
            issue_text = request.form['issue_text']
            analysis = strategy_engine.analyze_customer_issue(issue_text)
            return render_template('call_analysis.html', 
                                 transcription=issue_text,
                                 analysis=analysis)
    
    return render_template('call_analysis.html')

@app.route('/api/competitor-analysis')
def api_competitor_analysis():
    """API endpoint for competitor analysis"""
    competitor_data = strategy_engine.bright_data.scrape_competitor_pricing()
    return jsonify(competitor_data)

@app.route('/api/similar-situations/<issue>')
def api_similar_situations(issue):
    """API endpoint for finding similar situations"""
    similar = strategy_engine.business_intelligence.find_similar_situations(issue)
    return jsonify(similar)

if __name__ == '__main__':
    print("🚀 Starting SmartBiz Intelligence Agent...")
    print("📊 Dashboard: http://localhost:5000")
    print("🎤 Call Analysis: http://localhost:5000/analyze-call")
    app.run(debug=True)
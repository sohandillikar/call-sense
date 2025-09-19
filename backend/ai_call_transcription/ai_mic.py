

from flask import Flask, request, Response, session
from twilio.twiml.voice_response import VoiceResponse, Gather
from openai import OpenAI
from elevenlabs import ElevenLabs
import pymongo
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import csv
import os
import uuid
import json
import requests
from datetime import datetime
import re

# ---------------- CONFIG ----------------

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY",)
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY",)

client = OpenAI(api_key=OPENAI_API_KEY)
eleven_client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

CSV_FILE = "/Users/savirdillikar/aws-hack/call_insights.csv"
app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this to a secure secret key

# Global storage for call sessions
call_sessions = {}
server_url = "http://0.0.0.0:2133/save_call"  # Change to your server URL

class TicketSearchBot:
    def __init__(self, db_name="tickets"):
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.collection = self.client[db_name]["tickets"]
        self.escalations_collection = self.client[db_name]["escalations"]
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.similarity_threshold = 0.8
        self.max_troubleshoot_rounds = 5  # Changed to 5 rounds
    
    def add_ticket(self, problem, solution):
        """Add a ticket with its vector"""
        vector = self.model.encode(problem).tolist()
        ticket = {
            "problem": problem,
            "solution": solution,
            "vector": vector,
            "created_at": datetime.now()
        }
        return self.collection.insert_one(ticket).inserted_id
    
    def find_similar(self, problem, limit=5):
        """Find similar tickets"""
        query_vector = self.model.encode(problem)
        tickets = list(self.collection.find())
        
        if not tickets:
            print("🔍 No tickets found in database")
            return []
        
        print(f"🔍 Searching through {len(tickets)} tickets in database...")
        print(f"🔍 Query: '{problem}'")
        print(f"🔍 Query vector shape: {query_vector.shape}")
        
        results = []
        for i, ticket in enumerate(tickets):
            if 'vector' not in ticket:
                print(f"⚠️ Ticket {i} missing vector, skipping")
                continue
                
            similarity = cosine_similarity(
                [query_vector], 
                [ticket['vector']]
            )[0][0]
            
            results.append({
                "problem": ticket["problem"],
                "solution": ticket["solution"],
                "score": round(similarity, 3),
                "_id": str(ticket.get("_id", ""))
            })
        
        results.sort(key=lambda x: x['score'], reverse=True)
        
        print(f"🔍 Found {len(results)} results, returning top {limit}")
        return results[:limit]
    
    def escalate_ticket(self, problem, conversation_history):
        """Escalate unresolved ticket to developers"""
        escalation = {
            "problem": problem,
            "conversation_history": conversation_history,
            "escalated_at": datetime.now(),
            "status": "pending"
        }
        return self.escalations_collection.insert_one(escalation).inserted_id

# Initialize the bot
ticket_bot = TicketSearchBot()

# ---------------- HELPER FUNCTIONS ----------------
def get_session_id():
    """Get or create session ID from Twilio call"""
    call_sid = request.form.get('CallSid')
    return call_sid or str(uuid.uuid4())

def get_call_session(session_id):
    """Get call session data"""
    if session_id not in call_sessions:
        call_sessions[session_id] = {
            'transcripts': [],
            'troubleshoot_rounds': 0,
            'initial_problem': '',
            'similarity_results': [],
            'state': 'initial',  # initial, troubleshooting, escalated, resolved
            'phone_number': '',
            'problem_resolved': False
        }
    return call_sessions[session_id]

def get_phone_number_from_request():
    """Extract phone number from Twilio request"""
    return request.form.get('From', 'Unknown')

def analyze_problem_severity(problem_text, conversation_history):
    """Analyze problem severity using AI (1-10 scale)"""
    try:
        severity_prompt = f"""
        Analyze the severity of this technical problem on a scale of 1-10 (where 10 is extremely severe/critical):
        
        Problem: {problem_text}
        Conversation context: {' '.join(conversation_history[-5:]) if conversation_history else 'None'}
        
        Consider:
        - Impact on user's ability to use the service
        - Urgency of resolution needed
        - Business criticality
        - User frustration level
        
        Respond with only a single integer from 1 to 10.
        """
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": severity_prompt}],
            temperature=0.1,
            max_tokens=10
        )
        
        severity_text = response.choices[0].message.content.strip()
        # Extract integer from response
        severity_match = re.search(r'\b([1-9]|10)\b', severity_text)
        severity = int(severity_match.group(1)) if severity_match else 5
        
        print(f"🎯 Problem severity analysis: {severity}/10")
        return max(1, min(10, severity))  # Ensure it's between 1-10
        
    except Exception as e:
        print(f"Error analyzing severity: {e}")
        return 5  # Default to medium severity

def check_problem_resolved(user_response):
    """Check if user indicates problem is resolved"""
    positive_indicators = [
        'fixed', 'solved', 'resolved', "working",
        'great', 'excellent', 'perfect', 'thank you', 'thanks',
        'yes it works', 'yes that worked', 'problem solved', 'all good',
        'thats it', 'that did it', 'successful'
    ]
    
    user_lower = user_response.lower().strip()
    
    # Check for exact matches or phrases
    for indicator in positive_indicators:
        if indicator in user_lower:
            return True
    
    # Check for simple "yes" responses (but be more careful)
    if user_lower in ['yes', 'yep', 'yeah', 'yup']:
        return True
        
    return False

def generate_ai_response(prompt, context=""):
    """Generate AI response with context"""
    system_prompt = (
        "You are a helpful technical support assistant. "
        "Keep responses brief (under 50 words) and ask specific troubleshooting questions. "
        "Be empathetic and solution-focused."
    )
    
    messages = [
        {"role": "system", "content": system_prompt}
    ]
    
    if context:
        messages.append({"role": "system", "content": f"Context: {context}"})
    
    messages.append({"role": "user", "content": prompt})
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        temperature=0.5,
        max_tokens=150
    )
    return response.choices[0].message.content.strip()

def save_insights_to_csv(call_session, csv_file, session_id, server_url=server_url):
    """Analyze call, build schema, and push to FastAPI server"""

    try:
        # Analyze problem severity (optional - can be used to adjust sentiment)
        severity_score = analyze_problem_severity(
            call_session['initial_problem'], 
            call_session['transcripts']
        )

        # Generate single-sentence AI insight
        ai_insights = client.chat.completions.create(
            model="gpt-4",
            messages=[{
                "role": "user", 
                "content": f"Never use commas only 1 sentence. Analyze the following conversation and provide what the company should do:\n{call_session['transcripts']}"
            }],
            temperature=0.3,
            max_tokens=100
        )

        # Map into FastAPI schema
        payload = {
            "phone": call_session.get("phone_number", "Unknown"),
            "transcript": " | ".join(call_session['transcripts']),
            "sentiment": round((severity_score - 5) / 5, 2),  # normalize severity to [-1, 1]
            "insight": ai_insights.choices[0].message.content.strip(),
            "solved": True
        }

        # -------- POST TO SERVER --------
        response = requests.post(server_url, json=payload)
        if response.status_code == 200:
            print(f"✅ Posted to server: {server_url}")
        else:
            print(f"⚠️ Server returned {response.status_code}: {response.text}")

    except Exception as e:
        print(f"Error pushing to server: {e}")


# ---------------- FLASK ROUTES ----------------
@app.route("/voice", methods=['GET', 'POST'])
def voice():
    """Initial voice endpoint"""
    session_id = get_session_id()
    call_session = get_call_session(session_id)
    call_session['phone_number'] = get_phone_number_from_request()
    
    response = VoiceResponse()
    gather = Gather(input='speech', action='/gather', timeout=15, speech_timeout=5)
    gather.say("Hello! I'm your technical support assistant. Please describe the problem you're experiencing.")
    response.append(gather)
    response.say("I didn't hear anything. Please call back when you're ready. Goodbye!")
    return Response(str(response), mimetype='text/xml')

@app.route("/gather", methods=['POST'])
def gather():
    """Handle speech input and provide responses"""
    session_id = get_session_id()
    call_session = get_call_session(session_id)
    speech_result = request.form.get('SpeechResult')
    
    if not speech_result or not speech_result.strip():
        return handle_no_input(call_session, session_id)
    
    # Log user input
    call_session['transcripts'].append(f"User: {speech_result}")
    print(f"User said: {speech_result}")
    
    try:
        if call_session['state'] == 'initial':
            return handle_initial_problem(speech_result, call_session)
        elif call_session['state'] == 'troubleshooting':
            return handle_troubleshooting(speech_result, call_session, session_id)
        else:
            return handle_escalated(call_session)
            
    except Exception as e:
        print(f"Error processing request: {e}")
        response = VoiceResponse()
        response.say("I'm sorry, I encountered a technical issue. Please try calling back later.")
        response.hangup()
        return Response(str(response), mimetype='text/xml')

def handle_initial_problem(problem, call_session):
    """Handle the initial problem statement"""
    call_session['initial_problem'] = problem
    
    # Search for similar tickets
    similar_tickets = ticket_bot.find_similar(problem, limit=5)
    call_session['similarity_results'] = similar_tickets  # Store for CSV logging
    
    # Print similarity results to console for debugging
    print(f"\n=== SIMILARITY SEARCH RESULTS for: '{problem}' ===")
    if similar_tickets:
        for i, ticket in enumerate(similar_tickets, 1):
            print(f"#{i} Score: {ticket['score']:.3f} | Problem: '{ticket['problem'][:50]}...' | Solution: '{ticket['solution'][:50]}...'")
    else:
        print("No similar tickets found in database")
    print("=" * 60)
    
    response = VoiceResponse()
    
    if similar_tickets and similar_tickets[0]['score'] >= ticket_bot.similarity_threshold:
        # Found high-confidence solution
        best_match = similar_tickets[0]
        ai_response = (
            f"I found a similar issue that was resolved before. "
            f"The problem was: {best_match['problem']}. "
            f"Try this solution: {best_match['solution']}. "
            f"Did this help resolve your issue?"
        )
        call_session['state'] = 'troubleshooting'
        call_session['suggested_solution'] = best_match['solution']
        print(f"✅ HIGH CONFIDENCE MATCH (Score: {best_match['score']:.3f}) - Providing direct solution")
        
    else:
        # No high-confidence solution found, start troubleshooting
        ai_response = generate_ai_response(
            f"The user has this problem: {problem}. "
            f"Ask a specific troubleshooting question to help diagnose the issue."
        )
        call_session['state'] = 'troubleshooting'
        if similar_tickets:
            print(f"⚠️ LOW CONFIDENCE MATCH (Best: {similar_tickets[0]['score']:.3f}) - Starting troubleshooting")
        else:
            print("❌ NO MATCHES FOUND - Starting troubleshooting")
    
    call_session['transcripts'].append(f"AI: {ai_response}")
    
    gather = Gather(input='speech', action='/gather', timeout=15, speech_timeout=5)
    gather.say(ai_response)
    response.append(gather)
    response.say("I didn't hear your response. Let me transfer you to our escalation team.")
    response.redirect('/escalate')
    
    return Response(str(response), mimetype='text/xml')

def handle_troubleshooting(user_response, call_session, session_id):
    """Handle troubleshooting conversation"""
    call_session['troubleshoot_rounds'] += 1
    
    response = VoiceResponse()
    
    # Check if user indicates problem is solved
    if check_problem_resolved(user_response):
        call_session['problem_resolved'] = True
        call_session['state'] = 'resolved'
        
        ai_response = "Excellent! I'm glad we could resolve your issue. Have a great day!"
        call_session['transcripts'].append(f"AI: {ai_response}")
        
        response.say(ai_response)
        response.hangup()
        
        # Save insights to CSV
        save_insights_to_csv(call_session, CSV_FILE, session_id)
        return Response(str(response), mimetype='text/xml')
    
    # Check if we've reached the 5th troubleshooting round
    if call_session['troubleshoot_rounds'] >= ticket_bot.max_troubleshoot_rounds:
        ai_response = "Is the problem still there?"
        call_session['transcripts'].append(f"AI: {ai_response}")
        call_session['state'] = 'final_check'
        
        gather = Gather(input='speech', action='/final_problem_check', timeout=15, speech_timeout=5)
        gather.say(ai_response)
        response.append(gather)
        response.say("I will contact the developers. You will get a call back in 24 hours.")
        response.redirect('/escalate')
        return Response(str(response), mimetype='text/xml')
    
    # Continue troubleshooting
    context = f"Previous conversation: {call_session['transcripts'][-3:]}"
    ai_response = generate_ai_response(
        f"User response: {user_response}. Continue troubleshooting the original problem: {call_session['initial_problem']}",
        context
    )
    
    call_session['transcripts'].append(f"AI: {ai_response}")
    
    gather = Gather(input='speech', action='/gather', timeout=15, speech_timeout=5)
    gather.say(ai_response)
    response.append(gather)
    response.say("I didn't hear your response. Let me escalate this to our development team.")
    response.redirect('/escalate')
    
    return Response(str(response), mimetype='text/xml')

@app.route("/final_problem_check", methods=['POST'])
def final_problem_check():
    """Handle the final check after 5 rounds"""
    session_id = get_session_id()
    call_session = get_call_session(session_id)
    speech_result = request.form.get('SpeechResult')
    
    response = VoiceResponse()
    
    if speech_result:
        call_session['transcripts'].append(f"User: {speech_result}")
        
        # Check if problem is resolved
        if check_problem_resolved(speech_result) or 'no' in speech_result.lower():
            call_session['problem_resolved'] = True
            call_session['state'] = 'resolved'
            
            response.say("Excellent! I'm glad we could resolve your issue. Have a great day!")
            response.hangup()
        else:
            # Problem still exists, escalate
            call_session['state'] = 'escalated'
            response.say("I will contact the developers. You will get a call back in 24 hours.")
            response.hangup()
            
            # Escalate to developers
            ticket_bot.escalate_ticket(
                call_session['initial_problem'],
                call_session['transcripts']
            )
    else:
        # No response, assume escalation needed
        call_session['state'] = 'escalated'
        response.say("I will contact the developers. You will get a call back in 24 hours.")
        response.hangup()
    
    # Save insights to CSV
    save_insights_to_csv(call_session, CSV_FILE, session_id)
    return Response(str(response), mimetype='text/xml')

def escalate_to_developers(call_session, session_id):
    """Escalate the issue to developers"""
    # Save to escalations database
    ticket_bot.escalate_ticket(
        call_session['initial_problem'],
        call_session['transcripts']
    )
    
    ai_response = "I will contact the developers. You will get a call back in 24 hours."
    
    call_session['transcripts'].append(f"AI: {ai_response}")
    call_session['state'] = 'escalated'
    
    response = VoiceResponse()
    response.say(ai_response)
    response.hangup()
    
    # Save insights to CSV
    save_insights_to_csv(call_session, CSV_FILE, session_id)
    return Response(str(response), mimetype='text/xml')

def handle_no_input(call_session, session_id):
    """Handle when no speech is detected"""
    response = VoiceResponse()
    response.say("I didn't hear anything. Thank you for calling. Goodbye!")
    response.hangup()
    
    # Save session data
    if call_session['transcripts']:
        save_insights_to_csv(call_session, CSV_FILE, session_id)
    
    return Response(str(response), mimetype='text/xml')

def handle_escalated(call_session):
    """Handle responses after escalation"""
    response = VoiceResponse()
    response.say("Your issue has already been escalated. You'll hear back from our team in 24 hours. Goodbye!")
    response.hangup()
    return Response(str(response), mimetype='text/xml')

@app.route("/final_check", methods=['POST'])
def final_check():
    """Final check if user needs more help"""
    session_id = get_session_id()
    call_session = get_call_session(session_id)
    speech_result = request.form.get('SpeechResult')
    
    response = VoiceResponse()
    
    if speech_result and any(word in speech_result.lower() for word in ['yes', 'help', 'issue', 'problem']):
        response.say("I'll transfer you back to start a new support session.")
        response.redirect('/voice')
    else:
        response.say("Thank you for calling! Have a great day!")
        response.hangup()
        
        # Save session data
        if call_session['transcripts']:
            save_insights_to_csv(call_session, CSV_FILE, session_id)
    
    return Response(str(response), mimetype='text/xml')

@app.route("/escalate", methods=['POST'])
def escalate():
    """Direct escalation endpoint"""
    session_id = get_session_id()
    call_session = get_call_session(session_id)
    
    return escalate_to_developers(call_session, session_id)

@app.route("/hangup", methods=['POST'])
def hangup():
    """Handle call hangup"""
    session_id = get_session_id()
    if session_id in call_sessions:
        call_session = call_sessions[session_id]
        if call_session['transcripts']:
            save_insights_to_csv(call_session, CSV_FILE, session_id)
        del call_sessions[session_id]
    
    return Response("OK", mimetype='text/plain')

@app.route("/health", methods=['GET'])
def health():
    """Health check endpoint"""
    return Response("OK", mimetype='text/plain')

# ---------------- ADMIN ENDPOINTS (for adding tickets) ----------------
@app.route("/add_ticket", methods=['POST'])
def add_ticket():
    """Add a new ticket to the knowledge base"""
    data = request.get_json()
    if not data or 'problem' not in data or 'solution' not in data:
        return Response("Missing problem or solution", status=400)
    
    ticket_id = ticket_bot.add_ticket(data['problem'], data['solution'])
    return Response(f"Ticket added with ID: {ticket_id}", mimetype='text/plain')

@app.route("/search_tickets", methods=['POST'])
def search_tickets():
    """Search for similar tickets (for testing)"""
    data = request.get_json()
    if not data or 'problem' not in data:
        return Response("Missing problem", status=400)
    
    results = ticket_bot.find_similar(data['problem'])
    return Response(json.dumps(results, indent=2), mimetype='application/json')

if __name__ == "__main__":
    # Add some sample tickets for testing
    print("Adding sample tickets...")
    ticket_bot.add_ticket("Can't login to the app", "Reset your password by clicking 'Forgot Password' and check your email")
    ticket_bot.add_ticket("App crashes when opening", "Update to the latest version from your app store")
    ticket_bot.add_ticket("Slow performance and loading", "Clear your app cache, restart the device, and ensure stable internet connection")
    ticket_bot.add_ticket("Cannot receive notifications", "Check notification settings in your device settings and app permissions")
    ticket_bot.add_ticket("Payment failed", "Verify your payment method, check bank account balance, and try a different card if needed")
    
    print("Starting Flask app...")
    app.run(port=2222, debug=True)
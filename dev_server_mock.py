#!/usr/bin/env python3
"""
Local development server without external dependencies
"""

import json
import sqlite3
from pathlib import Path
from datetime import datetime

class MockSmartAgentAPI:
    def __init__(self):
        self.db_path = "dev_smartagent.db"
        self.init_database()
    
    def init_database(self):
        """Initialize SQLite database for development"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create basic tables
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS calls (
                id INTEGER PRIMARY KEY,
                audio_url TEXT,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transcripts (
                id INTEGER PRIMARY KEY,
                call_id INTEGER,
                text TEXT,
                confidence REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
        print(f"✅ Database initialized: {self.db_path}")
    
    def simulate_webhook(self, call_data):
        """Simulate Twilio webhook"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO calls (audio_url, status) 
            VALUES (?, 'received')
        """, (call_data.get('recordingUrl', 'mock://audio.mp3'),))
        
        call_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        print(f"✅ Mock webhook processed, call_id: {call_id}")
        return {"call_id": call_id, "status": "received"}
    
    def simulate_transcription(self, call_id):
        """Simulate audio transcription"""
        mock_transcripts = [
            "שלום, אני משה כהן מתל אביב. יש לי בעיה עם המקרר, הוא לא מקרר. אפשר לבוא מחר ב-3?",
            "היי, אני שרה מירושלים. המזגן לא עובד. כמה זה יעלה לתקן? אני יכולה ביום ראשון.",
            "בוקר טוב, יש לי בעיה עם המכונת כביסה. היא עושה רעש מוזר. מתי אתם פנויים?"
        ]
        
        import random
        mock_text = random.choice(mock_transcripts)
        confidence = round(random.uniform(0.75, 0.95), 2)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO transcripts (call_id, text, confidence) 
            VALUES (?, ?, ?)
        """, (call_id, mock_text, confidence))
        
        cursor.execute("""
            UPDATE calls SET status = 'transcribed' WHERE id = ?
        """, (call_id,))
        
        conn.commit()
        conn.close()
        
        print(f"✅ Mock transcription completed for call {call_id}")
        return {"text": mock_text, "confidence": confidence}
    
    def simulate_llm_extraction(self, transcript_text):
        """Simulate LLM information extraction"""
        mock_extraction = {
            "customer": {
                "name": "משה כהן" if "משה" in transcript_text else "שרה לוי",
                "phone": "+972501234567",
                "address": {
                    "city": "תל אביב" if "תל אביב" in transcript_text else "ירושלים"
                }
            },
            "device": {
                "category": "מקרר" if "מקרר" in transcript_text else "מזגן",
                "issue": "לא מקרר" if "מקרר" in transcript_text else "לא עובד",
                "urgency": "medium"
            },
            "appointment": {
                "date": "2025-09-05",
                "time": "15:00",
                "is_confirmed_by_customer": True
            },
            "free_text_summary_he": f"לקוח דיווח על בעיה. תואם ביקור.",
            "confidence": 0.85
        }
        
        print(f"✅ Mock LLM extraction completed")
        return mock_extraction
    
    def run_demo(self):
        """Run complete demo flow"""
        print("🚀 Starting SmartAgent Local Demo...")
        
        # Step 1: Simulate webhook
        webhook_data = {
            "recordingUrl": "https://mock.example.com/call1.mp3",
            "callSid": "CA_demo_123",
            "from": "+972501234567",
            "to": "+972599999999"
        }
        
        result1 = self.simulate_webhook(webhook_data)
        call_id = result1["call_id"]
        
        # Step 2: Simulate transcription
        transcript_result = self.simulate_transcription(call_id)
        
        # Step 3: Simulate LLM extraction
        extraction_result = self.simulate_llm_extraction(transcript_result["text"])
        
        print("\n📊 Demo Results:")
        print(f"Call ID: {call_id}")
        print(f"Transcript: {transcript_result['text'][:50]}...")
        print(f"Customer: {extraction_result['customer']['name']}")
        print(f"Device: {extraction_result['device']['category']}")
        print(f"Appointment: {extraction_result['appointment']['date']} {extraction_result['appointment']['time']}")
        
        print("\n🎉 Local demo completed successfully!")

if __name__ == "__main__":
    api = MockSmartAgentAPI()
    api.run_demo()

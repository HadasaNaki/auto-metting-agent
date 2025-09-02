#!/usr/bin/env python3
"""
SmartAgent Minimal Development Server
שירת פיתוח מינימלי לSmartAgent
"""

import os
import sys
from pathlib import Path

# Add backend to Python path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
import json

# Create FastAPI app
app = FastAPI(
    title="SmartAgent Development Server",
    description="מערכת ניהול טכנאים חכמה - שירת פיתוח",
    version="1.0.0-dev",
)

# Mock data storage
mock_data = {
    "organizations": [{"id": 1, "name": "טכנאים ישראל", "domain": "teknaim.co.il"}],
    "users": [
        {
            "id": 1,
            "org_id": 1,
            "email": "admin@teknaim.co.il",
            "name": "יוסי המנהל",
            "role": "admin",
        }
    ],
    "customers": [
        {
            "id": 1,
            "org_id": 1,
            "name": "משה כהן",
            "phone": "+972501234567",
            "city": "תל אביב",
        }
    ],
    "calls": [],
    "appointments": [],
}


# Pydantic models
class CallWebhook(BaseModel):
    CallSid: str
    RecordingUrl: str
    From: str
    To: str
    CallDuration: str


class CustomerCreate(BaseModel):
    name: str
    phone: str
    city: str


class AppointmentCreate(BaseModel):
    customer_id: int
    date: str
    time: str
    service_type: str


# Routes
@app.get("/")
async def root():
    return {
        "message": "SmartAgent Development Server is running!",
        "message_he": "שירת הפיתוח של SmartAgent פועל!",
        "version": "1.0.0-dev",
        "status": "✅ Working",
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "smartagent-dev",
        "timestamp": datetime.now().isoformat(),
    }


@app.get("/api/organizations")
async def get_organizations():
    return {"organizations": mock_data["organizations"]}


@app.get("/api/customers")
async def get_customers():
    return {"customers": mock_data["customers"]}


@app.post("/api/customers")
async def create_customer(customer: CustomerCreate):
    new_id = len(mock_data["customers"]) + 1
    new_customer = {
        "id": new_id,
        "org_id": 1,
        "name": customer.name,
        "phone": customer.phone,
        "city": customer.city,
        "created_at": datetime.now().isoformat(),
    }
    mock_data["customers"].append(new_customer)
    return {"customer": new_customer, "message": "לקוח נוצר בהצלחה"}


@app.get("/api/calls")
async def get_calls():
    return {"calls": mock_data["calls"]}


@app.post("/webhook/twilio/calls")
async def twilio_webhook(webhook_data: CallWebhook):
    """Simulate Twilio webhook processing"""

    # Create new call record
    call_id = len(mock_data["calls"]) + 1
    call_record = {
        "id": call_id,
        "org_id": 1,
        "twilio_call_sid": webhook_data.CallSid,
        "audio_url": webhook_data.RecordingUrl,
        "customer_phone": webhook_data.From,
        "duration": int(webhook_data.CallDuration),
        "status": "received",
        "created_at": datetime.now().isoformat(),
    }

    mock_data["calls"].append(call_record)

    # Simulate processing
    return {
        "call_id": call_id,
        "status": "received",
        "message": "שיחה התקבלה ועובדת",
        "next_steps": ["תמלול השיחה", "חילוץ מידע מהשיחה", "יצירת תור אוטומטית"],
    }


@app.post("/api/appointments")
async def create_appointment(appointment: AppointmentCreate):
    """Create new appointment"""

    appointment_id = len(mock_data["appointments"]) + 1
    new_appointment = {
        "id": appointment_id,
        "org_id": 1,
        "customer_id": appointment.customer_id,
        "date": appointment.date,
        "time": appointment.time,
        "service_type": appointment.service_type,
        "status": "scheduled",
        "created_at": datetime.now().isoformat(),
    }

    mock_data["appointments"].append(new_appointment)

    return {"appointment": new_appointment, "message": "תור נקבע בהצלחה"}


@app.get("/api/appointments")
async def get_appointments():
    return {"appointments": mock_data["appointments"]}


@app.post("/api/simulate/full-call-flow")
async def simulate_full_call_flow():
    """Simulate complete call processing flow"""

    # Step 1: Simulate incoming call
    webhook_data = {
        "CallSid": f"CA_demo_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "RecordingUrl": "https://mock.example.com/recording.mp3",
        "From": "+972501234567",
        "To": "+972599999999",
        "CallDuration": "45",
    }

    # Step 2: Create call record
    call_id = len(mock_data["calls"]) + 1
    call_record = {
        "id": call_id,
        "org_id": 1,
        "twilio_call_sid": webhook_data["CallSid"],
        "audio_url": webhook_data["RecordingUrl"],
        "customer_phone": webhook_data["From"],
        "duration": int(webhook_data["CallDuration"]),
        "status": "processing",
        "created_at": datetime.now().isoformat(),
    }
    mock_data["calls"].append(call_record)

    # Step 3: Simulate transcription
    transcript = {
        "text": "שלום, אני משה כהן מתל אביב. יש לי בעיה עם המקרר, הוא לא מקרר. אפשר לבוא מחר ב-3?",
        "confidence": 0.92,
        "language": "he",
    }

    # Step 4: Simulate AI extraction
    extraction = {
        "customer": {
            "name": "משה כהן",
            "phone": "+972501234567",
            "address": {"city": "תל אביב"},
        },
        "device": {"category": "מקרר", "issue": "לא מקרר", "urgency": "medium"},
        "appointment": {
            "date": "2025-09-05",
            "time": "15:00",
            "is_confirmed_by_customer": True,
        },
        "confidence": 0.89,
    }

    # Step 5: Create customer if not exists
    customer_exists = any(
        c["phone"] == extraction["customer"]["phone"] for c in mock_data["customers"]
    )
    if not customer_exists:
        customer_id = len(mock_data["customers"]) + 1
        new_customer = {
            "id": customer_id,
            "org_id": 1,
            "name": extraction["customer"]["name"],
            "phone": extraction["customer"]["phone"],
            "city": extraction["customer"]["address"]["city"],
            "created_at": datetime.now().isoformat(),
        }
        mock_data["customers"].append(new_customer)
    else:
        customer_id = next(
            c["id"]
            for c in mock_data["customers"]
            if c["phone"] == extraction["customer"]["phone"]
        )

    # Step 6: Create appointment
    appointment_id = len(mock_data["appointments"]) + 1
    new_appointment = {
        "id": appointment_id,
        "org_id": 1,
        "customer_id": customer_id,
        "date": extraction["appointment"]["date"],
        "time": extraction["appointment"]["time"],
        "service_type": f"תיקון {extraction['device']['category']}",
        "status": "scheduled",
        "created_at": datetime.now().isoformat(),
    }
    mock_data["appointments"].append(new_appointment)

    # Update call status
    call_record["status"] = "completed"

    return {
        "success": True,
        "message": "זרימת עבודה מלאה הושלמה בהצלחה!",
        "flow_summary": {
            "call_id": call_id,
            "transcript": transcript["text"][:50] + "...",
            "customer_name": extraction["customer"]["name"],
            "device": extraction["device"]["category"],
            "issue": extraction["device"]["issue"],
            "appointment_id": appointment_id,
            "appointment_date": extraction["appointment"]["date"],
            "appointment_time": extraction["appointment"]["time"],
        },
        "next_steps": ["שליחת הודעת אישור ללקוח", "סנכרון עם לוח שנה", "הודעה לטכנאי"],
    }


@app.get("/api/stats")
async def get_stats():
    """Get system statistics"""
    return {
        "statistics": {
            "total_organizations": len(mock_data["organizations"]),
            "total_users": len(mock_data["users"]),
            "total_customers": len(mock_data["customers"]),
            "total_calls": len(mock_data["calls"]),
            "total_appointments": len(mock_data["appointments"]),
            "last_updated": datetime.now().isoformat(),
        },
        "status": "✅ SmartAgent Development Server Working",
    }


if __name__ == "__main__":
    import uvicorn

    print("🚀 Starting SmartAgent Development Server...")
    print("📡 Server will be available at: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("📊 Health Check: http://localhost:8000/health")
    print("🔄 Mock Full Flow: http://localhost:8000/api/simulate/full-call-flow")

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True, log_level="info")

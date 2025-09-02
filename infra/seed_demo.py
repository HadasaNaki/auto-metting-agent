#!/usr/bin/env python3
"""
Demo script to seed the database with sample data
"""

import requests
import json
import os
import sys

API_BASE = "http://localhost:8000"


def create_demo_org_and_user():
    """Create demo organization and user"""

    # Register demo organization
    register_data = {
        "email": "demo@smartagent.com",
        "password": "demo123",
        "full_name": "Demo User",
        "org_name": "Demo Repair Services",
    }

    try:
        response = requests.post(f"{API_BASE}/auth/register", json=register_data)
        if response.status_code == 200:
            tokens = response.json()
            print("✅ Demo organization created successfully")
            return tokens["access_token"]
        else:
            print(f"❌ Registration failed: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return None


def simulate_twilio_webhook(token):
    """Simulate a Twilio webhook with demo call"""

    webhook_data = {
        "recordingUrl": "https://demo.smartagent.com/sample_call.mp3",
        "callSid": "CA123456789abcdef",
        "from": "+972501234567",
        "to": "+972599999999",
        "startTime": "2025-08-30T12:00:00Z",
        "duration": 180,
    }

    headers = {"Authorization": f"Bearer {token}"}

    try:
        response = requests.post(
            f"{API_BASE}/calls/webhook/twilio", json=webhook_data, headers=headers
        )
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Demo call created: Call ID {result.get('call_id')}")
            return result.get("call_id")
        else:
            print(f"❌ Webhook failed: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Webhook failed: {e}")
        return None


def create_demo_customer(token):
    """Create demo customer"""

    customer_data = {
        "name": "משה כהן",
        "phone": "+972501234567",
        "email": "moshe@example.com",
    }

    headers = {"Authorization": f"Bearer {token}"}

    try:
        response = requests.post(
            f"{API_BASE}/customers", json=customer_data, headers=headers
        )
        if response.status_code == 200:
            customer = response.json()
            print(f"✅ Demo customer created: {customer['name']}")
            return customer["id"]
        else:
            print(f"❌ Customer creation failed: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Customer creation failed: {e}")
        return None


def main():
    """Main demo setup function"""

    print("🚀 Starting SmartAgent demo setup...")
    print()

    # Create demo org and user
    token = create_demo_org_and_user()
    if not token:
        print("❌ Setup failed - could not create demo organization")
        sys.exit(1)

    # Create demo customer
    customer_id = create_demo_customer(token)

    # Simulate webhook call
    call_id = simulate_twilio_webhook(token)

    print()
    print("🎉 Demo setup completed!")
    print()
    print("Demo credentials:")
    print("  Email: demo@smartagent.com")
    print("  Password: demo123")
    print()
    print("Access the system:")
    print("  Frontend: http://localhost:3000")
    print("  API Docs: http://localhost:8000/docs")
    print()
    print("Note: Audio transcription and LLM extraction will be simulated")
    print("since this is a demo environment.")


if __name__ == "__main__":
    main()

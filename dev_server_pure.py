#!/usr/bin/env python3
"""
SmartAgent Pure Python Development Server
שירת פיתוח Python טהור ללא תלויות חיצוניות
"""

import json
import http.server
import socketserver
import urllib.parse
from datetime import datetime
import threading
import webbrowser
import time

# Port for the server
PORT = 8000

# Mock data storage
mock_data = {
    "organizations": [
        {
            "id": 1,
            "name": "טכנאים ישראל",
            "domain": "teknaim.co.il",
            "subscription": "premium",
        }
    ],
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
    "messages": [],
}


class SmartAgentHandler(http.server.SimpleHTTPRequestHandler):
    """Custom HTTP handler for SmartAgent API"""

    def do_GET(self):
        """Handle GET requests"""
        path = urllib.parse.urlparse(self.path).path
        query = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)

        if path == "/":
            self.send_json_response(
                {
                    "message": "SmartAgent Pure Python Server is running!",
                    "message_he": "שירת SmartAgent Python טהור פועל!",
                    "version": "1.0.0-pure",
                    "status": "✅ Working",
                    "endpoints": [
                        "GET / - This page",
                        "GET /health - Health check",
                        "GET /api/organizations - Get organizations",
                        "GET /api/customers - Get customers",
                        "GET /api/calls - Get calls",
                        "GET /api/appointments - Get appointments",
                        "GET /api/stats - Get statistics",
                        "POST /api/simulate/call - Simulate incoming call",
                        "POST /api/simulate/full-flow - Simulate full workflow",
                    ],
                }
            )

        elif path == "/health":
            self.send_json_response(
                {
                    "status": "healthy",
                    "service": "smartagent-pure-python",
                    "timestamp": datetime.now().isoformat(),
                    "uptime": "Running",
                }
            )

        elif path == "/api/organizations":
            self.send_json_response(
                {
                    "organizations": mock_data["organizations"],
                    "count": len(mock_data["organizations"]),
                }
            )

        elif path == "/api/customers":
            self.send_json_response(
                {
                    "customers": mock_data["customers"],
                    "count": len(mock_data["customers"]),
                }
            )

        elif path == "/api/calls":
            self.send_json_response(
                {"calls": mock_data["calls"], "count": len(mock_data["calls"])}
            )

        elif path == "/api/appointments":
            self.send_json_response(
                {
                    "appointments": mock_data["appointments"],
                    "count": len(mock_data["appointments"]),
                }
            )

        elif path == "/api/stats":
            self.send_json_response(
                {
                    "statistics": {
                        "total_organizations": len(mock_data["organizations"]),
                        "total_users": len(mock_data["users"]),
                        "total_customers": len(mock_data["customers"]),
                        "total_calls": len(mock_data["calls"]),
                        "total_appointments": len(mock_data["appointments"]),
                        "total_messages": len(mock_data["messages"]),
                        "last_updated": datetime.now().isoformat(),
                    },
                    "status": "✅ SmartAgent Pure Python Server Working",
                }
            )

        elif path == "/dashboard":
            self.send_html_dashboard()

        else:
            self.send_json_response(
                {
                    "error": "Not Found",
                    "message": f"Path '{path}' not found",
                    "available_endpoints": [
                        "/",
                        "/health",
                        "/api/organizations",
                        "/api/customers",
                        "/api/calls",
                        "/api/appointments",
                        "/api/stats",
                        "/dashboard",
                    ],
                },
                status=404,
            )

    def do_POST(self):
        """Handle POST requests"""
        path = urllib.parse.urlparse(self.path).path
        content_length = (
            int(self.headers["Content-Length"])
            if "Content-Length" in self.headers
            else 0
        )

        try:
            post_data = (
                self.rfile.read(content_length).decode("utf-8")
                if content_length > 0
                else "{}"
            )
            data = json.loads(post_data) if post_data else {}
        except:
            data = {}

        if path == "/api/simulate/call":
            self.simulate_incoming_call(data)

        elif path == "/api/simulate/full-flow":
            self.simulate_full_workflow()

        elif path == "/webhook/twilio":
            self.handle_twilio_webhook(data)

        elif path == "/api/customers":
            self.create_customer(data)

        elif path == "/api/appointments":
            self.create_appointment(data)

        else:
            self.send_json_response(
                {"error": "Not Found", "message": f"POST path '{path}' not found"},
                status=404,
            )

    def simulate_incoming_call(self, data):
        """Simulate incoming call processing"""
        call_id = len(mock_data["calls"]) + 1

        call_record = {
            "id": call_id,
            "org_id": 1,
            "twilio_call_sid": f"CA_demo_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "audio_url": "https://mock.example.com/recording.mp3",
            "customer_phone": data.get("phone", "+972501234567"),
            "duration": 45,
            "status": "received",
            "created_at": datetime.now().isoformat(),
        }

        mock_data["calls"].append(call_record)

        self.send_json_response(
            {
                "success": True,
                "call_id": call_id,
                "status": "received",
                "message": "שיחה התקבלה בהצלחה",
                "call_record": call_record,
            }
        )

    def simulate_full_workflow(self):
        """Simulate complete SmartAgent workflow"""

        # Step 1: Incoming call
        call_id = len(mock_data["calls"]) + 1
        call_record = {
            "id": call_id,
            "org_id": 1,
            "twilio_call_sid": f"CA_workflow_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "audio_url": "https://mock.example.com/call_recording.mp3",
            "customer_phone": "+972501234567",
            "duration": 45,
            "status": "processing",
            "created_at": datetime.now().isoformat(),
        }
        mock_data["calls"].append(call_record)

        # Step 2: Mock transcription
        transcript = {
            "text": "שלום, אני רחל לוי מירושלים. יש לי בעיה עם המזגן, הוא לא מקרר. אפשר לבוא מחר ב-2?",
            "confidence": 0.91,
            "language": "he",
            "segments": [
                {"start": 0.0, "end": 2.5, "text": "שלום, אני רחל לוי מירושלים"},
                {"start": 2.5, "end": 6.0, "text": "יש לי בעיה עם המזגן, הוא לא מקרר"},
                {"start": 6.0, "end": 8.5, "text": "אפשר לבוא מחר ב-2?"},
            ],
        }

        # Step 3: Mock AI extraction
        extraction = {
            "customer": {
                "name": "רחל לוי",
                "phone": "+972501234567",
                "address": {"city": "ירושלים"},
            },
            "device": {"category": "מזגן", "issue": "לא מקרר", "urgency": "medium"},
            "appointment": {
                "date": "2025-09-05",
                "time": "14:00",
                "is_confirmed_by_customer": True,
            },
            "confidence": 0.88,
        }

        # Step 4: Create/update customer
        customer_exists = any(
            c["phone"] == extraction["customer"]["phone"]
            for c in mock_data["customers"]
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

        # Step 5: Create appointment
        appointment_id = len(mock_data["appointments"]) + 1
        new_appointment = {
            "id": appointment_id,
            "org_id": 1,
            "customer_id": customer_id,
            "technician_id": 1,
            "date": extraction["appointment"]["date"],
            "time": extraction["appointment"]["time"],
            "service_type": f"תיקון {extraction['device']['category']}",
            "issue": extraction["device"]["issue"],
            "status": "scheduled",
            "created_at": datetime.now().isoformat(),
        }
        mock_data["appointments"].append(new_appointment)

        # Step 6: Create confirmation message
        message_id = len(mock_data["messages"]) + 1
        confirmation_message = {
            "id": message_id,
            "org_id": 1,
            "customer_id": customer_id,
            "appointment_id": appointment_id,
            "message_type": "sms",
            "recipient": extraction["customer"]["phone"],
            "content": f"שלום {extraction['customer']['name']}, התור שלך נקבע ל-{extraction['appointment']['date']} בשעה {extraction['appointment']['time']} לתיקון {extraction['device']['category']}. נשמח לראותך!",
            "status": "sent",
            "sent_at": datetime.now().isoformat(),
            "created_at": datetime.now().isoformat(),
        }
        mock_data["messages"].append(confirmation_message)

        # Update call status
        call_record["status"] = "completed"
        call_record["processed_at"] = datetime.now().isoformat()

        self.send_json_response(
            {
                "success": True,
                "message": "זרימת עבודה מלאה הושלמה בהצלחה! 🎉",
                "workflow_summary": {
                    "step_1_call": {
                        "call_id": call_id,
                        "status": "completed",
                        "duration": "45 seconds",
                    },
                    "step_2_transcription": {
                        "text_preview": transcript["text"][:50] + "...",
                        "confidence": transcript["confidence"],
                        "language": "Hebrew",
                    },
                    "step_3_ai_extraction": {
                        "customer_name": extraction["customer"]["name"],
                        "device": extraction["device"]["category"],
                        "issue": extraction["device"]["issue"],
                        "confidence": extraction["confidence"],
                    },
                    "step_4_customer": {
                        "customer_id": customer_id,
                        "action": "created" if not customer_exists else "updated",
                    },
                    "step_5_appointment": {
                        "appointment_id": appointment_id,
                        "date": extraction["appointment"]["date"],
                        "time": extraction["appointment"]["time"],
                        "service": f"תיקון {extraction['device']['category']}",
                    },
                    "step_6_notification": {
                        "message_id": message_id,
                        "type": "SMS confirmation",
                        "status": "sent",
                    },
                },
                "next_steps": [
                    "סנכרון עם לוח שנה של הטכנאי",
                    "שליחת הודעת תזכורת 24 שעות לפני",
                    "הכנת דוח עבודה",
                ],
            }
        )

    def handle_twilio_webhook(self, data):
        """Handle Twilio webhook"""
        call_id = len(mock_data["calls"]) + 1
        call_record = {
            "id": call_id,
            "twilio_call_sid": data.get("CallSid", "CA_unknown"),
            "audio_url": data.get("RecordingUrl", ""),
            "customer_phone": data.get("From", ""),
            "duration": int(data.get("CallDuration", 0)),
            "status": "received",
            "created_at": datetime.now().isoformat(),
        }
        mock_data["calls"].append(call_record)

        self.send_json_response(
            {
                "success": True,
                "message": "Webhook processed successfully",
                "call_id": call_id,
            }
        )

    def create_customer(self, data):
        """Create new customer"""
        customer_id = len(mock_data["customers"]) + 1
        new_customer = {
            "id": customer_id,
            "org_id": 1,
            "name": data.get("name", "לקוח חדש"),
            "phone": data.get("phone", ""),
            "city": data.get("city", ""),
            "created_at": datetime.now().isoformat(),
        }
        mock_data["customers"].append(new_customer)

        self.send_json_response(
            {"success": True, "customer": new_customer, "message": "לקוח נוצר בהצלחה"}
        )

    def create_appointment(self, data):
        """Create new appointment"""
        appointment_id = len(mock_data["appointments"]) + 1
        new_appointment = {
            "id": appointment_id,
            "org_id": 1,
            "customer_id": data.get("customer_id", 1),
            "date": data.get("date", "2025-09-05"),
            "time": data.get("time", "10:00"),
            "service_type": data.get("service_type", "שירות כללי"),
            "status": "scheduled",
            "created_at": datetime.now().isoformat(),
        }
        mock_data["appointments"].append(new_appointment)

        self.send_json_response(
            {
                "success": True,
                "appointment": new_appointment,
                "message": "תור נקבע בהצלחה",
            }
        )

    def send_html_dashboard(self):
        """Send HTML dashboard"""
        html_content = f"""
<!DOCTYPE html>
<html dir="rtl" lang="he">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SmartAgent Dashboard - לוח בקרה</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .header {{ background: #2563eb; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }}
        .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-bottom: 20px; }}
        .stat-card {{ background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .stat-number {{ font-size: 2em; font-weight: bold; color: #2563eb; }}
        .button {{ background: #2563eb; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; margin: 5px; }}
        .button:hover {{ background: #1d4ed8; }}
        .results {{ background: white; padding: 20px; border-radius: 8px; margin-top: 15px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .results pre {{ background: #f8f9fa; padding: 15px; border-radius: 5px; overflow-x: auto; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 SmartAgent Development Dashboard</h1>
            <p>לוח בקרה לפיתוח מערכת ניהול טכנאים חכמה</p>
        </div>

        <div class="stats">
            <div class="stat-card">
                <div class="stat-number">{len(mock_data["organizations"])}</div>
                <div>ארגונים</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{len(mock_data["customers"])}</div>
                <div>לקוחות</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{len(mock_data["calls"])}</div>
                <div>שיחות</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{len(mock_data["appointments"])}</div>
                <div>תורים</div>
            </div>
        </div>

        <div class="results">
            <h3>🧪 Test SmartAgent Functionality</h3>
            <p>לחץ על הכפתורים כדי לבדוק תפקודיות:</p>

            <button class="button" onclick="testAPI('/api/stats')">📊 Statistics</button>
            <button class="button" onclick="testAPI('/api/customers')">👥 Customers</button>
            <button class="button" onclick="testAPI('/api/calls')">📞 Calls</button>
            <button class="button" onclick="testAPI('/api/appointments')">📅 Appointments</button>
            <button class="button" onclick="simulateCall()">🎭 Simulate Call</button>
            <button class="button" onclick="simulateFullFlow()">🔄 Full Workflow</button>

            <div id="results"></div>
        </div>
    </div>

    <script>
        async function testAPI(endpoint) {{
            try {{
                const response = await fetch(endpoint);
                const data = await response.json();
                document.getElementById('results').innerHTML =
                    '<h4>Results for ' + endpoint + ':</h4><pre>' +
                    JSON.stringify(data, null, 2) + '</pre>';
            }} catch (error) {{
                document.getElementById('results').innerHTML =
                    '<h4>Error:</h4><pre>' + error.message + '</pre>';
            }}
        }}

        async function simulateCall() {{
            try {{
                const response = await fetch('/api/simulate/call', {{
                    method: 'POST',
                    headers: {{'Content-Type': 'application/json'}},
                    body: JSON.stringify({{phone: '+972501234567'}})
                }});
                const data = await response.json();
                document.getElementById('results').innerHTML =
                    '<h4>🎭 Simulated Call:</h4><pre>' +
                    JSON.stringify(data, null, 2) + '</pre>';
                updateStats();
            }} catch (error) {{
                document.getElementById('results').innerHTML =
                    '<h4>Error:</h4><pre>' + error.message + '</pre>';
            }}
        }}

        async function simulateFullFlow() {{
            try {{
                const response = await fetch('/api/simulate/full-flow', {{
                    method: 'POST',
                    headers: {{'Content-Type': 'application/json'}}
                }});
                const data = await response.json();
                document.getElementById('results').innerHTML =
                    '<h4>🔄 Full Workflow Simulation:</h4><pre>' +
                    JSON.stringify(data, null, 2) + '</pre>';
                updateStats();
            }} catch (error) {{
                document.getElementById('results').innerHTML =
                    '<h4>Error:</h4><pre>' + error.message + '</pre>';
            }}
        }}

        function updateStats() {{
            setTimeout(() => location.reload(), 2000);
        }}
    </script>
</body>
</html>
        """

        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html_content.encode("utf-8"))

    def send_json_response(self, data, status=200):
        """Send JSON response"""
        self.send_response(status)
        self.send_header("Content-type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8"))

    def do_OPTIONS(self):
        """Handle OPTIONS for CORS"""
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()


def start_server():
    """Start the development server"""
    handler = SmartAgentHandler

    try:
        with socketserver.TCPServer(("", PORT), handler) as httpd:
            print("🚀 SmartAgent Pure Python Development Server Starting...")
            print(f"📡 Server running at: http://localhost:{PORT}")
            print(f"📊 Dashboard: http://localhost:{PORT}/dashboard")
            print(f"🔗 API Endpoints: http://localhost:{PORT}/")
            print(f"❤️ Health Check: http://localhost:{PORT}/health")
            print("\n🧪 Quick Tests:")
            print(
                f"  📞 Simulate Call: curl -X POST http://localhost:{PORT}/api/simulate/call"
            )
            print(
                f"  🔄 Full Workflow: curl -X POST http://localhost:{PORT}/api/simulate/full-flow"
            )
            print(f"  📊 Statistics: curl http://localhost:{PORT}/api/stats")
            print("\n⏹️ Press Ctrl+C to stop")

            # Open browser automatically
            def open_browser():
                time.sleep(1)
                webbrowser.open(f"http://localhost:{PORT}/dashboard")

            threading.Thread(target=open_browser, daemon=True).start()

            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except OSError as e:
        if "Address already in use" in str(e):
            print(
                f"❌ Port {PORT} is already in use. Please close other applications or use a different port."
            )
        else:
            print(f"❌ Error starting server: {e}")


if __name__ == "__main__":
    start_server()

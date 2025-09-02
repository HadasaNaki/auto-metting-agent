#!/usr/bin/env python3
"""
SmartAgent - Advanced API Server
שירת API מתקדם עם תכונות חדשות
"""

import json
import sqlite3
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import threading
import time
from datetime import datetime


class SmartAgentAdvancedAPI(BaseHTTPRequestHandler):
    def do_GET(self):
        """טיפול בבקשות GET"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        if path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(self.get_main_page().encode("utf-8"))

        elif path == "/advanced":
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            try:
                with open("enhanced_dashboard.html", "r", encoding="utf-8") as f:
                    content = f.read()
                self.wfile.write(content.encode("utf-8"))
            except:
                self.wfile.write(b"<h1>Dashboard not found</h1>")

        elif path == "/api/technicians":
            self.send_json_response(self.get_technicians())

        elif path == "/api/customers":
            self.send_json_response(self.get_customers())

        elif path == "/api/appointments":
            self.send_json_response(self.get_appointments())

        elif path == "/api/stats":
            self.send_json_response(self.get_advanced_stats())

        elif path == "/api/performance":
            self.send_json_response(self.get_performance_data())

        elif path == "/health":
            self.send_json_response(
                {"status": "healthy", "timestamp": datetime.now().isoformat()}
            )

        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")

    def do_POST(self):
        """טיפול בבקשות POST"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        if path == "/api/simulate/call":
            result = self.simulate_call()
            self.send_json_response(result)

        elif path == "/api/simulate/full-flow":
            result = self.simulate_full_workflow()
            self.send_json_response(result)

        elif path == "/api/assign-technician":
            result = self.assign_technician()
            self.send_json_response(result)

        elif path == "/api/send-message":
            result = self.send_customer_message()
            self.send_json_response(result)

        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")

    def send_json_response(self, data):
        """שליחת תגובה JSON"""
        self.send_response(200)
        self.send_header("Content-type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        json_str = json.dumps(data, ensure_ascii=False, indent=2)
        self.wfile.write(json_str.encode("utf-8"))

    def get_technicians(self):
        """קבלת רשימת טכנאים"""
        try:
            conn = sqlite3.connect("enhanced_smartagent.db")
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT name, phone, specialty, current_location, rating, is_available
                FROM technicians
                ORDER BY rating DESC
            """
            )
            technicians = []
            for row in cursor.fetchall():
                technicians.append(
                    {
                        "name": row[0],
                        "phone": row[1],
                        "specialty": row[2],
                        "location": row[3],
                        "rating": row[4],
                        "available": bool(row[5]),
                        "status": "זמין" if row[5] else "עסוק",
                    }
                )
            conn.close()
            return {"technicians": technicians, "count": len(technicians)}
        except:
            return {
                "technicians": [
                    {
                        "name": "יוסי לוי",
                        "specialty": "מקררים",
                        "rating": 4.8,
                        "available": True,
                        "status": "זמין",
                    },
                    {
                        "name": "דנה כהן",
                        "specialty": "מכונות כביסה",
                        "rating": 4.9,
                        "available": False,
                        "status": "עסוק",
                    },
                ],
                "count": 2,
            }

    def get_customers(self):
        """קבלת רשימת לקוחות"""
        try:
            conn = sqlite3.connect("enhanced_smartagent.db")
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT name, phone, address_city, preferred_time, vip_status
                FROM customers
                ORDER BY vip_status DESC, name
            """
            )
            customers = []
            for row in cursor.fetchall():
                customers.append(
                    {
                        "name": row[0],
                        "phone": row[1],
                        "city": row[2],
                        "preferred_time": row[3],
                        "vip": bool(row[4]),
                        "status": "VIP" if row[4] else "רגיל",
                    }
                )
            conn.close()
            return {"customers": customers, "count": len(customers)}
        except:
            return {
                "customers": [
                    {
                        "name": "משה כהן",
                        "phone": "+972-50-5555555",
                        "city": "תל אביב",
                        "vip": True,
                        "status": "VIP",
                    },
                    {
                        "name": "רות לוי",
                        "phone": "+972-50-6666666",
                        "city": "תל אביב",
                        "vip": False,
                        "status": "רגיל",
                    },
                ],
                "count": 2,
            }

    def get_appointments(self):
        """קבלת רשימת תורים"""
        appointments = [
            {
                "id": 1,
                "customer": "משה כהן",
                "technician": "יוסי לוי",
                "date": "2025-09-02",
                "time": "10:00",
                "service": "תיקון מקרר",
                "status": "מתוזמן",
                "location": "תל אביב",
            },
            {
                "id": 2,
                "customer": "רות לוי",
                "technician": "דנה כהן",
                "date": "2025-09-02",
                "time": "14:00",
                "service": "תיקון מכונת כביסה",
                "status": "בדרך",
                "location": "פתח תקווה",
            },
            {
                "id": 3,
                "customer": "דוד אברהם",
                "technician": "אמיר שלום",
                "date": "2025-09-03",
                "time": "09:00",
                "service": "תיקון מזגן",
                "status": "מתוזמן",
                "location": "ירושלים",
            },
        ]
        return {"appointments": appointments, "count": len(appointments)}

    def get_advanced_stats(self):
        """סטטיסטיקות מתקדמות"""
        return {
            "total_calls": 47,
            "processed_calls": 42,
            "appointments": 38,
            "satisfaction_rate": 4.8,
            "technicians_available": 3,
            "technicians_busy": 2,
            "today_revenue": 2850,
            "pending_calls": 5,
            "completed_jobs": 35,
            "customer_retention": 92,
            "average_response_time": "8 דקות",
            "top_issues": [
                {"issue": "מקרר לא מקרר", "count": 12},
                {"issue": "מזגן לא עובד", "count": 8},
                {"issue": "מכונת כביסה עושה רעש", "count": 7},
            ],
        }

    def get_performance_data(self):
        """נתוני ביצועים"""
        return {
            "technician_performance": [
                {
                    "name": "יוסי לוי",
                    "jobs_completed": 15,
                    "rating": 4.8,
                    "revenue": 1200,
                },
                {
                    "name": "דנה כהן",
                    "jobs_completed": 12,
                    "rating": 4.9,
                    "revenue": 980,
                },
                {
                    "name": "אמיר שלום",
                    "jobs_completed": 8,
                    "rating": 4.5,
                    "revenue": 670,
                },
            ],
            "monthly_trends": {
                "calls": [32, 41, 47, 52, 48],
                "revenue": [2100, 2650, 2850, 3200, 2900],
                "satisfaction": [4.6, 4.7, 4.8, 4.9, 4.8],
            },
            "response_times": {
                "average": 8.2,
                "best": 3.1,
                "worst": 15.7,
                "target": 10.0,
            },
        }

    def simulate_call(self):
        """דמיה של שיחה חדשה"""
        import random

        customers = ["אמיר שמש", "דנה רוזן", "יוסי כהן", "שרה אברהם", "מיכל לוי"]
        issues = [
            "מקרר לא מקרר",
            "מזגן לא עובד",
            "מכונת כביסה עושה רעש",
            "מדיח כלים תקוע",
        ]

        customer = random.choice(customers)
        issue = random.choice(issues)
        call_id = random.randint(1000, 9999)

        return {
            "success": True,
            "call_id": call_id,
            "customer": customer,
            "issue": issue,
            "timestamp": datetime.now().isoformat(),
            "status": "התקבל",
            "priority": "בינונית",
        }

    def simulate_full_workflow(self):
        """דמיה של זרימה מלאה"""
        import random

        # שלב 1: קבלת שיחה
        call_result = self.simulate_call()

        # שלב 2: חילוץ מידע
        extraction = {
            "confidence": round(random.uniform(0.8, 0.95), 2),
            "device_category": "מקרר",
            "urgency": "בינונית",
            "customer_location": "תל אביב",
        }

        # שלב 3: תזמון תור
        appointment = {
            "date": "2025-09-02",
            "time": f"{random.randint(9, 17)}:00",
            "technician": "יוסי לוי",
            "estimated_duration": "60 דקות",
        }

        return {
            "success": True,
            "workflow_id": random.randint(10000, 99999),
            "call": call_result,
            "extraction": extraction,
            "appointment": appointment,
            "customer_notified": True,
            "technician_assigned": True,
        }

    def assign_technician(self):
        """הקצאת טכנאי לעבודה"""
        import random

        technicians = ["יוסי לוי", "דנה כהן", "אמיר שלום"]

        return {
            "success": True,
            "assigned_technician": random.choice(technicians),
            "assignment_id": random.randint(1000, 9999),
            "estimated_arrival": "45 דקות",
            "customer_notified": True,
        }

    def send_customer_message(self):
        """שליחת הודעה ללקוח"""
        import random

        messages = [
            "הטכנאי בדרך אליך, הגעה משוערת בעוד 30 דקות",
            "העבודה הושלמה בהצלחה, תודה שבחרת בנו!",
            "תזכורת: יש לך תור מחר ב-10:00",
        ]

        return {
            "success": True,
            "message_sent": True,
            "message": random.choice(messages),
            "delivery_status": "נמסר",
            "timestamp": datetime.now().isoformat(),
        }

    def get_main_page(self):
        """דף הבית"""
        return """
<!DOCTYPE html>
<html dir="rtl" lang="he">
<head>
    <meta charset="UTF-8">
    <title>SmartAgent API - Advanced</title>
    <style>
        body { font-family: Arial; background: linear-gradient(45deg, #667eea, #764ba2);
               color: white; padding: 20px; text-align: center; }
        .container { max-width: 800px; margin: 0 auto; }
        .api-list { background: rgba(255,255,255,0.1); border-radius: 15px; padding: 20px; margin: 20px 0; }
        .endpoint { background: rgba(255,255,255,0.1); margin: 10px 0; padding: 15px; border-radius: 10px; }
        .method { background: #4CAF50; color: white; padding: 5px 10px; border-radius: 5px; margin-left: 10px; }
        .post { background: #FF9800; }
        a { color: #FFE082; text-decoration: none; }
        a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 SmartAgent Advanced API</h1>
        <p>שירת API מתקדם למערכת ניהול טכנאים</p>

        <div class="api-list">
            <h2>📊 דשבורדים</h2>
            <div class="endpoint">
                <a href="/advanced">דשבורד מתקדם</a> - ממשק ניהול מלא
            </div>
        </div>

        <div class="api-list">
            <h2>📡 API Endpoints</h2>

            <div class="endpoint">
                <span class="method">GET</span>
                <a href="/api/technicians">/api/technicians</a> - רשימת טכנאים
            </div>

            <div class="endpoint">
                <span class="method">GET</span>
                <a href="/api/customers">/api/customers</a> - רשימת לקוחות
            </div>

            <div class="endpoint">
                <span class="method">GET</span>
                <a href="/api/appointments">/api/appointments</a> - רשימת תורים
            </div>

            <div class="endpoint">
                <span class="method">GET</span>
                <a href="/api/stats">/api/stats</a> - סטטיסטיקות מתקדמות
            </div>

            <div class="endpoint">
                <span class="method">GET</span>
                <a href="/api/performance">/api/performance</a> - נתוני ביצועים
            </div>

            <div class="endpoint">
                <span class="method post">POST</span>
                /api/simulate/call - דמיה של שיחה
            </div>

            <div class="endpoint">
                <span class="method post">POST</span>
                /api/simulate/full-flow - זרימה מלאה
            </div>

            <div class="endpoint">
                <span class="method post">POST</span>
                /api/assign-technician - הקצאת טכנאי
            </div>
        </div>

        <div class="api-list">
            <h2>🧪 בדיקות מהירות</h2>
            <p>curl -X POST http://localhost:8001/api/simulate/call</p>
            <p>curl http://localhost:8001/api/stats</p>
        </div>
    </div>
</body>
</html>
        """


def run_advanced_server():
    """הרצת השירת המתקדם"""
    server_address = ("localhost", 8001)
    httpd = HTTPServer(server_address, SmartAgentAdvancedAPI)

    print("🚀 SmartAgent Advanced API Server Starting...")
    print(f"📡 Server running at: http://localhost:8001")
    print(f"📊 Advanced Dashboard: http://localhost:8001/advanced")
    print(f"🔗 API Endpoints: http://localhost:8001/")
    print(f"❤️ Health Check: http://localhost:8001/health")
    print()
    print("🧪 Quick Tests:")
    print("  📞 Simulate Call: curl -X POST http://localhost:8001/api/simulate/call")
    print("  👥 View Technicians: curl http://localhost:8001/api/technicians")
    print("  📊 Statistics: curl http://localhost:8001/api/stats")
    print()
    print("⏹️ Press Ctrl+C to stop")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        httpd.shutdown()


if __name__ == "__main__":
    run_advanced_server()

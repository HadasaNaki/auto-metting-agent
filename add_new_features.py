#!/usr/bin/env python3
"""
SmartAgent - Enhanced Features
הוספת תכונות מתקדמות לאתר
"""

import json
import sqlite3
from datetime import datetime, timedelta
import random


class SmartAgentEnhancer:
    def __init__(self):
        self.db_file = "enhanced_smartagent.db"
        self.setup_enhanced_database()

    def setup_enhanced_database(self):
        """הקמת מסד נתונים משופר"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        # טבלת ארגונים משופרת
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS organizations (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                domain TEXT UNIQUE,
                subscription_plan TEXT DEFAULT 'basic',
                phone_number TEXT,
                address TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT 1,
                settings JSON
            )
        """
        )

        # טבלת טכנאים
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS technicians (
                id INTEGER PRIMARY KEY,
                org_id INTEGER,
                name TEXT NOT NULL,
                phone TEXT,
                email TEXT,
                specialty TEXT,
                is_available BOOLEAN DEFAULT 1,
                current_location TEXT,
                rating REAL DEFAULT 5.0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (org_id) REFERENCES organizations (id)
            )
        """
        )

        # טבלת לקוחות משופרת
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY,
                org_id INTEGER,
                name TEXT NOT NULL,
                phone TEXT,
                email TEXT,
                address_full TEXT,
                address_city TEXT,
                address_coordinates TEXT,
                preferred_time TEXT,
                notes TEXT,
                vip_status BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (org_id) REFERENCES organizations (id)
            )
        """
        )

        # טבלת שיחות משופרת
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS calls (
                id INTEGER PRIMARY KEY,
                org_id INTEGER,
                customer_id INTEGER,
                technician_id INTEGER,
                audio_url TEXT,
                duration INTEGER,
                call_quality REAL,
                status TEXT DEFAULT 'pending',
                priority TEXT DEFAULT 'medium',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                processed_at TIMESTAMP,
                FOREIGN KEY (org_id) REFERENCES organizations (id),
                FOREIGN KEY (customer_id) REFERENCES customers (id),
                FOREIGN KEY (technician_id) REFERENCES technicians (id)
            )
        """
        )

        # טבלת תורים משופרת
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS appointments (
                id INTEGER PRIMARY KEY,
                org_id INTEGER,
                customer_id INTEGER,
                technician_id INTEGER,
                call_id INTEGER,
                date TEXT,
                time TEXT,
                duration INTEGER DEFAULT 60,
                status TEXT DEFAULT 'scheduled',
                service_type TEXT,
                estimated_cost REAL,
                actual_cost REAL,
                notes TEXT,
                location_confirmed BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (org_id) REFERENCES organizations (id),
                FOREIGN KEY (customer_id) REFERENCES customers (id),
                FOREIGN KEY (technician_id) REFERENCES technicians (id),
                FOREIGN KEY (call_id) REFERENCES calls (id)
            )
        """
        )

        # טבלת משוב ודירוגים
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY,
                appointment_id INTEGER,
                customer_rating INTEGER,
                technician_rating INTEGER,
                service_rating INTEGER,
                comments TEXT,
                would_recommend BOOLEAN,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (appointment_id) REFERENCES appointments (id)
            )
        """
        )

        conn.commit()
        conn.close()
        print("✅ Enhanced database created")

    def generate_sample_data(self):
        """יצירת נתוני דמו"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        # ארגונים לדוגמה
        orgs = [
            ("טכנאים ישראל", "teknaim.co.il", "premium", "+972-3-1234567", "תל אביב"),
            ("שירותי בית", "sherut-bayit.com", "basic", "+972-2-7654321", "ירושלים"),
            (
                "תיקונים מהירים",
                "fix-fast.co.il",
                "professional",
                "+972-4-5555555",
                "חיפה",
            ),
        ]

        for name, domain, plan, phone, address in orgs:
            cursor.execute(
                """
                INSERT OR IGNORE INTO organizations (name, domain, subscription_plan, phone_number, address)
                VALUES (?, ?, ?, ?, ?)
            """,
                (name, domain, plan, phone, address),
            )

        # טכנאים לדוגמה
        technicians = [
            (
                1,
                "יוסי לוי",
                "+972-50-1111111",
                "yossi@teknaim.co.il",
                "מקררים ומזגנים",
                "תל אביב",
                4.8,
            ),
            (
                1,
                "דנה כהן",
                "+972-50-2222222",
                "dana@teknaim.co.il",
                "מכונות כביסה",
                "פתח תקווה",
                4.9,
            ),
            (
                2,
                "אמיר שלום",
                "+972-50-3333333",
                "amir@sherut-bayit.com",
                "כללי",
                "ירושלים",
                4.5,
            ),
            (
                3,
                "שרה אברהם",
                "+972-50-4444444",
                "sara@fix-fast.co.il",
                "אלקטרוניקה",
                "חיפה",
                4.7,
            ),
        ]

        for org_id, name, phone, email, specialty, location, rating in technicians:
            cursor.execute(
                """
                INSERT OR IGNORE INTO technicians (org_id, name, phone, email, specialty, current_location, rating)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
                (org_id, name, phone, email, specialty, location, rating),
            )

        # לקוחות לדוגמה
        customers = [
            (
                1,
                "משה כהן",
                "+972-50-5555555",
                "moshe@gmail.com",
                "רחוב הרצל 123, תל אביב",
                "תל אביב",
                "32.0853,34.7818",
                "בבוקר",
                "לקוח VIP",
                1,
            ),
            (
                1,
                "רות לוי",
                "+972-50-6666666",
                "ruth@gmail.com",
                "רחוב דיזנגוף 456, תל אביב",
                "תל אביב",
                "32.0783,34.7711",
                "אחר הצהריים",
                "",
                0,
            ),
            (
                2,
                "דוד אברהם",
                "+972-50-7777777",
                "david@gmail.com",
                "רחוב יפו 789, ירושלים",
                "ירושלים",
                "31.7767,35.2345",
                "בערב",
                "",
                0,
            ),
            (
                3,
                "מרים שמש",
                "+972-50-8888888",
                "miriam@gmail.com",
                "רחוב הנשיא 321, חיפה",
                "חיפה",
                "32.7940,34.9896",
                "גמיש",
                "",
                0,
            ),
        ]

        for (
            org_id,
            name,
            phone,
            email,
            address,
            city,
            coords,
            time,
            notes,
            vip,
        ) in customers:
            cursor.execute(
                """
                INSERT OR IGNORE INTO customers (org_id, name, phone, email, address_full, address_city, address_coordinates, preferred_time, notes, vip_status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (org_id, name, phone, email, address, city, coords, time, notes, vip),
            )

        conn.commit()
        conn.close()
        print("✅ Sample data generated")

    def create_enhanced_html_dashboard(self):
        """יצירת דשבורד HTML משופר"""
        html_content = """
<!DOCTYPE html>
<html dir="rtl" lang="he">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SmartAgent - דשבורד מתקדם</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        .header { background: rgba(255,255,255,0.1); backdrop-filter: blur(10px); border-radius: 15px; padding: 20px; margin-bottom: 30px; }
        .header h1 { color: white; font-size: 2.5em; text-align: center; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); }
        .header p { color: rgba(255,255,255,0.9); text-align: center; margin-top: 10px; font-size: 1.2em; }
        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 30px; }
        .stat-card { background: rgba(255,255,255,0.15); backdrop-filter: blur(10px); border-radius: 15px; padding: 25px; color: white; transition: transform 0.3s ease; }
        .stat-card:hover { transform: translateY(-5px); }
        .stat-number { font-size: 3em; font-weight: bold; margin-bottom: 10px; }
        .stat-label { font-size: 1.1em; opacity: 0.9; }
        .actions-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-bottom: 30px; }
        .action-card { background: rgba(255,255,255,0.1); backdrop-filter: blur(10px); border-radius: 15px; padding: 25px; }
        .action-card h3 { color: white; margin-bottom: 15px; font-size: 1.4em; }
        .btn { background: linear-gradient(45deg, #FF6B6B, #4ECDC4); color: white; border: none; padding: 12px 25px; border-radius: 25px; cursor: pointer; font-size: 1em; transition: all 0.3s ease; margin: 5px; display: inline-block; text-decoration: none; }
        .btn:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(0,0,0,0.3); }
        .recent-activity { background: rgba(255,255,255,0.1); backdrop-filter: blur(10px); border-radius: 15px; padding: 25px; }
        .recent-activity h3 { color: white; margin-bottom: 20px; font-size: 1.4em; }
        .activity-item { background: rgba(255,255,255,0.1); border-radius: 10px; padding: 15px; margin-bottom: 10px; color: white; }
        .activity-time { font-size: 0.9em; opacity: 0.7; }
        .quick-stats { display: flex; justify-content: space-around; margin: 20px 0; }
        .quick-stat { text-align: center; color: white; }
        .emoji { font-size: 2em; display: block; margin-bottom: 10px; }
        .status-indicator { width: 10px; height: 10px; border-radius: 50%; display: inline-block; margin-left: 10px; }
        .status-online { background-color: #4CAF50; }
        .status-busy { background-color: #FF9800; }
        .status-offline { background-color: #F44336; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 SmartAgent - דשבורד מתקדם</h1>
            <p>מערכת ניהול שיחות וטכנאים חכמה</p>
            <div class="quick-stats">
                <div class="quick-stat">
                    <span class="emoji">📞</span>
                    <div>שיחות היום</div>
                    <div id="today-calls">12</div>
                </div>
                <div class="quick-stat">
                    <span class="emoji">⚡</span>
                    <div>תורים פעילים</div>
                    <div id="active-appointments">8</div>
                </div>
                <div class="quick-stat">
                    <span class="emoji">👥</span>
                    <div>טכנאים זמינים</div>
                    <div id="available-technicians">3</div>
                </div>
                <div class="quick-stat">
                    <span class="emoji">⭐</span>
                    <div>שביעות רצון</div>
                    <div id="satisfaction">4.8/5</div>
                </div>
            </div>
        </div>

        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number" id="total-calls">47</div>
                <div class="stat-label">סה״כ שיחות</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" id="processed-calls">42</div>
                <div class="stat-label">שיחות מעובדות</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" id="scheduled-appointments">38</div>
                <div class="stat-label">תורים מתוזמנים</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" id="satisfied-customers">92%</div>
                <div class="stat-label">לקוחות מרוצים</div>
            </div>
        </div>

        <div class="actions-grid">
            <div class="action-card">
                <h3>🎯 פעולות מהירות</h3>
                <button class="btn" onclick="simulateCall()">דמה שיחה חדשה</button>
                <button class="btn" onclick="processWorkflow()">הרץ זרימה מלאה</button>
                <button class="btn" onclick="refreshData()">רענן נתונים</button>
                <button class="btn" onclick="viewReports()">דוחות מתקדמים</button>
            </div>

            <div class="action-card">
                <h3>📊 ניהול טכנאים</h3>
                <button class="btn" onclick="viewTechnicians()">רשימת טכנאים</button>
                <button class="btn" onclick="assignJobs()">הקצאת עבודות</button>
                <button class="btn" onclick="trackLocation()">מעקב מיקום</button>
                <button class="btn" onclick="performanceReview()">סקירת ביצועים</button>
            </div>

            <div class="action-card">
                <h3>💼 ניהול לקוחות</h3>
                <button class="btn" onclick="viewCustomers()">רשימת לקוחות</button>
                <button class="btn" onclick="addCustomer()">הוסף לקוח חדש</button>
                <button class="btn" onclick="sendMessage()">שלח הודעה</button>
                <button class="btn" onclick="feedbackAnalysis()">ניתוח משוב</button>
            </div>
        </div>

        <div class="recent-activity">
            <h3>📈 פעילות אחרונה</h3>
            <div id="activity-list">
                <div class="activity-item">
                    <strong>שיחה חדשה התקבלה</strong> - משה כהן, תיקון מקרר
                    <div class="activity-time">לפני 5 דקות</div>
                    <span class="status-indicator status-online"></span>
                </div>
                <div class="activity-item">
                    <strong>תור נקבע בהצלחה</strong> - רות לוי, מזגן לא עובד
                    <div class="activity-time">לפני 12 דקות</div>
                    <span class="status-indicator status-busy"></span>
                </div>
                <div class="activity-item">
                    <strong>טכנאי יוסי סיים עבודה</strong> - דירוג 5 כוכבים
                    <div class="activity-time">לפני 20 דקות</div>
                    <span class="status-indicator status-online"></span>
                </div>
                <div class="activity-item">
                    <strong>הודעת SMS נשלחה</strong> - אישור תור לדוד אברהם
                    <div class="activity-time">לפני 25 דקות</div>
                    <span class="status-indicator status-online"></span>
                </div>
            </div>
        </div>
    </div>

    <script>
        function simulateCall() {
            fetch('/api/simulate/call', { method: 'POST' })
                .then(response => response.json())
                .then(data => {
                    alert('✅ שיחה חדשה נוצרה בהצלחה!\\nמזהה שיחה: ' + (data.call_id || 'חדש'));
                    refreshData();
                })
                .catch(err => alert('❌ שגיאה: ' + err.message));
        }

        function processWorkflow() {
            fetch('/api/simulate/full-flow', { method: 'POST' })
                .then(response => response.json())
                .then(data => {
                    alert('✅ זרימה מלאה הושלמה!\\nלקוח: ' + (data.customer || 'חדש') + '\\nתור: ' + (data.appointment || 'נקבע'));
                    refreshData();
                })
                .catch(err => alert('❌ שגיאה: ' + err.message));
        }

        function refreshData() {
            fetch('/api/stats')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('total-calls').textContent = data.total_calls || '47';
                    document.getElementById('processed-calls').textContent = data.processed_calls || '42';
                    document.getElementById('scheduled-appointments').textContent = data.appointments || '38';

                    // עדכון פעילות אחרונה
                    updateRecentActivity();
                })
                .catch(err => console.error('Error refreshing data:', err));
        }

        function updateRecentActivity() {
            const activities = [
                'שיחה חדשה מעובדת - ' + ['אמיר שמש', 'דנה רוזן', 'יוסי כהן'][Math.floor(Math.random() * 3)],
                'תור נקבע - ' + ['מכונת כביסה', 'מקרר', 'מזגן'][Math.floor(Math.random() * 3)],
                'טכנאי סיים עבודה - דירוג ' + (4 + Math.random()).toFixed(1) + ' כוכבים',
                'הודעה נשלחה ללקוח - אישור הגעה'
            ];

            const activityList = document.getElementById('activity-list');
            const newActivity = document.createElement('div');
            newActivity.className = 'activity-item';
            newActivity.innerHTML = `
                <strong>${activities[Math.floor(Math.random() * activities.length)]}</strong>
                <div class="activity-time">עכשיו</div>
                <span class="status-indicator status-online"></span>
            `;
            activityList.insertBefore(newActivity, activityList.firstChild);

            if (activityList.children.length > 6) {
                activityList.removeChild(activityList.lastChild);
            }
        }

        function viewTechnicians() { alert('📋 פתיחת ממשק ניהול טכנאים...'); }
        function assignJobs() { alert('⚡ פתיחת מערכת הקצאת עבודות...'); }
        function trackLocation() { alert('📍 פתיחת מעקב מיקום בזמן אמת...'); }
        function performanceReview() { alert('📊 פתיחת דוח ביצועי טכנאים...'); }
        function viewCustomers() { alert('👥 פתיחת רשימת לקוחות...'); }
        function addCustomer() { alert('➕ פתיחת טופס לקוח חדש...'); }
        function sendMessage() { alert('💬 פתיחת מערכת הודעות...'); }
        function feedbackAnalysis() { alert('⭐ פתיחת ניתוח משוב לקוחות...'); }
        function viewReports() { alert('📈 פתיחת דוחות מתקדמים...'); }

        // רענון אוטומטי כל 30 שניות
        setInterval(refreshData, 30000);

        // רענון נתונים בטעינה
        window.onload = refreshData;
    </script>
</body>
</html>
        """

        with open("enhanced_dashboard.html", "w", encoding="utf-8") as f:
            f.write(html_content)
        print("✅ Enhanced dashboard created: enhanced_dashboard.html")

    def run_enhancement(self):
        """הרצת שיפורים"""
        print("🚀 Starting SmartAgent Enhancement...")
        self.generate_sample_data()
        self.create_enhanced_html_dashboard()
        print("🎉 Enhancement completed!")
        print("\n📋 Next steps:")
        print("1. פתח את enhanced_dashboard.html בדפדפן")
        print("2. בדוק את הפונקציות החדשות")
        print("3. השתמש ב-API endpoints החדשים")


if __name__ == "__main__":
    enhancer = SmartAgentEnhancer()
    enhancer.run_enhancement()

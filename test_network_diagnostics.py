#!/usr/bin/env python3
"""
Network connectivity troubleshooting and alternative solutions
"""

import subprocess
import sys
import json
from pathlib import Path


def test_network_connectivity():
    """Test various network connections"""
    print("🌐 Testing network connectivity...")

    hosts_to_test = [
        ("pypi.org", "PyPI main"),
        ("pypi.python.org", "PyPI Python"),
        ("files.pythonhosted.org", "PyPI files"),
        ("github.com", "GitHub"),
        ("google.com", "Google DNS"),
        ("8.8.8.8", "Google Public DNS"),
    ]

    results = {}

    for host, description in hosts_to_test:
        try:
            result = subprocess.run(
                ["ping", "-n", "1", host],  # Windows ping
                capture_output=True,
                text=True,
                timeout=10,
            )

            if result.returncode == 0:
                results[host] = "✅ Reachable"
            else:
                results[host] = "❌ Unreachable"

        except subprocess.TimeoutExpired:
            results[host] = "⏰ Timeout"
        except Exception as e:
            results[host] = f"❌ Error: {e}"

        print(f"  {description} ({host}): {results[host]}")

    return results


def test_dns_resolution():
    """Test DNS resolution"""
    print("\n🔍 Testing DNS resolution...")

    hosts = ["pypi.org", "github.com"]

    for host in hosts:
        try:
            result = subprocess.run(
                ["nslookup", host], capture_output=True, text=True, timeout=10
            )

            if "Non-authoritative answer" in result.stdout:
                print(f"  ✅ {host}: DNS resolves correctly")
            else:
                print(f"  ❌ {host}: DNS resolution issues")
                print(f"    Output: {result.stdout[:100]}...")

        except Exception as e:
            print(f"  ❌ {host}: DNS test failed - {e}")


def check_proxy_settings():
    """Check if proxy settings are configured"""
    print("\n🔧 Checking proxy settings...")

    proxy_vars = ["HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy"]

    found_proxy = False
    for var in proxy_vars:
        try:
            result = subprocess.run(
                ["echo", f"%{var}%"], capture_output=True, text=True, shell=True
            )

            value = result.stdout.strip()
            if value and value != f"%{var}%":
                print(f"  ✅ {var}: {value}")
                found_proxy = True
            else:
                print(f"  ❌ {var}: Not set")

        except Exception as e:
            print(f"  ❌ {var}: Error checking - {e}")

    if not found_proxy:
        print("\n💡 No proxy settings found. If you're behind a corporate firewall:")
        print("   You may need to configure proxy settings.")
        print("   Contact your IT department for proxy details.")


def test_pip_alternatives():
    """Test alternative pip installation methods"""
    print("\n📦 Testing pip alternative approaches...")

    # Test if we can at least check pip config
    try:
        result = subprocess.run(
            ["pip", "config", "list"], capture_output=True, text=True, timeout=10
        )
        print(f"  ✅ pip config accessible")
        if result.stdout.strip():
            print(f"    Current config: {result.stdout}")
        else:
            print("    No custom config found")
    except Exception as e:
        print(f"  ❌ pip config test failed: {e}")

    # Suggest offline installation
    print("\n💡 Alternative installation approaches:")
    print("   1. Download wheel files manually from PyPI website")
    print("   2. Use corporate package mirror if available")
    print("   3. Install from local .whl files")
    print("   4. Use conda instead of pip")
    print("   5. Use Docker with pre-built images")


def suggest_solutions():
    """Suggest solutions based on network test results"""
    print("\n🛠️  Suggested solutions:")

    print("\n1. 🔗 Corporate Network Solutions:")
    print("   - Contact IT for proxy configuration")
    print("   - Request whitelist for pypi.org, github.com")
    print("   - Use corporate package repository if available")

    print("\n2. 🐳 Docker-based Development:")
    print("   - Use pre-built Docker images")
    print("   - Build images on unrestricted network, copy to restricted environment")
    print("   - Use Docker Hub images instead of building from scratch")

    print("\n3. 📥 Offline Installation:")
    print("   - Download packages on unrestricted machine")
    print("   - Transfer .whl files manually")
    print("   - Install using: pip install --find-links /path/to/wheels package_name")

    print("\n4. 🐍 Alternative Python Package Managers:")
    print("   - conda (often has different network policies)")
    print("   - pipenv with custom indexes")
    print("   - poetry with custom repositories")


def create_offline_requirements():
    """Create a guide for offline installation"""
    print("\n📝 Creating offline installation guide...")

    offline_guide = """
# SmartAgent Offline Installation Guide

## Prerequisites
1. Python 3.11+ installed
2. Basic packages: pip, setuptools, wheel

## Core Dependencies (download these .whl files manually)
```
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
pydantic==2.5.0
celery==5.3.4
redis==5.0.1
```

## Manual Installation Steps

### 1. Download packages on unrestricted machine:
```bash
pip download -r requirements.txt -d ./wheels/
```

### 2. Transfer 'wheels' folder to restricted machine

### 3. Install from local wheels:
```bash
pip install --find-links ./wheels/ --no-index fastapi
pip install --find-links ./wheels/ --no-index uvicorn
# ... repeat for all packages
```

### 4. Alternative: Use Docker
```bash
# On unrestricted machine:
docker build -t smartagent-backend ./backend
docker save smartagent-backend > smartagent-backend.tar

# On restricted machine:
docker load < smartagent-backend.tar
```

## Testing Without External Dependencies
- Run: python test_structure.py
- Run: python test_mock_functionality.py
- These tests validate the code structure without network calls

## Minimal Development Setup
1. Use local SQLite instead of PostgreSQL
2. Use in-memory Redis simulation
3. Mock external API calls (Twilio, OpenAI)
4. Skip actual audio transcription for testing
"""

    try:
        with open("OFFLINE_INSTALLATION.md", "w", encoding="utf-8") as f:
            f.write(offline_guide)
        print("  ✅ Created OFFLINE_INSTALLATION.md")
    except Exception as e:
        print(f"  ❌ Failed to create guide: {e}")


def create_development_env_script():
    """Create a script for local development without external dependencies"""
    print("\n🧪 Creating local development environment script...")

    dev_script = '''#!/usr/bin/env python3
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

        print("\\n📊 Demo Results:")
        print(f"Call ID: {call_id}")
        print(f"Transcript: {transcript_result['text'][:50]}...")
        print(f"Customer: {extraction_result['customer']['name']}")
        print(f"Device: {extraction_result['device']['category']}")
        print(f"Appointment: {extraction_result['appointment']['date']} {extraction_result['appointment']['time']}")

        print("\\n🎉 Local demo completed successfully!")

if __name__ == "__main__":
    api = MockSmartAgentAPI()
    api.run_demo()
'''

    try:
        with open("dev_server_mock.py", "w", encoding="utf-8") as f:
            f.write(dev_script)
        print("  ✅ Created dev_server_mock.py")
    except Exception as e:
        print(f"  ❌ Failed to create dev script: {e}")


def main():
    """Run network diagnostics and create solutions"""
    print("🔍 SmartAgent Network Diagnostics & Solutions\n")

    # Test network connectivity
    connectivity_results = test_network_connectivity()

    # Test DNS
    test_dns_resolution()

    # Check proxy settings
    check_proxy_settings()

    # Test pip alternatives
    test_pip_alternatives()

    # Suggest solutions
    suggest_solutions()

    # Create offline guides
    create_offline_requirements()
    create_development_env_script()

    print("\n🎯 Summary:")
    reachable_hosts = sum(
        1 for result in connectivity_results.values() if "Reachable" in result
    )
    total_hosts = len(connectivity_results)

    if reachable_hosts == 0:
        print("❌ No external connectivity detected")
        print("✅ Use offline/mock development approach")
    elif reachable_hosts < total_hosts:
        print(
            f"⚠️  Partial connectivity ({reachable_hosts}/{total_hosts} hosts reachable)"
        )
        print("✅ Try proxy configuration or alternative mirrors")
    else:
        print("✅ Full connectivity available")
        print("✅ Standard pip install should work")

    print("\n📋 Next Steps:")
    print("1. Run: python dev_server_mock.py  (for local testing)")
    print("2. Check: OFFLINE_INSTALLATION.md  (for offline setup)")
    print("3. Contact IT for proxy/firewall configuration")


if __name__ == "__main__":
    main()

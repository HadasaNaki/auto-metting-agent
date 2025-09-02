
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

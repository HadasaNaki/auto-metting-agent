# SmartAgent

מערכת SaaS מתקדמת לניהול טכנאים בתחום השירות עם יכולות עיבוד שיחות אוטומטי, תמלול, הפקת מידע באמצעות AI, וסנכרון יומנים.

## ארכיטקטורה

### טכנולוגיות עיקריות
- **Backend**: Python FastAPI, SQLAlchemy 2.0, Pydantic v2
- **Workers**: Celery + Redis
- **Database**: PostgreSQL
- **Storage**: MinIO/S3
- **Frontend**: Next.js 14, React, TypeScript, TailwindCSS
- **AI**: OpenAI GPT + Whisper
- **Integrations**: Twilio, Google Calendar, Outlook
- **Infrastructure**: Docker, docker-compose

### רכיבים מרכזיים
1. **API Backend** - FastAPI עם JWT auth ו-multi-tenancy
2. **Async Workers** - עיבוד אסינכרוני של תמלול והפקת מידע
3. **Frontend Web App** - ממשק משתמש מודרני ונגיש
4. **Telephony Integration** - אינטגרציה עם ספקי טלפוניה
5. **Calendar Sync** - סנכרון דו-כיווני עם Google/Outlook
6. **Messaging** - שליחת SMS/WhatsApp

## התקנה והפעלה

### דרישות מוקדמות
- Docker & Docker Compose
- Git

### הפעלה מהירה

1. **שכפול הפרויקט**
   ```bash
   git clone <repo-url>
   cd Smart\ Agent
   ```

2. **הגדרת environment**
   ```bash
   cp infra/.env.example infra/.env
   # ערוך את infra/.env עם המפתחות הנדרשים
   ```

3. **הפעלת המערכת**
   ```bash
   make up
   # או:
   cd infra && docker-compose up --build
   ```

4. **טעינת נתוני demo**
   ```bash
   python infra/seed_demo.py
   ```

### גישה למערכת
- **API Documentation**: http://localhost:8000/docs
- **Frontend**: http://localhost:3000
- **Database**: localhost:5432 (postgres/smart:agent)
- **Redis**: localhost:6379
- **MinIO**: localhost:9000 (minio/minio123)

## API עיקריים

### Authentication
```bash
# רישום ארגון חדש
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@company.com","password":"123456","full_name":"Admin User","org_name":"My Company"}'

# התחברות
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@company.com","password":"123456"}'
```

### Telephony Webhook
```bash
# webhook מ-Twilio
curl -X POST http://localhost:8000/calls/webhook/twilio \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "recordingUrl": "https://api.twilio.com/recording.mp3",
    "callSid": "CA123456789",
    "from": "+972501234567",
    "to": "+972599999999",
    "startTime": "2025-08-30T12:00:00Z",
    "duration": 120
  }'
```

### תמלול והפקת מידע
```bash
# צפייה בשיחה
curl -X GET http://localhost:8000/calls/1 \
  -H "Authorization: Bearer <token>"

# קבלת תמלול
curl -X GET http://localhost:8000/transcripts/1 \
  -H "Authorization: Bearer <token>"

# צפייה במידע מופק
curl -X GET http://localhost:8000/extractions/1 \
  -H "Authorization: Bearer <token>"
```

### יומן ופגישות
```bash
# יומן יומי
curl -X GET "http://localhost:8000/calendar/agenda?day=2025-09-05" \
  -H "Authorization: Bearer <token>"

# יצירת פגישה
curl -X POST http://localhost:8000/appointments \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "customer_id": 1,
    "start_at": "2025-09-05T15:00:00",
    "duration_minutes": 60,
    "title": "תיקון מקרר",
    "notes": "לקוח: משה כהן, כתובת: הרצל 10 תל אביב"
  }'
```

## תהליך עבודה מלא

### 1. קליטת שיחה
- Webhook מ-Twilio → יצירת רשומת Call
- הורדת קובץ אודיו ל-S3
- הפעלת task תמלול (Celery)

### 2. תמלול ועיבוד
- Whisper → טקסט מתומלל
- LLM (GPT) → JSON מובנה עם:
  - פרטי לקוח
  - פרטי מכשיר/בעיה
  - מחיר מוסכם
  - תיאום פגישה
  - סיכום חופשי

### 3. יצירת פגישה
- אם נמצאו תאריך/שעה → יצירת Appointment
- סנכרון ליומן חיצוני (Google/Outlook)
- שליחת אישור ללקוח (SMS/WhatsApp)

### 4. ניהול יומי
- לוח יומן עם פגישות ו-follow-ups
- ניהול קריאות שירות (Jobs)
- חיפוש לקוחות ורשומות

## מבנה נתונים

### טבלאות עיקריות
- `organizations` - ארגונים (multi-tenancy)
- `users` - משתמשים/טכנאים
- `customers` - לקוחות קצה
- `calls` - שיחות טלפון
- `transcripts` - תמלולים
- `extractions` - מידע מובנה מ-LLM
- `jobs` - קריאות שירות
- `appointments` - פגישות
- `messages` - הודעות שנשלחו

### JSON Schema (תוצאת LLM)
```json
{
  "customer": {
    "name": "משה כהן",
    "phone": "+972501234567",
    "address": {"line1": "הרצל 10", "city": "תל אביב"}
  },
  "device": {
    "category": "מקרר",
    "brand": "Samsung",
    "issue": "לא מקרר",
    "urgency": "high"
  },
  "quote": {"agreed_price": 400, "currency": "ILS"},
  "appointment": {
    "date": "2025-09-05",
    "time": "15:00",
    "is_confirmed_by_customer": true
  },
  "free_text_summary_he": "תואם ביקור לתיקון מקרר...",
  "confidence": 0.88
}
```

## אבטחה ו-Multi-Tenancy

- JWT tokens עם org_id embedded
- כל query מסונן לפי ארגון
- Rate limiting על webhooks ו-auth
- RBAC: owner/admin/technician roles
- Audit logging לפעולות רגישות

## בדיקות

### Backend Tests
```bash
cd backend
pytest tests/ -v
```

### Frontend E2E Tests
```bash
cd frontend
npx playwright test
```

### Integration Tests
```bash
# בדיקת webhook מלא
./scripts/test_webhook.sh
```

## פיתוח ו-Contributing

### מבנה Monorepo
```
Smart Agent/
├── infra/          # Docker, Makefile, configs
├── backend/        # FastAPI application
├── worker/         # Celery workers
├── frontend/       # Next.js application
└── docs/          # Documentation
```

### הוספת פיצ'רים
1. עדכון models.py (אם נדרש)
2. הרצת migration: `alembic revision --autogenerate`
3. עדכון schemas.py ו-API endpoints
4. הוספת tests
5. עדכון frontend components

### Deploy Production
1. הגדרת environment variables
2. הרצת migrations
3. Build ו-deploy containers
4. הגדרת monitoring ו-logging

## תמיכה

לשאלות או בעיות:
1. בדוק את הלוגים: `docker-compose logs <service>`
2. ווודא שכל הסרביסים פועלים: `docker-compose ps`
3. בדוק חיבור DB: `docker-compose exec db psql -U smart smartagent`

---

**הערה**: זהו MVP ראשוני. פיצ'רים נוספים כמו תשלומים, sentiment analysis, ו-team scheduling יתווספו בגרסאות עתידיות.

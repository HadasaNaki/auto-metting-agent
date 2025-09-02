# SmartAgent Architecture

## Mermaid Diagrams

### Component Map
```mermaid
flowchart LR
  subgraph Client["Clients"]
    W[Web App (Next.js)]
    M[Mobile (React Native - אופציונלי)]
  end

  subgraph API["Backend API (FastAPI)"]
    Auth[Auth & Multi-Tenant]
    Calls[Calls & Uploads]
    NLP[LLM Orchestrator]
    Calendar[Calendar Integrations]
    Msg[SMS/WhatsApp]
    CRM[CRM & Scheduling]
    Webhooks[Webhooks (Telephony, Calendars)]
  end

  subgraph Worker["Async Workers (Celery/RQ)"]
    Transcribe[Transcription Jobs (Whisper/STT)]
    Extract[Info Extraction (LLM)]
    Notify[Notifications/Reminders]
    Sync[Calendar/CRM Sync]
  end

  subgraph Data["Data Layer"]
    PG[(PostgreSQL)]
    Redis[(Redis)]
    S3[(Object Storage - Recordings/Transcripts)]
  end

  subgraph Telephony["Telephony"]
    Twilio[Twilio/Vonage/Plivo]
  end

  subgraph Providers["External Providers"]
    GCal[Google Calendar]
    O365[Outlook/Office 365]
    WA[WhatsApp Business API]
    SMS[SMS Provider]
    Pay[Stripe/PayPal - אופציונלי]
  end

  W -->|HTTPS| API
  M -->|HTTPS| API

  API <--> PG
  API <--> Redis
  API <--> S3

  Calls --> Worker
  NLP --> Worker
  Worker --> S3
  Worker --> PG
  Worker --> Calendar
  Worker --> Msg

  Telephony -->|Webhook| Webhooks
  Webhooks --> Calls
  Calendar <--> GCal
  Calendar <--> O365
  Msg --> WA
  Msg --> SMS
```

### Sequence Diagram
```mermaid
sequenceDiagram
  participant C as לקוח
  participant T as טכנאי (אפליקציה/טלפון)
  participant Tel as ספק טלפוניה
  participant API as Backend API
  participant W as Worker
  participant STT as Transcription
  participant LLM as LLM
  participant DB as DB
  participant Cal as Google/Outlook

  C->>T: שיחה טלפונית
  T->>Tel: הקלטה/ניתוב מספרים
  Tel-->>API: Webhook + לינק להקלטה
  API->>S3: שמירת הקלטה
  API->>W: טריגר משימת תמלול
  W->>STT: תמלול אודיו
  STT-->>W: טקסט מתומלל
  W->>LLM: הפקת ישויות/שדות + סיכום
  LLM-->>W: JSON מובנה + סיכום
  W->>DB: שמירת Call, Transcript, Summary, Appointment Draft
  W->>Cal: יצירת אירוע ביומן (אם קיימת שעה/תאריך)
  Cal-->>W: אישור אירוע + ID
  W->>API: עדכון סטטוסים
  API-->>T: התראה/תצוגה בלוח
  W->>לקוח: SMS/WhatsApp אישור פגישה (אופציונלי)
```

-- SmartAgent Database Initialization
-- אתחול מסד נתונים SmartAgent

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Organizations table - טבלת ארגונים
CREATE TABLE IF NOT EXISTS organizations (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    domain VARCHAR(255) UNIQUE,
    subscription_plan VARCHAR(50) DEFAULT 'basic',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT true
);

-- Users table - טבלת משתמשים
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    org_id INTEGER REFERENCES organizations(id),
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'technician',
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Customers table - טבלת לקוחות
CREATE TABLE IF NOT EXISTS customers (
    id SERIAL PRIMARY KEY,
    org_id INTEGER REFERENCES organizations(id),
    name VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    email VARCHAR(255),
    address_street VARCHAR(500),
    address_city VARCHAR(100),
    address_coordinates POINT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Calls table - טבלת שיחות
CREATE TABLE IF NOT EXISTS calls (
    id SERIAL PRIMARY KEY,
    org_id INTEGER REFERENCES organizations(id),
    customer_id INTEGER REFERENCES customers(id),
    twilio_call_sid VARCHAR(255) UNIQUE,
    audio_url TEXT,
    duration INTEGER,
    status VARCHAR(50) DEFAULT 'pending',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    processed_at TIMESTAMP WITH TIME ZONE
);

-- Transcripts table - טבלת תמלילים
CREATE TABLE IF NOT EXISTS transcripts (
    id SERIAL PRIMARY KEY,
    call_id INTEGER REFERENCES calls(id),
    text TEXT,
    confidence DECIMAL(3,2),
    language VARCHAR(10) DEFAULT 'he',
    segments JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Extractions table - טבלת חילוצי מידע
CREATE TABLE IF NOT EXISTS extractions (
    id SERIAL PRIMARY KEY,
    call_id INTEGER REFERENCES calls(id),
    customer_name VARCHAR(255),
    customer_phone VARCHAR(20),
    device_category VARCHAR(100),
    device_issue TEXT,
    urgency_level VARCHAR(20),
    appointment_date DATE,
    appointment_time TIME,
    confidence DECIMAL(3,2),
    extracted_data JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Jobs table - טבלת עבודות אסינכרוניות
CREATE TABLE IF NOT EXISTS jobs (
    id SERIAL PRIMARY KEY,
    org_id INTEGER REFERENCES organizations(id),
    call_id INTEGER REFERENCES calls(id),
    job_type VARCHAR(50) NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    celery_task_id VARCHAR(255),
    result JSONB,
    error_message TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP WITH TIME ZONE
);

-- Appointments table - טבלת תורים
CREATE TABLE IF NOT EXISTS appointments (
    id SERIAL PRIMARY KEY,
    org_id INTEGER REFERENCES organizations(id),
    customer_id INTEGER REFERENCES customers(id),
    technician_id INTEGER REFERENCES users(id),
    extraction_id INTEGER REFERENCES extractions(id),
    date DATE NOT NULL,
    time TIME NOT NULL,
    status VARCHAR(50) DEFAULT 'scheduled',
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Messages table - טבלת הודעות
CREATE TABLE IF NOT EXISTS messages (
    id SERIAL PRIMARY KEY,
    org_id INTEGER REFERENCES organizations(id),
    customer_id INTEGER REFERENCES customers(id),
    appointment_id INTEGER REFERENCES appointments(id),
    message_type VARCHAR(20) NOT NULL,
    recipient VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    external_id VARCHAR(255),
    sent_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Integrations table - טבלת אינטגרציות
CREATE TABLE IF NOT EXISTS integrations (
    id SERIAL PRIMARY KEY,
    org_id INTEGER REFERENCES organizations(id),
    user_id INTEGER REFERENCES users(id),
    integration_type VARCHAR(50) NOT NULL,
    credentials JSONB,
    config JSONB,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_users_org_id ON users(org_id);
CREATE INDEX IF NOT EXISTS idx_customers_org_id ON customers(org_id);
CREATE INDEX IF NOT EXISTS idx_calls_org_id ON calls(org_id);
CREATE INDEX IF NOT EXISTS idx_calls_customer_id ON calls(customer_id);
CREATE INDEX IF NOT EXISTS idx_calls_status ON calls(status);
CREATE INDEX IF NOT EXISTS idx_appointments_org_id ON appointments(org_id);
CREATE INDEX IF NOT EXISTS idx_appointments_date ON appointments(date);
CREATE INDEX IF NOT EXISTS idx_messages_org_id ON messages(org_id);

-- Insert demo organization and user
INSERT INTO organizations (name, domain, subscription_plan)
VALUES ('Demo Technicians', 'demo.smartagent.co.il', 'premium')
ON CONFLICT (domain) DO NOTHING;

INSERT INTO users (org_id, email, name, hashed_password, role)
SELECT 1, 'admin@demo.smartagent.co.il', 'Admin User',
       '$argon2id$v=19$m=65536,t=3,p=4$demo_hash', 'admin'
WHERE NOT EXISTS (SELECT 1 FROM users WHERE email = 'admin@demo.smartagent.co.il');

-- Create a test customer
INSERT INTO customers (org_id, name, phone, address_city)
SELECT 1, 'לקוח דמו', '+972501234567', 'תל אביב'
WHERE NOT EXISTS (SELECT 1 FROM customers WHERE phone = '+972501234567');

COMMIT;

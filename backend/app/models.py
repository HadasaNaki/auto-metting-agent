from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    Boolean,
    JSON,
    Index,
    Text,
    Decimal,
    Enum as SQLEnum,
)
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func
from datetime import datetime
import enum


Base = declarative_base()


class RoleEnum(enum.Enum):
    OWNER = "owner"
    ADMIN = "admin"
    TECHNICIAN = "technician"


class CallStatusEnum(enum.Enum):
    PENDING_TRANSCRIPTION = "pending_transcription"
    TRANSCRIBING = "transcribing"
    EXTRACTING = "extracting"
    COMPLETED = "completed"
    FAILED = "failed"


class JobStatusEnum(enum.Enum):
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    timezone = Column(String(50), default="Asia/Jerusalem")
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    users = relationship("User", back_populates="organization")
    customers = relationship("Customer", back_populates="organization")
    calls = relationship("Call", back_populates="organization")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    org_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255))
    role = Column(SQLEnum(RoleEnum), default=RoleEnum.TECHNICIAN)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    organization = relationship("Organization", back_populates="users")


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True)
    org_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    name = Column(String(255))
    phone = Column(String(50))
    email = Column(String(255))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    organization = relationship("Organization", back_populates="customers")
    addresses = relationship("Address", back_populates="customer")
    devices = relationship("Device", back_populates="customer")
    calls = relationship("Call", back_populates="customer")
    jobs = relationship("Job", back_populates="customer")


class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True)
    org_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    line1 = Column(String(255))
    city = Column(String(100))
    postal_code = Column(String(20))
    notes = Column(Text)
    created_at = Column(DateTime, default=func.now())

    customer = relationship("Customer", back_populates="addresses")


class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True)
    org_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    category = Column(String(100))  # מקרר, מזגן, etc
    brand = Column(String(100))
    model = Column(String(100))
    serial_number = Column(String(100))
    notes = Column(Text)
    created_at = Column(DateTime, default=func.now())

    customer = relationship("Customer", back_populates="devices")


class Call(Base):
    __tablename__ = "calls"

    id = Column(Integer, primary_key=True)
    org_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    call_sid = Column(String(100))  # Twilio/external ID
    from_number = Column(String(50))
    to_number = Column(String(50))
    audio_url = Column(String(500))
    duration_seconds = Column(Integer)
    status = Column(
        SQLEnum(CallStatusEnum), default=CallStatusEnum.PENDING_TRANSCRIPTION
    )
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    organization = relationship("Organization", back_populates="calls")
    customer = relationship("Customer", back_populates="calls")
    transcripts = relationship("Transcript", back_populates="call")
    extractions = relationship("Extraction", back_populates="call")


class Transcript(Base):
    __tablename__ = "transcripts"

    id = Column(Integer, primary_key=True)
    org_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    call_id = Column(Integer, ForeignKey("calls.id"), nullable=False)
    text = Column(Text)
    language = Column(String(10), default="he")
    confidence = Column(Decimal(3, 2))
    created_at = Column(DateTime, default=func.now())

    call = relationship("Call", back_populates="transcripts")


class Extraction(Base):
    __tablename__ = "extractions"

    id = Column(Integer, primary_key=True)
    org_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    call_id = Column(Integer, ForeignKey("calls.id"), nullable=False)
    extracted_data = Column(JSON)  # Structured JSON from LLM
    summary_he = Column(Text)
    confidence = Column(Decimal(3, 2))
    created_at = Column(DateTime, default=func.now())

    call = relationship("Call", back_populates="extractions")


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True)
    org_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    call_id = Column(Integer, ForeignKey("calls.id"))
    title = Column(String(255))
    description = Column(Text)
    status = Column(SQLEnum(JobStatusEnum), default=JobStatusEnum.DRAFT)
    agreed_price = Column(Decimal(10, 2))
    currency = Column(String(3), default="ILS")
    priority = Column(String(20), default="medium")  # low, medium, high, urgent
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    customer = relationship("Customer", back_populates="jobs")
    appointments = relationship("Appointment", back_populates="job")


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True)
    org_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id"))
    customer_id = Column(Integer, ForeignKey("customers.id"))
    technician_id = Column(Integer, ForeignKey("users.id"))
    start_at = Column(DateTime, nullable=False)
    duration_minutes = Column(Integer, default=60)
    title = Column(String(255))
    notes = Column(Text)
    calendar_event_id = Column(String(255))  # External calendar ID
    is_confirmed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    job = relationship("Job", back_populates="appointments")


class Followup(Base):
    __tablename__ = "followups"

    id = Column(Integer, primary_key=True)
    org_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    job_id = Column(Integer, ForeignKey("jobs.id"))
    due_at = Column(DateTime, nullable=False)
    reason = Column(String(255))
    channel = Column(String(20))  # sms, whatsapp, email, call
    is_completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    org_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    channel = Column(String(20))  # sms, whatsapp, email
    to_number = Column(String(50))
    content = Column(Text)
    status = Column(String(20))  # sent, delivered, failed
    external_id = Column(String(255))
    created_at = Column(DateTime, default=func.now())


class Integration(Base):
    __tablename__ = "integrations"

    id = Column(Integer, primary_key=True)
    org_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    provider = Column(String(50))  # google, outlook, twilio, whatsapp
    config = Column(JSON)  # Tokens, settings
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True)
    org_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    action = Column(String(100))
    resource_type = Column(String(50))
    resource_id = Column(Integer)
    details = Column(JSON)
    created_at = Column(DateTime, default=func.now())


# Indexes for performance
Index("ix_customers_org_id_phone", Customer.org_id, Customer.phone)
Index("ix_calls_org_id_created_at", Call.org_id, Call.created_at)
Index("ix_appointments_org_id_start_at", Appointment.org_id, Appointment.start_at)
Index("ix_jobs_org_id_status", Job.org_id, Job.status)
Index("ix_followups_org_id_due_at", Followup.org_id, Followup.due_at)

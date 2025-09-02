from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from enum import Enum


class RoleEnum(str, Enum):
    OWNER = "owner"
    ADMIN = "admin"
    TECHNICIAN = "technician"


class CallStatusEnum(str, Enum):
    PENDING_TRANSCRIPTION = "pending_transcription"
    TRANSCRIBING = "transcribing"
    EXTRACTING = "extracting"
    COMPLETED = "completed"
    FAILED = "failed"


class JobStatusEnum(str, Enum):
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


# Auth Schemas
class UserRegister(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    org_name: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


# Customer Schemas
class CustomerCreate(BaseModel):
    name: str
    phone: Optional[str] = None
    email: Optional[EmailStr] = None


class CustomerResponse(BaseModel):
    id: int
    name: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


# Address Schema
class AddressCreate(BaseModel):
    line1: str
    city: str
    postal_code: Optional[str] = None
    notes: Optional[str] = None


class AddressResponse(BaseModel):
    id: int
    line1: Optional[str]
    city: Optional[str]
    postal_code: Optional[str]
    notes: Optional[str]

    class Config:
        from_attributes = True


# Device Schema
class DeviceCreate(BaseModel):
    category: str
    brand: Optional[str] = None
    model: Optional[str] = None
    serial_number: Optional[str] = None
    notes: Optional[str] = None


# Call Schemas
class CallWebhook(BaseModel):
    recordingUrl: str
    callSid: str
    from_: str = None
    to: str
    startTime: str
    duration: Optional[int] = None

    class Config:
        fields = {"from_": "from"}


class CallResponse(BaseModel):
    id: int
    call_sid: Optional[str]
    from_number: Optional[str]
    to_number: Optional[str]
    audio_url: Optional[str]
    duration_seconds: Optional[int]
    status: CallStatusEnum
    created_at: datetime
    customer: Optional[CustomerResponse] = None

    class Config:
        from_attributes = True


# Extraction Schema (LLM Output)
class ExtractedCustomer(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[AddressCreate] = None


class ExtractedDevice(BaseModel):
    category: Optional[str] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    issue: Optional[str] = None
    urgency: Optional[str] = None


class ExtractedQuote(BaseModel):
    agreed_price: Optional[float] = None
    currency: str = "ILS"
    notes: Optional[str] = None


class ExtractedAppointment(BaseModel):
    date: Optional[str] = None  # YYYY-MM-DD
    time: Optional[str] = None  # HH:MM
    duration_minutes: int = 60
    is_confirmed_by_customer: bool = False


class ExtractedFollowup(BaseModel):
    required: bool = False
    due_at: Optional[str] = None
    reason: Optional[str] = None


class ExtractionResult(BaseModel):
    customer: Optional[ExtractedCustomer] = None
    device: Optional[ExtractedDevice] = None
    quote: Optional[ExtractedQuote] = None
    appointment: Optional[ExtractedAppointment] = None
    follow_up: Optional[ExtractedFollowup] = None
    free_text_summary_he: Optional[str] = None
    confidence: float = 0.0


# Job Schemas
class JobCreate(BaseModel):
    customer_id: int
    title: str
    description: Optional[str] = None
    agreed_price: Optional[Decimal] = None
    currency: str = "ILS"
    priority: str = "medium"


class JobResponse(BaseModel):
    id: int
    title: Optional[str]
    description: Optional[str]
    status: JobStatusEnum
    agreed_price: Optional[Decimal]
    currency: Optional[str]
    priority: Optional[str]
    created_at: datetime
    customer: Optional[CustomerResponse] = None

    class Config:
        from_attributes = True


# Appointment Schemas
class AppointmentCreate(BaseModel):
    job_id: Optional[int] = None
    customer_id: int
    technician_id: Optional[int] = None
    start_at: datetime
    duration_minutes: int = 60
    title: str
    notes: Optional[str] = None


class AppointmentResponse(BaseModel):
    id: int
    start_at: datetime
    duration_minutes: int
    title: Optional[str]
    notes: Optional[str]
    is_confirmed: bool
    created_at: datetime
    customer: Optional[CustomerResponse] = None

    class Config:
        from_attributes = True


# Message Schemas
class MessageSend(BaseModel):
    customer_id: int
    channel: str  # sms, whatsapp
    content: str


class MessageResponse(BaseModel):
    id: int
    channel: str
    to_number: Optional[str]
    content: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

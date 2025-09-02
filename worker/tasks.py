from celery import shared_task
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os


# Database connection
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://smart:agent@db:5432/smartagent")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


@shared_task
def transcribe_call(call_id):
    """Transcribe audio call and save transcript"""
    from backend.app.services.transcribe import transcription_service
    from backend.app.models import Call, Transcript, CallStatusEnum

    db = SessionLocal()
    try:
        # Get call
        call = db.query(Call).filter(Call.id == call_id).first()
        if not call:
            return {"error": "Call not found"}

        # Update status
        call.status = CallStatusEnum.TRANSCRIBING
        db.commit()

        # Transcribe audio
        text, confidence = transcription_service.transcribe_from_url(call.audio_url)

        # Save transcript
        transcript = Transcript(
            org_id=call.org_id, call_id=call.id, text=text, confidence=confidence
        )
        db.add(transcript)

        # Update call status
        call.status = CallStatusEnum.EXTRACTING
        db.commit()

        # Enqueue extraction task
        extract_info.delay(transcript.id)

        return {"transcript_id": transcript.id, "confidence": float(confidence)}

    except Exception as e:
        call.status = CallStatusEnum.FAILED
        db.commit()
        return {"error": str(e)}
    finally:
        db.close()


@shared_task
def extract_info(transcript_id):
    """Extract structured information from transcript using LLM"""
    from backend.app.services.extract import llm_service
    from backend.app.models import Transcript, Extraction, Call, CallStatusEnum

    db = SessionLocal()
    try:
        # Get transcript
        transcript = db.query(Transcript).filter(Transcript.id == transcript_id).first()
        if not transcript:
            return {"error": "Transcript not found"}

        # Extract information using LLM
        extraction_result = llm_service.extract_information(transcript.text)

        # Save extraction
        extraction = Extraction(
            org_id=transcript.org_id,
            call_id=transcript.call_id,
            extracted_data=extraction_result.dict(),
            summary_he=extraction_result.free_text_summary_he,
            confidence=extraction_result.confidence,
        )
        db.add(extraction)

        # Update call status
        call = db.query(Call).filter(Call.id == transcript.call_id).first()
        call.status = CallStatusEnum.COMPLETED
        db.commit()

        # If appointment info exists, create appointment
        if extraction_result.appointment and extraction_result.appointment.date:
            create_appointment_from_extraction.delay(extraction.id)

        # Send confirmation message if customer phone exists
        if extraction_result.customer and extraction_result.customer.phone:
            send_confirmation_message.delay(extraction.id)

        return {"extraction_id": extraction.id}

    except Exception as e:
        return {"error": str(e)}
    finally:
        db.close()


@shared_task
def create_appointment_from_extraction(extraction_id):
    """Create appointment from extraction data"""
    # Implementation for appointment creation and calendar sync
    pass


@shared_task
def send_confirmation_message(extraction_id):
    """Send SMS/WhatsApp confirmation to customer"""
    # Implementation for message sending
    pass


@shared_task
def sync_calendar_events():
    """Sync appointments with external calendars"""
    # Implementation for calendar synchronization
    pass

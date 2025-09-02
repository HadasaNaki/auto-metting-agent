from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.schemas import CallWebhook, CallResponse
from app import deps, models
from worker.tasks import transcribe_call
from typing import List

router = APIRouter()


@router.post("/webhook/twilio")
async def twilio_webhook(
    webhook_data: CallWebhook,
    db: Session = Depends(deps.get_db),
    current_org: models.Organization = Depends(deps.get_current_org),
):
    """Receive webhook from Twilio with call recording"""
    # Create call record
    call = models.Call(
        org_id=current_org.id,
        call_sid=webhook_data.callSid,
        from_number=webhook_data.from_,
        to_number=webhook_data.to,
        audio_url=webhook_data.recordingUrl,
        duration_seconds=webhook_data.duration,
        status=models.CallStatusEnum.PENDING_TRANSCRIPTION,
    )
    db.add(call)
    db.commit()
    db.refresh(call)

    # Enqueue transcription task
    transcribe_call.delay(call.id)

    return {"message": "Call received", "call_id": call.id}


@router.post("/upload", response_model=CallResponse)
async def upload_call(
    audio: UploadFile = File(...),
    customer_id: int = None,
    db: Session = Depends(deps.get_db),
    current_org: models.Organization = Depends(deps.get_current_org),
):
    """Manual upload of call recording"""
    # Save file to S3, create call record, enqueue transcription
    # Implementation here
    pass


@router.get("/{call_id}", response_model=CallResponse)
async def get_call(
    call_id: int,
    db: Session = Depends(deps.get_db),
    current_org: models.Organization = Depends(deps.get_current_org),
):
    """Get call details"""
    call = (
        db.query(models.Call)
        .filter(models.Call.id == call_id, models.Call.org_id == current_org.id)
        .first()
    )

    if not call:
        raise HTTPException(status_code=404, detail="Call not found")

    return call


@router.get("/", response_model=List[CallResponse])
async def list_calls(
    date_from: str = None,
    date_to: str = None,
    db: Session = Depends(deps.get_db),
    current_org: models.Organization = Depends(deps.get_current_org),
):
    """List calls with optional date filtering"""
    query = db.query(models.Call).filter(models.Call.org_id == current_org.id)

    # Add date filtering logic here

    calls = query.order_by(models.Call.created_at.desc()).limit(100).all()
    return calls

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas import MessageSend, MessageResponse
from app import deps, models
from typing import List

router = APIRouter()


@router.post("/sms", response_model=MessageResponse)
async def send_sms(
    message_data: MessageSend,
    db: Session = Depends(deps.get_db),
    current_org: models.Organization = Depends(deps.get_current_org),
):
    """Send SMS message"""
    # Implementation for SMS sending via Twilio
    pass


@router.post("/whatsapp", response_model=MessageResponse)
async def send_whatsapp(
    message_data: MessageSend,
    db: Session = Depends(deps.get_db),
    current_org: models.Organization = Depends(deps.get_current_org),
):
    """Send WhatsApp message"""
    # Implementation for WhatsApp sending
    pass


@router.get("/", response_model=List[MessageResponse])
async def list_messages(
    customer_id: int = None,
    db: Session = Depends(deps.get_db),
    current_org: models.Organization = Depends(deps.get_current_org),
):
    """List sent messages"""
    query = db.query(models.Message).filter(models.Message.org_id == current_org.id)

    if customer_id:
        query = query.filter(models.Message.customer_id == customer_id)

    messages = query.order_by(models.Message.created_at.desc()).all()
    return messages

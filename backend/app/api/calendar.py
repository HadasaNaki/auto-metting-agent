from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app import deps, models
from typing import List
from datetime import date

router = APIRouter()


@router.get("/agenda")
async def get_agenda(
    day: date = Query(..., description="Date in YYYY-MM-DD format"),
    db: Session = Depends(deps.get_db),
    current_org: models.Organization = Depends(deps.get_current_org),
):
    """Get daily agenda with appointments and follow-ups"""

    # Get appointments for the day
    appointments = (
        db.query(models.Appointment)
        .filter(
            models.Appointment.org_id == current_org.id,
            models.Appointment.start_at >= day,
            models.Appointment.start_at < day.replace(day=day.day + 1),
        )
        .order_by(models.Appointment.start_at)
        .all()
    )

    # Get follow-ups due for the day
    followups = (
        db.query(models.Followup)
        .filter(
            models.Followup.org_id == current_org.id,
            models.Followup.due_at >= day,
            models.Followup.due_at < day.replace(day=day.day + 1),
            models.Followup.is_completed == False,
        )
        .order_by(models.Followup.due_at)
        .all()
    )

    return {"date": day, "appointments": appointments, "followups": followups}


@router.post("/webhooks/calendar")
async def calendar_webhook(db: Session = Depends(deps.get_db)):
    """Receive webhooks from external calendars (Google/Outlook)"""
    # Implementation for calendar sync
    pass

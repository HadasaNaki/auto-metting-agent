from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import AppointmentCreate, AppointmentResponse
from app import deps, models
from typing import List
from datetime import datetime, date

router = APIRouter()


@router.post("/", response_model=AppointmentResponse)
async def create_appointment(
    appointment_data: AppointmentCreate,
    db: Session = Depends(deps.get_db),
    current_org: models.Organization = Depends(deps.get_current_org),
):
    """Create new appointment"""
    appointment = models.Appointment(org_id=current_org.id, **appointment_data.dict())
    db.add(appointment)
    db.commit()
    db.refresh(appointment)

    # TODO: Sync to external calendar

    return appointment


@router.get("/", response_model=List[AppointmentResponse])
async def list_appointments(
    date_from: str = None,
    date_to: str = None,
    db: Session = Depends(deps.get_db),
    current_org: models.Organization = Depends(deps.get_current_org),
):
    """List appointments"""
    query = db.query(models.Appointment).filter(
        models.Appointment.org_id == current_org.id
    )

    # Add date filtering logic here

    appointments = query.order_by(models.Appointment.start_at).all()
    return appointments

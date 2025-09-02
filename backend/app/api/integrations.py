from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import deps, models

router = APIRouter()


@router.post("/google/connect")
async def connect_google_calendar(
    db: Session = Depends(deps.get_db),
    current_org: models.Organization = Depends(deps.get_current_org),
):
    """Start Google Calendar OAuth flow"""
    # Implementation for Google OAuth
    pass


@router.post("/outlook/connect")
async def connect_outlook_calendar(
    db: Session = Depends(deps.get_db),
    current_org: models.Organization = Depends(deps.get_current_org),
):
    """Start Outlook Calendar OAuth flow"""
    # Implementation for Outlook OAuth
    pass


@router.get("/")
async def list_integrations(
    db: Session = Depends(deps.get_db),
    current_org: models.Organization = Depends(deps.get_current_org),
):
    """List active integrations"""
    integrations = (
        db.query(models.Integration)
        .filter(
            models.Integration.org_id == current_org.id,
            models.Integration.is_active == True,
        )
        .all()
    )

    return integrations

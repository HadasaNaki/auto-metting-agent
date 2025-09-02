from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import JobCreate, JobResponse
from app import deps, models
from typing import List

router = APIRouter()


@router.post("/", response_model=JobResponse)
async def create_job(
    job_data: JobCreate,
    db: Session = Depends(deps.get_db),
    current_org: models.Organization = Depends(deps.get_current_org),
):
    """Create new job/service ticket"""
    job = models.Job(org_id=current_org.id, **job_data.dict())
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


@router.get("/", response_model=List[JobResponse])
async def list_jobs(
    status: str = None,
    q: str = None,
    db: Session = Depends(deps.get_db),
    current_org: models.Organization = Depends(deps.get_current_org),
):
    """List jobs with filtering"""
    query = db.query(models.Job).filter(models.Job.org_id == current_org.id)

    if status:
        query = query.filter(models.Job.status == status)

    # Add search logic for 'q' parameter

    jobs = query.order_by(models.Job.created_at.desc()).all()
    return jobs


@router.get("/{job_id}", response_model=JobResponse)
async def get_job(
    job_id: int,
    db: Session = Depends(deps.get_db),
    current_org: models.Organization = Depends(deps.get_current_org),
):
    """Get job details"""
    job = (
        db.query(models.Job)
        .filter(models.Job.id == job_id, models.Job.org_id == current_org.id)
        .first()
    )

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    return job

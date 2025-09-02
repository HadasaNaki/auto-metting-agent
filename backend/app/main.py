from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.api import auth, calls, jobs, appointments, messages, integrations, calendar

app = FastAPI(
    title="SmartAgent API",
    description="Smart Field Technician Management System",
    version="1.0.0",
)


@app.get("/")
async def root():
    return {"message": "SmartAgent API is running", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "smartagent-backend"}


app.include_router(auth.router, prefix="/auth")
app.include_router(calls.router, prefix="/calls")
app.include_router(jobs.router, prefix="/jobs")
app.include_router(appointments.router, prefix="/appointments")
app.include_router(messages.router, prefix="/messages")
app.include_router(integrations.router, prefix="/integrations")
app.include_router(calendar.router, prefix="/calendar")

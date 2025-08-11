from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from . import models
from .config import settings
from .routers import auth, users, appointments, medications, lab_results, messages, agent, fitness, wellness, records, billing, forms, telehealth, surveys
from .routers import settings as settings_router

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Healthcare Patient Portal API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(appointments.router)
app.include_router(medications.router)
app.include_router(lab_results.router)
app.include_router(messages.router)
app.include_router(fitness.router)
app.include_router(wellness.router)
app.include_router(records.router)
app.include_router(billing.router)
app.include_router(forms.router)
app.include_router(telehealth.router)
app.include_router(settings_router.router)
app.include_router(surveys.router)
app.include_router(agent.router, prefix="/agent", tags=["AI Agent"])

@app.get("/")
def read_root():
    return {"message": "Healthcare Patient Portal API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

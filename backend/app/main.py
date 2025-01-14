from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import auth, goals, calendar

app = FastAPI(
    title="Training Planner API",
    description="API pour la planification d'entraînement avec intervals.icu",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # À configurer en production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes API
app.include_router(auth.router, prefix="/api")
app.include_router(goals.router, prefix="/api/goals")
app.include_router(calendar.router, prefix="/api/calendar")

@app.get("/")
async def read_root():
    return {"message": "Bienvenue sur l'API Training Planner"}

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.services.firebase_service import init_firebase
import os

load_dotenv()
init_firebase()

app = FastAPI(title="Plannery API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.routes import places, plans, chat  # ← agrega chat
app.include_router(places.router)
app.include_router(plans.router)
app.include_router(chat.router)             # ← NUEVO

@app.get("/health")
def health_check():
    return {"status": "ok"}
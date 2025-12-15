from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.infrastructure.database import engine
from app.infrastructure.database import Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Client Portal API",
    description="API for Client Portal application",
    version="1.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Client Portal API"}


@app.get("/health")
def health():
    return {"status": "ok"}


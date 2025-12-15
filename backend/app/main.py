from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.infrastructure.database import engine
from app.infrastructure.database import Base
from app.adapters.api.v1 import auth, projects, comments, users

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

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(projects.router, prefix="/api/projects", tags=["projects"])
app.include_router(comments.router, prefix="/api/projects", tags=["comments"])
app.include_router(users.router, prefix="/api/users", tags=["users"])


@app.get("/")
def root():
    return {"message": "Client Portal API"}


@app.get("/health")
def health():
    return {"status": "ok"}


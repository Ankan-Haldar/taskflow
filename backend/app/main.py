from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine
from .routers import boards, tasks


# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="TaskFlow API",
    version="1.0.0",
    description="Backend API for the TaskFlow take-home assignment.",
)


# Allow React frontend to communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Register routers
app.include_router(boards.router)
app.include_router(tasks.router)


@app.get("/health")
def health():
    return {
        "status": "ok"
    }
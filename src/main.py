from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.core.config import ALLOWED_ORIGINS
from app.routers import real_estate, statistics

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(real_estate.router)
app.include_router(statistics.router)
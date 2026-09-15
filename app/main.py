from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router


app = FastAPI(
    title="IROPS Recovery Copilot",
    description="Agentic airline disruption recovery system",
    version="1.0.0",
)


# Allow the frontend to communicate with the FastAPI backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router)


@app.get("/health")
def health():
    return {"status": "healthy"}
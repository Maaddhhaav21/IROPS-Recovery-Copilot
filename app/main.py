from fastapi import FastAPI

from app.api.routes import router


app = FastAPI(
    title="IROPS Recovery Copilot",
    description="Agentic airline disruption recovery system",
    version="1.0.0",
)

app.include_router(router)


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }
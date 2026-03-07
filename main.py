"""Simple API - FastAPI boilerplate with configurable settings."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    # Startup
    yield
    # Shutdown (cleanup if needed)


app = FastAPI(
    title="Simple API",
    description="A minimal FastAPI boilerplate with configuration",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    """Health check / root endpoint."""
    return {"status": "ok", "message": "Hello, World!"}


@app.get("/health")
def health_check():
    """Health check for load balancers and monitoring."""
    return {"status": "healthy"}


@app.get("/items/{item_id}")
def read_item(item_id: int, item_name: str | None = None):
    """Example item endpoint."""
    return {"item_id": item_id, "item_name": item_name}


def main() -> None:
    """Run the server with configured host and port. Use this instead of uvicorn main:app."""
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        reload_includes=[".env"] if settings.reload else None,
    )


if __name__ == "__main__":
    main()

from fastapi import FastAPI
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Connect to DB
    print("Connecting to Database...")
    yield
    # Shutdown: Disconnect
    print("Disconnecting from Database...")

app = FastAPI(title="SSFF API", lifespan=lifespan)

@app.get("/")
def read_root():
    return {"message": "SSFF Backend is running", "status": "ok"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# TODO: Add /api/network and /api/signals endpoints

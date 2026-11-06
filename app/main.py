from fastapi import FastAPI

from app.database import Base, engine
from app import models
from app.routers import admin, auth, client

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Customer Support Ticket API",
    description="Customer authentication and ticket management",
    version="1.0.0"
)

app.include_router(auth.router)
app.include_router(client.router)
app.include_router(admin.router)


@app.get("/")
def home():
    return {"message": "Customer Support Ticket API is running"}
print("Hello")
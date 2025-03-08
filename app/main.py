from fastapi import FastAPI
import models
from database import engine
from routes import notes, users, auth  # Import authentication routes

# Initialize FastAPI
app = FastAPI()

# Create tables
models.Base.metadata.create_all(bind=engine)

# Register Routes
app.include_router(notes.router)
app.include_router(users.router)
app.include_router(auth.router)

from fastapi import FastAPI
from app.routes import query_routes

app = FastAPI(
    title="E-commerce AI Agent",
    description="Ask questions about product sales, ads, and eligibility.",
    version="1.0.0"
)

# Include routes
app.include_router(query_routes.router)

# Run command: uvicorn app.main:app --reload

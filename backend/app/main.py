from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import data, visualization

app = FastAPI(
    title="Financial Analysis System",
    description="API for financial data analysis and visualization",
    version="2.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(data.router, prefix="/api/data", tags=["Data"])
app.include_router(visualization.router, prefix="/api/visualization", tags=["Visualization"])

@app.get("/")
async def root():
    return {"message": "Welcome to Financial Analysis System v2.0"} 
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import logging

import crud, schemas, models
from db import get_db, engine
from utils import trigger_airflow_dag, check_airflow_health

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Data Flow Hub API",
    description="A comprehensive data flow management system with ETL capabilities",
    version="1.0.0"
)

@app.get("/ping")
async def ping():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Data Flow Hub API is running"}

@app.get("/summary", response_model=schemas.SummaryResponse)
async def get_summary(db: Session = Depends(get_db)):
    """Get summary statistics of the data"""
    try:
        stats = crud.get_summary_stats(db)
        return schemas.SummaryResponse(**stats)
    except Exception as e:
        logger.error(f"Error getting summary: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get summary statistics")

@app.get("/hour-range-stats", response_model=schemas.TripHourRangeStatsResponse)
async def get_trip_duration_stats(db: Session = Depends(get_db)):
    """Get trip hour range statistics"""
    try:
        stats = crud.get_trip_hourrange_stats(db)
        return schemas.TripHourRangeStatsResponse(**stats)
    except Exception as e:
        logger.error(f"Error getting hour range statistics: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get trip hour range statistics")


@app.get("/trip-duration-stats", response_model=schemas.TripDurationStatsResponse)
async def get_trip_duration_stats(db: Session = Depends(get_db)):
    """Get trip duration statistics"""
    try:
        stats = crud.get_trip_duration_stats(db)
        return schemas.TripDurationStatsResponse(**stats)
    except Exception as e:
        logger.error(f"Error getting trip duration statistics: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get trip duration statistics")

@app.post("/refresh")
async def refresh_data():
    """Trigger the ETL pipeline manually"""
    try:
        result = trigger_airflow_dag()
        if result["status"] == "success":
            return {"status": "success", "message": "ETL pipeline triggered successfully"}
        else:
            raise HTTPException(status_code=500, detail=result["message"])
    except Exception as e:
        logger.error(f"Error triggering ETL pipeline: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to trigger ETL pipeline: {str(e)}")

@app.get("/top/{n}", response_model=schemas.TopNResponse)
async def get_top_n(n: int, db: Session = Depends(get_db)):
    """Get top N records by value"""
    if n <= 0:
        raise HTTPException(status_code=400, detail="N must be a positive integer")
    
    if n > 1000:
        raise HTTPException(status_code=400, detail="N cannot exceed 1000")
    
    try:
        records = crud.get_top_records(db, n)
        return schemas.TopNResponse(records=records, count=len(records))
    except Exception as e:
        logger.error(f"Error getting top {n} records: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get top records")

@app.get("/records", response_model=List[schemas.BikeTrip])
async def get_records(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all records with pagination"""
    if limit > 1000:
        limit = 1000
    
    try:
        records = crud.get_records(db, skip=skip, limit=limit)
        return records
    except Exception as e:
        logger.error(f"Error getting records: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get records")

@app.get("/health/airflow")
async def check_airflow():
    """Check Airflow health status"""
    try:
        health_status = check_airflow_health()
        return health_status
    except Exception as e:
        logger.error(f"Error checking Airflow health: {str(e)}")
        return {"status": "unhealthy", "error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

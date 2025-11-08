from sqlalchemy.orm import Session
from sqlalchemy import func, desc
import models, schemas
from typing import List, Optional

def create_record(db: Session, record: schemas.BikeTripCreate):
    """Create a new data record"""
    db_record = models.BikeTrip(**record.dict())
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

def get_record(db: Session, record_id: int):
    """Get a single record by ID"""
    return db.query(models.BikeTrip).filter(models.BikeTrip.id == record_id).first()

def get_records(db: Session, skip: int = 0, limit: int = 100):
    """Get multiple records with pagination"""
    return db.query(models.BikeTrip).offset(skip).limit(limit).all()

def get_top_records(db: Session, n: int = 10):
    """Get top N records by value"""
    return db.query(models.BikeTrip).order_by(desc(models.BikeTrip.start_time)).limit(n).all()

def get_summary_stats(db: Session):
    """Get summary statistics"""
    total_records = db.query(models.BikeTrip).count()
    
    return {
        "total_records": total_records
    }

def delete_all_records(db: Session):
    """Delete all records (for refresh functionality)"""
    db.query(models.BikeTrip).delete()
    db.commit()
    return True

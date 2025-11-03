from sqlalchemy.orm import Session
from sqlalchemy import func, desc
import models, schemas
from typing import List, Optional

def create_record(db: Session, record: schemas.DataRecordCreate):
    """Create a new data record"""
    db_record = models.DataRecord(**record.dict())
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

def get_record(db: Session, record_id: int):
    """Get a single record by ID"""
    return db.query(models.DataRecord).filter(models.DataRecord.id == record_id).first()

def get_records(db: Session, skip: int = 0, limit: int = 100):
    """Get multiple records with pagination"""
    return db.query(models.DataRecord).offset(skip).limit(limit).all()

def get_top_records(db: Session, n: int = 10):
    """Get top N records by value"""
    return db.query(models.DataRecord).order_by(desc(models.DataRecord.value)).limit(n).all()

def get_summary_stats(db: Session):
    """Get summary statistics"""
    total_records = db.query(models.DataRecord).count()
    
    # Get category counts
    category_stats = db.query(
        models.DataRecord.category,
        func.count(models.DataRecord.id).label('count')
    ).group_by(models.DataRecord.category).all()
    
    categories = {stat.category: stat.count for stat in category_stats}
    
    # Get average value
    avg_result = db.query(func.avg(models.DataRecord.value)).scalar()
    average_value = float(avg_result) if avg_result else 0.0
    
    # Get last updated timestamp
    last_record = db.query(models.DataRecord).order_by(desc(models.DataRecord.updated_at)).first()
    last_updated = last_record.updated_at if last_record else None
    
    return {
        "total_records": total_records,
        "categories": categories,
        "average_value": average_value,
        "last_updated": last_updated
    }

def delete_all_records(db: Session):
    """Delete all records (for refresh functionality)"""
    db.query(models.DataRecord).delete()
    db.commit()
    return True

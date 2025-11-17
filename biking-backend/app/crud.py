from sqlalchemy.orm import Session
from sqlalchemy import func, desc, select
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

def get_trip_hourrange_stats(db: Session):
    """Get trip hour range statistics"""
    rides_cte = (
        select(
            models.BikeTrip.id,
            models.BikeTrip.start_time,
            models.BikeTrip.stop_time,
            func.date_trunc('hour', models.BikeTrip.start_time).label("start_hour"),
            func.tsrange(models.BikeTrip.start_time, models.BikeTrip.stop_time, "[)").label("ride_range")
        )
        .cte("rides")
    )

    offsets_cte = (
        select(
            rides_cte.c.id,
            rides_cte.c.start_hour,
            rides_cte.c.ride_range,
            func.generate_series(0, 23).label("offset_hour")
        )
        .cte("offsets")
    )

    bucket_start = offsets_cte.c.start_hour + func.make_interval(0, 0, 0, 0, offsets_cte.c.offset_hour)
    bucket_end = offsets_cte.c.start_hour + func.make_interval(0, 0, 0, 0, offsets_cte.c.offset_hour + 1)
    bucket_hour = func.mod(func.extract("hour", offsets_cte.c.start_hour) + offsets_cte.c.offset_hour, 24).label("bucket_hour")
    hour_range = func.tsrange(bucket_start, bucket_end, "[)").label("hour_range")

    bucket_cte = (
        select(
            offsets_cte.c.id,
            offsets_cte.c.ride_range,
            func.mod(
                func.extract("hour", offsets_cte.c.start_hour) + offsets_cte.c.offset_hour,
                24
            ).label("bucket_hour"),
            func.tsrange(
                offsets_cte.c.start_hour + func.make_interval(0, 0, 0, 0, offsets_cte.c.offset_hour),
                offsets_cte.c.start_hour + func.make_interval(0, 0, 0, 0, offsets_cte.c.offset_hour + 1),
                "[)"
            ).label("hour_range")
        ).cte("bucket_cte")
    )

    stmt = (
        select(
            bucket_cte.c.bucket_hour,
            func.count().label("ride_count")
        )
        .where(bucket_cte.c.ride_range.op("&&")(bucket_cte.c.hour_range))
        .group_by(bucket_cte.c.bucket_hour)
        .order_by(bucket_cte.c.bucket_hour)
    )
    rows = db.execute(stmt).all()

    return {
        "hour_bucket": [row.bucket_hour for row in rows],
        "count": [row.ride_count for row in rows]
    }

def get_trip_duration_stats(db: Session):
    """Get trip duration statistics"""
    stmt = (
        select(
            (models.BikeTrip.tripduration // 3600).label("hours"),
            func.count().label("count")
        ).group_by(
            "hours"
        ).order_by(
            "hours"
        )
    )

    rows = db.execute(stmt).all()

    return {
        "hours": [row.hours for row in rows],
        "count": [row.count for row in rows]
    }

def delete_all_records(db: Session):
    """Delete all records (for refresh functionality)"""
    db.query(models.BikeTrip).delete()
    db.commit()
    return True

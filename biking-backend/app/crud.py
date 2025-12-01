from sqlalchemy.orm import Session
from sqlalchemy import func, desc, select, case
import models, schemas
from typing import List, Optional

def create_record(db: Session, record: schemas.BikeTripCreate):
    """Create a new data record"""
    db_record = models.BikeTrip(**record.dict())
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

def get_top_records(db: Session, n: int = 10):
    """Get top N records ordered by start time"""
    return db.query(models.BikeTrip).order_by(models.BikeTrip.start_time).limit(n).all()

def get_count_stats(db: Session):
    """Get count statistics"""
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
    hours = models.BikeTrip.tripduration / 3600.0

    bin_label = case(
        # 0–2 hours → 30-min bins (0.25 h)
        (hours < 0.5, "< 30 minutes"),
        (hours < 1, "30 minutes - 1 hour"),
        (hours < 1.5, "1-1.5 hours"),
        (hours < 2, "1.5-2 hours"),

        # 2–6 hours → 1-hour bins
        (hours < 3, "2-3 hours"),
        (hours < 4, "3-4 hours"),
        (hours < 5, "4-5 hours"),
        (hours < 6, "5-6 hours"),

        # 6–24 hours → 6-hour bins
        (hours < 12, "6-12 hours"),
        (hours < 18, "12-18 hours"),
        (hours < 24, "18-24 hours"),

        # 1–3 days → 1-day bins
        (hours < 48, "1-2 days"),
        (hours < 72, "2-3 days"),

        else_=">= 3 days"
    ).label("duration_bin")

    stmt = (
        select(
            bin_label,
            func.count().label("count")
        )
        .group_by(bin_label)
    )

    rows = db.execute(stmt).all()

    # Define the order based on case statement order (logical duration order)
    bin_order = {
        "< 30 minutes": 0,
        "30 minutes - 1 hour": 1,
        "1-1.5 hours": 2,
        "1.5-2 hours": 3,
        "2-3 hours": 4,
        "3-4 hours": 5,
        "4-5 hours": 6,
        "5-6 hours": 7,
        "6-12 hours": 8,
        "12-18 hours": 9,
        "18-24 hours": 10,
        "1-2 days": 11,
        "2-3 days": 12,
        ">= 3 days": 13
    }

    # Sort by the case statement order
    sorted_rows = sorted(rows, key=lambda row: bin_order.get(row.duration_bin, 999))

    return {
        "hours": [row.duration_bin for row in sorted_rows],
        "count": [row.count for row in sorted_rows]
    }

def delete_all_records(db: Session):
    """Delete all records (for refresh functionality)"""
    db.query(models.BikeTrip).delete()
    db.commit()
    return True

import os
import sys
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import pandas as pd

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'app'))

from app.models import BikeTrip, Base
from app.db import DATABASE_URL

logger = logging.getLogger(__name__)

def load_to_database(df: pd.DataFrame, clear_existing: bool = True) -> bool:
    """
    Load transformed data into PostgreSQL database
    
    Args:
        df: Transformed dataframe
        clear_existing: Whether to clear existing data before loading
        
    Returns:
        bool: True if successful
    """
    try:
        logger.info(f"Starting database load for {len(df)} records")
        
        # Create database engine and session
        engine = create_engine(DATABASE_URL)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        
        # Create tables if they don't exist
        Base.metadata.create_all(bind=engine)
        
        db = SessionLocal()
        
        try:
            # Clear existing data if requested
            if clear_existing:
                logger.info("Clearing existing bike_trips data")
                db.query(BikeTrip).delete()
                db.commit()

            # Convert dataframe to database records
            records = []
            for _, row in df.iterrows():
                record = BikeTrip(
                    tripduration=int(row['tripduration']) if pd.notna(row.get('tripduration')) else 0,
                    start_time=row.get('start_time'),
                    stop_time=row.get('stop_time'),
                    start_station_id=int(row['start_station_id']) if pd.notna(row.get('start_station_id')) else None,
                    start_station_name=row.get('start_station_name'),
                    start_station_latitude=float(row['start_station_latitude']) if pd.notna(row.get('start_station_latitude')) else None,
                    start_station_longitude=float(row['start_station_longitude']) if pd.notna(row.get('start_station_longitude')) else None,
                    end_station_id=int(row['end_station_id']) if pd.notna(row.get('end_station_id')) else None,
                    end_station_name=row.get('end_station_name'),
                    end_station_latitude=float(row['end_station_latitude']) if pd.notna(row.get('end_station_latitude')) else None,
                    end_station_longitude=float(row['end_station_longitude']) if pd.notna(row.get('end_station_longitude')) else None,
                    bike_id=int(row['bike_id']) if pd.notna(row.get('bike_id')) else None,
                    user_type=row.get('user_type'),
                    birth_year=int(row['birth_year']) if pd.notna(row.get('birth_year')) else None,
                    gender=int(row['gender']) if pd.notna(row.get('gender')) else None,
                )
                records.append(record)

            # Bulk insert records
            logger.info(f"Inserting {len(records)} records into database")
            db.add_all(records)
            db.commit()
            
            logger.info("Successfully loaded data into database")
            return True
            
        except Exception as e:
            db.rollback()
            logger.error(f"Database transaction failed: {str(e)}")
            raise
            
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Error loading data to database: {str(e)}")
        raise

def validate_database_connection() -> bool:
    """
    Validate database connection
    
    Returns:
        bool: True if connection is successful
    """
    try:
        engine = create_engine(DATABASE_URL)
        with engine.connect() as conn:
            # Use text() for SQLAlchemy 2.0 compatibility
            result = conn.execute(text("SELECT 1"))
            result.fetchone()
        
        logger.info("Database connection validated successfully")
        return True
        
    except Exception as e:
        logger.error(f"Database connection validation failed: {str(e)}")
        return False


import os
import sys
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import pandas as pd

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'app'))

from app.models import DataRecord, Base
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
                logger.info("Clearing existing data")
                db.query(DataRecord).delete()
                db.commit()
            
            # Convert dataframe to database records
            records = []
            for _, row in df.iterrows():
                record = DataRecord(
                    name=row['name'],
                    category=row['category'],
                    value=row['value'],
                    description=row.get('description', '')
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

def get_database_stats() -> dict:
    """
    Get statistics from the database
    
    Returns:
        dict: Database statistics
    """
    try:
        engine = create_engine(DATABASE_URL)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        
        db = SessionLocal()
        
        try:
            total_records = db.query(DataRecord).count()
            
            # Get category distribution
            from sqlalchemy import func
            category_stats = db.query(
                DataRecord.category,
                func.count(DataRecord.id).label('count')
            ).group_by(DataRecord.category).all()
            
            categories = {stat.category: stat.count for stat in category_stats}
            
            # Get value statistics
            avg_value = db.query(func.avg(DataRecord.value)).scalar()
            max_value = db.query(func.max(DataRecord.value)).scalar()
            min_value = db.query(func.min(DataRecord.value)).scalar()
            
            stats = {
                'total_records': total_records,
                'categories': categories,
                'average_value': float(avg_value) if avg_value else 0.0,
                'max_value': float(max_value) if max_value else 0.0,
                'min_value': float(min_value) if min_value else 0.0
            }
            
            logger.info(f"Database statistics: {stats}")
            return stats
            
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Error getting database statistics: {str(e)}")
        raise


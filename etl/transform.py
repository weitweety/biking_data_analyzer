import pandas as pd
import logging
from typing import Dict, Any, List
import re

logger = logging.getLogger(__name__)

def clean_text(text: str) -> str:
    """
    Clean and normalize text data
    
    Args:
        text: Input text to clean
        
    Returns:
        str: Cleaned text
    """
    if pd.isna(text) or text is None:
        return ""
    
    # Convert to string and strip whitespace
    text = str(text).strip()
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    return text

def normalize_category(category: str) -> str:
    """
    Normalize category names
    
    Args:
        category: Category name to normalize
        
    Returns:
        str: Normalized category name
    """
    if pd.isna(category) or category is None:
        return "Unknown"
    
    category = str(category).strip().lower()
    
    # Common category mappings
    category_mappings = {
        'tech': 'Technology',
        'techology': 'Technology',
        'it': 'Technology',
        'finance': 'Financial',
        'fin': 'Financial',
        'health': 'Healthcare',
        'healthcare': 'Healthcare',
        'edu': 'Education',
        'education': 'Education',
        'retail': 'Retail',
        'ecommerce': 'E-commerce',
        'e-commerce': 'E-commerce'
    }
    
    return category_mappings.get(category, category.title())

def validate_numeric_value(value: Any) -> float:
    """
    Validate and convert numeric values
    
    Args:
        value: Value to validate and convert
        
    Returns:
        float: Validated numeric value
    """
    if pd.isna(value) or value is None:
        return 0.0
    
    try:
        # Convert to float
        numeric_value = float(value)
        
        # Check for reasonable bounds
        if numeric_value < 0:
            logger.warning(f"Negative value found: {numeric_value}, setting to 0")
            return 0.0
        
        if numeric_value > 1e10:  # Very large number
            logger.warning(f"Very large value found: {numeric_value}")
            return min(numeric_value, 1e10)
        
        return numeric_value
        
    except (ValueError, TypeError) as e:
        logger.warning(f"Invalid numeric value: {value}, setting to 0")
        return 0.0

def transform_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transform the extracted dataframe for Citi Bike trips.
    - Renames columns to snake_case
    - Parses datetimes
    - Coerces numeric types and handles nulls
    
    Args:
        df: Input dataframe
        
    Returns:
        pd.DataFrame: Transformed dataframe ready for loading into bike_trips
    """
    try:
        logger.info(f"Starting transformation of {len(df)} records")

        rename_map = {
            'tripduration': 'tripduration',
            'starttime': 'start_time',
            'stoptime': 'stop_time',
            'start station id': 'start_station_id',
            'start station name': 'start_station_name',
            'start station latitude': 'start_station_latitude',
            'start station longitude': 'start_station_longitude',
            'end station id': 'end_station_id',
            'end station name': 'end_station_name',
            'end station latitude': 'end_station_latitude',
            'end station longitude': 'end_station_longitude',
            'bikeid': 'bike_id',
            'usertype': 'user_type',
            'birth year': 'birth_year',
            'gender': 'gender',
        }

        # Lowercase columns to match keys in rename_map
        df_columns_lower = {c: c.lower() for c in df.columns}
        df = df.rename(columns=df_columns_lower)

        # Rename to snake_case names
        transformed_df = df.rename(columns=rename_map)

        # Keep only expected columns
        expected_cols = list(rename_map.values())
        transformed_df = transformed_df[[c for c in expected_cols if c in transformed_df.columns]]

        # Parse datetimes
        for dt_col in ['start_time', 'stop_time']:
            if dt_col in transformed_df.columns:
                transformed_df[dt_col] = pd.to_datetime(transformed_df[dt_col], errors='coerce')

        # Coerce numeric fields
        int_cols = ['tripduration', 'start_station_id', 'end_station_id', 'bike_id', 'birth_year', 'gender']
        float_cols = ['start_station_latitude', 'start_station_longitude', 'end_station_latitude', 'end_station_longitude']

        for col in int_cols:
            if col in transformed_df.columns:
                transformed_df[col] = pd.to_numeric(transformed_df[col], errors='coerce').astype('Int64')

        for col in float_cols:
            if col in transformed_df.columns:
                transformed_df[col] = pd.to_numeric(transformed_df[col], errors='coerce')

        # Clean text columns
        text_cols = ['start_station_name', 'end_station_name', 'user_type']
        for col in text_cols:
            if col in transformed_df.columns:
                transformed_df[col] = transformed_df[col].apply(clean_text)

        # Drop rows missing essential datetimes or duration
        essential = ['tripduration', 'start_time', 'stop_time']
        missing_before = transformed_df.shape[0]
        transformed_df = transformed_df.dropna(subset=[c for c in essential if c in transformed_df.columns])
        missing_after = transformed_df.shape[0]
        if missing_before != missing_after:
            logger.info(f"Dropped {missing_before - missing_after} rows with missing essential fields")

        logger.info(f"Transformation completed. Final record count: {len(transformed_df)}")
        return transformed_df
    except Exception as e:
        logger.error(f"Error during transformation: {str(e)}")
        raise

def aggregate_data(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Create aggregated statistics from the dataframe
    
    Args:
        df: Input dataframe
        
    Returns:
        Dict[str, Any]: Aggregated statistics
    """
    try:
        stats = {
            'total_records': len(df),
            'categories': df['category'].value_counts().to_dict(),
            'average_value': df['value'].mean(),
            'max_value': df['value'].max(),
            'min_value': df['value'].min(),
            'total_value': df['value'].sum()
        }
        
        logger.info(f"Aggregated statistics: {stats}")
        return stats
        
    except Exception as e:
        logger.error(f"Error creating aggregated statistics: {str(e)}")
        raise

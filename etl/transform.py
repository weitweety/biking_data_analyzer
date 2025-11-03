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
    Transform the extracted dataframe
    
    Args:
        df: Input dataframe
        
    Returns:
        pd.DataFrame: Transformed dataframe
    """
    try:
        logger.info(f"Starting transformation of {len(df)} records")
        
        # Create a copy to avoid modifying the original
        transformed_df = df.copy()
        
        # Clean and normalize text columns
        if 'name' in transformed_df.columns:
            transformed_df['name'] = transformed_df['name'].apply(clean_text)
        
        if 'description' in transformed_df.columns:
            transformed_df['description'] = transformed_df['description'].apply(clean_text)
        
        # Normalize category
        if 'category' in transformed_df.columns:
            transformed_df['category'] = transformed_df['category'].apply(normalize_category)
        else:
            # If no category column, create one
            transformed_df['category'] = 'General'
        
        # Validate and clean numeric values
        if 'value' in transformed_df.columns:
            transformed_df['value'] = transformed_df['value'].apply(validate_numeric_value)
        else:
            # If no value column, create one with default values
            transformed_df['value'] = 1.0
        
        # Remove duplicates based on name and category
        initial_count = len(transformed_df)
        transformed_df = transformed_df.drop_duplicates(subset=['name', 'category'], keep='first')
        final_count = len(transformed_df)
        
        if initial_count != final_count:
            logger.info(f"Removed {initial_count - final_count} duplicate records")
        
        # Sort by value descending
        transformed_df = transformed_df.sort_values('value', ascending=False)
        
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

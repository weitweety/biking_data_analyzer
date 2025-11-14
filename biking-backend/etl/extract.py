import pandas as pd
import os
import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

def extract_csv_data(file_path: str) -> pd.DataFrame:
    """
    Extract data from CSV files
    
    Args:
        file_path: Path to the CSV file
        
    Returns:
        pandas.DataFrame: Extracted data
    """
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"CSV file not found: {file_path}")
        
        logger.info(f"Extracting data from {file_path}")
        df = pd.read_csv(file_path)
        
        logger.info(f"Successfully extracted {len(df)} records from {file_path}")
        return df
        
    except Exception as e:
        logger.error(f"Error extracting data from {file_path}: {str(e)}")
        raise

def extract_multiple_csvs(directory_path: str) -> Optional[pd.DataFrame]:
    """
    Extract data from multiple CSV files in a directory
    
    Args:
        directory_path: Path to directory containing CSV files
        
    Returns:
        Optional[pd.DataFrame]: Combined dataframe of extracted dataframes
    """
    dataframes = []
    
    try:
        if not os.path.exists(directory_path):
            raise FileNotFoundError(f"Directory not found: {directory_path}")
        
        csv_files = [f for f in os.listdir(directory_path) if f.endswith('.csv')]
        
        if not csv_files:
            logger.warning(f"No CSV files found in {directory_path}")
            return None
        
        logger.info(f"Found {len(csv_files)} CSV files in {directory_path}")
        
        for csv_file in csv_files:
            file_path = os.path.join(directory_path, csv_file)
            df = extract_csv_data(file_path)
            dataframes.append(df)

        combined_df = pd.concat(dataframes) 
        logger.info(f"Successfully extracted data from {len(dataframes)} files")
        return combined_df

    except Exception as e:
        logger.error(f"Error extracting multiple CSV files: {str(e)}")
        raise
        

def validate_dataframe(df: pd.DataFrame, required_columns: List[str]) -> bool:
    """
    Validate that the dataframe has required columns
    
    Args:
        df: DataFrame to validate
        required_columns: List of required column names
        
    Returns:
        bool: True if validation passes
    """
    try:
        missing_columns = set(required_columns) - set(df.columns)
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
        
        # Check for empty dataframe
        if df.empty:
            raise ValueError("DataFrame is empty")
        
        logger.info("Data validation passed")
        return True
        
    except Exception as e:
        logger.error(f"Data validation failed: {str(e)}")
        raise

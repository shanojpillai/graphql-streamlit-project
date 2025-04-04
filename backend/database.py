import pandas as pd
import os
from typing import List, Dict, Any

# File path to the dataset
DATASET_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'dataset.csv')

# In-memory cache for the data
_data_cache = None

def get_data_from_database() -> List[Dict[str, Any]]:
    """
    Loads data from the CSV file and returns it as a list of dictionaries.
    Uses a simple caching mechanism to avoid reading the file for every query.
    """
    global _data_cache
    
    if _data_cache is None:
        # Check if file exists
        if not os.path.exists(DATASET_PATH):
            # For development, return some dummy data if file doesn't exist
            _data_cache = [
                {"id": "1", "name": "Item 1", "value": 10.5, "category": "A"},
                {"id": "2", "name": "Item 2", "value": 20.0, "category": "B"},
                {"id": "3", "name": "Item 3", "value": 30.7, "category": "A"},
                {"id": "4", "name": "Item 4", "value": 15.2, "category": "C"},
                {"id": "5", "name": "Item 5", "value": 25.8, "category": "B"},
                {"id": "6", "name": "Item 6", "value": 35.9, "category": "A"},
                {"id": "7", "name": "Item 7", "value": 18.3, "category": "C"},
                {"id": "8", "name": "Item 8", "value": 22.1, "category": "B"},
                {"id": "9", "name": "Item 9", "value": 40.5, "category": "A"},
                {"id": "10", "name": "Item 10", "value": 33.7, "category": "C"},
            ]
            return _data_cache
        
        try:
            # Load the dataset
            df = pd.read_csv(DATASET_PATH)
            
            # Convert DataFrame to list of dictionaries
            _data_cache = df.to_dict(orient='records')
            
            # If the dataset doesn't have an 'id' column, add one
            if 'id' not in df.columns:
                for i, item in enumerate(_data_cache):
                    item['id'] = str(i + 1)
                    
        except Exception as e:
            print(f"Error loading dataset: {e}")
            # Return empty list in case of error
            _data_cache = []
    
    return _data_cache

def refresh_data_cache():
    """
    Force a refresh of the data cache
    """
    global _data_cache
    _data_cache = None
    return get_data_from_database()
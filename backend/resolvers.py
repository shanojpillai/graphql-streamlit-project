from typing import List, Optional
from database import get_data_from_database

# This file contains resolver functions for GraphQL queries
# These functions will be responsible for fetching data from our "database"
# (in this case, a CSV file loaded with pandas)

def get_items(limit: Optional[int] = 10, offset: Optional[int] = 0, category: Optional[str] = None) -> List:
    """
    Resolver for fetching multiple items with pagination and filtering
    """
    data = get_data_from_database()
    
    # Apply category filter if provided
    if category:
        data = [item for item in data if item.get('category') == category]
    
    # Apply pagination
    paginated_data = data[offset:offset + limit]
    
    return paginated_data

def get_item_by_id(id: str):
    """
    Resolver for fetching a single item by ID
    """
    data = get_data_from_database()
    
    # Find the item with the matching ID
    for item in data:
        if item.get('id') == id:
            return item
    
    return None
from typing import List, Optional, Dict, Any
from database import get_data_from_database
from models import Item  # Import from models.py instead of schema.py

# This file contains resolver functions for GraphQL queries
# These functions will be responsible for fetching data from our "database"
# (in this case, a CSV file loaded with pandas)

def map_dict_to_item(data_dict: Dict[str, Any]) -> Item:
    """
    Map a dictionary to an Item type
    """
    # Create an Item with only the fields that are in our schema
    return Item(
        id=str(data_dict.get('id', '')),
        name=str(data_dict.get('name', '')),
        value=float(data_dict.get('value', 0.0)),
        category=str(data_dict.get('category', ''))
    )

def get_items(limit: Optional[int] = 10, offset: Optional[int] = 0, category: Optional[str] = None) -> List[Item]:
    """
    Resolver for fetching multiple items with pagination and filtering
    """
    data = get_data_from_database()
    
    # Apply category filter if provided
    if category:
        data = [item for item in data if item.get('category') == category]
    
    # Apply pagination
    paginated_data = data[offset:offset + limit]
    
    # Map the data to Item types
    return [map_dict_to_item(item) for item in paginated_data]

def get_item_by_id(id: str) -> Optional[Item]:
    """
    Resolver for fetching a single item by ID
    """
    data = get_data_from_database()
    
    # Find the item with the matching ID
    for item in data:
        if str(item.get('id', '')) == id:
            return map_dict_to_item(item)
    
    return None
from dataclasses import dataclass
from typing import Optional, List

# This file will contain data models that will be used in the application
# These models will be adjusted based on the chosen dataset

@dataclass
class Item:
    """
    Base data model class for items in the dataset
    Will be extended based on the actual dataset columns
    """
    id: str
    name: str
    value: float
    category: str
    
    # Additional fields will be added based on the dataset structure

@dataclass
class PaginatedResponse:
    """
    Generic paginated response model
    """
    items: List
    total: int
    page: int
    limit: int
    
    @property
    def has_more(self) -> bool:
        return self.total > (self.page * self.limit)
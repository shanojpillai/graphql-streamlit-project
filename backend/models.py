from dataclasses import dataclass
from typing import Optional, List
import strawberry

# Define Strawberry types for GraphQL schema
@strawberry.type
class Item:
    id: str
    name: str
    value: float
    category: str

@strawberry.input
class ItemInput:
    name: str
    value: float
    category: str

# Define regular dataclasses for internal use
@dataclass
class ItemModel:
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
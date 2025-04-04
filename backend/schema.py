import strawberry
from typing import List, Optional
from models import Item

# Import resolvers - moved down to avoid circular imports
from resolvers import get_items, get_item_by_id

@strawberry.type
class Query:
    @strawberry.field
    def items(
        self, 
        limit: Optional[int] = 10, 
        offset: Optional[int] = 0,
        category: Optional[str] = None
    ) -> List[Item]:
        """Get a list of items with optional pagination and filtering"""
        return get_items(limit, offset, category)
    
    @strawberry.field
    def item(self, id: str) -> Optional[Item]:
        """Get a single item by ID"""
        return get_item_by_id(id)

# Create the schema
schema = strawberry.Schema(query=Query)
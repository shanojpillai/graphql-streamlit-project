import strawberry
from typing import List, Optional
from resolvers import get_items, get_item_by_id

# Define GraphQL types
@strawberry.type
class Item:
    id: str
    name: str
    value: float
    category: str
    
    # Additional fields will be added based on the dataset

@strawberry.type
class Query:
    @strawberry.field
    def items(
        self, 
        limit: Optional[int] = 10, 
        offset: Optional[int] = 0,
        category: Optional[str] = None
    ) -> List[Item]:
        return get_items(limit, offset, category)
    
    @strawberry.field
    def item(self, id: str) -> Optional[Item]:
        return get_item_by_id(id)

# Create the schema
schema = strawberry.Schema(query=Query)
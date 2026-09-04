from pydantic import BaseModel, Field
from typing import List, Optional

class ExtractedConstraints(BaseModel):
    categories: List[str] = Field(default_factory=list, description="List of product categories requested")
    max_budget: float = Field(default=0.0, description="Max budget in INR")
    priority: str = Field(default="rating", description="User preference: 'rating' or 'price'")

class ProductItem(BaseModel):
    id: str
    name: str
    category: str
    price: float
    rating: float

class RunAgentRequest(BaseModel):
    query: str
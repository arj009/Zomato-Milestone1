from pydantic import BaseModel
from typing import List, Optional

class RecommendRequest(BaseModel):
    location: str
    budget: str
    cuisine: Optional[str] = None
    min_rating: float = 3.5
    extra: Optional[str] = None

class RestaurantInfo(BaseModel):
    id: str
    name: str
    location: str
    rating: Optional[float]
    cost_for_two: Optional[float]
    cuisines: str
    rest_type: Optional[str]

class RecommendationResponse(BaseModel):
    rank: int
    restaurant: RestaurantInfo
    explanation: str

class EngineResponse(BaseModel):
    summary: str
    recommendations: List[RecommendationResponse]
    source: str

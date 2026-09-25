from typing import Literal
from pydantic import BaseModel, Field

class RegisterRequest(BaseModel):
    email: str = Field(min_length=5, max_length=200)
    password: str = Field(min_length=8, max_length=128)

class LoginRequest(BaseModel):
    email: str
    password: str

class HomeItem(BaseModel):
    category: str = Field(min_length=2, max_length=80)
    quantity: int = Field(default=1, ge=1, le=100)
    notes: str = Field(default="", max_length=300)

class HomeRequest(BaseModel):
    budget: float = Field(gt=0, le=10_000_000)
    room_type: str = Field(min_length=2, max_length=80)
    style: str = Field(default="modern", max_length=80)
    items: list[HomeItem] = Field(default_factory=list, max_length=30)

class PartyRequest(BaseModel):
    budget: float = Field(gt=0, le=10_000_000)
    guests: int = Field(gt=0, le=100_000)
    event_type: str = Field(min_length=2, max_length=80)
    venue: str = Field(default="flexible", max_length=120)
    city: str = Field(default="", max_length=100)
    preferences: str = Field(default="", max_length=500)

class JewelryRequest(BaseModel):
    budget: float = Field(gt=0, le=10_000_000)
    occasion: str = Field(min_length=2, max_length=100)
    style: str = Field(default="elegant", max_length=100)
    outfit_description: str = Field(default="", max_length=1000)

class RecommendationItem(BaseModel):
    title: str
    category: str
    platform: str
    estimated_price: float = Field(ge=0)
    reason: str
    url: str = ""

class RecommendationResponse(BaseModel):
    planner: Literal["home", "party", "jewelry"]
    budget: float
    budget_used: float
    summary: str
    allocation: dict[str, float] = {}
    recommendations: list[RecommendationItem] = []
    ai_generated: bool = False
    warning: str | None = None

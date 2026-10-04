from pydantic import BaseModel
from typing import Optional


class UserRegister(BaseModel):
    username: str
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class HomePlannerRequest(BaseModel):
    room_type: str
    budget: float
    quantity: int
    preferences: Optional[str] = None


class PartyPlannerRequest(BaseModel):
    budget: float
    guest_count: int
    event_type: str
    venue: Optional[str] = None


class JewelryPlannerRequest(BaseModel):
    budget: float
    occasion: str
    style: str
    outfit_description: Optional[str] = None
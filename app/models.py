# BaseModel - the base class all Pydantic models inherit from
# Field - lets us add constraints and descriptions to individual fields
# field_validator - a decorator that runs custom validation logic on a field

from pydantic import BaseModel, Field, field_validator

# Literal - restricts a field to a fixed set of allowed string values
from typing import Literal

# datetime - Python's built-in type for timestamps
from datetime import datetime

class QuoteRequest(BaseModel):

    property_type: Literal["flat", "terraced", "detached", "semi-detached"]
    bedrooms: int = Field(ge=1, le=10)
    property_value: float = Field(gt=0)

    @field_validator("property_value")
    @classmethod

    def round_property_value(cls, v:float) -> float:
        return round(v, 2)
    
class QuoteResponse(BaseModel):

    id: int
    property_type: str
    bedrooms: int
    property_value: float
    annual_premium: float
    created_at: datetime
    model_config = {"from_attributes": True}

class StatsResponse(BaseModel):

    property_type: str
    total_quotes: int
    average_premium: float
    average_property_value: float

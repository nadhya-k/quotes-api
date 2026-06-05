# BaseModel - the base class all Pydantic models inherit from
# Field - lets us add constraints and descriptions to individual fields
# field_validator - a decorator that runs custom validation logic on a field

from pydantic import BaseModel, Field, field_validator

# Literal - restricts a field to a fixed set of allowed string values
from typing import Literal

# datetime - Python's built-in type for timestamps
from datetime import datetime

# Create class QuoteRequest to validate data sent by the client in the POST/quotes request body.
# If any field fails validation, FastAPI will automatically return a 422 error with a description.
# Literal - restrict input to defined strings
class QuoteRequest(BaseModel):

    property_type: Literal["flat", "terraced", "detached", "semi-detached"]
    bedrooms: int = Field(ge=1, le=10)      # ge- greater than or equal to
    property_value: float = Field(gt=0)         # gt - greater than

    @field_validator("property_value")
    @classmethod

    def round_property_value(cls, v:float) -> float:
        return round(v, 2)

# Create class QuoteResponse to define the shape of the data that is returned to the client after a quote is created or retrieved.
# All fields must map directly to the columns in the quotes table.    
class QuoteResponse(BaseModel):

    id: int
    property_type: str
    bedrooms: int
    property_value: float
    annual_premium: float
    created_at: datetime
    model_config = {"from_attributes": True}        #tells Pydantic to read values from object attributes


# Create class Statsresponse to define the shape of the response from GET/stats.
class StatsResponse(BaseModel):

    property_type: str
    total_quotes: int
    average_premium: float
    average_property_value: float

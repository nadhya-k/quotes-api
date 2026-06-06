from fastapi import FastAPI, HTTPException, Query
# FastAPI - the application class
# HTTPException - raised to return error responses
# Query - used to declare optional query string parameters

from contextlib import asynccontextmanager
# asynccontextmanager - run startup and shutdown code around app lifecycle

from app import crud, models        # import business logic and Pydantic models

from app.database import create_tables      # the function that creates the quotes table on startup

from typing import Optional         # Optional[str] - |None allows parameter omission


# Runs create_tables() once when server starts. the yield seperates startup (before) and shutdown (after) logic.
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield


app = FastAPI(
    title="Quotes API",
    description="An insurance policy quote service - Python + FastAPI + PostgreSQL",
    version="1.0.0",
    lifespan=lifespan,      # lifespan wires up startup function
)


# Simple health check endpoint used by Docker to verify that the server is running.
@app.get("/health")
def health_check():
    return {"status":"ok"}


# Accept a quote request, calculate a premium, store it and return the full quote.
@app.post("/quotes", response_model=models.QuoteResponse, status_code=201)
def create_quote(request: models.QuoteRequest):

# Parse the JSON body request
    quote = crud.create_quote(
        property_type=request.property_type,
        bedrooms=request.bedrooms,
        property_value=request.property_value,
    )
    return quote

# Returns all quotes optionally filtered by property type using a query string.
# Query(default=None): makes property_type optional in the URL. fastAPI documents this parameter automatically in /docs.
@app.get("/quotes", response_model=list[models.QuoteResponse])
def list_quotes(
    property_type: Optional[str] = Query(default=None, description="Filter by property type")
):
    return crud.get_all_quotes(property_type=property_type)

# {quote_id} in the path is a path parameter extracted by FastAPI and passed into the function get_quote. 
# It is declared as an integer so FastAPI can validate it as an integer.
@app.get("/quotes/{quote_id}", response_model=models.QuoteResponse)
def get_quote(quote_id: int):
    quote = crud.get_quote_by_id(quote_id)

    if quote is None:
        raise HTTPException(status_code=404, detail=f"Quote {quote_id} not found")
    return quote

# Return aggregate statistics grouped by property type.
@app.get("/stats", response_model=list[models.StatsResponse])
def get_stats():
    return crud.get_stats()
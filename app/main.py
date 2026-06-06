from fastapi import FastAPI, HTTPException, Query
from contextlib import asynccontextmanager
from app import crud, models
from app.database import create_tables
from typing import Optional

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield


app = FastAPI(
    title="Quotes API",
    description="An insurance policy quote service - Python + FastAPI + PostgreSQL",
    version="1.0.0",
    lifespan=lifespan,
)

@app.get("/health")
def health_check():
    return {"status":"ok"}

@app.post("/quotes", response_model=models.QuoteResponse, status_code=201)
def create_quote(request: models.QuoteRequest):

    quote = crud.create_quote(
        property_type=request.property_type,
        bedrooms=request.bedrooms,
        property_value=request.property_value,
    )
    return quote

@app.get("/quotes/{quote_id}", response_model=models.QuoteResponse)
def get_quote(quote_id: int):
    quote = crud.get_quote_by_id(quote_id)

    if quote is None:
        raise HTTPException(status_code=404, detail=f"Quote {quote_id} not found")
    return quote 

@app.get("/stats", response_model=list[models.StatsResponse])
def get_stats():
    return crud.get_stats()
    
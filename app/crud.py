from app.database import get_connection, release_connection

from app import schemas

from typing import Optional

def calculate_premium(property_type: str, bedrooms: int, property_value: float) -> float:
    base_rates = {
        "flat": 120.0,
        "terraced": 140.0,
        "semi-detached": 160.0,
        "detached": 200.0,
    }

    base = base_rates[property_type]
    bedroom_surcharge = (bedrooms - 1)*15
    value_factor = property_value*0.001

    premium = base + bedroom_surcharge + value_factor
    return round(premium, 2)

def create_quote(property_type: str, bedrooms: int, property_value: float) -> dict:
    premium = calculate_premium(property_type, bedrooms, property_value)
    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute(
                schemas.INSERT_QUOTE,
                (property_type, bedrooms, property_value, premium)
            )
            row = cur.fetchone()
            conn.commit()
            columns = ["id", "property_type", "bedrooms", "property_value", "annual_premium", "created_at"]
            return dict(zip(columns,row))
        
    finally:
        release_connection(conn)

def get_all_quotes(property_type: Optional[str] = None) -> list[dict]:

    conn = get_connection()
    try:
        with conn.cursor() as cur:
            if property_type:
                cur.execute(schemas.SELECT_QUOTES_BY_TYPE, (property_type,))
            else:
                cur.execute(schemas.SELECT_ALL_QUOTES)

            rows = cur.fetchall()

        columns = ["id", "property_type", "bedrooms", "property_value", "annual_premium", "created_at"]
        return [dict(zip(columns,row)) for row in rows]
    finally:
        release_connection(conn)

def get_quotes_by_id(quote_id: int) -> Optional[dict]:
    conn = get_connection() 
    try:
        with conn.cursor()as cur:
            cur.execute(schemas.SELECT_QUOTE_BY_ID, (quote_id,))
            row = cur.fetchone()

        if row is None:
            return None
        
        columns = ["id", "property_type", "bedrooms", "property_value", "annual_premium", "created_at"]
        return dict(zip(columns,row))
    finally:
        release_connection()

def get_stats() -> list[dict]:

    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(schemas.SELECT_STATS)
            rows = cur.fetchall()

        columns = ["id", "property_type", "bedrooms", "property_value", "annual_premium", "created_at"]
        return [dict(zip(columns,row)) for row in rows]
    finally:
        release_connection()
        

                    
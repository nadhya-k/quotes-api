from app.database import get_connection, release_connection         # Importing the connection pool helpers defined in database.py file.

from app import schemas         # Importing the SQL string constants defined in schemas.py.

from typing import Optional         # Optional[X] means the value can be X or None.

# Define a function calculate_premium to calculate the annual insurance premium from quote inputs.

"""
Formula:
    base rate varies by property type (detached = higher risk) 
        + bedroom surcharge (more rooms = more contents to cover) 
            + value factor (0.1% of property value)
Returns a float rounded to 2 decimal places.
"""

def calculate_premium(property_type: str, bedrooms: int, property_value: float) -> float:
    base_rates = {      # Set up base_rates as a dictionary lookup which can be extended without using if/elif chains.
        "flat": 120.0,
        "terraced": 140.0,
        "semi-detached": 160.0,
        "detached": 200.0,
    }

    base = base_rates[property_type]        # Lookup the base rate for this property type.
    bedroom_surcharge = (bedrooms - 1)*15       # each bedroom above 1 adds £15.
    value_factor = property_value*0.001         # define value_factor as 0.1% of property value.

    premium = base + bedroom_surcharge + value_factor
    return round(premium, 2)        # Round money value returned to 2 decimal places.



# Define a function create_quote which calculates the premium, inserts a new quote row, and returns the created row as a dictionary with all quote fields.

def create_quote(property_type: str, bedrooms: int, property_value: float) -> dict:
    premium = calculate_premium(property_type, bedrooms, property_value)        # Calculate premium before calling database connection - if the calculation fails, nothing is written.
    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute(
                schemas.INSERT_QUOTE,
                (property_type, bedrooms, property_value, premium)      # values are passed as a tuple whcih psycopg2 maps to %s in order
            )
            row = cur.fetchone()        # fetchone() - retrieves the single row returned by RETURNING
            conn.commit()       # commit() - persists the INSERT to disk
            columns = ["id", "property_type", "bedrooms", "property_value", "annual_premium", "created_at"]
            return dict(zip(columns,row))       
        
        # dict() - converts the pairs into dictionary
        # zip - pairs each column name with its value from the row tuple
        
    finally:
        release_connection(conn)        # Always return the connection to the pool.



# Define a function get_all_quptes to return all quotes and apply optional filtering by property type.
# Optional[str] = None is used to mean that the caller can omit this aergument entirely.
def get_all_quotes(property_type: Optional[str] = None) -> list[dict]:

    conn = get_connection()
    try:
        with conn.cursor() as cur:
            if property_type:
                cur.execute(schemas.SELECT_QUOTES_BY_TYPE, (property_type,))        # trailing comma is a tuple
            else:
                cur.execute(schemas.SELECT_ALL_QUOTES)

            rows = cur.fetchall()       # fetchall() - returns a list of tuples, one per row

        columns = ["id", "property_type", "bedrooms", "property_value", "annual_premium", "created_at"]
        return [dict(zip(columns,row)) for row in rows]         # Use list comprehension to apply dict(zip(...)) to every row in one line
    finally:
        release_connection(conn)



# Define a function get_quotes_by_id that returns a single quote by it's primary key, or None if it doesn't exist. 
# The route handler uses None to decide whether to return a 404.
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



# Define a function get_stats to return aggregate statistics grouped by property type.
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
        

                    
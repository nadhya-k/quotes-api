## Quotes API
A REST API that creates and retrievs insurance policy quotes. This ASPI was built with Python, fastAPI, Pydantic, and PostgreSQL.

## Section 1 - tech Stack

-- Python 3.11 - application logic and insurance premium calculaton
-- FastAPI - REST API framework with automatic validation and docs
-- Pydantic - request/response validation and serialization
-- PostgreSQL 16 - relational database storing all quotes
-- pycopg2 - PostgreSQL driver for Python
-- Docker - containerised database for consistent local setup

## Section 2 - Project Structure

```
quotes-api/
|
|__ app/
|   |__ database.py
|   |__ models.py
|   |__ schemas.py
|   |__ crud.py
|   |__ main.py
|
|__ docker-compose.yml
|
|__ requirements.txt
|
|__ .env.example

```

## Section 3 - Getting started

### Step 1 - Clone and enter the project
Enter the following commands into the terminal:
`
git clone https://github.com/your-username/quotes-api.git
cd quotes-api
`

### Step 2 - Create and activate virtual environment
Enter the following commands into the terminal:
`
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate       # Windows
`

### Step 3 - Install dependencies
Enter the following commands into the terminal:
`  
pip install -r requirements.txt
`

### Step 4 - Configure environment
Enter the following commands into the terminal:
`
cp .env.example .env
`

The default values in .env.example match the Docker Compose config and work out of the box for local development.

### Step 5 - Start the database
Enter the following commands into the terminal:
`
docker compose up -d
`

### Step 6 - Start the API
Enter the following commands into the terminal:
`
uvicorn app.main:app --reload
`

The API is running at http://localhost:8000 with interactive docs available at http://localhost:800/docs


## Section 4 - API Endpoints

Method: GET
Path: /health
Description: Health Check

Method: POST
Path: /quotes
Description: Create a new quote

Method: GET
Path: /quotes 
Description: List all quotes (filter by type)

Method: GET
Path: /quotes/ {id}
Description: Get a single quote by ID

Method: GET
Path: /stats
Description: Aggregate stats grouped by type

---

## Section 5 - Example Requests

### Example Request - Create a quote

    curl -X POST http://localhost:8000/quotes \
      -H "Content-Type: application/json" \
      -d '{"property_type": "flat", "bedrooms": 2, "property_value": 350000}'

### Example Request - List all flat quotes

    curl http://localhost:8000/quotes?property_type=flat

### Example Request - Get quote by ID

    curl http://localhost:8000/quotes/1

### Example Request - View statistics

    curl http://localhost:8000/stats

---

## Section 6 - Insurance Premium Calculation

Annual Premium = Base rate + Bedroom Surcharge + Value Factor
 
Property Type: Flat
Base Rate: £120

Property Type: Terraced
Base Rate: £140

Property Type: Semi-detached
Base Rate: £160

Property Type: Detached
Base Rate: £200

-- Each bedroom above 1 adds £15
-- Value factor = 0.1% of property value
# Each constant defined in this file is a SQL string used by crud.py file.
# Parameterised queries use %s placeholders which psycopg2 substitutes with real values safely to prevent SQL injection by not interpolating user input directly into the string.

INSERT_QUOTE ="""
    INSERT INTO quotes (property_type, bedrooms, property_value, annual_premium)
    VALUES (%s, %s, %s, %s)
    RETURNING id, property_type, bedrooms, property_value, annual_premium, created_at      
"""
# RETURNING tells PostgreSQL to send basck the full row after inserting it to save making a second SELECT query to retrieve the id and created_at.

SELECT_ALL_QUOTES = """
    SELECT id, property_type, bedrooms, property_value, annual_premium, created_at
    FROM quotes
    ORDER BY created_at DESC
"""

# ORDER BY created_at DESC ensures the newest quotes are displayed first.

SELECT_QUOTES_BY_TYPE = """
    SELECT id, property_type, bedrooms, property_value, annual_premium, created_at
    FROM quotes
    WHERE property_type = %s
    ORDER BY created_at DESC
"""

# WHERE property_type = %s applies a filter to quotes that only match the given type.
# %s is the safe placeholder that is used by psycopg2 to handle quoting and escaping.

SELECT_QUOTE_BY_ID = """
    SELECT id, property_type, bedrooms, property_value, annual_premium, created_at
    FROM quotes
    WHERE id = %s
"""

SELECT_STATS = """
    SELECT 
        property_type,
        COUNT(*) AS total_quotes,
        ROUND(AVG(annual_premium), 2) AS average_premium,
        ROUND(AVG(property_value), 2) AS average_property_value,
    FROM quotes
    GROUP BY property_type
    ORDER BY total_quotes DESC
"""
# AVG is used to calculate the mean across all rows in the group.
# ROUND(..., 2) is used to round to 2 decimal places in SQL before returning.
# GROUP BY is used to collapse all rows with the same property_type into one summary row. Without GROUP BY, AVG and COUNT would operate on the entire table.
# ORDER BY is used to show the most common property types first.
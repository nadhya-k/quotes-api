INSERT_QUOTE ="""
    INSERT INTO quotes (property_type, bedrooms, property_value, annual_premium)
    VALUES (%s, %s, %s, %s)
    RETURNING id, property_type, bedrooms, property_value, annual_premium, created_at
"""

SELECT_ALL_QUOTES = """
    SELECT id, property_type, bedrooms, property_value, annual_premium, created_at
    FROM quotes
    ORDER BY created_at DESC
"""

SELECT_QUOTES_BY_TYPE = """
    SELECT id, property_type, bedrooms, property_value, annual_premium, created_at
    FROM quotes
    WHERE property_type = %s
    ORDER BY created_at DESC
"""

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
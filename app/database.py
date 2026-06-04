# This file manages the connection to PostgreSQL and creates the quotes table if it doesn't exist. Every other file imports from here.

import os 
# built-in: reads environment variables

from dotenv import load_dotenv
# reads .env file into os.environ

import psycopg2
# PostgreSQL driver for Python

from psycopg2.pool import SimpleConnectionPool
# Manages a pool of DB connections so a connection does not need to be opened/closed for every request


load_dotenv()
# Calls load_dotenv() before os.getenv and loads .env into the environment

DATABASE_URL = os.getenv("DATABASE_URL")
# Reads the connection string set in .env file

connection_pool = SimpleConnectionPool(1, 10, dsn=DATABASE_URL)
# SimpleConnectionPool keeps between 1 and 10 connections open
# minconn=1: always keep at least one connection ready
# maxconn=10: never open more than 10 simultaneous connections

def get_connection():
    return connection_pool.getconn()

def release_connection(conn):
    connection_pool.putconn(conn)

"""
Create the quotes table if it does not already exist to be called once at application startup. from main.py.
Use 'IF NOT EXISTS' so that it is safe to run every time - it won't fail or erase data if the table is already there.

"""
def create_tables():
    conn = get_connection()
    
    try:
        with conn.cursor as cur:
            cur.execute("""
                        
                        CREATE TABLE IF NOT EXISTS quotes (
                        
                        id SERIAL PRIMARY KEY,
                        property type VARCHAR(50) NOT NULL,
                        bedrooms INTEGER NOT NULL,
                        property_value NUMERIC (12,2) NOT NULL,
                        annual_premium NUMERIC (10,2) NOT NULL,
                        created_at TIMESTAMPZ DEFAULT NOW()
                        
                        )
                        
                        """)
            
            conn.commit()
            
    finally:
        release_connection(conn)

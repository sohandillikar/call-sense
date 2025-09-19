# src/data/database.py
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def create_tables():
    conn = psycopg2.connect(os.getenv('TIMESCALE_CONNECTION_STRING'))
    cur = conn.cursor()
    
    # Create tables for time-series data
    cur.execute("""
        CREATE TABLE IF NOT EXISTS competitor_pricing (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMPTZ NOT NULL,
            business_name VARCHAR(255),
            competitor_name VARCHAR(255),
            product_item VARCHAR(255),
            price DECIMAL(10,2),
            source VARCHAR(100)
        );
        
        CREATE TABLE IF NOT EXISTS review_analysis (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMPTZ NOT NULL,
            business_name VARCHAR(255),
            platform VARCHAR(100),
            rating INTEGER,
            review_text TEXT,
            sentiment_score DECIMAL(3,2),
            key_issues TEXT[]
        );
        
        CREATE TABLE IF NOT EXISTS customer_calls (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMPTZ NOT NULL,
            call_duration INTEGER,
            transcription TEXT,
            customer_issue VARCHAR(500),
            sentiment_score DECIMAL(3,2),
            resolution_status VARCHAR(100)
        );
    """)
    
    # Create hypertables for time-series optimization
    cur.execute("SELECT create_hypertable('competitor_pricing', 'timestamp', if_not_exists => TRUE);")
    cur.execute("SELECT create_hypertable('review_analysis', 'timestamp', if_not_exists => TRUE);")
    cur.execute("SELECT create_hypertable('customer_calls', 'timestamp', if_not_exists => TRUE);")
    
    conn.commit()
    cur.close()
    conn.close()
    print("✅ TigerData tables created successfully!")

if __name__ == "__main__":
    create_tables()
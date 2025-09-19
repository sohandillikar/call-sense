-- Initialize the database for AI Business Assistant
-- This script runs when the PostgreSQL container starts for the first time

-- Create the database if it doesn't exist (this is handled by POSTGRES_DB env var)
-- But we can add any additional setup here

-- Create extensions that might be useful
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Set timezone
SET timezone = 'UTC';

-- Create a user for the application (optional, using postgres user for simplicity)
-- CREATE USER ai_business_user WITH PASSWORD 'ai_business_password';
-- GRANT ALL PRIVILEGES ON DATABASE ai_business_assistant TO ai_business_user;

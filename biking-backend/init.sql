-- Database initialization script for Data Flow Hub
-- This script creates the necessary database and user

-- Create the database if it doesn't exist
CREATE DATABASE biking_data;
-- Create Airflow metadata database required by Airflow services
CREATE DATABASE airflow;

-- Create a user for the application (optional, using postgres for simplicity)
-- CREATE USER dataflowhub_user WITH PASSWORD 'your_password_here';
-- GRANT ALL PRIVILEGES ON DATABASE biking_data TO dataflowhub_user;

-- Connect to the biking_data database
\c biking_data;

-- Create extensions if needed
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- The tables will be created by SQLAlchemy when the application starts


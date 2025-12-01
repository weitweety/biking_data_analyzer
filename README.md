# Biking Data Analyzer

A comprehensive biking data flow management and visualization system built with Python, FastAPI, PostgreSQL, Apache Airflow, and React. (With the help from Cursor AI assistance).
This application provides ETL capabilities with a RESTful API for data management and monitoring, along with an interactive web frontend for data visualization.

## Architecture

```
biking_data_analyzer/
│
├── biking-backend/           # Backend services
│   ├── airflow/
│   │   ├── dags/
│   │   │   └── etl_pipeline.py
│   │   ├── logs/
│   │   ├── plugins/
│   │   └── config/
│   │
│   ├── app/
│   │   ├── main.py           # FastAPI entry point
│   │   ├── db.py             # SQLAlchemy setup
│   │   ├── models.py         # ORM models
│   │   ├── crud.py           # Database queries
│   │   ├── schemas.py        # Pydantic models
│   │   └── utils.py         # Helper functions
│   │
│   ├── etl/
│   │   ├── extract.py        # Data extraction from CSV
│   │   ├── transform.py      # Data transformation
│   │   └── load.py           # Data loading to PostgreSQL
│   │
│   ├── data/                 # CSV data files to be processed
│   ├── processed/            # Processed CSV data files
│   ├── init.sql              # Database initialization script
│   ├── requirements.txt      # Python dependencies
│   └── start.sh              # Startup script
│
├── biking-frontend/          # Frontend React application
│   ├── src/
│   │   ├── api/              # API client
│   │   ├── components/       # React components
│   │   │   ├── NavigationBar.jsx
│   │   │   ├── TripDurationChart.jsx
│   │   │   └── TripHourRangeChart.jsx
│   │   ├── App.jsx           # Main app component
│   │   └── main.jsx         # Entry point
│   ├── Dockerfile            # Frontend Docker image
│   ├── nginx.conf            # Nginx configuration
│   ├── package.json          # Node.js dependencies
│   └── vite.config.js        # Vite configuration
│
├── docker-compose.yml        # Main Docker Compose configuration
├── Dockerfile.api            # Backend API Docker image
└── README.md
```

## Tech Stack

- **Backend**: Python 3.11, FastAPI
- **Frontend**: React 18, Vite, Recharts
- **Database**: PostgreSQL 15
- **ORM**: SQLAlchemy 2.0
- **Workflow**: Apache Airflow 2.7.3
- **Containerization**: Docker & Docker Compose
- **Data Processing**: Pandas
- **Web Server**: Nginx (for frontend)

## Features

### API Endpoints

- **GET /ping** - Health check endpoint
- **GET /count** - Get count statistics of the data
- **POST /refresh** - Manually trigger the ETL pipeline
- **GET /top/{n}** - Get top N records ordered by start time
- **GET /health/airflow** - Check Airflow health status
- **GET /trip-duration-stats** - Get trip duration statistics (for charts)
- **GET /hour-range-stats** - Get trip hour range statistics (for charts)

### Frontend Features

- **Interactive Charts**: Visualize trip duration and hour range statistics
- **Navigation**: Easy switching between different chart views
- **Responsive Design**: Modern, dark-themed UI
- **Real-time Data**: Fetches data from the backend API

### ETL Pipeline

The ETL pipeline processes CSV files through three stages:

1. **Extract**: Reads CSV files from the `data/` directory
2. **Transform**: Cleans, normalizes, and validates the data
3. **Load**: Stores the processed data in PostgreSQL
4. **Move**: Move the processed csv files from `data/` to `processed/`

### Data Model

The application uses a simple data model with the following fields:

- tripduration: int
- start_time: datetime
- stop_time: datetime
- start_station_id: Optional[int]
- start_station_name: Optional[str]
- start_station_latitude: Optional[float]
- start_station_longitude: Optional[float]
- end_station_id: Optional[int]
- end_station_name: Optional[str]
- end_station_latitude: Optional[float]
- end_station_longitude: Optional[float]
- bike_id: Optional[int]
- user_type: Optional[str]
- birth_year: Optional[int]
- gender: Optional[int]

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Python 3.11+ (for local development)

### Using Docker Compose (Recommended)

1. **Clone and navigate to the project root**:
   ```bash
   cd /home/syssec/biking_data_analyzer
   ```

2. **Build and start all services**:
   ```bash
   docker-compose build
   docker-compose up -d
   ```
   - The first time you run this, `init.sql` will be executed automatically to create the database in the PostgreSQL container.

3. **Access the services**:
   - **Frontend Web App**: http://localhost:3000
   - **API**: http://localhost:8000
   - **API Documentation**: http://localhost:8000/docs
   - **Airflow Web UI**: http://localhost:8080 (admin/admin)
   - **PostgreSQL**: localhost:5433 (postgres/postgres)

4. **Test the API**:
   ```bash
   # Health check
   curl http://localhost:8000/ping
   
   # Get records count
   curl http://localhost:8000/count
   
   # Get trip duration stats
   curl http://localhost:8000/trip-duration-stats
   
   # Get hour range stats
   curl http://localhost:8000/hour-range-stats
   
   # Get top 5 records
   curl http://localhost:8000/top/5
   
   # Trigger ETL pipeline
   curl -X POST http://localhost:8000/refresh
   ```

5. **Rebuild specific services** (after code changes):
   ```bash
   # Rebuild and restart only the frontend
   docker-compose build frontend
   docker-compose up -d frontend
   
   # Rebuild and restart only the API
   docker-compose build api
   docker-compose up -d api
   ```

## Configuration

### Environment Variables

#### Backend Environment Variables

The backend services use the following environment variables (set in `docker-compose.yml`):

```env
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/biking_data
AIRFLOW_URL=http://airflow-webserver:8080
AIRFLOW_USERNAME=admin
AIRFLOW_PASSWORD=admin
```

#### Frontend Environment Variables

For local frontend development, you can set:

```env
VITE_API_URL=http://localhost:8000/api/
```

If not set, the frontend will use `/api/` as the default (for production with nginx proxy).

### Database Configuration

The application uses PostgreSQL with the following default settings:

- **Host**: localhost (or `postgres` service name in Docker network)
- **Port**: 5433 (mapped from container's 5432)
- **Database**: biking_data
- **Username**: postgres
- **Password**: postgres

Note: The port is mapped to 5433 on the host to avoid conflicts with local PostgreSQL installations.

## API Documentation

Once the API is running, you can access the interactive API documentation at:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Frontend Application

The frontend application provides interactive data visualization:

- **Main Application**: http://localhost:3000
- **Trip Duration Chart**: http://localhost:3000/trip-duration
- **Hour Range Chart**: http://localhost:3000/hour-range

The frontend uses React Router for navigation and Recharts for data visualization. All API calls are proxied through nginx to the backend API service.

## Airflow Web UI

Access the Airflow web interface at http://localhost:8080 with the following credentials:

- **Username**: admin
- **Password**: admin

The ETL pipeline (`etl_pipeline`) will be available in the DAGs list and can be triggered manually or will run automatically every hour.

## Data

In this project we use the data from [Citi Bike](https://citibikenyc.com/system-data)

The `biking-backend/data/` directory contains input CSV files.
Each CSV file should have the following columns:
"tripduration"
"starttime"
"stoptime"
"start station id"
"start station name"
"start station latitude"
"start station longitude"
"end station id"
"end station name"
"end station latitude"
"end station longitude"
"bikeid","usertype"
"birth year","gender"


## ETL Pipeline Details

### Extract Phase
- Reads all CSV files from the `biking-backend/data/` directory
- Validates file existence and format
- Combines multiple CSV files into a single DataFrame

### Transform Phase
- Cleans and normalizes text data
- Validates and converts numeric values
- Groups trip durations into bins for statistics

### Load Phase
- Validates database connection
- Clears existing data (optional)
- Bulk inserts transformed data
- Provides loading statistics
- Moves processed files to `biking-backend/processed/` directory

## Monitoring and Logging

The application includes comprehensive logging:

- **API logs**: Request/response logging
- **ETL logs**: Pipeline execution logging
- **Airflow logs**: Workflow execution logs

Logs are available in:
- **API**: Console output (view with `docker-compose logs api`)
- **Frontend**: Nginx logs (view with `docker-compose logs frontend`)
- **Airflow**: Web UI and log files in `biking-backend/airflow/logs/`

## Troubleshooting

### Common Issues

1. **Database Connection Error**:
   - Ensure PostgreSQL is running
   - Check database credentials
   - Verify network connectivity

2. **Airflow Connection Error**:
   - Ensure Airflow services are running
   - Check Airflow web UI accessibility
   - Verify DAG file syntax

3. **ETL Pipeline Failures**:
   - Check CSV file format and location
   - Verify data directory permissions
   - Review Airflow task logs

### Useful Commands

```bash
# Check service status
docker-compose ps

# View logs
docker-compose logs api
docker-compose logs frontend
docker-compose logs airflow-webserver
docker-compose logs postgres

# Follow logs in real-time
docker-compose logs -f api
docker-compose logs -f frontend

# Restart specific services
docker-compose restart api
docker-compose restart frontend
docker-compose restart airflow-webserver

# Rebuild and restart a service
docker-compose build frontend
docker-compose up -d frontend

# Stop all services
docker-compose down

# Stop and remove volumes (clean start)
docker-compose down -v

# View service logs with timestamps
docker-compose logs -t api
```
---

**Happy Data Processing! 🚀**



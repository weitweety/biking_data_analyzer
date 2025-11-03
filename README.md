# Biking Data Analyzer

A comprehensive data flow management system built with Python, FastAPI, PostgreSQL, and Apache Airflow. This application provides ETL capabilities with a RESTful API for data management and monitoring.

## Architecture

```
biking_data_analyzer/
│
├── airflow/
│   ├── dags/
│   │   └── etl_pipeline.py
│   └── docker-compose.yml
│
├── app/
│   ├── main.py               # FastAPI entry point
│   ├── db.py                 # SQLAlchemy setup
│   ├── models.py             # ORM models
│   ├── crud.py               # Database queries
│   ├── schemas.py            # Pydantic models
│   └── utils.py              # Helper functions
│
├── etl/
│   ├── extract.py            # Data extraction from CSV
│   ├── transform.py          # Data transformation
│   └── load.py               # Data loading to PostgreSQL
│
├── data/                     # Sample CSV data files
├── docker-compose.yml        # Main Docker Compose configuration
├── Dockerfile.api            # API Docker image
├── requirements.txt          # Python dependencies
└── README.md
```

## Tech Stack

- **Backend**: Python 3.11, FastAPI
- **Database**: PostgreSQL 15
- **ORM**: SQLAlchemy 2.0
- **Workflow**: Apache Airflow 2.7.3
- **Containerization**: Docker & Docker Compose
- **Data Processing**: Pandas

## Features

### API Endpoints

- **GET /ping** - Health check endpoint
- **GET /summary** - Get summary statistics of the data
- **POST /refresh** - Manually trigger the ETL pipeline
- **GET /top/{n}** - Get top N records by value
- **GET /records** - Get all records with pagination
- **GET /health/airflow** - Check Airflow health status

### ETL Pipeline

The ETL pipeline processes CSV files through three stages:

1. **Extract**: Reads CSV files from the `data/` directory
2. **Transform**: Cleans, normalizes, and validates the data
3. **Load**: Stores the processed data in PostgreSQL

### Data Model

The application uses a simple data model with the following fields:

- `id`: Primary key
- `name`: Record name
- `category`: Data category
- `value`: Numeric value
- `description`: Optional description
- `created_at`: Timestamp when record was created
- `updated_at`: Timestamp when record was last updated

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Python 3.11+ (for local development)

### Using Docker Compose (Recommended)

1. **Clone and navigate to the project**:
   ```bash
   cd /home/syssec/biking_data_analyzer
   ```

2. **Start all services**:
   ```bash
   docker-compose up -d
   ```
   - Only for first time: init.sql should be executed to create a database in the PostgreSQL container.

3. **Access the services**:
   - **API**: http://localhost:8000
   - **Airflow Web UI**: http://localhost:8080 (admin/admin)
   - **PostgreSQL**: localhost:5432 (postgres/postgres)

4. **Test the API**:
   ```bash
   # Health check
   curl http://localhost:8000/ping
   
   # Get summary
   curl http://localhost:8000/summary
   
   # Get top 5 records
   curl http://localhost:8000/top/5
   
   # Trigger ETL pipeline
   curl -X POST http://localhost:8000/refresh
   ```

### Local Development Setup

1. **Create virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Start PostgreSQL** (using Docker):
   ```bash
   docker run -d --name postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=biking_data -p 5432:5432 postgres:15
   ```

4. **Start Airflow** (using Docker Compose):
   ```bash
   cd airflow
   docker-compose up -d
   ```

5. **Run the API**:
   ```bash
   cd app
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/biking_data
AIRFLOW_URL=http://localhost:8080
```

### Database Configuration

The application uses PostgreSQL with the following default settings:

- **Host**: localhost
- **Port**: 5432
- **Database**: biking_data
- **Username**: postgres
- **Password**: postgres

## API Documentation

Once the API is running, you can access the interactive API documentation at:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Airflow Web UI

Access the Airflow web interface at http://localhost:8080 with the following credentials:

- **Username**: admin
- **Password**: admin

The ETL pipeline (`etl_pipeline`) will be available in the DAGs list and can be triggered manually or will run automatically every hour.

## Sample Data

The `data/` directory contains sample CSV files:

- `sample_data.csv` - General company data
- `financial_data.csv` - Financial services companies
- `healthcare_data.csv` - Healthcare companies

Each CSV file should have the following columns:
- `name`: Company or entity name
- `category`: Data category
- `value`: Numeric value
- `description`: Description of the entity

## ETL Pipeline Details

### Extract Phase
- Reads all CSV files from the `data/` directory
- Validates file existence and format
- Combines multiple CSV files into a single DataFrame

### Transform Phase
- Cleans and normalizes text data
- Validates and converts numeric values
- Normalizes category names
- Removes duplicate records
- Sorts data by value (descending)

### Load Phase
- Validates database connection
- Clears existing data (optional)
- Bulk inserts transformed data
- Provides loading statistics

## Monitoring and Logging

The application includes comprehensive logging:

- **API logs**: Request/response logging
- **ETL logs**: Pipeline execution logging
- **Airflow logs**: Workflow execution logs

Logs are available in:
- **API**: Console output
- **Airflow**: Web UI and log files in `airflow/logs/`

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
docker-compose logs airflow-webserver
docker-compose logs postgres

# Restart services
docker-compose restart api
docker-compose restart airflow-webserver

# Stop all services
docker-compose down

# Remove volumes (clean start)
docker-compose down -v
```

## Development

### Adding New Data Sources

1. Add CSV files to the `data/` directory
2. Ensure CSV format matches expected schema
3. The ETL pipeline will automatically process new files

### Extending the API

1. Add new endpoints in `app/main.py`
2. Create corresponding CRUD operations in `app/crud.py`
3. Define Pydantic schemas in `app/schemas.py`
4. Update database models if needed in `app/models.py`

### Customizing ETL Pipeline

1. Modify transformation logic in `etl/transform.py`
2. Add new extraction methods in `etl/extract.py`
3. Extend loading capabilities in `etl/load.py`
4. Update the Airflow DAG in `airflow/dags/etl_pipeline.py`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues and questions:

1. Check the troubleshooting section
2. Review the logs for error messages
3. Create an issue in the repository
4. Contact the development team

---

**Happy Data Processing! 🚀**



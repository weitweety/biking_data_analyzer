# Data Flow Hub - Quick Start Script

echo "🚀 Starting Data Flow Hub..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

# Check if Docker Compose is available
if ! docker compose version > /dev/null 2>&1; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose and try again."
    exit 1
fi

echo "✅ Docker is running"

# Create necessary directories
mkdir -p airflow/logs airflow/plugins airflow/config

# Start the services
echo "🐳 Starting services with Docker Compose..."
docker compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 30

# Check service health
echo "🔍 Checking service health..."

# Check API health
if curl -s http://localhost:8000/ping > /dev/null; then
    echo "✅ API is running at http://localhost:8000"
else
    echo "❌ API is not responding"
fi

# Check Airflow health
if curl -s http://localhost:8080/health > /dev/null; then
    echo "✅ Airflow is running at http://localhost:8080"
else
    echo "❌ Airflow is not responding"
fi

# Check PostgreSQL
if docker compose exec postgres pg_isready -U postgres > /dev/null 2>&1; then
    echo "✅ PostgreSQL is running"
else
    echo "❌ PostgreSQL is not responding"
fi

echo ""
echo "🎉 Data Flow Hub is ready!"
echo ""
echo "📊 Access points:"
echo "   - API: http://localhost:8000"
echo "   - API Docs: http://localhost:8000/docs"
echo "   - Airflow: http://localhost:8080 (admin/admin)"
echo "   - PostgreSQL: localhost:5432 (postgres/postgres)"
echo ""
echo "🧪 Test the API:"
echo "   curl http://localhost:8000/ping"
echo "   curl http://localhost:8000/summary"
echo "   curl http://localhost:8000/top/5"
echo ""
echo "🔄 Trigger ETL pipeline:"
echo "   curl -X POST http://localhost:8000/refresh"
echo ""
echo "📝 View logs:"
echo "   docker compose logs -f api"
echo "   docker compose logs -f airflow-webserver"
echo ""
echo "🛑 Stop services:"
echo "   docker compose down"
echo ""
echo "🐳 Starting services with Docker Compose..."
echo "   docker compose up -d"

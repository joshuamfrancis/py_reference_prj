# Python REST API Project

A simple, well-structured Python REST API built with Flask, complete with sample endpoints and comprehensive pytest unit tests.

## Project Structure

```
py_reference_prj/
├── app/
│   ├── __init__.py           # Flask app factory
│   ├── config.py             # Configuration settings
│   ├── models.py             # Data models and in-memory storage
│   └── routes.py             # API endpoints
├── tests/
│   ├── conftest.py           # Pytest configuration and fixtures
│   ├── test_health.py        # Health check tests
│   ├── test_create_user.py   # User creation tests
│   ├── test_get_user.py      # User retrieval tests
│   ├── test_update_user.py   # User update tests
│   ├── test_delete_user.py   # User deletion tests
│   └── test_integration.py   # Integration tests
├── requirements.txt          # Python dependencies
├── run.py                    # Application entry point
└── README.md                 # This file
```

## Features

- **RESTful API endpoints** for user management (CRUD operations)
- **In-memory data storage** for simplicity
- **Comprehensive test coverage** with pytest
- **Error handling** for invalid requests
- **JSON request/response format**
- **Development configuration** with debug mode

## API Endpoints

### Health Check
- `GET /api/health` - Check API health status

### User Management
- `GET /api/users` - List all users
- `GET /api/users/<id>` - Get a specific user
- `POST /api/users` - Create a new user
- `PUT /api/users/<id>` - Update a user
- `DELETE /api/users/<id>` - Delete a user
- `GET /api/users/count` - Get total user count

## Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd py_reference_prj
   ```

2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

Start the development server:

```bash
python run.py
```

The API will be available at `http://localhost:5000`

### Example Requests

**Create a user:**
```bash
curl -X POST http://localhost:5000/api/users \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "email": "john@example.com"}'
```

**Get all users:**
```bash
curl http://localhost:5000/api/users
```

**Get a specific user:**
```bash
curl http://localhost:5000/api/users/1
```

**Update a user:**
```bash
curl -X PUT http://localhost:5000/api/users/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "Jane Doe"}'
```

**Delete a user:**
```bash
curl -X DELETE http://localhost:5000/api/users/1
```

## Docker

Build the Docker image locally (single-arch):
```bash
docker build -t <your-docker-username>/py_reference_prj:latest .
```

Run the container locally:
```bash
docker run -p 5000:5000 <your-docker-username>/py_reference_prj:latest
```

Build and push a multi-architecture image with Buildx to Docker Hub:
```bash
# create and use a buildx builder (one-time)
docker buildx create --use --name multi-builder

docker buildx build --platform linux/amd64,linux/arm64 \
  -t <your-docker-username>/py_reference_prj:latest \
  -t <your-docker-username>/py_reference_prj:$(git rev-parse --short HEAD) \
  --push .
```

Scan the built image with Trivy (local example):
```bash
# install trivy: https://aquasecurity.github.io/trivy/v0.40.0/installation/
trivy image --severity CRITICAL,HIGH <your-docker-username>/py_reference_prj:latest
```

Notes for CI (GitHub Actions):
- The provided CI workflow will build the image, run a Trivy scan, and push to Docker Hub only if the scan passes.
- Add the following repository secrets in GitHub settings: `DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN`.
- The workflow tags images as `<DOCKERHUB_USERNAME>/py_reference_prj:latest` and `<DOCKERHUB_USERNAME>/py_reference_prj:<sha>`.

## Running Tests

Run all tests:
```bash
python -m pytest tests/ -v
```

Run tests with coverage:
```bash
python -m pytest tests/ --cov=app
```

Run specific test file:
```bash
python -m pytest tests/test_health.py -v
```

Run tests and show only failures:
```bash
python -m pytest tests/ --tb=short
```

**Note:** Use `python -m pytest` instead of just `pytest` to ensure proper module resolution of the `app` package.

## Test Coverage

The project includes comprehensive test suites:

- **test_health.py** - Health check endpoint tests
- **test_create_user.py** - User creation with validation
- **test_get_user.py** - User retrieval operations
- **test_update_user.py** - User update operations
- **test_delete_user.py** - User deletion operations
- **test_integration.py** - Full workflow integration tests

## Dependencies

- **Flask** - Web framework
- **pytest** - Testing framework
- **pytest-cov** - Coverage reporting

## Future Enhancements

- Add database integration (SQLAlchemy, SQLite/PostgreSQL)
- Add authentication and authorization
- Add input validation and schema validation
- Add API documentation (Swagger/OpenAPI)
- Add logging and monitoring
- Add Docker containerization
- Deploy to cloud platforms (Heroku, AWS, GCP)

## License

This project is open source and available under the MIT License.

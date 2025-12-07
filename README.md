# Async FastAPI App

A modern asynchronous FastAPI application with background task processing and SQLite storage.

## Requirements

- Python 3.11+
- fastapi==0.104.1
- uvicorn[standard]==0.24.0
- pydantic==2.5.0
- python-multipart==0.0.6
- pytest==7.4.3
- httpx==0.25.2

## Installation

### Using Conda

```bash
conda create -n async-fastapi python=3.11
conda activate async-fastapi
pip install -r requirements.txt
```

### Using venv

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Project Structure

```
async-fastapi-app/
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI application entry point
│   ├── models.py         # Pydantic models
│   ├── background.py     # Background task management
│   └── storage.py        # Data persistence layer
├── tests/
│   ├── __init__.py
│   └── test_api.py       # API tests
├── requirements.txt      # Project dependencies
└── README.md            # This file
```

## Running the Application

Activate the environment first:

```bash
conda activate async-fastapi
```

Start the development server:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000/docs`

## Running Tests

### Run all tests

```bash
conda activate async-fastapi
pytest tests/test_api.py -v
```

### Run tests with verbose output

```bash
pytest tests/test_api.py -v -s
```

### Run a specific test class

```bash
# Test health endpoints
pytest tests/test_api.py::TestHealthEndpoint -v

# Test upload endpoints
pytest tests/test_api.py::TestUploadEndpoint -v

# Test status endpoints
pytest tests/test_api.py::TestStatusEndpoint -v
```

### Run a specific test

```bash
pytest tests/test_api.py::TestUploadEndpoint::test_upload_invoice_returns_200 -v
```

### Run tests and stop on first failure

```bash
pytest tests/test_api.py -v -x
```

### Skip timing tests (faster run)

```bash
pytest tests/test_api.py -v -k "not processing"
```

### Test Coverage

Test suite includes 21 comprehensive tests covering:

- **Health Check** (2 tests) - Verify health endpoint
- **Upload Endpoint** (6 tests) - Document upload with validation
- **Process Endpoint** (3 tests) - Process status retrieval
- **Status Endpoint** (6 tests) - Job status tracking
- **Background Processing** (2 tests) - Async task execution
- **Error Handling** (2 tests) - Error cases and validation

**Expected Output:**
```
======================== 21 passed in 36.17s ========================
```

## API Endpoints

### POST `/upload`
Upload a document and start background processing.

**Request:**
```json
{
  "type": "invoice",
  "content": {"amount": 1000, "vendor": "ABC Corp"},
  "metaData": {"reference": "INV-001"}
}
```

**Response:**
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "message": "Document received. Processing started.",
  "timestamp": "2024-12-08T10:30:45.123456"
}
```

### GET `/status/{job_id}`
Get the processing status of a job.

**Response:**
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "progress": 100,
  "result": {
    "invoice_number": "INV-5678",
    "amount": 1234.56,
    "status": "processed"
  },
  "created_at": "2024-12-08T10:30:45.123456",
  "updated_at": "2024-12-08T10:30:48.123456"
}
```

### POST `/process`
Check processing status with job ID and document type.

**Request:**
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "document": "invoice"
}
```

### GET `/health`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-12-08T10:30:45.123456"
}
```

## Interactive API Documentation

Visit the interactive Swagger UI:
- **Swagger**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Features

- Asynchronous request handling with FastAPI
- Background task processing (2-3 second delays)
- Data validation with Pydantic
- In-memory job storage
- UUID-based job tracking
- Comprehensive test suite (21 tests)
- Type hints and async/await patterns
- RESTful API design

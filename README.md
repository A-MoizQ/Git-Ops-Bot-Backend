# Git-Ops-Bot-Backend
Automated git ops bot backend server

## Setup

To set up the development environment, run:

```bash
./setup.sh
```

This script will:
1. Create a virtual environment in the `venv` directory
2. Activate the virtual environment
3. Install all dependencies from `requirements.txt`

## Running the Server

After setup, you can run the FastAPI server with:

```bash
source venv/bin/activate
uvicorn main:app --reload
```

The server will start on `http://localhost:8000`

## API Endpoints

- `GET /` - Welcome message
- `GET /health` - Health check endpoint
- `GET /docs` - Interactive API documentation (Swagger UI)

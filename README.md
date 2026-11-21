# SWYNEX Python API Project

## Task Management REST API

A Python-based REST API developed using FastAPI and SQLite to manage tasks efficiently. The application supports creating, retrieving, updating, and deleting tasks through HTTP requests.

## Project Overview

This project demonstrates how to build a REST API using Python. It provides endpoints for task management, validates incoming data, handles errors, and stores task information in an SQLite database.

## Technologies Used

- Python 3.13
- FastAPI
- SQLite
- Pydantic
- Uvicorn
- Pytest
- HTTPX

## Features

- Create new tasks.
- Retrieve all tasks.
- Retrieve individual tasks by ID.
- Update existing tasks.
- Delete tasks.
- Validate API request data.
- Handle missing task errors.
- Store information using SQLite.
- Interactive Swagger API documentation.
- Automated API testing.

## Project Structure

```text
SWYNEX-Python-API-Project/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   └── schemas.py
│
├── tests/
│   ├── __init__.py
│   └── test_api.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/SWYNEX-Python-API-Project.git
```

Navigate into the project:

```bash
cd SWYNEX-Python-API-Project
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Running the Application

Start the FastAPI server:

```bash
python -m uvicorn app.main:app --reload
```

Open the API documentation:

http://127.0.0.1:8000/docs

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | / | Welcome message |
| POST | /tasks | Create a task |
| GET | /tasks | Retrieve all tasks |
| GET | /tasks/{task_id} | Retrieve a task |
| PATCH | /tasks/{task_id} | Update a task |
| DELETE | /tasks/{task_id} | Delete a task |

## Example API Request

POST /tasks

```json
{
  "title": "Learn Python API",
  "description": "Complete SWYNEX Task 3",
  "status": "pending"
}
```

## Database

The project uses SQLite to store task information.

The database is automatically initialized when the application starts.

## Testing

Run automated tests using:

```bash
python -m pytest tests -v
```

The test suite covers API functionality, data validation, task creation, retrieval, updating, deletion, and error handling.

## Learning Outcomes

Through this project, I gained practical experience in:

- REST API development.
- Python backend programming.
- Database connectivity.
- Request and response handling.
- Data validation using Pydantic.
- Exception handling.
- API testing.
- Backend application development.


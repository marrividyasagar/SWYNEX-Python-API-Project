
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, status

from app.database import (
    get_connection,
    initialize_database
)

from app.schemas import TaskCreate, TaskUpdate


@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_database()
    yield


app = FastAPI(
    title="SWYNEX Task Management API",
    description="A REST API for managing tasks using Python and SQLite.",
    version="1.0.0",
    lifespan=lifespan
)


@app.get("/")
def home():
    return {
        "message": "Welcome to SWYNEX Task Management API",
        "status": "Running",
        "documentation": "/docs"
    }


# CREATE TASK
@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate):

    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            INSERT INTO tasks (title, description, status)
            VALUES (?, ?, ?)
            """,
            (task.title, task.description, task.status)
        )

        connection.commit()

        task_id = cursor.lastrowid

        row = connection.execute(
            "SELECT * FROM tasks WHERE id = ?",
            (task_id,)
        ).fetchone()

        return dict(row)

    finally:
        connection.close()


# GET ALL TASKS
@app.get("/tasks")
def get_all_tasks():

    connection = get_connection()

    try:
        rows = connection.execute(
            "SELECT * FROM tasks ORDER BY id DESC"
        ).fetchall()

        return [dict(row) for row in rows]

    finally:
        connection.close()


# GET TASK BY ID
@app.get("/tasks/{task_id}")
def get_task(task_id: int):

    connection = get_connection()

    try:
        row = connection.execute(
            "SELECT * FROM tasks WHERE id = ?",
            (task_id,)
        ).fetchone()

        if row is None:
            raise HTTPException(
                status_code=404,
                detail="Task not found"
            )

        return dict(row)

    finally:
        connection.close()


# UPDATE TASK
@app.patch("/tasks/{task_id}")
def update_task(task_id: int, task: TaskUpdate):

    update_data = task.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="Provide at least one field to update"
        )

    if any(value is None for value in update_data.values()):
        raise HTTPException(
            status_code=422,
            detail="Updated fields cannot be null"
        )

    connection = get_connection()

    try:
        existing = connection.execute(
            "SELECT * FROM tasks WHERE id = ?",
            (task_id,)
        ).fetchone()

        if existing is None:
            raise HTTPException(
                status_code=404,
                detail="Task not found"
            )

        allowed_fields = {
            "title",
            "description",
            "status"
        }

        fields = [
            field for field in update_data
            if field in allowed_fields
        ]

        assignments = ", ".join(
            f"{field} = ?" for field in fields
        )

        values = [update_data[field] for field in fields]

        connection.execute(
            f"UPDATE tasks SET {assignments} WHERE id = ?",
            (*values, task_id)
        )

        connection.commit()

        updated = connection.execute(
            "SELECT * FROM tasks WHERE id = ?",
            (task_id,)
        ).fetchone()

        return dict(updated)

    finally:
        connection.close()


# DELETE TASK
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):

    connection = get_connection()

    try:
        existing = connection.execute(
            "SELECT * FROM tasks WHERE id = ?",
            (task_id,)
        ).fetchone()

        if existing is None:
            raise HTTPException(
                status_code=404,
                detail="Task not found"
            )

        connection.execute(
            "DELETE FROM tasks WHERE id = ?",
            (task_id,)
        )

        connection.commit()

        return {
            "message": "Task deleted successfully",
            "task_id": task_id
        }

    finally:
        connection.close()

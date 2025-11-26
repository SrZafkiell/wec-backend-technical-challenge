from ..database.db import db_session
from ..models.schemas import NumberRecord
from tinydb import Query
from typing import List, Optional
from threading import Lock
from datetime import datetime

TABLE_NAME = "numbers"
_repository_lock = Lock()

def insert_number(record: NumberRecord) -> Optional[dict]:
    """Insert a new number into the database."""
    try:
        data = record.model_dump()
        if isinstance(data.get("created_at"), datetime):
            dt = data["created_at"]
            data["created_at"] = dt.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        
        with _repository_lock:
            with db_session() as db:
                table = db.table(TABLE_NAME)
                doc_id = table.insert(data)
                return {**data, "id": doc_id}
    except Exception as e:
        print(f"Failed to insert number: {e}")
        return None

def list_numbers_for_user(username: str) -> List[dict]:
    """List all numbers for a specific user."""
    try:
        with db_session() as db:
            table = db.table(TABLE_NAME)
            q = Query()
            rows = table.search(q.username == username)
            
            # Add doc_id as "id" to each row
            results = [{**doc, "id": doc.doc_id} for doc in rows]
            
            results_sorted = sorted(
                results,
                key=lambda r: r.get("created_at") or "1970-01-01T00:00:00",
                reverse=False
            )
            return results_sorted
    except Exception as e:
        print(f"Failed to list numbers for user {username}: {e}")
        return []

def get_number_by_id(number_id: int, username: str) -> Optional[dict]:
    """Get a number by TinyDB doc_id (only if owned by username)."""
    try:
        with db_session() as db:
            table = db.table(TABLE_NAME)
            doc = table.get(doc_id=number_id)
            if doc and doc.get("username") == username:
                return {**doc, "id": doc.doc_id}
            return None
    except Exception as e:
        print(f"Failed to get number {number_id}: {e}")
        return None

def delete_number(number_id: int, username: str) -> bool:
    """Delete a number by doc_id (only if owned by username)."""
    try:
        with _repository_lock:
            with db_session() as db:
                table = db.table(TABLE_NAME)
                doc = table.get(doc_id=number_id)
                if doc and doc.get("username") == username:
                    table.remove(doc_ids=[number_id])
                    return True
                return False
    except Exception as e:
        print(f"Failed to delete number {number_id}: {e}")
        return False

def update_number(number_id: int, username: str, new_value: int) -> Optional[dict]:
    """Update a number's value (only if owned by username)."""
    try:
        with _repository_lock:
            with db_session() as db:
                table = db.table(TABLE_NAME)
                doc = table.get(doc_id=number_id)
                if doc and doc.get("username") == username:
                    table.update({"value": new_value}, doc_ids=[number_id])
                    # Fetch updated document
                    updated = table.get(doc_id=number_id)
                    return {**updated, "id": updated.doc_id}
                return None
    except Exception as e:
        print(f"Failed to update number {number_id}: {e}")
        return None

def count_numbers_for_user(username: str) -> int:
    """Count how many numbers a user has stored."""
    try:
        with db_session() as db:
            table = db.table(TABLE_NAME)
            q = Query()
            return table.count(q.username == username)
    except Exception as e:
        print(f"Failed to count numbers for user {username}: {e}")
        return 0
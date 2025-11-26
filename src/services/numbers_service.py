from ..models.schemas import NumberCreate, NumberRecord, NumberStatistics, NumberUpdate
from ..repositories.numbers_repository import insert_number, list_numbers_for_user, get_number_by_id, delete_number, update_number

def create_number(username: str, payload: NumberCreate) -> dict | None:
    """Business logic for creating a number."""
    record = NumberRecord(username=username, value=payload.value)
    return insert_number(record)

def get_user_numbers(username: str) -> dict:
    """Business logic for getting user's numbers."""
    rows = list_numbers_for_user(username)
    
    numbers = [
        {"value": r["value"], "created_at": r["created_at"]} 
        for r in rows
    ]
    
    return {"username": username, "numbers": numbers}

def get_number(username: str, number_id: int) -> dict | None:
    """Get a specific number by ID."""
    return get_number_by_id(number_id, username)

def remove_number(username: str, number_id: int) -> bool:
    """Delete a specific number by ID."""
    return delete_number(number_id, username)

def modify_number(username: str, number_id: int, payload: NumberUpdate) -> dict | None:
    """Update a specific number's value."""
    return update_number(number_id, username, payload.value)

def get_user_statistics(username: str) -> dict:
    """Calculate statistics for user's numbers."""
    rows = list_numbers_for_user(username)
    
    if not rows:
        return {
            "username": username,
            "statistics": {
                "count": 0,
                "sum": 0,
                "average": 0.0,
                "min": None,
                "max": None
            }
        }
    
    values = [r["value"] for r in rows]
    
    return {
        "username": username,
        "statistics": {
            "count": len(values),
            "sum": sum(values),
            "average": round(sum(values) / len(values), 2),
            "min": min(values),
            "max": max(values)
        }
    }
from fastapi import APIRouter, Depends, HTTPException
from ..models.schemas import NumberCreate, NumberResponse, NumberUpdate
from ..services.numbers_service import create_number, get_user_numbers, get_user_statistics, get_number, remove_number, modify_number
from ..services.auth_service import require_permission

router = APIRouter()

@router.post("/numbers")
async def post_number(payload: NumberCreate, user: dict = Depends(require_permission("numbers:write"))):
    """Create a new number for the authenticated user."""
    result = create_number(user["username"], payload)
    if not result:
        raise HTTPException(status_code=500, detail="Failed to save number")
    return result

@router.get("/numbers", response_model=NumberResponse)
async def get_numbers(user: dict = Depends(require_permission("numbers:read"))):
    """Get all numbers for the authenticated user."""
    return get_user_numbers(user["username"])

@router.get("/numbers/{number_id}")
async def get_number_by_id(number_id: int, user: dict = Depends(require_permission("numbers:read"))):
    """Get a specific number by ID."""
    result = get_number(user["username"], number_id)
    if not result:
        raise HTTPException(status_code=404, detail="Number not found")
    return result

@router.put("/numbers/{number_id}")
async def update_number(number_id: int,payload: NumberUpdate, user: dict = Depends(require_permission("numbers:write"))):
    """Update a specific number's value."""
    result = modify_number(user["username"], number_id, payload)
    if not result:
        raise HTTPException(status_code=404, detail="Number not found")
    return result

@router.delete("/numbers/{number_id}")
async def delete_number(number_id: int, user: dict = Depends(require_permission("numbers:delete"))):
    """Delete a specific number."""
    success = remove_number(user["username"], number_id)
    if not success:
        raise HTTPException(status_code=404, detail="Number not found")
    return {"message": "Number deleted successfully"}

@router.get("/stats")
async def get_stats(user: dict = Depends(require_permission("numbers:read"))):
    """Get statistics for the authenticated user's numbers."""
    return get_user_statistics(user["username"])
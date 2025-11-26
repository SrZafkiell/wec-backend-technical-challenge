from fastapi import APIRouter, HTTPException, Depends
from ..models.schemas import LoginPayload, TokenResponse
from ..services.auth_service import authenticate_user, create_access_token, get_current_user, blacklist_token
from datetime import timedelta

router = APIRouter()

@router.post("/login", response_model=TokenResponse)
def login(payload: LoginPayload):
    """Authenticate user and return JWT token."""
    user_data = authenticate_user(payload.username, payload.password)
    
    if not user_data:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token(user_data, expires_delta=timedelta(minutes=15))
    return {"access_token": token, "token_type": "bearer"}

@router.post("/logout")
async def logout(user: dict = Depends(get_current_user)):
    """Invalidate the current token."""
    blacklist_token(user["token"])
    return {"message": "Successfully logged out"}

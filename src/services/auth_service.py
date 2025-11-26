from jose import jwt, JWTError
from datetime import datetime, timedelta
import os
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from threading import Lock

SECRET_KEY = os.getenv("JWT_SECRET", "supersecret_change_me")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", 15))

# Predefined users with their roles and permissions
USERS_DB = {
    "admin": {
        "password": "1234",
        "role": "administrator",
        "permissions": ["numbers:read", "numbers:write", "numbers:delete"]
    }
}

bearer_scheme = HTTPBearer(auto_error=False)

# >>>>> TOKEN BLACKLIST <<<<<

# Token blacklist in memory (for logout functionality) [Extra: o	POST /logout → invalidar token (opcional si se gestiona en memoria o DB).]
_blacklist: set[str] = set()
_blacklist_lock = Lock()

def blacklist_token(token: str) -> None:
    """Add a token to the blacklist."""
    with _blacklist_lock:
        _blacklist.add(token)

def is_token_blacklisted(token: str) -> bool:
    """Check if a token is blacklisted."""
    with _blacklist_lock:
        return token in _blacklist

def clear_expired_from_blacklist() -> None:
    """Remove expired tokens from blacklist (optional cleanup)."""
    with _blacklist_lock:
        valid_tokens = set()
        for token in _blacklist:
            try:
                jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
                valid_tokens.add(token)  # Still valid, keep it
            except JWTError:
                pass  # Expired, don't keep it
        _blacklist.clear()
        _blacklist.update(valid_tokens)

# >>>>> AUTH SERVICE FUNCTIONS <<<<<

def authenticate_user(username: str, password: str) -> dict | None:
    """Verify credentials and return user data if valid."""
    user = USERS_DB.get(username)
    if user and user["password"] == password:
        return {
            "username": username,
            "role": user["role"],
            "permissions": user["permissions"]
        }
    return None

def create_access_token(user_data: dict, expires_delta: timedelta | None = None) -> str:
    """Create a JWT token with custom claims."""
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    
    # Build token payload with custom claims
    to_encode = {
        "sub": user_data["username"],
        "role": user_data["role"],
        "permissions": user_data["permissions"],
        "exp": expire,
        "iat": datetime.utcnow(),
    }
    
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> dict:
    """Decode and validate a JWT token."""
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )

async def get_current_user(creds: HTTPAuthorizationCredentials | None = Depends(bearer_scheme)) -> dict:
    """Dependency to get current authenticated user with all claims."""
    if not creds:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    token = creds.credentials  # Store token in variable
    
    # Check blacklist BEFORE decoding
    if is_token_blacklisted(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been revoked"
        )
    
    payload = decode_token(token)
    username = payload.get("sub")
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )
    
    # Return all claims
    return {
        "username": username,
        "role": payload.get("role"),
        "permissions": payload.get("permissions", []),
        "token": token
    }


# >>>>> PERMISSIONS AND ROLES <<<<<
# Permission and Role Dependencies (Not even optional but cool to have)
def require_permission(permission: str):
    """Dependency factory to check for specific permission."""
    async def check_permission(user: dict = Depends(get_current_user)) -> dict:
        if permission not in user.get("permissions", []):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission denied: {permission} required"
            )
        return user
    return check_permission

def require_role(role: str):
    """Dependency factory to check for specific role."""
    async def check_role(user: dict = Depends(get_current_user)) -> dict:
        if user.get("role") != role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role denied: {role} required"
            )
        return user
    return check_role
from fastapi import Request
from starlette.responses import JSONResponse
import time
import traceback

async def error_middleware(request: Request, call_next):
    """Middleware to catch unhandled exceptions and return a standardized error response."""
    start = time.time()
    try:
        response = await call_next(request)
        response.headers["X-Response-Time"] = f"{time.time() - start:.4f}s"
        return response
    except Exception as exc:
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={
                "type": "about:blank",
                "title": "Internal Server Error",
                "status": 500,
                "detail": "An unexpected error occurred",
                "instance": request.url.path,
            },
            media_type="application/problem+json"
        )
    
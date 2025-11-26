from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

HTTP_STATUS_TITLES = {
    400: "Bad Request",
    401: "Unauthorized",
    403: "Forbidden",
    404: "Not Found",
    422: "Validation Error",
    500: "Internal Server Error",
}

def problem_response(status: int, detail: str, request: Request, title: str = None) -> JSONResponse:
    """Create RFC 7807 Problem Details response."""
    return JSONResponse(
        status_code=status,
        content={
            "type": "about:blank",
            "title": title or HTTP_STATUS_TITLES.get(status, "Error"),
            "status": status,
            "detail": detail,
            "instance": request.url.path,
        },
        media_type="application/problem+json"
    )

def register_exception_handlers(app):
    """Register custom exception handlers to the FastAPI app."""
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        return problem_response(
            status=exc.status_code,
            detail=exc.detail,
            request=request
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """Handle validation errors and return RFC 7807 response."""
        errors = exc.errors()
        detail = "; ".join(
            f"{err['loc'][-1]}: {err['msg']}" for err in errors
        )
        return problem_response(
            status=422,
            detail=detail,
            request=request
        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        """Handle generic exceptions and return RFC 7807 response."""
        return problem_response(
            status=500,
            detail="An unexpected error occurred",
            request=request
        )
    
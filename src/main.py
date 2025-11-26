# Import dotenv for environment variables
from dotenv import load_dotenv
# Load environment variables
load_dotenv()

# Importing FastAPI and related modules
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager

# Importing database close function
from .database.db import close_db

# Importing the numbers router
from .routes.numbers_route import router as numbers_router

# Importing the auth router
from .routes.auth_route import router as auth_router

# Importing CORS middleware
from fastapi.middleware.cors import CORSMiddleware

# Importing custom exception handlers and error middleware
from .middleware.handlers import register_exception_handlers
from .middleware.error_middleware import error_middleware

# Shutdown: flush TinyDB cache
#@app.on_event("shutdown") <- Deprecated, replaced with lifespan events in FastAPI 0.95.0+
#def on_shutdown():
#    close_db()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Here go the startup actions
    yield
    # This are the shutdown actions
    close_db()

# Creating FastAPI application instance
app = FastAPI(title="WEC Backend Technical Challenge", version="1.0.0", lifespan=lifespan)

# Defining allowed origins for CORS 
origins = [
    "http://localhost",
    "http://localhost:8000",
]

# Adding CORS middleware to the application
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Allowing all HTTP methods, GET, POST, PUT, DELETE, etc. (Challenge didn't require to restrict any)
    allow_headers=["*"],
)

# Registering middleware and exception handlers
register_exception_handlers(app)
app.middleware("http")(error_middleware)

# Registering the numbers router
app.include_router(numbers_router, tags=["numbers"])

# Registering the auth router
app.include_router(auth_router, tags=["login"])

# Root endpoint for health check or welcome message
@app.get("/")
async def root():
    return {"message": "App is running"}

# This is to make the application executable directly with `python main.py`
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080) # Running on port 8080 as required for the challenge

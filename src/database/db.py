# Importing TinyDB and necessary components
from tinydb import TinyDB
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware

# Importing additional components
from pathlib import Path
from contextlib import contextmanager
from threading import Lock
import atexit

# Configuration
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = (BASE_DIR / ".." / "data").resolve()
DATA_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = DATA_DIR / "db.json"

# Thread-local storage for database instances
_db_instance = None
_db_lock = Lock()

def get_db_instance() -> TinyDB:
    """Get a thread-safe singleton instance of the TinyDB database."""
    global _db_instance
    if _db_instance is None:
        with _db_lock:
            # double-checked locking optimization
            if _db_instance is None:
                _db_instance = TinyDB(DB_PATH, storage=CachingMiddleware(JSONStorage), sort_keys=True, indent=4)

    return _db_instance

def get_table(table_name: str):
    """Get a specific table from the TinyDB database."""
    db = get_db_instance()
    return db.table(table_name)

def close_db():
    """Close the TinyDB database instance."""
    global _db_instance
    if _db_instance is not None:
        with _db_lock:
            if _db_instance is not None:
                _db_instance.close()
                _db_instance = None

# https://tinydb.readthedocs.io/en/latest/usage.html 
# Context manager for database sessions
@contextmanager
def db_session():
    """Context manager for TinyDB database session."""
    db = get_db_instance()
    try:
        yield db
    finally:
        if hasattr(db.storage, 'flush'):
            db.storage.flush()

# Register the close_db function to be called at exit
atexit.register(close_db)
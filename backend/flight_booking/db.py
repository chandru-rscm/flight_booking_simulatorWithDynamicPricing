from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Create SQLite Database URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./flight_booking.db"

# 2. Create Engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 3. Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Create Base class (used by models.py)
Base = declarative_base()

# 5. Dependency (Used by backend.py)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
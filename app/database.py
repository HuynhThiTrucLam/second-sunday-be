from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Connection string for Azure SQL Database (ODBC Driver 18)
DATABASE_URL = (
    "mssql+pyodbc://admin123:Password123@shop-ss.database.windows.net:1433/shop-db"
    "?driver=ODBC+Driver+18+for+SQL+Server&Encrypt=yes&TrustServerCertificate=no&ConnectionTimeout=30"
)

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL, connect_args={"driver": "ODBC Driver 18 for SQL Server"}
)

# SessionLocal for managing database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

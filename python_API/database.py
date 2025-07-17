from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Update this with your correct MySQL credentials
DATABASE_URL = "mysql+pymysql://root:Nihal@2006.07@localhost/myapi_db"

# Creating engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

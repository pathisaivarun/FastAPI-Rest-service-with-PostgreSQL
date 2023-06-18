from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings

#Forming database connection using required details
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOSTNAME}:{settings.DATABASE_PORT}/{settings.POSTGRES_DB}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=True, autoflush=False, bind=engine)
Base = declarative_base()

#Below method is to create DB connection with 3 retries
def get_db():
    attempts = 0
    while True:
        try:
            db = SessionLocal()
            print("Successfully created DB connection")
            return db
        except:
            attempts += 1
            if attempts < 3:
                continue
            print("Not able to create DB session")
            break
    return None

#Below method is to close the current db connection
def close_db(db):
    if db is None:
        print("DB connection is not created")
        return
    try:
        db.close()
        print("Successfully closed DB connection")
    except:
        print("Not able to close db connection.")


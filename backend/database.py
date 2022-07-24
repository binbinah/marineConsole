from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from backend.config import MarineConfig


class DBInfo(MarineConfig):
    def __init__(self):
        super().__init__()
        self.name = self.config["db_name"]
        self.user = self.config["db_user"]
        self.password = self.config["db_password"]
        self.host = self.config["db_host"]
        self.port = self.config["db_port"]


db_info = DBInfo()

SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{db_info.user}:{db_info.password}@{db_info.host}:{db_info.port}/{db_info.name}"
engine = create_engine(SQLALCHEMY_DATABASE_URI, poolclass=NullPool)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

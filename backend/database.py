from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from backend.config import MarineConfig


class DBInfo(MarineConfig):
    def __init__(self):
        super().__init__()
        self.name = self.config.get("db_name", "marine")
        self.user = self.config.get("db_user", "marine")
        self.password = self.config.get("db_password", "marine")
        self.host = self.config.get("db_host", "db")
        self.port = self.config.get("db_port", 3306)


db_info = DBInfo()

SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{db_info.user}:{db_info.password}@{db_info.host}:{db_info.port}/{db_info.name}"
engine = create_engine(SQLALCHEMY_DATABASE_URI, poolclass=NullPool)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

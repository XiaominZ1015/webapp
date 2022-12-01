from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

ip = os.getenv('IP')
if not ip:
    SQLALCHEMY_DATABASE_URL = "mysql://sherry:123456@" + ip + "/users_db"
    # SQLALCHEMY_DATABASE_URL = "mysql://sherry:123456@127.0.0.1/users_db"
    # SQLALCHEMY_DATABASE_URL = "postgresql://webapp:zxm123456@127.0.0.1/users_db"
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL
    )
else:
    SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

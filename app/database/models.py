from sqlalchemy import Boolean, Column, ForeignKey, Integer, String


from .db import Base

# SQLAlchemy models
class User(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    account_created = Column(String)
    account_updated = Column(String)


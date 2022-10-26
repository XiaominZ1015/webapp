from sqlalchemy import Boolean, Column, ForeignKey, Integer, String


from .db import Base

# SQLAlchemy models
class User(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(256))
    last_name = Column(String(256))
    username = Column(String(256), unique=True, index=True)
    password = Column(String(256))
    account_created = Column(String(256))
    account_updated = Column(String(256))


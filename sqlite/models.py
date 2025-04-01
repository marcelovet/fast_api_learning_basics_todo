from sqlalchemy import TEXT, Boolean, Column, Integer, String, ForeignKey

from sqlite.database import Base

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False)
    username = Column(String(256), unique=True, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)

class Todo(Base):
    __tablename__ = "todo"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(256))
    description = Column(TEXT)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

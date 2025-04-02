from sqlalchemy import TEXT, Boolean, Column, ForeignKey, Integer, String

from database.config import Base


class Roles(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    role_name = Column(String(256), unique=True, nullable=False)
    description = Column(TEXT)


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False)
    username = Column(String(256), unique=True, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String(256), ForeignKey("roles.role_name", ondelete="SET NULL"))
    phone_number = Column(String(20))


class Todo(Base):
    __tablename__ = "todo"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(256))
    description = Column(TEXT)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

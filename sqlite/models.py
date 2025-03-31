from sqlalchemy import TEXT, Boolean, Column, Integer, String

from sqlite.database import Base


class Todo(Base):
    __tablename__ = "todo"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(256))
    description = Column(TEXT)
    priority = Column(Integer)
    comlete = Column(Boolean, default=False)

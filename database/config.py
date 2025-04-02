import urllib.parse

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from setup import settings as st

CONN_STRING = "postgresql+psycopg2://"
CONN_STRING += f"{urllib.parse.quote_plus(st.POSTGRES_USER)}"  # type: ignore[attr]
CONN_STRING += f":{urllib.parse.quote_plus(st.POSTGRES_PASSWORD)}@"  # type: ignore[attr]
CONN_STRING += f"{st.POSTGRES_HOST}:{st.POSTGRES_PORT}/"  # type: ignore[attr]
CONN_STRING += f"{st.POSTGRES_DB}"  # type: ignore[attr]

engine = create_engine(CONN_STRING)
DbSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

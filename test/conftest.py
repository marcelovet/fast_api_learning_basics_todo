import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from starlette import status

from auth.security import pwd_context
from main import app
from models.database_models import Base
from models.database_models import Todo
from models.database_models import Users
from service.dependencies import get_current_user
from service.dependencies import get_db

SQLALCHEMY_DATABASE_URI = "sqlite:///./test_database.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URI,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    # Create tables
    Base.metadata.create_all(bind=engine)
    yield
    # Drop tables after all tests are done
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(autouse=True)
def clean_tables():
    # Clean all tables before each test
    with TestingSessionLocal() as db:
        db.query(Todo).delete()
        # Don't delete Users as they're needed for tests
        db.commit()


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


def override_get_current_user_admin():
    return {"username": "user_test", "id": 1, "role": "admin"}


def override_get_current_user_user():
    return {"username": "user_test", "id": 1, "role": "user"}


def override_get_current_user_not_authenticated():
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture
def admin():
    with TestingSessionLocal() as db:
        user = Users(
            id=1,
            email="admin@test.com",
            username="admin",
            first_name="admin",
            last_name="admin",
            hashed_password=pwd_context.hash("admin"),
            is_active=True,
            role="admin",
            phone_number="1234567890",
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        yield user
        db.delete(user)
        db.commit()


@pytest.fixture
def todo(admin):
    with TestingSessionLocal() as db:
        existing_todo = db.query(Todo).filter(Todo.id == 1).first()
        if existing_todo:
            db.delete(existing_todo)
            db.commit()

        todo = Todo(
            title="test todo",
            description="test description",
            priority=admin.id,
            complete=False,
            owner_id=1,
        )
        db.add(todo)
        db.commit()
        db.refresh(todo)
        yield todo
        db.query(Todo).filter(Todo.id == todo.id).delete()
        db.commit()


@pytest.fixture
def client_admin():
    app.dependency_overrides[get_current_user] = override_get_current_user_admin
    with TestClient(app) as client:
        yield client


@pytest.fixture
def client_user():
    app.dependency_overrides[get_current_user] = override_get_current_user_user
    with TestClient(app) as client:
        yield client


@pytest.fixture
def client_non_user():
    app.dependency_overrides[get_current_user] = (
        override_get_current_user_not_authenticated
    )
    with TestClient(app) as client:
        yield client

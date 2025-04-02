from random import choice

from faker import Faker
from sqlalchemy import select

from auth.security import pwd_context
from database.config import DbSession
from models.database_models import Todo, Users

faker = Faker()


def create_fake_data():
    with DbSession() as session:
        users = session.scalars(select(Users).where(Users.role != "admin")).all()
        if not users:
            return
        for _ in range(100):
            todo = Todo(
                title=faker.sentence(nb_words=10),
                description=faker.text(),
                priority=faker.random_int(min=1, max=5),
                complete=faker.boolean(),
                owner_id=choice(users).id,
            )
            session.add(todo)
        session.commit()


def create_fake_users():
    emails = set([faker.email() for _ in range(100)])
    usernames = set([faker.user_name() for _ in range(100)])
    with DbSession() as session:
        for _ in range(10):
            user = Users(
                email=emails.pop(),
                username=usernames.pop(),
                first_name=faker.first_name(),
                last_name=faker.last_name(),
                hashed_password=pwd_context.hash(faker.password()),
                is_active=True,
                role="user",
                phone_number=faker.phone_number(),
            )
            session.add(user)
        session.commit()


def create_fake_admin():
    with DbSession() as session:
        admin = Users(
            email=faker.email(),
            username="admin",
            first_name=faker.first_name(),
            last_name=faker.last_name(),
            hashed_password=pwd_context.hash("admin"),
            is_active=True,
            role="admin",
            phone_number=faker.phone_number(),
        )
        session.add(admin)
        session.commit()

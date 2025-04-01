from faker import Faker

from sqlite.database import SqliteSession
from sqlite.models import Todo

faker = Faker()


def create_fake_data():
    with SqliteSession() as session:
        for _ in range(10):
            todo = Todo(
                title=faker.sentence(nb_words=10),
                description=faker.text(),
                priority=faker.random_int(min=1, max=5),
                complete=faker.boolean(),
            )
            session.add(todo)
        session.commit()

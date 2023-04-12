"""Models for the trview application.""" ""

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from faker import Faker

db = SQLAlchemy()


class Users(db.Model):
    """User model."""

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    name = db.Column(db.String(64), index=True, unique=True, nullable=False)
    password = db.Column(db.String(512), nullable=False)

    @staticmethod
    def insert_user_to_database(username, password):
        """Insert a user to the database.

        Args:
            username (str): username
            password (str): password
        """
        salted_hash = generate_password_hash(password)
        new_user = Users(username=username, name=username, password=salted_hash)
        db.session.add(new_user)
        db.session.commit()


class Webhooks(db.Model):
    """Webhook model."""

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created = db.Column(
        db.TIMESTAMP, nullable=False, server_default=db.func.current_timestamp()
    )
    strategy_name = db.Column(db.TEXT, nullable=False)
    ticker = db.Column(db.TEXT, nullable=False)
    strategy_action = db.Column(db.TEXT, nullable=False)
    market_position = db.Column(db.TEXT, nullable=False)
    price = db.Column(db.TEXT, nullable=False)
    position_size = db.Column(db.TEXT, nullable=False)
    market_position_size = db.Column(db.TEXT, nullable=False)
    contracts = db.Column(db.TEXT, nullable=False)
    order_id = db.Column(db.TEXT, nullable=False)

    @staticmethod
    def generate_webhook_data(num_records=10):
        """Generate fake webhook data.

        Args:
            num_records (int, optional): _description_. Defaults to 10.

        Returns:
            list: Fake webhook models to insert into the database.
        """
        faker = Faker()
        data = []
        for _ in range(num_records):
            webhook = Webhooks(
                strategy_name="drsi_with_filters",
                ticker=faker.random_element(elements=("BTCBUSD", "ETHBUSD")),
                strategy_action=faker.random_element(elements=("BUY", "SELL")),
                market_position=faker.random_element(elements=("LONG", "SHORT")),
                price=faker.pyfloat(min_value=1000, max_value=10000, right_digits=2),
                position_size=faker.random_number(digits=4),
                market_position_size=faker.pyfloat(
                    min_value=1000, max_value=10000, right_digits=2
                ),
                contracts=faker.pyfloat(
                    min_value=1000, max_value=10000, right_digits=2
                ),
                order_id=faker.uuid4(),
            )
            data.append(webhook)

        return data

    @staticmethod
    def populate_model(db, num_records=10):
        """Populate the database with fake data.

        Args:
            db (SQLAlchemy): Database object
            num_records (int, optional): Number of records to insert. Defaults to 10.
        """
        data = Webhooks.generate_webhook_data(num_records)
        print("session")
        print(db.session)
        for fake_data in data:
            db.session.add(fake_data)
        db.session.commit()

@staticmethod
def populate_database():
    """Populate the database with fake data."""
    data = Webhooks.generate_webhook_data()
    for fake_data in data:
        db.session.add(fake_data)
    db.session.commit()

"""
Models for the trview application.
Contains the database models and helper functions. 
Model specific operations should be implemented in the models.py file.
"""

import click
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import OperationalError, DataError, IntegrityError
from faker import Faker

db = SQLAlchemy()


def populate_models(model_class, num_records=10):
    """Populate the database with fake data.

    Args:
        num_records (int, optional): Number of records to insert. Defaults to 10.
    """
    click.echo(f"Populating {model_class.__name__} table with {num_records} records.")
    data = model_class.generate_webhook_data(num_records)
    for fake_data in data:
        db.session.add(fake_data)
    click.echo("Committing transaction.")
    try:
        db.session.commit()

    except (IntegrityError, DataError, OperationalError) as exception:
        click.echo("Error inserting data into the database.")
        click.echo(f"Error: {exception.args[0]}")
        click.echo("Rolling back transaction.")
        db.session.rollback()  # Rollback the transaction or it will be stuck in a bad state.


class Users(db.Model):
    """User model."""

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    name = db.Column(db.String(64), index=True, unique=True, nullable=False)
    password = db.Column(db.String(512), nullable=False)
    
    
    def to_dict(self):
        """Convert the model to a dictionary.

        Returns:
            dict: Dictionary representation of the model.
        """
        data = {
            "id": self.id,
            "username": self.username,
            "name": self.name,
            "password": self.password,
        }
        return data

    @staticmethod
    def insert_user(username, password):
        """Insert a user to the database.

        Args:
            username (str): username in email format
            name (str): name of the user
            password (str): password
        """
        salted_hash = generate_password_hash(password)
        new_user = Users(username=username, name=username, password=salted_hash)
        db.session.add(new_user)
        try:
            db.session.commit()
        except (IntegrityError, DataError, OperationalError) as exception:
            click.echo("Error inserting data into the database.")
            click.echo(f"Error: {exception.args[0]}")
            click.echo("Rolling back transaction.")
            db.session.rollback()  # Rollback the transaction or it will be stuck in a bad state.
            return exception.args[0]

    @staticmethod
    def generate_webhook_data(num_records=10):
        """Generate fake users data.

        Args:
            num_records (int, optional): _description_. Defaults to 10.

        Returns:
            list: Fake webhook models to insert into the database.
        """
        faker = Faker()
        data = []
        # Create a fixed user named 'dev' for development purposes.
        dev_user = Users(
            username="dev@dev.com",
            name=faker.name(),
            password=generate_password_hash("1234-asd"),
        )
        data.append(dev_user)
        for _ in range(num_records):
            user = Users(
                username=faker.email(),
                name=faker.name(),
                password=generate_password_hash("1234-asd"),
            )
            data.append(user)

        return data


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
    
    def to_dict(self):
        """Convert the model to a dictionary.

        Returns:
            dict: Dictionary representation of the model.
        """
        data = {
            "id": self.id,
            "created": self.created,
            "strategy_name": self.strategy_name,
            "ticker": self.ticker,
            "strategy_action": self.strategy_action,
            "market_position": self.market_position,
            "price": self.price,
            "position_size": self.position_size,
            "market_position_size": self.market_position_size,
            "contracts": self.contracts,
            "order_id": self.order_id,
        }
        return data

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

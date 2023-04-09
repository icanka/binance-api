from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    name = db.Column(db.String(64), index=True, unique=True, nullable=False)
    password = db.Column(db.String(512), nullable=False)


class Webhooks(db.Model):
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

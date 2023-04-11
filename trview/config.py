# config.py
import os
from flask import app


class Config:
    # general configuration options
    SECRET_KEY = "trview"
    APPLICATION_NAME = "Trview"
    DATABASE = os.path.join(os.getcwd(), "instance", "trading.sqlite")
    LOG_LEVEL = "INFO"


class ProductionConfig(Config):
    SECRET_KEY = "wkqImoT6ENhmvH457LC3vPEW491C7Od5lp4sIB2N8g4="


class DevelopmentConfig(Config):
    """
    The DEBUG config value is special because it may behave inconsistently
    if changed after the app has begun setting up. In order to set debug
    mode reliably, use the --debug option on the flask or flask run command.
    """

    # development configuration options
    DATABASE = os.path.join(os.getcwd(), "instance", "trading.development.sqlite")
    SECRET_KEY = "development"
    # DEBUG = True


class TestingConfig(Config):
    # testing configuration options
    TESTING = True
    DATABASE = "sqlite:///:memory:"
    LOG_LEVEL = "CRITICAL"

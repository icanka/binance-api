""" 
Configuration for the application. 
The 'DEBUG' config value is special because it may behave inconsistently
if changed after the app has begun setting up. In order to set debug
mode reliably, use the --debug option on the flask or flask run command.
Set your application configuration with CONFIGURATION_SETUP environment variable.
Example: export CONFIGURATION_SETUP=trview.config.DevelopmentConfig
"""
# config.py
import os


class Config:
    """Base configuration."""

    # general configuration options
    SECRET_KEY = "trview"
    APPLICATION_NAME = "Trview"
    BASEPATH = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    DATABASE = f"sqlite:////{os.path.join(BASEPATH, 'instance', 'trading.sqlite')}"
    LOG_LEVEL = "INFO"


class ProductionConfig(Config):
    """Production configuration."""

    SECRET_KEY = "wkqImoT6ENhmvH457LC3vPEW491C7Od5lp4sIB2N8g4="


class DevelopmentConfig(Config):
    """Development configuration."""

    DATABASE = f"sqlite:////{os.path.join(Config.BASEPATH, 'instance', 'trading.development.sqlite')}"
    SECRET_KEY = "development"


class TestingConfig(Config):
    """Testing configuration."""

    # testing configuration options
    TESTING = True
    DATABASE = "sqlite:///:memory:"
    LOG_LEVEL = "CRITICAL"

#!/bin/bash
#env_dir="$HOME/Documents/python-virtenv"

#source "${env_dir}/binance-api/bin/activate"
#export FLASK_APP=main.py
export FLASK_DEBUG=1
export CONFIGURATION_SETUP=trview.config.DevelopmentConfig
# Sets the current working directory to flask_app/trview then imports app.py and uses the create_app function to create the app.
export FLASK_APP=trview/app:create_app

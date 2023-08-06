# # -*- encoding: utf-8 -*-
# """
# License: Commercial
# Copyright (c) 2019 - present AppSeed.us
# """

# from flask_migrate import Migrate
# from os import environ
# from sys import exit

# from config import config_dict
# from app import create_app, db

# get_config_mode = environ.get('APPSEED_CONFIG_MODE', 'Debug')

# try:
#     config_mode = config_dict[get_config_mode.capitalize()]
# except KeyError:
#     exit('Error: Invalid APPSEED_CONFIG_MODE environment variable entry.')

# app = create_app(config_mode) 
# Migrate(app, db)

# if __name__ == "__main__":
#     app.run()


# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_migrate import Migrate
from os import environ
from sys import exit
from decouple import config

from config import config_dict
from app import create_app, db

# WARNING: Don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True)

# The configuration
get_config_mode = 'Debug' if DEBUG else 'Production'

try:
    
    # Load the configuration using the default values 
    app_config = config_dict[get_config_mode.capitalize()]

except KeyError:
    exit('Error: Invalid <config_mode>. Expected values [Debug, Production] ')

app = create_app( app_config ) 
Migrate(app, db)

if __name__ == "__main__":
    import eventlet
    from eventlet import wsgi, wrap_ssl
    wsgi.server(sock = eventlet.listen((app_config.APPIP, app_config.APPPort)), site=app)
    #app.run(debug=True)
    # app.run()

# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os
from   flask_migrate import Migrate
from   flask_minify  import Minify
from   sys import exit

from apps.config import config_dict
from apps import create_app, db

# WARNING: Don't run with debug turned on in production!
DEBUG = (os.getenv('DEBUG', 'False') == 'True')

# The configuration
get_config_mode = 'Debug' if DEBUG else 'Production'

try:

    # Load the configuration using the default values
    app_config = config_dict[get_config_mode.capitalize()]

except KeyError:
    exit('Error: Invalid <config_mode>. Expected values [Debug, Production] ')

app = create_app(app_config)

from sqlalchemy import create_engine
from sqlalchemy import text
# or from sqlalchemy.sql import text

engine = create_engine('postgresql://postgres:chua@localhost:5432/postgres', echo=True)

#import insert table set 
with engine.connect() as con:
    with open("apps/data.sql") as file:
        query = text(file.read())
        con.execute(query)

#Migrate(app, db)

if not DEBUG:
    Minify(app=app, html=True, js=False, cssless=False)
    
if DEBUG:
    app.logger.info('DEBUG       = ' + str(DEBUG)             )
    app.logger.info('DBMS        = ' + app_config.SQLALCHEMY_DATABASE_URI)
    app.logger.info('ASSETS_ROOT = ' + app_config.ASSETS_ROOT )

if __name__ == "__main__":
    app.run()


#run SQL Queries 
class Models:
    def __init__(self):
        self.engine = engine

    def executeRawSql(self, statement, params={}):
        out = None
        with self.engine.connect() as con:
            out = con.execute(text(statement), params)
        return out

    def hostsgraph(self):
        return self.executeRawSql("""SELECT account_created,count(*) FROM host GROUP BY account_created ORDER BY account_created ASC""")

#result = db.session.execute('SELECT * FROM my_table WHERE my_column = :val', {'val': 5})


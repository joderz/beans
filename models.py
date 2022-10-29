# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os
from   flask_migrate import Migrate
from   flask_minify  import Minify
from   sys import exit
from flask import Flask, redirect, request, render_template, url_for, session, flash

from apps.config import config_dict
from apps import create_app, db

from sqlalchemy import create_engine
from sqlalchemy import text

#run SQL Queries 
class Modelz:
    def __init__(self):
        self.engine = create_engine('postgresql://postgres:chua@localhost:5432/postgres', echo=True)

    def executeRawSql(self, statement, params={}):
        out = None
        with self.engine.connect() as con:
            out = con.execute(text(statement), params)
        return out

    def hostsgraph(self):
        return self.executeRawSql("""SELECT account_created,count(*) FROM host GROUP BY account_created ORDER BY account_created ASC""")

    def reservation_list(self):
        return self.executeRawSql("""SELECT * FROM reservation""")
#result = db.session.execute('SELECT * FROM my_table WHERE my_column = :val', {'val': 5})
'''
from apps.authentication import blueprint


@blueprint.route('/index', methods=['GET'])
def Modelz2():  # put application's code here
    # create a cursor
    cur = engine.connect().cursor()

    # execute a statement
    print('PostgreSQL database version:')
    cur.execute('SELECT version()')
    # display the PostgreSQL database server version
    session["db_version"] = cur.fetchone()[0]
    #Sales and Attendance by Day of Week Section Display
    cur.execute("""SELECT * FROM reservation;""")
    session["reservations"] = cur.fetchall()
    return render_template('index.html', version=session["db_version"],
                           results = session["reservations"])

'''
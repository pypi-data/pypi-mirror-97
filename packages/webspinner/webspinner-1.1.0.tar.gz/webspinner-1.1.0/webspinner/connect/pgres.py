"""
webspinner.connect.pgres
----------------------
This module provides utilities for connecting to AWS data sources.

:copyright: (c) 2021, Alliance for Sustainable Energy, LLC
:license: BSD-3
"""

import pgpasslib
import psycopg2
from sqlalchemy import create_engine

import webspinner

def make_pg_connection(user=None, dbase=None, host=None, port=None):

    if webspinner.WEBSPINNER_CONFIGURATION is not None:
        if 'PGRES' in webspinner.WEBSPINNER_CONFIGURATION:
            if user is None and 'user' in webspinner.WEBSPINNER_CONFIGURATION['PGRES']:
                user = webspinner.WEBSPINNER_CONFIGURATION['PGRES']['user']
            if dbase is None and 'dbase' in webspinner.WEBSPINNER_CONFIGURATION['PGRES']:
                dbase = webspinner.WEBSPINNER_CONFIGURATION['PGRES']['dbase']
            if host is None and 'host' in webspinner.WEBSPINNER_CONFIGURATION['PGRES']:
                host = webspinner.WEBSPINNER_CONFIGURATION['PGRES']['host']
            if port is None and 'port' in webspinner.WEBSPINNER_CONFIGURATION['PGRES']:
                port = webspinner.WEBSPINNER_CONFIGURATION['PGRES']['port']

    # get password from pgpass
    pwd = pgpasslib.getpass(host, port, dbase, user)
    con = psycopg2.connect('host={host} dbname={dbase} user={user} password={pwd}'.format(
        host = host, dbase = dbase, user = user, pwd = pwd))
    cur = con.cursor()
    engine = create_engine('postgresql://{user}:{pwd}@{host}:{port}/{dbase}'.format(
        host = host, dbase = dbase, port = port, user = user, pwd = pwd))
    
    return con, cur, engine

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlite3 import Connection as SQLite3Connection


# This function is necessary to perform cacade deletes in SQLite
@event.listens_for(Engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()


app = Flask(__name__)
app.config["SECRET_KEY"] = "1f9c17c87d50c86558bff9c2517253c9"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///p2mt.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
app.jinja_env.globals.update(zip=zip)

from P2MT_App import routes, routes_fet

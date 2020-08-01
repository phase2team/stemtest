from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SECRET_KEY"] = "1f9c17c87d50c86558bff9c2517253c9"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///p2mt.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
app.jinja_env.globals.update(zip=zip)

from P2MT_App import routes

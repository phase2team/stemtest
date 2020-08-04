from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from sqlalchemy.engine import Engine
from P2MT_App.config import Config
from sqlite3 import Connection as SQLite3Connection
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


# This function is necessary to perform cacade deletes in SQLite
@event.listens_for(Engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()


db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    app.jinja_env.globals.update(zip=zip)

    db.init_app(app)
    migrate.init_app(app, db)

    from P2MT_App.main.routes import main
    from P2MT_App.classAttendance.routes import classAttendance
    from P2MT_App.dailyAttendance.routes import dailyAttendance
    from P2MT_App.fetTools.routes import fetTools
    from P2MT_App.interventionInfo.routes import interventionInfo
    from P2MT_App.masterSchedule.routes import masterSchedule
    from P2MT_App.scheduleAdmin.routes import scheduleAdmin
    from P2MT_App.schoolCalendar.routes import schoolCalendar
    from P2MT_App.studentInfo.routes import studentInfo

    app.register_blueprint(main)
    app.register_blueprint(classAttendance)
    app.register_blueprint(dailyAttendance)
    app.register_blueprint(fetTools)
    app.register_blueprint(interventionInfo)
    app.register_blueprint(masterSchedule)
    app.register_blueprint(scheduleAdmin)
    app.register_blueprint(schoolCalendar)
    app.register_blueprint(studentInfo)

    return app

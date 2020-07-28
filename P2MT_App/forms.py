from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import (
    SubmitField,
    StringField,
    SelectField,
    TextAreaField,
    RadioField,
    FormField,
    FieldList,
    IntegerField,
    HiddenField,
)
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired
from datetime import datetime


class addDailyAttendanceForm(FlaskForm):
    studentID = StringField("Student ID")
    attendanceCode = SelectField(
        "Attendance Code",
        choices=[
            ("Missed Swipe", "Missed Swipe"),
            ("W/D Use Only", "W/D Use Only"),
            ("P (Present)", "P (Present)"),
            ("UNX (Unexcused)", "UNX (Unexcused)"),
            ("EXC (Excused)", "EXC (Excused)"),
            ("UTY (Unexcused Tardy)", "UTY (Unexcused Tardy)"),
            ("TDY (Tardy)", "TDY (Tardy)"),
            ("ACT (Activity)", "ACT (Activity)"),
            ("ALT (Alt_Remanded)", "ALT (Alt_Remanded)"),
            ("DTH (Death in Family)", "DTH (Death in Family)"),
            ("CRT (Court)", "CRT (Court)"),
            ("EVS (Evening School)", "EVS (Evening School)"),
            ("FLU (Flu)", "FLU (Flu)"),
            ("HBD (Homebound)", "HBD (Homebound)"),
            ("ISS (In-School Suspension)", "ISS (In-School Suspension)"),
            ("MED (Medical)", "MED (Medical)"),
            ("PEX (Parent Excuse)", "PEX (Parent Excuse)"),
            ("REL (Religious)", "REL (Religious)"),
            ("SUS (Suspended)", "SUS (Suspended)"),
            ("TNT (Unexcused Trans)", "TNT (Unexcused Trans)"),
            ("TXT (Excused Trans)", "TXT (Excused Trans)"),
            ("Z (Expelled)", "Z (Expelled)"),
        ],
        validators=[DataRequired()],
    )
    absenceDate = DateField("Absence Date", validators=[DataRequired()])
    comment = TextAreaField("Comment")
    submit = SubmitField("Submit New Daily Attendance")


class addInterventionLogForm(FlaskForm):
    studentID = StringField("Student ID")
    interventionType = SelectField("Intervention Type")
    interventionLevel = StringField("Intervention Level")
    startDate = DateField("Start Date")
    endDate = DateField("End Date")
    comment = TextAreaField("Comment")
    submit = SubmitField("Submit New Intervention")


class classAttendanceLogFilters(FlaskForm):
    identifier = StringField()
    teacherName = SelectField("Teacher")
    className = SelectField("Class")
    classDate = DateField("Class Date")
    submit = SubmitField("Submit Log Filters")


class updateStudentAttendanceForm(FlaskForm):
    identifier = StringField()
    log_id = HiddenField()
    attendanceCode = RadioField(
        "Attendance Code",
        choices=[("P", "P"), ("T", "T"), ("E", "E"), ("U", "U"), ("Q", "?"),],
    )
    comment = StringField("Comment")
    className = HiddenField()
    teacherName = HiddenField()
    classDate = HiddenField()


class updateClassAttendanceForm(FlaskForm):
    identifier = StringField()
    classMembers = FieldList(FormField(updateStudentAttendanceForm))
    teacherName = SelectField("Teacher", coerce=str)
    className = SelectField("Class", coerce=str)
    classDate = DateField("Class Date")
    submitFilters = SubmitField("Submit Log Filters")

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import SubmitField, StringField, SelectField, TextAreaField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired


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
    interventionType = SelectField(
        "Intervention Type"
        # choices=[getInterventionTypes()]
        # choices=[
        #     ("1", "Conduct Behavior"),
        #     ("2", "Academic Behavior"),
        #     ("3", "Attendance"),
        #     ("4", "Dress Code"),
        #     ("5", "Bullying / Harassment"),
        # ],
    )
    interventionLevel = StringField("Intervention Level")
    startDate = DateField("Start Date")
    endDate = DateField("End Date")
    comment = TextAreaField("Comment")
    submit = SubmitField("Submit New Intervention")

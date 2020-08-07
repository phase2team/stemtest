from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import SubmitField, StringField, SelectField
from wtforms.fields.html5 import DateField, EmailField
from wtforms.validators import DataRequired


class addStudentForm(FlaskForm):
    firstName = StringField("First Name", validators=[DataRequired()])
    lastName = StringField("Last Name", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()])
    chattStateANumber = StringField("Chatt State A Number", validators=[DataRequired()])
    yearOfGraduation = StringField("Year of Graduation", validators=[DataRequired()])
    house = StringField("House (Use TBD if unknown)", validators=[DataRequired()])
    googleCalendarId = StringField(
        "Google Calendar ID (Use TBD if unknown", validators=[DataRequired()]
    )
    submitAddStudent = SubmitField("Add Student")


class uploadStudentListForm(FlaskForm):
    csvStudentListFile = FileField(
        "Student List (*.csv format)",
        validators=[FileAllowed(["csv"]), FileRequired()],
    )
    submitUploadStudentList = SubmitField("Upload Student List")


class deleteStudentForm(FlaskForm):
    studentName = SelectField("Student Name", validators=[DataRequired()])
    confirmDeleteStudent = StringField(
        "Type DELETE to confirm", validators=[DataRequired()]
    )
    submitDeleteStudent = SubmitField("Delete Student")

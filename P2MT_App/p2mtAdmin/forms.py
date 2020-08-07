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
        "Google Calendar ID (Use TBD if unknown)", validators=[DataRequired()]
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


class addStaffForm(FlaskForm):
    firstName = StringField("First Name", validators=[DataRequired()])
    lastName = StringField("Last Name", validators=[DataRequired()])
    position = StringField("Position", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()])
    phoneNumber = StringField("Phone Number (Optional)")
    chattStateANumber = StringField("Chatt State A Number (Optional)")
    myersBriggs = StringField("Myers Briggs Personality Type (Optional)")
    house = StringField("House (Optional)")
    houseGrade = SelectField(
        "House Grade (for House Teachers) (Optional)",
        coerce=int,
        choices=[(0, ""), (12, "12"), (11, "11"), (10, 10), (9, "9")],
    )
    twitterAccount = StringField("Twitter Account (Optional)", default="@")
    submitAddStaff = SubmitField("Add Staff")


class uploadStaffListForm(FlaskForm):
    csvStaffListFile = FileField(
        "Staff List (*.csv format)", validators=[FileAllowed(["csv"]), FileRequired()],
    )
    submitUploadStaffList = SubmitField("Upload Staff List")


class deleteStaffForm(FlaskForm):
    staffName = SelectField("Staff Name", coerce=int, validators=[DataRequired()])
    confirmDeleteStaff = StringField(
        "Type DELETE to confirm", validators=[DataRequired()]
    )
    submitDeleteStaff = SubmitField("Delete Staff Member")

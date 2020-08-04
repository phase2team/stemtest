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
    TimeField,
    BooleanField,
    SelectMultipleField,
    widgets,
)
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Optional
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
    submitDailyAttendance = SubmitField("Submit New Daily Attendance")


class addInterventionLogForm(FlaskForm):
    studentID = StringField("Student ID")
    interventionType = SelectField(
        "Intervention Type", coerce=int, validators=[DataRequired()]
    )
    interventionLevel = SelectField(
        "Intervention Level",
        coerce=int,
        choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6)],
        validators=[DataRequired()],
    )
    startDate = DateField("Start Date", validators=[DataRequired()])
    endDate = DateField("End Date", validators=[DataRequired()])
    comment = TextAreaField("Comment")
    submitIntervention = SubmitField("Submit New Intervention")


class classAttendanceLogFilters(FlaskForm):
    identifier = StringField()
    teacherName = SelectField("Teacher")
    className = SelectField("Class")
    classDate = DateField("Class Date")
    submit = SubmitField("Submit Log Filters")


class updateStudentAttendanceForm(FlaskForm):
    # identifier = StringField()
    log_id = HiddenField()
    attendanceCode = RadioField(
        "Attendance Code",
        choices=[("P", "P"), ("T", "T"), ("E", "E"), ("U", "U"), ("Q", "?"),],
        validators=[Optional()],
    )
    comment = StringField("Comment")
    # className = HiddenField()
    # teacherName = HiddenField()
    # classDate = HiddenField()
    updateFlag = HiddenField()


class updateClassAttendanceForm(FlaskForm):
    # identifier = StringField()
    classMembers = FieldList(FormField(updateStudentAttendanceForm))
    teacherName = SelectField("Teacher", coerce=str)
    className = SelectField("Class", coerce=str)
    classDate = DateField("Class Date")
    updateFiltersFlag = HiddenField()


class uploadClassScheduleForm(FlaskForm):
    csvClassScheduleFile = FileField(
        "Class Schedule File (*.csv format)",
        validators=[FileAllowed(["csv"]), FileRequired()],
    )
    submitUploadClassSchedule = SubmitField("Upload Class Schedule")


class MultiCheckboxField(SelectMultipleField):
    """
    A multiple-select, except displays a list of checkboxes.

    Iterating the field will produce subfields, allowing custom rendering of
    the enclosed checkbox fields.
    """

    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class addSingleClassSchedule(FlaskForm):
    schoolYear = SelectField("Year", coerce=int, validators=[DataRequired()])
    semester = SelectField("Semester", validators=[DataRequired()])
    studentName = SelectField("Student Name", validators=[DataRequired()])
    campus = SelectField("Campus", validators=[DataRequired()])
    className = SelectField("Class Name", validators=[DataRequired()])
    teacherName = SelectField("Teacher", coerce=str, validators=[DataRequired()])
    classDays = MultiCheckboxField("Class Days", validators=[DataRequired()])
    startTime = TimeField("Start Time", validators=[DataRequired()])
    endTime = TimeField("End Time", validators=[DataRequired()])
    online = BooleanField("Online")
    indStudy = BooleanField("Independent Study")
    comment = StringField("Comment")
    googleCalendarEventID = StringField("Google Calendar Event ID")
    submitAddSingleClassSchedule = SubmitField("Add Class Schedule for Single Student")


class propagateClassAttendanceLogsForm(FlaskForm):
    schoolYear = SelectField("Year", coerce=int, validators=[DataRequired()])
    semester = SelectField("Semester", validators=[DataRequired()])
    startDate = DateField("Start Date", validators=[DataRequired()])
    endDate = DateField("End Date", validators=[DataRequired()])
    submitPropagatelassAttendanceLogs = SubmitField("Propagate Class Attendance Logs")


class deleteClassScheduleForm(FlaskForm):
    schoolYear = SelectField("Year", coerce=int, validators=[DataRequired()])
    semester = SelectField("Semester", validators=[DataRequired()])
    yearOfGraduation = SelectField("Year of Graduation", coerce=int)
    confirmDeleteClassSchedule = StringField(
        "Type DELETE to confirm", validators=[DataRequired()]
    )
    submitDeleteClassScheduleForm = SubmitField("Delete Class Schedule")


class downloadClassScheduleForm(FlaskForm):
    schoolYear = SelectField("Year", coerce=int, validators=[DataRequired()])
    semester = SelectField("Semester", validators=[DataRequired()])
    submitDownloadClassScheduleForm = SubmitField("Download Class Schedule")


class downloadClassAttendanceForm(FlaskForm):
    schoolYear = SelectField("Year", coerce=int, validators=[DataRequired()])
    semester = SelectField("Semester", validators=[DataRequired()])
    teacherName = SelectField("Teacher", coerce=str, validators=[DataRequired()])
    startDate = DateField("Start Date", validators=[DataRequired()])
    endDate = DateField("End Date", validators=[DataRequired()])
    submitDownloadClassAttendanceForm = SubmitField("Download Class Attendance Log")


class editSchoolCalendar(FlaskForm):
    classDate = DateField("Start Date", validators=[DataRequired()])
    stemSchoolDay = BooleanField("STEM School Day")
    phaseIIDay = BooleanField("Phase II Day")
    chattStateSchoolDay = BooleanField("Chatt State School Day")
    seniorErDay = BooleanField("Senior ER Day")
    juniorErDay = BooleanField("Junior ER Day")
    seniorUpDay = BooleanField("Senior UP Day")
    juniorUpDay = BooleanField("Junior UP Day")


class UploadFetDataForm(FlaskForm):
    yearOfGraduation = StringField(
        "Year of Graduation (YYYY)", validators=[DataRequired()]
    )
    schoolYear = StringField("Schedule Year (YYYY)", validators=[DataRequired()])
    semester = StringField(
        "Schedule Semester (Fall or Spring)", validators=[DataRequired()]
    )
    csvFetStudentInputFile = FileField(
        "FET Student Input File (*.csv format)",
        validators=[FileAllowed(["csv"]), FileRequired()],
    )
    csvFetClassTeacherInputFile = FileField(
        "FET Class Teacher Input File (*.csv format)",
        validators=[FileAllowed(["csv"]), FileRequired()],
    )
    csvFetTimetableInputFile = FileField(
        "FET Timetable Input File (*.csv format)",
        validators=[FileAllowed(["csv"]), FileRequired()],
    )
    submitFetDataForm = SubmitField("Generate Schedule File")


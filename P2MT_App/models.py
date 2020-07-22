from P2MT_App import db
from datetime import datetime


class Student(db.Model):
    __tablename__ = "Student"
    id = db.Column(db.Integer, primary_key=True)
    chattStateANumber = db.Column(db.String(20), unique=True, nullable=False)
    firstName = db.Column(db.String(50), nullable=False)
    lastName = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    yearOfGraduation = db.Column(db.Integer, nullable=False)
    house = db.Column(db.String(20), nullable=False)
    googleCalendarId = db.Column(db.String(100), nullable=True)
    classSchedule = db.relationship(
        "ClassSchedule", backref="Student", passive_deletes=True, lazy=True,
    )
    dailyAttendance = db.relationship(
        "DailyAttendanceLog", backref="Student", passive_deletes=True, lazy=True,
    )
    interventionLog = db.relationship(
        "InterventionLog", backref="Student", passive_deletes=True, lazy=True,
    )

    def __repr__(self):
        return (
            f"Students('{self.chattStateANumber}','{self.firstName}','{self.lastName}')"
        )


class ClassSchedule(db.Model):
    __tablename__ = "ClassSchedule"
    id = db.Column(db.Integer, primary_key=True)
    schoolYear = db.Column(db.Integer, nullable=False)
    semester = db.Column(db.String(20), nullable=False)
    chattStateANumber = db.Column(
        db.String(20),
        db.ForeignKey("Student.chattStateANumber", ondelete="CASCADE"),
        nullable=False,
    )
    campus = db.Column(db.String(50), nullable=False)
    className = db.Column(db.String(50), nullable=False)
    staffID = db.Column(db.Integer, db.ForeignKey("FacultyAndStaff.id"), nullable=True)
    online = db.Column(db.Boolean, nullable=False, default=False)
    indStudy = db.Column(db.Boolean, nullable=False, default=False)
    classDays = db.Column(db.String(10), nullable=False)
    startTime = db.Column(db.DateTime, nullable=True)
    endTime = db.Column(db.DateTime, nullable=True)
    comment = db.Column(db.String(250), nullable=True)
    googleCalendarEventID = db.Column(db.String(250), nullable=True)
    ClassAttendanceLog = db.relationship(
        "ClassAttendanceLog", backref="ClassSchedule", passive_deletes=True, lazy=True,
    )

    def __repr__(self):
        return f"ClassSchedule('{self.className}','{self.startTime}','{self.endTime}','{self.classDays}')"


class ClassAttendanceLog(db.Model):
    __tablename__ = "ClassAttendanceLog"
    id = db.Column(db.Integer, primary_key=True)
    classSchedule_id = db.Column(
        db.Integer,
        db.ForeignKey("ClassSchedule.id", ondelete="CASCADE"),
        nullable=False,
    )
    classDate = db.Column(db.DateTime, nullable=False)
    attendanceCode = db.Column(db.String(2), nullable=True)
    comment = db.Column(db.Text, nullable=True)
    assignTmi = db.Column(db.Boolean, nullable=False, default=False)
    interventionLog_id = db.Column(
        db.Integer, db.ForeignKey("InterventionLog.id"), nullable=True,
    )

    def __repr__(self):
        return f"ClassAttendanceLog('{self.id}','{self.classSchedule_id}','{self.classDate}','{self.attendanceCode}')"


class DailyAttendanceLog(db.Model):
    __tablename__ = "DailyAttendanceLog"
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(
        db.Integer, db.ForeignKey("Student.id", ondelete="CASCADE"), nullable=False
    )
    absenceDate = db.Column(db.DateTime, nullable=False)
    createDate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    attendanceCode = db.Column(db.String(1), nullable=False, default="P")
    comment = db.Column(db.Text, nullable=False)
    staffID = db.Column(db.Integer, db.ForeignKey("FacultyAndStaff.id"), nullable=False)
    assignTmi = db.Column(db.Boolean, nullable=False, default=False)
    recordDeleted = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f"DailyAttendanceLog('{self.absenceDate}','{self.attendanceCode}','{self.comment}')"


class InterventionType(db.Model):
    __tablename__ = "InterventionType"
    id = db.Column(db.Integer, primary_key=True)
    interventionType = db.Column(db.String(30), nullable=False)
    maxLevel = db.Column(db.Integer, nullable=False)
    interventionLog = db.relationship(
        "InterventionLog", backref="InterventionType", lazy=True
    )

    def __repr__(self):
        return (
            f"InterventionType('{self.id}','{self.interventionType}','{self.maxLevel}')"
        )


class InterventionLog(db.Model):
    __tablename__ = "InterventionLog"
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(
        db.Integer, db.ForeignKey("Student.id", ondelete="CASCADE"), nullable=False
    )
    intervention_id = db.Column(
        db.Integer, db.ForeignKey("InterventionType.id"), nullable=False
    )
    interventionLevel = db.Column(db.Integer, nullable=False)
    createDate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    startDate = db.Column(db.DateTime, nullable=False)
    endDate = db.Column(db.DateTime, nullable=False)
    staffID = db.Column(db.Integer, db.ForeignKey("FacultyAndStaff.id"), nullable=False)
    comment = db.Column(db.Text, nullable=True)
    tmiMinutes = db.Column(db.Integer, nullable=True)
    tmiMinutesServed = db.Column(db.Integer, nullable=True)
    tmiMinutesRemaining = db.Column(db.Integer, nullable=True)
    inTmiNow = db.Column(db.Boolean, nullable=True, default=True)
    # learningLabClass_id = db.Column(db.Integer, db.ForeignKey("Classes.id"), nullable=False)
    erSession = db.Column(db.String(50), nullable=True)
    erSession = db.Column(db.String(50), nullable=True)
    interventionStatus = db.Column(db.String(50), nullable=True)
    recordDeleted = db.Column(db.Boolean, nullable=True, default=False)
    classAttendanceLog_id = db.relationship(
        "ClassAttendanceLog", backref="InterventionLog", lazy=True
    )

    def __repr__(self):
        return f"InterventionLog('{self.id}','{self.intervention_id}','{self.startDate}','{self.endDate}')"


class FacultyAndStaff(db.Model):
    __tablename__ = "FacultyAndStaff"
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(50), nullable=False)
    lastName = db.Column(db.String(50), nullable=False)
    position = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=True)
    phoneNumber = db.Column(db.String(20), nullable=True)
    chattStateANumber = db.Column(db.String(20), unique=True, nullable=True)
    myersBrigg = db.Column(db.Integer, nullable=True)
    house = db.Column(db.String(20), nullable=True)
    houseGrade = db.Column(db.Integer, nullable=True)
    twitterAccount = db.Column(db.String(50), nullable=True)
    status = db.Column(db.String(20), nullable=True)
    DailyAttendanceLog = db.relationship(
        "DailyAttendanceLog", backref="FacultyAndStaff", lazy=True
    )
    InterventionLog = db.relationship(
        "InterventionLog", backref="FacultyAndStaff", lazy=True
    )
    ClassSchedule = db.relationship(
        "ClassSchedule", backref="FacultyAndStaff", lazy=True
    )

    def __repr__(self):
        return (
            f"FacultyAndStaff('{self.firstName}','{self.lastName}','{self.position}')"
        )

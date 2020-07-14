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
    classSchedule = db.relationship("ClassSchedule", backref="Student", lazy=True)
    dailyAttendance = db.relationship(
        "DailyAttendanceLog", backref="Student", lazy=True
    )

    def __repr__(self):
        return (
            f"Students('{self.chattStateANumber}','{self.firstName}','{self.lastName}')"
        )


class ClassSchedule(db.Model):
    __tablename__ = "ClassSchedule"
    id = db.Column(db.Integer, primary_key=True)
    className = db.Column(db.String(50), nullable=False)
    startTime = db.Column(db.DateTime, nullable=False)
    endTime = db.Column(db.DateTime, nullable=False)
    classDays = db.Column(db.String(10), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey("Student.id"), nullable=False)

    def __repr__(self):
        return f"ClassSchedule('{self.className}','{self.startTime}','{self.endTime}','{self.classDays}')"


class DailyAttendanceLog(db.Model):
    __tablename__ = "DailyAttendanceLog"
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("Student.id"), nullable=False)
    absenceDate = db.Column(db.DateTime, nullable=False)
    createDate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    attendanceCode = db.Column(db.String(1), nullable=False, default="P")
    comment = db.Column(db.Text, nullable=False)
    staffID = db.Column(db.Integer, db.ForeignKey("FacultyAndStaff.id"), nullable=False)
    assignTmi = db.Column(db.Boolean, nullable=False, default=False)
    recordDeleted = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f"DailyAttendanceLog('{self.absenceDate}','{self.attendanceCode}','{self.comment}')"


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

    def __repr__(self):
        return (
            f"FacultyAndStaff('{self.firstName}','{self.lastName}','{self.position}')"
        )


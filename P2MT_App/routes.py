from flask import render_template
from P2MT_App import app
from P2MT_App.models import Student, ClassSchedule, FacultyAndStaff, DailyAttendanceLog


@app.route("/")
def home():
    return render_template("home.html", title="Home")


@app.route("/students")
def students():
    students = Student.query.all()
    for student in students:
        print(student.firstName)
    return render_template("students.html", title="Students", students=students)


@app.route("/dailyattendancelog")
def displayDailyAttendanceLogs():
    DailyAttendanceLogs = DailyAttendanceLog.query.all()
    return render_template(
        "dailyattendancelog.html",
        title="Daily Attendance Log",
        DailyAttendanceLogs=DailyAttendanceLogs,
    )


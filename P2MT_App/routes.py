from flask import render_template, redirect, url_for, flash, request
from P2MT_App import app, db
from P2MT_App.models import (
    Student,
    ClassSchedule,
    FacultyAndStaff,
    DailyAttendanceLog,
    InterventionLog,
    ClassAttendanceLog,
)
from P2MT_App.forms import (
    addDailyAttendanceForm,
    addInterventionLogForm,
    updateStudentAttendanceForm,
    updateClassAttendanceForm,
)
from P2MT_App.referenceData import getInterventionTypes
from datetime import datetime


def add_DailyAttendanceLog(student_id, absenceDate, attendanceCode, comment):
    print(student_id, attendanceCode, comment, absenceDate)
    dailyAttendanceLog = DailyAttendanceLog(
        absenceDate=absenceDate,
        attendanceCode=attendanceCode,
        comment=comment,
        staffID=2,
        student_id=student_id,
    )
    db.session.add(dailyAttendanceLog)
    db.session.commit()
    flash("Daily attendance log has been added!", "success")
    return


def add_InterventionLog(
    student_id, interventionType, interventionLevel, startDate, endDate, comment
):
    print(student_id, interventionType, interventionLevel, startDate, endDate)
    interventionLog = InterventionLog(
        intervention_id=interventionType,
        interventionLevel=interventionLevel,
        startDate=startDate,
        endDate=endDate,
        comment=comment,
        staffID=2,
        student_id=student_id,
    )
    db.session.add(interventionLog)
    db.session.commit()
    flash("Intervention log has been added!", "success")
    return


@app.route("/")
def home():
    return render_template("home.html", title="Home")


@app.route("/students", methods=["GET", "POST"])
def students():
    dailyAttendanceForm = addDailyAttendanceForm()
    interventionForm = addInterventionLogForm()
    interventionForm.interventionType.choices = getInterventionTypes()
    students = Student.query.order_by(
        Student.yearOfGraduation.asc(), Student.lastName.asc()
    )
    if dailyAttendanceForm.validate_on_submit():
        add_DailyAttendanceLog(
            int(dailyAttendanceForm.studentID.data),
            dailyAttendanceForm.absenceDate.data,
            dailyAttendanceForm.attendanceCode.data,
            dailyAttendanceForm.comment.data,
        )
        print(
            "===   Completed add_DailyAttendanceLog.  Redirecting to students   ===",
            datetime.now(),
            "   ===",
        )
        return redirect(url_for("students"))
    elif interventionForm.validate_on_submit():
        add_InterventionLog(
            int(interventionForm.studentID.data),
            int(interventionForm.interventionType.data),
            int(interventionForm.interventionLevel.data),
            interventionForm.startDate.data,
            interventionForm.endDate.data,
            interventionForm.comment.data,
        )
        print(
            "===   Completed add_InterventionLog.  Redirecting to students   ===",
            datetime.now(),
            "   ===",
        )
        return redirect(url_for("students"))
    elif request.method == "GET":
        return render_template(
            "students.html",
            title="Students",
            students=students,
            dailyAttendanceForm=dailyAttendanceForm,
            interventionForm=interventionForm,
        )


@app.route("/dailyattendancelog")
def displayDailyAttendanceLogs():
    DailyAttendanceLogs = DailyAttendanceLog.query.order_by(
        DailyAttendanceLog.absenceDate.desc()
    )
    return render_template(
        "dailyattendancelog.html",
        title="Daily Attendance Log",
        DailyAttendanceLogs=DailyAttendanceLogs,
    )


@app.route("/dailyattendancelog/<int:log_id>/delete", methods=["POST"])
def delete_DailyAttendanceLog(log_id):
    log = DailyAttendanceLog.query.get_or_404(log_id)
    db.session.delete(log)
    db.session.commit()
    flash("Daily attendance log has been deleted!", "success")
    return redirect(url_for("displayDailyAttendanceLogs"))


@app.route("/interventionlog")
def displayInterventionLogs():
    InterventionLogs = InterventionLog.query.order_by(InterventionLog.endDate.desc())
    return render_template(
        "interventionlog.html",
        title="Intervention Log",
        InterventionLogs=InterventionLogs,
    )


@app.route("/interventionlog/<int:log_id>/delete", methods=["POST"])
def delete_InterventionLog(log_id):
    log = InterventionLog.query.get_or_404(log_id)
    db.session.delete(log)
    db.session.commit()
    flash("Intervention log has been deleted!", "success")
    return redirect(url_for("displayInterventionLogs"))


@app.route("/masterschedule")
def displayMasterSchedule():
    ClassSchedules = ClassSchedule.query.order_by(
        ClassSchedule.chattStateANumber.desc()
    )
    return render_template(
        "masterschedule.html", title="Master Schedule", ClassSchedules=ClassSchedules,
    )


@app.route("/masterschedule/<int:log_id>/delete", methods=["POST"])
def delete_ClassSchedule(log_id):
    log = ClassSchedule.query.get_or_404(log_id)
    db.session.delete(log)
    db.session.commit()
    flash("Class schedule has been deleted!", "success")
    return redirect(url_for("displayMasterSchedule"))


@app.route("/classattendancelog")
def displayClassAttendanceLog():
    classAttendanceFixedFields = ClassAttendanceLog.query.all()
    classAttendanceForm = updateClassAttendanceForm()
    classAttendanceForm.title.data = "My class"

    for studentAttendance in ClassAttendanceLog.query.all():
        studentAttendanceForm = updateStudentAttendanceForm()
        studentAttendanceForm.attendanceCode = studentAttendance.attendanceCode
        studentAttendanceForm.comment = studentAttendance.comment
        classAttendanceForm.classMembers.append_entry(studentAttendanceForm)

    return render_template(
        "classattendancelog.html",
        title="Class Attendance Log",
        classAttendanceForm=classAttendanceForm,
        classAttendanceFixedFields=classAttendanceFixedFields,
    )


@app.route("/bootstraptest")
def displayBootstrapTest():
    DailyAttendanceLogs = DailyAttendanceLog.query.all()
    return render_template(
        "bootstraptest.html",
        title="Bootstrap Test",
        DailyAttendanceLogs=DailyAttendanceLogs,
    )


@app.route("/analytics")
def displayAnalyticsTest():
    return render_template("analytics.html")


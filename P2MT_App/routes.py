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
    classAttendanceLogFilters,
)
from P2MT_App.referenceData import getInterventionTypes, getTeachers, getClassNames
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


@app.route("/classattendancelognew", methods=["GET", "POST"])
def displayClassAttendanceLogNew():
    classAttendanceForm = updateClassAttendanceForm()
    classAttendanceForm.teacherName.choices = getTeachers()
    classAttendanceForm.className.choices = getClassNames()

    classDateTime = datetime(
        datetime.today().year, datetime.today().month, datetime.today().day, 0, 0, 0, 0
    )
    print(
        "\nclassAttendanceForm.identifier.data = ", classAttendanceForm.identifier.data
    )
    # if request.method == "POST":

    if request.method == "POST":
        print("request.form =", request.form)

    # if classAttendanceForm.validate_on_submit():
    #     print("classAttendanceForm.validate_on_submit() =", classAttendanceForm.validate_on_submit())
    # print("classAttendanceForm.errors =", classAttendanceForm.errors)

    if (
        classAttendanceForm.identifier.data == "classAttendanceForm"
        and classAttendanceForm.is_submitted()
    ):

        log_id = classAttendanceForm.classMembers.data[0]["log_id"]
        classAttendanceLog = ClassAttendanceLog.query.get_or_404(log_id)
        classAttendanceLog.attendanceCode = classAttendanceForm.classMembers.data[0][
            "attendanceCode"
        ]
        classAttendanceLog.comment = classAttendanceForm.classMembers.data[0]["comment"]
        db.session.commit()

        print(
            "CAF log filter data:",
            classAttendanceForm.classDate.data,
            classAttendanceForm.className.data,
            classAttendanceForm.teacherName.data,
        )
        parsedDate = datetime.strptime(
            classAttendanceForm.classMembers.data[0]["classDate"], "%Y-%m-%d"
        )
        print(
            "CAF classAttendanceFormLogFilters data:",
            classAttendanceForm.classMembers.data[0]["className"],
            classAttendanceForm.classMembers.data[0]["teacherName"],
            classAttendanceForm.classMembers.data[0]["classDate"],
            parsedDate,
        )
        logFilterData = classAttendanceForm.classMembers.data
        className = logFilterData[0]["className"]
        teacherName = logFilterData[0]["teacherName"]
        classDate = datetime.strptime(logFilterData[0]["classDate"], "%Y-%m-%d")

        # classAttendanceForm = updateClassAttendanceForm()
        # classAttendanceForm.teacherName.choices = getTeachers()
        # classAttendanceForm.className.choices = getClassNames()

        classAttendanceForm.className.default = className
        classAttendanceForm.teacherName.default = teacherName
        classAttendanceForm.classDate.default = classDate

        # classAttendanceForm.className.default = classAttendanceForm.classMembers.data[
        #     0
        # ]["className"]

        # classAttendanceForm.teacherName.default = classAttendanceForm.classMembers.data[
        #     0
        # ]["teacherName"]

        # classAttendanceForm.classDate.default = datetime.strptime(
        #     classAttendanceForm.classMembers.data[0]["classDate"], "%Y-%m-%d"
        # )
        # classAttendanceForm.process()

        print(
            "CAF log filter default:",
            classAttendanceForm.classDate.default,
            classAttendanceForm.className.default,
            classAttendanceForm.teacherName.default,
        )

        classAttendanceForm.process()

        classAttendanceFixedFields = ClassAttendanceLog.query.filter(
            ClassAttendanceLog.classDate == parsedDate
        ).all()
        # classAttendanceForm = updateClassAttendanceForm()

        for studentAttendance in ClassAttendanceLog.query.filter(
            ClassAttendanceLog.classDate == parsedDate
        ).all():
            studentAttendanceForm = updateStudentAttendanceForm()
            studentAttendanceForm.log_id = studentAttendance.id
            studentAttendanceForm.attendanceCode = studentAttendance.attendanceCode
            studentAttendanceForm.comment = studentAttendance.comment
            studentAttendanceForm.teacherName = ""
            studentAttendanceForm.className = ""
            studentAttendanceForm.classDate = ""
            # studentAttendanceForm.process()
            classAttendanceForm.classMembers.append_entry(studentAttendanceForm)
            print(
                "SAF ",
                studentAttendanceForm.log_id,
                studentAttendanceForm.attendanceCode,
                studentAttendanceForm.comment,
            )
        print("classAttendanceForm =", classAttendanceForm)

    elif classAttendanceForm.identifier.data == "logFilters":
        print(
            "LF log filter data:",
            classAttendanceForm.classDate.data,
            classAttendanceForm.className.data,
            classAttendanceForm.teacherName.data,
        )

        classAttendanceForm.classDate.default = classAttendanceForm.classDate.data
        classDate = classAttendanceForm.classDate.data
        classAttendanceForm.className.default = classAttendanceForm.className.data
        classAttendanceForm.teacherName.default = classAttendanceForm.teacherName.data

        print(
            "LF log filter default:",
            classAttendanceForm.classDate.default,
            classAttendanceForm.className.default,
            classAttendanceForm.teacherName.default,
        )

        print(
            "LF log filter choices:",
            classAttendanceForm.className.choices,
            classAttendanceForm.teacherName.choices,
        )

        # print(type(classDate))
        classDateTime = datetime(
            classDate.year, classDate.month, classDate.day, 0, 0, 0, 0
        )
        # print(type(classDate), classDateTime)
        # print(logFilters.className.data)
        # print(logFilters.teacherName.data)

        classAttendanceFixedFields = ClassAttendanceLog.query.filter(
            ClassAttendanceLog.classDate == classDateTime
        ).all()
        # classAttendanceForm = updateClassAttendanceForm()
        for studentAttendance in ClassAttendanceLog.query.filter(
            ClassAttendanceLog.classDate == classDateTime
        ).all():
            studentAttendanceForm = updateStudentAttendanceForm()
            studentAttendanceForm.log_id = studentAttendance.id
            studentAttendanceForm.attendanceCode = studentAttendance.attendanceCode
            studentAttendanceForm.comment = studentAttendance.comment
            studentAttendanceForm.teacherName = ""
            studentAttendanceForm.className = ""
            studentAttendanceForm.classDate = ""
            classAttendanceForm.classMembers.append_entry(studentAttendanceForm)

        print(
            "LF log filter default:",
            classAttendanceForm.classDate.default,
            classAttendanceForm.className.default,
            classAttendanceForm.teacherName.default,
        )

        print(
            "LF log filter choices:",
            classAttendanceForm.className.choices,
            classAttendanceForm.teacherName.choices,
        )
    elif classAttendanceForm.identifier.data is None:
        print(
            "classAttendanceForm.identifier.data =", classAttendanceForm.identifier.data
        )
        # classDate = datetime(
        #     datetime.today().year, datetime.today().month, datetime.today().day
        # )

        classAttendanceFixedFields = ClassAttendanceLog.query.filter(
            ClassAttendanceLog.classDate == classDateTime
        ).all()
        # classAttendanceForm = updateClassAttendanceForm()

        for studentAttendance in ClassAttendanceLog.query.filter(
            ClassAttendanceLog.classDate == classDateTime
        ).all():
            studentAttendanceForm = updateStudentAttendanceForm()
            studentAttendanceForm.log_id = studentAttendance.id
            studentAttendanceForm.attendanceCode = studentAttendance.attendanceCode
            studentAttendanceForm.comment = studentAttendance.comment
            studentAttendanceForm.teacherName = ""
            studentAttendanceForm.className = ""
            studentAttendanceForm.classDate = ""
            classAttendanceForm.classMembers.append_entry(studentAttendanceForm)

        print(
            "NONE log filter default:",
            classAttendanceForm.classDate.default,
            classAttendanceForm.className.default,
            classAttendanceForm.teacherName.default,
        )
        print(
            "NONE log filter choices:",
            classAttendanceForm.className.choices,
            classAttendanceForm.teacherName.choices,
        )
    print("Final before render_template")
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


from flask import render_template, flash, request, Blueprint
from P2MT_App import db
from P2MT_App.main.utilityfunctions import printLogEntry
from P2MT_App.models import Student, ClassSchedule, ClassAttendanceLog
from P2MT_App.classAttendance.forms import (
    updateClassAttendanceForm,
    updateStudentAttendanceForm,
)
from P2MT_App.main.referenceData import getTeachers, getClassNames
from datetime import date

classAttendance_bp = Blueprint("classAttendance_bp", __name__)


@classAttendance_bp.route("/classattendancelog", methods=["GET", "POST"])
def displayClassAttendanceLog():
    printLogEntry("Running displayClassAttendanceLog()")
    classAttendanceForm = updateClassAttendanceForm()
    classAttendanceForm.teacherName.choices = getTeachers()
    classAttendanceForm.className.choices = getClassNames()

    classDateTime = date.today()
    # classDateTime = datetime(
    #     datetime.today().year, datetime.today().month, datetime.today().day, 0, 0, 0, 0
    # )
    # print(
    #     "\nclassAttendanceForm.identifier.data = ", classAttendanceForm.identifier.data
    # )
    print(
        "classAttendanceForm.updateFiltersFlag.data =",
        classAttendanceForm.updateFiltersFlag.data,
    )

    print("request.method =", request.method)

    if classAttendanceForm.validate_on_submit():
        print(
            "classAttendanceForm.validate_on_submit() =",
            classAttendanceForm.validate_on_submit(),
        )
    print("classAttendanceForm.errors =", classAttendanceForm.errors)

    # if classAttendanceForm.identifier.data is None:
    if request.method == "GET":

        if classAttendanceForm.classDate.data:
            classDateTime = classAttendanceForm.classDate.data
            classAttendanceForm.classDate.default = classDateTime
        else:
            classDateTime = date.today()
            # classDateTime = datetime.now()
            # classDateTime = classDateTime.replace(
            #     hour=0, minute=0, second=0, microsecond=0
            # )
            classAttendanceForm.classDate.data = classDateTime
            # classAttendanceForm.classDate.data = classDateTime.date()

        classAttendanceForm.className.default = classAttendanceForm.className.data
        classAttendanceForm.teacherName.default = classAttendanceForm.teacherName.data
        classAttendanceForm.updateFiltersFlag.data = ""

    if classAttendanceForm.validate_on_submit():

        # Update default values for teacher name and class name
        classAttendanceForm.className.default = classAttendanceForm.className.data
        classAttendanceForm.teacherName.default = classAttendanceForm.teacherName.data

        # Format class date for compatibility with database
        classDate = classAttendanceForm.classDate.data
        classDateTime = classDate
        print(classDate, classDateTime)
        # classDateTime = datetime(
        #     classDate.year, classDate.month, classDate.day, 0, 0, 0, 0
        # )
        print(
            "classAttendanceForm.updateFiltersFlag.data =",
            classAttendanceForm.updateFiltersFlag.data,
        )

        # Update database with attendance updates
        if (
            classAttendanceForm.classMembers
            and classAttendanceForm.updateFiltersFlag.data != "updated"
        ):
            print("Class attendance submitted")
            print(len(classAttendanceForm.classMembers.data))
            for studentForm in classAttendanceForm.classMembers.data:
                if studentForm["updateFlag"] == "updated":
                    log_id = studentForm["log_id"]
                    print("log_id = ", log_id)
                    classAttendanceLog = ClassAttendanceLog.query.get_or_404(log_id)
                    classAttendanceLog.attendanceCode = studentForm["attendanceCode"]
                    classAttendanceLog.comment = studentForm["comment"]
                    db.session.commit()

        # Need to run the next statement [classAttendanceForm.process()]
        # or the updated values for the studentAttendanceForm won't display
        classAttendanceForm.process()

    # Retrive updated fixed-value attendance fields from database
    classAttendanceFixedFields = (
        ClassAttendanceLog.query.filter(ClassAttendanceLog.classDate == classDateTime)
        .join(ClassSchedule)
        .join(ClassSchedule.Student)
        .filter(
            ClassSchedule.teacherLastName == classAttendanceForm.teacherName.default
        )
        .filter(ClassSchedule.className == classAttendanceForm.className.default)
        .order_by(ClassSchedule.startTime)
        .order_by(ClassSchedule.className)
        .order_by(Student.lastName)
        .all()
    )

    # Retrieve updated student attendance fields from database
    for studentAttendance in classAttendanceFixedFields:
        studentAttendanceForm = updateStudentAttendanceForm()
        studentAttendanceForm.log_id = studentAttendance.id
        studentAttendanceForm.attendanceCode = studentAttendance.attendanceCode
        studentAttendanceForm.comment = studentAttendance.comment
        studentAttendanceForm.updateFlag = ""
        print(
            "ROSTER ",
            studentAttendanceForm.log_id,
            studentAttendance.ClassSchedule.className,
            studentAttendance.ClassSchedule.startTime,
            studentAttendance.ClassSchedule.endTime,
            studentAttendance.ClassSchedule.Student.firstName,
            studentAttendance.ClassSchedule.Student.lastName,
            studentAttendanceForm.attendanceCode,
            studentAttendanceForm.comment,
        )
        classAttendanceForm.classMembers.append_entry(studentAttendanceForm)

    # Reset the updateFiltersFlag before rendering page
    classAttendanceForm.updateFiltersFlag.data = ""

    print("Final before render_template")
    print(
        "classAttendanceForm.classDate.default =",
        classAttendanceForm.classDate.default,
    )
    print(
        "classAttendanceForm.classDate.data =", classAttendanceForm.classDate.data,
    )
    return render_template(
        "classattendancelog.html",
        title="Class Attendance Log",
        classAttendanceForm=classAttendanceForm,
        classAttendanceFixedFields=classAttendanceFixedFields,
    )

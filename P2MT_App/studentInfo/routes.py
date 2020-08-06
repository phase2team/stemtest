from flask import render_template, redirect, request, url_for, flash, Blueprint
from P2MT_App import db
from P2MT_App.models import Student
from P2MT_App.dailyAttendance.dailyAttendance import add_DailyAttendanceLog
from P2MT_App.interventionInfo.interventionInfo import add_InterventionLog
from P2MT_App.interventionInfo.forms import addInterventionLogForm
from P2MT_App.dailyAttendance.forms import addDailyAttendanceForm
from P2MT_App.main.referenceData import getInterventionTypes
from datetime import datetime

studentInfo_bp = Blueprint("studentInfo_bp", __name__)


@studentInfo_bp.route("/students", methods=["GET", "POST"])
def displayStudents():
    dailyAttendanceForm = addDailyAttendanceForm()
    interventionForm = addInterventionLogForm()
    interventionForm.interventionType.choices = getInterventionTypes()
    students = Student.query.order_by(
        Student.yearOfGraduation.asc(), Student.lastName.asc()
    )
    if "submitDailyAttendance" in request.form:
        if dailyAttendanceForm.validate_on_submit():
            print("Running dailyAttendanceForm")
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
            return redirect(url_for("studentInfo_bp.displayStudents"))

    if "submitIntervention" in request.form:
        if interventionForm.validate_on_submit():
            print("Running interventionForm")
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
            return redirect(url_for("studentInfo_bp.displayStudents"))

    if request.method == "GET":
        return render_template(
            "students.html",
            title="Students",
            students=students,
            dailyAttendanceForm=dailyAttendanceForm,
            interventionForm=interventionForm,
        )

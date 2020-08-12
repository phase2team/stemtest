from flask import render_template, flash, request, Blueprint
from P2MT_App import db
from P2MT_App.main.utilityfunctions import printLogEntry
from P2MT_App.models import Student, ClassSchedule, ClassAttendanceLog
from P2MT_App.main.referenceData import getCurrent_Start_End_Tmi_Dates
from datetime import date
from P2MT_App.tmiFinalApproval.tmiFinalApproval import (
    calculateTmi,
    assignTmiForTardy,
)

tmiFinalApproval_bp = Blueprint("tmiFinalApproval_bp", __name__)


@tmiFinalApproval_bp.route("/tmifinalapproval", methods=["GET", "POST"])
def displayTmiFinalApproval():
    printLogEntry("Running displayTmiFinalApproval()")
    startTmiPeriod, endTmiPeriod, tmiDay = getCurrent_Start_End_Tmi_Dates()
    assignTmiForTardy(startTmiPeriod, endTmiPeriod)
    print("db.session.dirty =", db.session.dirty)
    db.session.commit()
    print("db.session.dirty =", db.session.dirty)

    print("request.method =", request.method)

    classAttendanceFixedFields = (
        ClassAttendanceLog.query.filter(
            ClassAttendanceLog.classDate >= startTmiPeriod,
            ClassAttendanceLog.classDate <= endTmiPeriod,
        )
        .filter(ClassAttendanceLog.assignTmi == True)
        .join(ClassSchedule)
        .join(ClassSchedule.Student)
        .order_by(Student.lastName, ClassAttendanceLog.classDate)
        .all()
    )

    # calculateTmi(classAttendanceFixedFields)

    return render_template(
        "tmifinalapproval.html",
        title="TMI Final Approval",
        classAttendanceFixedFields=classAttendanceFixedFields,
        startTmiPeriod=startTmiPeriod,
        endTmiPeriod=endTmiPeriod,
        tmiDay=tmiDay,
    )

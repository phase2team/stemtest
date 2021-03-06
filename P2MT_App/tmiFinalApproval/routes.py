from flask import render_template, flash, request, Blueprint
from P2MT_App import db
from P2MT_App.main.utilityfunctions import printLogEntry
from P2MT_App.models import Student, ClassSchedule, ClassAttendanceLog, InterventionLog
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
    startTmiPeriod, endTmiPeriod, tmiDate = getCurrent_Start_End_Tmi_Dates()

    # Update assignTmi for students with tardies
    assignTmiForTardy(startTmiPeriod, endTmiPeriod)
    db.session.commit()

    classAttendanceFixedFields = (
        ClassAttendanceLog.query.filter(
            ClassAttendanceLog.classDate >= startTmiPeriod,
            ClassAttendanceLog.classDate <= endTmiPeriod,
        )
        .filter(ClassAttendanceLog.assignTmi == True)
        .join(ClassSchedule)
        .join(ClassSchedule.Student)
        .order_by(
            Student.lastName, ClassAttendanceLog.classDate, ClassSchedule.className
        )
        .all()
    )

    calculateTmi(startTmiPeriod, endTmiPeriod, tmiDate)
    db.session.commit()

    tmiInterventionLog = (
        InterventionLog.query.filter(
            InterventionLog.intervention_id == 3, InterventionLog.startDate == tmiDate
        )
        .join(Student)
        .order_by(Student.lastName)
        .all()
    )

    return render_template(
        "tmifinalapproval.html",
        title="TMI Final Approval",
        classAttendanceFixedFields=classAttendanceFixedFields,
        tmiInterventionLog=tmiInterventionLog,
        startTmiPeriod=startTmiPeriod,
        endTmiPeriod=endTmiPeriod,
        tmiDay=tmiDate,
    )

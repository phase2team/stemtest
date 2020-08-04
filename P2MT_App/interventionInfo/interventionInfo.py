from flask import flash
from P2MT_App import db
from P2MT_App.models import InterventionLog


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
        staffID=5,
        student_id=student_id,
    )
    db.session.add(interventionLog)
    db.session.commit()
    flash("Intervention log has been added!", "success")
    return

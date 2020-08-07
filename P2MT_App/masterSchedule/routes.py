from flask import render_template, redirect, url_for, flash, Blueprint
from P2MT_App import db
from P2MT_App.main.utilityfunctions import printLogEntry
from P2MT_App.models import ClassSchedule

masterSchedule_bp = Blueprint("masterSchedule_bp", __name__)


@masterSchedule_bp.route("/masterschedule")
def displayMasterSchedule():
    printLogEntry("Running displayMasterSchedule()")
    ClassSchedules = ClassSchedule.query.order_by(
        ClassSchedule.chattStateANumber.desc()
    )
    return render_template(
        "masterschedule.html", title="Master Schedule", ClassSchedules=ClassSchedules,
    )


@masterSchedule_bp.route("/masterschedule/<int:log_id>/delete", methods=["POST"])
def delete_ClassSchedule(log_id):

    log = ClassSchedule.query.get_or_404(log_id)
    classScheduleLogDetails = f"{(log_id)} {log.chattStateANumber} {log.className}"
    printLogEntry("Running deleteClassSchedule(" + classScheduleLogDetails + ")")
    db.session.delete(log)
    db.session.commit()
    flash("Class schedule has been deleted!", "success")
    return redirect(url_for("masterSchedule_bp.displayMasterSchedule"))

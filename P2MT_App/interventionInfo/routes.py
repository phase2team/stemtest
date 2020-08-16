from flask import render_template, redirect, url_for, flash, Blueprint
from P2MT_App import db
from P2MT_App.models import InterventionLog
from P2MT_App.main.utilityfunctions import printLogEntry
from P2MT_App.interventionInfo.interventionInfo import downloadInterventionLog

interventionInfo_bp = Blueprint("interventionInfo_bp", __name__)


@interventionInfo_bp.route("/interventionlog")
def displayInterventionLogs():
    printLogEntry("Running displayInterventionLogs()")
    InterventionLogs = InterventionLog.query.order_by(InterventionLog.endDate.desc())
    return render_template(
        "interventionlog.html",
        title="Intervention Log",
        InterventionLogs=InterventionLogs,
    )


@interventionInfo_bp.route("/interventionlog/<int:log_id>/delete", methods=["POST"])
def delete_InterventionLog(log_id):
    log = InterventionLog.query.get_or_404(log_id)
    LogDetails = f"{(log_id)} {log.chattStateANumber} {log.staffID}"
    printLogEntry("Running delete_InterventionLog(" + LogDetails + ")")
    db.session.delete(log)
    db.session.commit()
    flash("Intervention log has been deleted!", "success")
    return redirect(url_for("interventionInfo_bp.displayInterventionLogs"))


@interventionInfo_bp.route("/interventionlog/download")
def download_InterventionLog():
    printLogEntry(
        "download_Daildownload_InterventionLogyAttendanceLog() function called"
    )
    return downloadInterventionLog()

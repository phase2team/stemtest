from flask import render_template, redirect, url_for, flash, Blueprint
from P2MT_App import db
from P2MT_App.models import DailyAttendanceLog

dailyAttendance_bp = Blueprint("dailyAttendance_bp", __name__)


@dailyAttendance_bp.route("/dailyattendancelog")
def displayDailyAttendanceLogs():
    printLogEntry("displayDailyAttendanceLogs() function called")
    DailyAttendanceLogs = DailyAttendanceLog.query.order_by(
        DailyAttendanceLog.absenceDate.desc()
    )
    return render_template(
        "dailyattendancelog.html",
        title="Daily Attendance Log",
        DailyAttendanceLogs=DailyAttendanceLogs,
    )


@dailyAttendance_bp.route("/dailyattendancelog/<int:log_id>/delete", methods=["POST"])
def delete_DailyAttendanceLog(log_id):
    log = DailyAttendanceLog.query.get_or_404(log_id)
    LogDetails = f"{(log_id)} {log.student_id} {log.staffID}"
    printLogEntry("Running delete_DailyAttendanceLog(" + LogDetails + ")")
    db.session.delete(log)
    db.session.commit()
    flash("Daily attendance log has been deleted!", "success")
    return redirect(url_for("dailyAttendance_bp.displayDailyAttendanceLogs"))

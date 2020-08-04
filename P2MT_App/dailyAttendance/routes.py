from flask import render_template, redirect, url_for, flash, Blueprint
from P2MT_App import db
from P2MT_App.models import DailyAttendanceLog

dailyAttendance = Blueprint("dailyAttendance", __name__)


@dailyAttendance.route("/dailyattendancelog")
def displayDailyAttendanceLogs():
    DailyAttendanceLogs = DailyAttendanceLog.query.order_by(
        DailyAttendanceLog.absenceDate.desc()
    )
    return render_template(
        "dailyattendancelog.html",
        title="Daily Attendance Log",
        DailyAttendanceLogs=DailyAttendanceLogs,
    )


@dailyAttendance.route("/dailyattendancelog/<int:log_id>/delete", methods=["POST"])
def delete_DailyAttendanceLog(log_id):
    log = DailyAttendanceLog.query.get_or_404(log_id)
    db.session.delete(log)
    db.session.commit()
    flash("Daily attendance log has been deleted!", "success")
    return redirect(url_for("dailyAttendance.displayDailyAttendanceLogs"))

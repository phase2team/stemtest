from flask import render_template, redirect, url_for, flash, Blueprint
from P2MT_App import db
from P2MT_App.models import InterventionLog

interventionInfo = Blueprint("interventionInfo", __name__)


@interventionInfo.route("/interventionlog")
def displayInterventionLogs():
    InterventionLogs = InterventionLog.query.order_by(InterventionLog.endDate.desc())
    return render_template(
        "interventionlog.html",
        title="Intervention Log",
        InterventionLogs=InterventionLogs,
    )


@interventionInfo.route("/interventionlog/<int:log_id>/delete", methods=["POST"])
def delete_InterventionLog(log_id):
    log = InterventionLog.query.get_or_404(log_id)
    db.session.delete(log)
    db.session.commit()
    flash("Intervention log has been deleted!", "success")
    return redirect(url_for("interventionInfo.displayInterventionLogs"))

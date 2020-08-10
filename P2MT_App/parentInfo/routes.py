from flask import render_template, request, flash, Blueprint
from P2MT_App import db
from P2MT_App.models import Parents, Student
from P2MT_App.main.utilityfunctions import printLogEntry
from P2MT_App.p2mtAdmin.p2mtAdmin import downloadParentsList

parentsInfo_bp = Blueprint("parentsInfo_bpInfo_bp", __name__)


@parentsInfo_bp.route("/parents/download")
def download_ParentList():
    printLogEntry("download_ParentList() function called")
    return downloadParentsList()


@parentsInfo_bp.route("/parents", methods=["GET", "POST"])
def displayParents():
    printLogEntry("Running displayParents()")
    parents = Parents.query.join(Student).order_by(Student.lastName.asc())

    if request.method == "GET":
        return render_template("parents.html", title="Parent Info", parents=parents,)

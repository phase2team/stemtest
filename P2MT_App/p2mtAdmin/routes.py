from flask import (
    render_template,
    flash,
    request,
    Blueprint,
)
from P2MT_App.models import Student
from P2MT_App.p2mtAdmin.forms import (
    addStudentForm,
    uploadStudentListForm,
    deleteStudentForm,
)
from P2MT_App.main.referenceData import (
    getTeachers,
    getClassNames,
    getSchoolYear,
    getSemester,
    getStudents,
    getCampusChoices,
    getYearOfGraduation,
)

from P2MT_App.p2mtAdmin.p2mtAdmin import (
    addStudentToDatabase,
    uploadStudentList,
    deleteStudent,
)
from P2MT_App.main.utilityfunctions import save_File
from P2MT_App.main.utilityfunctions import printLogEntry, printFormErrors

p2mtAdmin_bp = Blueprint("p2mtAdmin_bp", __name__)


@p2mtAdmin_bp.route("/p2mtadmin", methods=["GET", "POST"])
def displayP2MTAdmin():
    printLogEntry("Running displayP2MTAdmin()")
    addStudentFormDetails = addStudentForm()
    uploadStudentListFormDetails = uploadStudentListForm()
    deleteStudentFormDetails = deleteStudentForm()
    deleteStudentFormDetails.studentName.choices = getStudents()

    if request.method == "POST":
        printLogEntry("form= " + str(request.form))
    if "submitAddStudent" in request.form:
        if addStudentFormDetails.validate():
            printLogEntry("Add Student submitted")
            firstName = addStudentFormDetails.firstName.data
            lastName = addStudentFormDetails.lastName.data
            chattStateANumber = addStudentFormDetails.chattStateANumber.data
            email = addStudentFormDetails.email.data
            yearOfGraduation = int(addStudentFormDetails.yearOfGraduation.data)
            house = addStudentFormDetails.house.data
            googleCalendarId = addStudentFormDetails.googleCalendarId.data

            addStudentToDatabase(
                chattStateANumber,
                firstName,
                lastName,
                email,
                house,
                yearOfGraduation,
                googleCalendarId,
            )

    if "submitUploadStudentList" in request.form:
        if uploadStudentListFormDetails.validate_on_submit():
            printLogEntry("Upload Student List Form Submitted")
            if uploadStudentListFormDetails.csvStudentListFile.data:
                uploadedStudentListFile = save_File(
                    uploadStudentListFormDetails.csvStudentListFile.data,
                    "Uploaded_StudentList_File.csv",
                )
                uploadStudentList(uploadedStudentListFile)
    printFormErrors(uploadStudentListFormDetails)

    if "submitDeleteStudent" in request.form:
        if deleteStudentFormDetails.validate_on_submit():
            if deleteStudentFormDetails.confirmDeleteStudent.data == "DELETE":
                printLogEntry("Delete Student Form Submitted")
                # studentName returns chattStateANumber as its value
                chattStateANumber = deleteStudentFormDetails.studentName.data
                print("chattStateANumber =", chattStateANumber)
                deleteStudent(chattStateANumber)
                deleteStudentFormDetails.confirmDeleteStudent.data = ""
                # deleteClassScheduleFormDetails.process()
            else:
                deleteStudentFormDetails.confirmDeleteStudent.data = ""
                printLogEntry("Type DELETE in the text box to confirm delete")

    return render_template(
        "p2mtadmin.html",
        title="P2MT Admin",
        addStudentForm=addStudentFormDetails,
        uploadStudentListForm=uploadStudentListFormDetails,
        deleteStudentForm=deleteStudentFormDetails,
    )


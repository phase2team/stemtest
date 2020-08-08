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
    addStaffForm,
    uploadStaffListForm,
    deleteStaffForm,
)
from P2MT_App.main.referenceData import getStudents, getStaffFromFacultyAndStaff

from P2MT_App.p2mtAdmin.p2mtAdmin import (
    addStudentToDatabase,
    uploadStudentList,
    deleteStudent,
    addStaffToDatabase,
    uploadStaffList,
    deleteStaff,
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
    addStaffFormDetails = addStaffForm()
    uploadStaffListFormDetails = uploadStaffListForm()
    deleteStaffFormDetails = deleteStaffForm()
    deleteStaffFormDetails.staffName.choices = getStaffFromFacultyAndStaff()

    if request.method == "POST":
        printLogEntry("form= " + str(request.form))
    if "submitAddStudent" in request.form:
        if addStudentFormDetails.validate_on_submit():
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
    printFormErrors(addStudentFormDetails)

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
    printFormErrors(deleteStudentFormDetails)

    if "submitAddStaff" in request.form:
        if addStaffFormDetails.validate_on_submit():
            printLogEntry("Add Staff submitted")
            firstName = addStaffFormDetails.firstName.data
            lastName = addStaffFormDetails.lastName.data
            position = addStaffFormDetails.position.data
            email = addStaffFormDetails.email.data
            phoneNumber = addStaffFormDetails.phoneNumber.data
            chattStateANumber = addStaffFormDetails.chattStateANumber.data
            myersBriggs = addStaffFormDetails.myersBriggs.data
            house = addStaffFormDetails.house.data
            houseGrade = addStaffFormDetails.houseGrade.data
            twitterAccount = addStaffFormDetails.twitterAccount.data

            addStaffToDatabase(
                firstName,
                lastName,
                position,
                email,
                phoneNumber,
                chattStateANumber,
                myersBriggs,
                house,
                houseGrade,
                twitterAccount,
            )
    printFormErrors(addStaffFormDetails)

    if "submitUploadStaffList" in request.form:
        if uploadStaffListFormDetails.validate_on_submit():
            printLogEntry("Upload Staff List Form Submitted")
            if uploadStaffListFormDetails.csvStaffListFile.data:
                uploadedStaffListFile = save_File(
                    uploadStaffListFormDetails.csvStaffListFile.data,
                    "Uploaded_StaffList_File.csv",
                )
                uploadStaffList(uploadedStaffListFile)
    printFormErrors(uploadStaffListFormDetails)

    if "submitDeleteStaff" in request.form:
        if deleteStaffFormDetails.validate_on_submit():
            if deleteStaffFormDetails.confirmDeleteStaff.data == "DELETE":
                printLogEntry("Delete Staff Form Submitted")
                # staffname returns log id as its value
                log_id = int(deleteStaffFormDetails.staffName.data)
                print("log_id =", log_id)
                deleteStaff(log_id)
                deleteStaffFormDetails.confirmDeleteStaff.data = ""
                # deleteClassScheduleFormDetails.process()
            else:
                deleteStaffFormDetails.confirmDeleteStaff.data = ""
                printLogEntry("Type DELETE in the text box to confirm delete")
    printFormErrors(deleteStaffFormDetails)

    return render_template(
        "p2mtadmin.html",
        title="P2MT Admin",
        addStudentForm=addStudentFormDetails,
        uploadStudentListForm=uploadStudentListFormDetails,
        deleteStudentForm=deleteStudentFormDetails,
        addStaffForm=addStaffFormDetails,
        uploadStaffListForm=uploadStaffListFormDetails,
        deleteStaffForm=deleteStaffFormDetails,
    )


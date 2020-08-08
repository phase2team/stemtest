from flask import (
    render_template,
    redirect,
    url_for,
    flash,
    request,
    Blueprint,
)
from P2MT_App import db
from P2MT_App.models import Student
from P2MT_App.p2mtAdmin.forms import (
    addStudentForm,
    updateStudentForm,
    selectStudentToEditForm,
    uploadStudentListForm,
    deleteStudentForm,
    addStaffForm,
    uploadStaffListForm,
    deleteStaffForm,
)
from P2MT_App.main.referenceData import (
    getStudents,
    getStudentsById,
    getStaffFromFacultyAndStaff,
)

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
    selectStudentToEditFormDetails = selectStudentToEditForm()
    selectStudentToEditFormDetails.studentName.choices = getStudentsById()
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
            return redirect(url_for("p2mtAdmin_bp.displayP2MTAdmin"))
    printFormErrors(addStudentFormDetails)

    if "submitStudentToEdit" in request.form:
        if selectStudentToEditFormDetails.validate_on_submit:
            printLogEntry("Student to Edit Form Submitted")
            student_id = int(selectStudentToEditFormDetails.studentName.data)
            print("student_id = ", student_id)
            return redirect(
                url_for("p2mtAdmin_bp.updateStudent", student_id=student_id)
            )
    printFormErrors(selectStudentToEditFormDetails)

    if "submitUploadStudentList" in request.form:
        if uploadStudentListFormDetails.validate_on_submit():
            printLogEntry("Upload Student List Form Submitted")
            if uploadStudentListFormDetails.csvStudentListFile.data:
                uploadedStudentListFile = save_File(
                    uploadStudentListFormDetails.csvStudentListFile.data,
                    "Uploaded_StudentList_File.csv",
                )
                uploadStudentList(uploadedStudentListFile)
                return redirect(url_for("p2mtAdmin_bp.displayP2MTAdmin"))
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
                return redirect(url_for("p2mtAdmin_bp.displayP2MTAdmin"))
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
            return redirect(url_for("p2mtAdmin_bp.displayP2MTAdmin"))
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
                return redirect(url_for("p2mtAdmin_bp.displayP2MTAdmin"))
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
                return redirect(url_for("p2mtAdmin_bp.displayP2MTAdmin"))
            else:
                deleteStaffFormDetails.confirmDeleteStaff.data = ""
                printLogEntry("Type DELETE in the text box to confirm delete")
    printFormErrors(deleteStaffFormDetails)

    return render_template(
        "p2mtadmin.html",
        title="P2MT Admin",
        addStudentForm=addStudentFormDetails,
        selectStudentToEditForm=selectStudentToEditFormDetails,
        uploadStudentListForm=uploadStudentListFormDetails,
        deleteStudentForm=deleteStudentFormDetails,
        addStaffForm=addStaffFormDetails,
        uploadStaffListForm=uploadStaffListFormDetails,
        deleteStaffForm=deleteStaffFormDetails,
    )


@p2mtAdmin_bp.route("/p2mtadmin/<int:student_id>/update", methods=["GET", "POST"])
def updateStudent(student_id):
    printLogEntry("Running updateStudent()")
    student = Student.query.get_or_404(student_id)
    updateStudentFormDetails = updateStudentForm()
    if "submitUpdateStudent" in request.form:
        if updateStudentFormDetails.validate_on_submit():
            student.firstName = updateStudentFormDetails.firstName.data
            student.lastName = updateStudentFormDetails.lastName.data
            student.email = updateStudentFormDetails.email.data
            student.chattStateANumber = updateStudentFormDetails.chattStateANumber.data
            student.yearOfGraduation = int(
                updateStudentFormDetails.yearOfGraduation.data
            )
            student.house = updateStudentFormDetails.house.data
            student.googleCalendarId = updateStudentFormDetails.googleCalendarId.data
            db.session.commit()
            studentUpdateString = (
                student.firstName
                + " "
                + student.lastName
                + " "
                + student.chattStateANumber
            )
            printLogEntry("Student info updated for " + studentUpdateString)
            flash("Student details for " + studentUpdateString + " updated!", "success")
            return redirect(url_for("p2mtAdmin_bp.displayP2MTAdmin"))
    elif request.method == "GET":
        updateStudentFormDetails.student_id.data = student.id
        updateStudentFormDetails.firstName.data = student.firstName
        updateStudentFormDetails.lastName.data = student.lastName
        updateStudentFormDetails.email.data = student.email
        updateStudentFormDetails.chattStateANumber.data = student.chattStateANumber
        updateStudentFormDetails.yearOfGraduation.data = student.yearOfGraduation
        updateStudentFormDetails.house.data = student.house
        updateStudentFormDetails.googleCalendarId.data = student.googleCalendarId
    return render_template(
        "updatestudent.html",
        title="Update Student",
        updateStudentForm=updateStudentFormDetails,
    )


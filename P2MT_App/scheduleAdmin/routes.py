from flask import (
    render_template,
    flash,
    request,
    Blueprint,
)
from P2MT_App.scheduleAdmin.forms import (
    uploadClassScheduleForm,
    propagateClassAttendanceLogsForm,
    deleteClassScheduleForm,
    downloadClassScheduleForm,
    downloadClassAttendanceForm,
    addSingleClassSchedule,
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
from P2MT_App.scheduleAdmin.ScheduleAdmin import (
    propagateClassSchedule,
    uploadSchedules,
    deleteClassSchedule,
    downloadClassSchedule,
    downloadClassAttendanceLog,
    addClassSchedule,
)
from P2MT_App.main.utilityfunctions import save_File

scheduleAdmin = Blueprint("scheduleAdmin", __name__)


@scheduleAdmin.route("/scheduleadmin", methods=["GET", "POST"])
def displayScheduleAdmin():
    uploadClassScheduleFormDetails = uploadClassScheduleForm()
    propagateClassAttendanceLogsFormDetails = propagateClassAttendanceLogsForm()
    propagateClassAttendanceLogsFormDetails.schoolYear.choices = getSchoolYear()
    propagateClassAttendanceLogsFormDetails.semester.choices = getSemester()
    deleteClassScheduleFormDetails = deleteClassScheduleForm()
    deleteClassScheduleFormDetails.schoolYear.choices = getSchoolYear()
    deleteClassScheduleFormDetails.semester.choices = getSemester()
    deleteClassScheduleFormDetails.yearOfGraduation.choices = getYearOfGraduation()
    downloadClassScheduleFormDetails = downloadClassScheduleForm()
    downloadClassScheduleFormDetails.schoolYear.choices = getSchoolYear()
    downloadClassScheduleFormDetails.semester.choices = getSemester()
    downloadClassAttendanceFormDetails = downloadClassAttendanceForm()
    downloadClassAttendanceFormDetails.schoolYear.choices = getSchoolYear()
    downloadClassAttendanceFormDetails.semester.choices = getSemester()
    downloadClassAttendanceFormDetails.teacherName.choices = getTeachers()
    addSingleClassScheduleDetails = addSingleClassSchedule()
    addSingleClassScheduleDetails.schoolYear.choices = getSchoolYear()
    addSingleClassScheduleDetails.semester.choices = getSemester()
    addSingleClassScheduleDetails.teacherName.choices = getTeachers()
    addSingleClassScheduleDetails.studentName.choices = getStudents()
    addSingleClassScheduleDetails.campus.choices = getCampusChoices()
    addSingleClassScheduleDetails.className.choices = getClassNames()
    addSingleClassScheduleDetails.classDays.choices = [
        ("M", "M"),
        ("T", "T"),
        ("W", "W"),
        ("R", "R"),
        ("F", "F"),
    ]
    print(request.form)
    if "submitUploadClassSchedule" in request.form:
        if uploadClassScheduleFormDetails.validate_on_submit():
            print("Upload Form Submitted")
            if uploadClassScheduleFormDetails.csvClassScheduleFile.data:
                uploadedScheduleFile = save_File(
                    uploadClassScheduleFormDetails.csvClassScheduleFile.data,
                    "Uploaded_Schedule_File.csv",
                )
                uploadSchedules(uploadedScheduleFile)
    print(uploadClassScheduleFormDetails.errors)
    if "submitPropagatelassAttendanceLogs" in request.form:
        if propagateClassAttendanceLogsFormDetails.validate_on_submit():
            print("Propagate Form Submitted")
            schoolYear = int(propagateClassAttendanceLogsFormDetails.schoolYear.data)
            semester = propagateClassAttendanceLogsFormDetails.semester.data
            startDate = propagateClassAttendanceLogsFormDetails.startDate.data
            endDate = propagateClassAttendanceLogsFormDetails.endDate.data
            print(
                "schoolYear=",
                schoolYear,
                "semester=",
                semester,
                "startDate=",
                startDate,
                "endDate=",
                endDate,
            )
            propagateClassSchedule(startDate, endDate, schoolYear, semester)
    print(propagateClassAttendanceLogsFormDetails.errors)
    if "submitDeleteClassScheduleForm" in request.form:
        if deleteClassScheduleFormDetails.validate_on_submit():
            if (
                deleteClassScheduleFormDetails.confirmDeleteClassSchedule.data
                == "DELETE"
            ):
                schoolYear = deleteClassScheduleFormDetails.schoolYear.data
                semester = deleteClassScheduleFormDetails.semester.data
                yearOfGraduation = deleteClassScheduleFormDetails.yearOfGraduation.data
                print(
                    "Delete Class Schedule Form Submitted: SchoolYear=",
                    schoolYear,
                    " Semester=",
                    semester,
                    yearOfGraduation,
                )
                deleteClassSchedule(schoolYear, semester, yearOfGraduation)
                deleteClassScheduleFormDetails.confirmDeleteClassSchedule.data = ""
                # deleteClassScheduleFormDetails.process()
            else:
                deleteClassScheduleFormDetails.confirmDeleteClassSchedule.data = ""
                print("Type DELETE in the text box to confirm delete")
    if "submitAddSingleClassSchedule" in request.form:
        if addSingleClassScheduleDetails.validate():
            schoolYear = addSingleClassScheduleDetails.schoolYear.data
            semester = addSingleClassScheduleDetails.semester.data
            chattStateANumber = addSingleClassScheduleDetails.studentName.data
            teacherLastName = addSingleClassScheduleDetails.teacherName.data
            className = addSingleClassScheduleDetails.className.data
            classDaysList = addSingleClassScheduleDetails.classDays.data
            classDays = ""
            for classDay in classDaysList:
                classDays = classDays + classDay
            startTime = addSingleClassScheduleDetails.startTime.data
            endTime = addSingleClassScheduleDetails.endTime.data
            online = addSingleClassScheduleDetails.online.data
            indStudy = addSingleClassScheduleDetails.indStudy.data
            comment = addSingleClassScheduleDetails.comment.data
            googleCalendarEventID = (
                addSingleClassScheduleDetails.googleCalendarEventID.data
            )
            campus = "STEM School"
            staffID = None

            print(
                schoolYear,
                semester,
                chattStateANumber,
                teacherLastName,
                className,
                classDays,
                startTime,
                endTime,
                online,
                indStudy,
                comment,
                googleCalendarEventID,
            )
            addClassSchedule(
                schoolYear,
                semester,
                chattStateANumber,
                campus,
                className,
                teacherLastName,
                staffID,
                online,
                indStudy,
                classDays,
                startTime,
                endTime,
                comment,
                googleCalendarEventID,
            )
    if "submitDownloadClassScheduleForm" in request.form:
        if downloadClassScheduleFormDetails.validate_on_submit():
            schoolYear = downloadClassScheduleFormDetails.schoolYear.data
            semester = downloadClassScheduleFormDetails.semester.data
            print(
                "Download Class Schedule Form Submitted: SchoolYear=",
                schoolYear,
                " Semester=",
                semester,
            )
            return downloadClassSchedule(schoolYear, semester)
    if "submitDownloadClassAttendanceForm" in request.form:
        if downloadClassAttendanceFormDetails.validate_on_submit():
            schoolYear = downloadClassAttendanceFormDetails.schoolYear.data
            semester = downloadClassAttendanceFormDetails.semester.data
            teacherName = downloadClassAttendanceFormDetails.teacherName.data
            startDate = downloadClassAttendanceFormDetails.startDate.data
            endDate = downloadClassAttendanceFormDetails.endDate.data
            print(
                "Download Class Attendance Form Submitted: SchoolYear=",
                schoolYear,
                " Semester=",
                semester,
                " teacherName=",
                teacherName,
                " startDate=",
                startDate,
                " endDate=",
                endDate,
            )
            return downloadClassAttendanceLog(
                schoolYear, semester, teacherName, startDate, endDate
            )
    return render_template(
        "scheduleadmin.html",
        title="Schedule Admin",
        propagateClassAttendanceLogsForm=propagateClassAttendanceLogsFormDetails,
        uploadClassScheduleForm=uploadClassScheduleFormDetails,
        deleteClassScheduleForm=deleteClassScheduleFormDetails,
        downloadClassScheduleForm=downloadClassScheduleFormDetails,
        downloadClassAttendanceForm=downloadClassAttendanceFormDetails,
        addSingleClassSchedule=addSingleClassScheduleDetails,
    )

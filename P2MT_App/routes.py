from flask import render_template, redirect, url_for, flash, request, send_file
from P2MT_App import app, db
from P2MT_App.models import (
    Student,
    ClassSchedule,
    FacultyAndStaff,
    DailyAttendanceLog,
    InterventionLog,
    ClassAttendanceLog,
)
from P2MT_App.forms import (
    addDailyAttendanceForm,
    addInterventionLogForm,
    updateStudentAttendanceForm,
    updateClassAttendanceForm,
    classAttendanceLogFilters,
    uploadClassScheduleForm,
    propagateClassAttendanceLogsForm,
    deleteClassScheduleForm,
    downloadClassScheduleForm,
    downloadClassAttendanceForm,
    addSingleClassSchedule,
    editSchoolCalendar,
)
from P2MT_App.referenceData import (
    getInterventionTypes,
    getTeachers,
    getClassNames,
    getSchoolYear,
    getSemester,
    getStudents,
    getCampusChoices,
    getYearOfGraduation,
)
from P2MT_App.ScheduleAdmin import (
    propagateClassSchedule,
    uploadSchedules,
    deleteClassSchedule,
    downloadClassSchedule,
    downloadClassAttendanceLog,
    addClassSchedule,
)
from P2MT_App.utilityfunctions import save_File
from datetime import datetime, date


def add_DailyAttendanceLog(student_id, absenceDate, attendanceCode, comment):
    print(student_id, attendanceCode, comment, absenceDate)
    dailyAttendanceLog = DailyAttendanceLog(
        absenceDate=absenceDate,
        attendanceCode=attendanceCode,
        comment=comment,
        staffID=5,
        student_id=student_id,
    )
    db.session.add(dailyAttendanceLog)
    db.session.commit()
    flash("Daily attendance log has been added!", "success")
    return


def add_InterventionLog(
    student_id, interventionType, interventionLevel, startDate, endDate, comment
):
    print(student_id, interventionType, interventionLevel, startDate, endDate)
    interventionLog = InterventionLog(
        intervention_id=interventionType,
        interventionLevel=interventionLevel,
        startDate=startDate,
        endDate=endDate,
        comment=comment,
        staffID=5,
        student_id=student_id,
    )
    db.session.add(interventionLog)
    db.session.commit()
    flash("Intervention log has been added!", "success")
    return


@app.route("/")
def home():
    return render_template("home.html", title="Home")


@app.route("/students", methods=["GET", "POST"])
def displayStudents():
    dailyAttendanceForm = addDailyAttendanceForm()
    interventionForm = addInterventionLogForm()
    interventionForm.interventionType.choices = getInterventionTypes()
    students = Student.query.order_by(
        Student.yearOfGraduation.asc(), Student.lastName.asc()
    )
    if "submitDailyAttendance" in request.form:
        if dailyAttendanceForm.validate_on_submit():
            print("Running dailyAttendanceForm")
            add_DailyAttendanceLog(
                int(dailyAttendanceForm.studentID.data),
                dailyAttendanceForm.absenceDate.data,
                dailyAttendanceForm.attendanceCode.data,
                dailyAttendanceForm.comment.data,
            )
            print(
                "===   Completed add_DailyAttendanceLog.  Redirecting to students   ===",
                datetime.now(),
                "   ===",
            )
            return redirect(url_for("displayStudents"))

    if "submitIntervention" in request.form:
        if interventionForm.validate_on_submit():
            print("Running interventionForm")
            add_InterventionLog(
                int(interventionForm.studentID.data),
                int(interventionForm.interventionType.data),
                int(interventionForm.interventionLevel.data),
                interventionForm.startDate.data,
                interventionForm.endDate.data,
                interventionForm.comment.data,
            )
            print(
                "===   Completed add_InterventionLog.  Redirecting to students   ===",
                datetime.now(),
                "   ===",
            )
            return redirect(url_for("displayStudents"))

    if request.method == "GET":
        return render_template(
            "students.html",
            title="Students",
            students=students,
            dailyAttendanceForm=dailyAttendanceForm,
            interventionForm=interventionForm,
        )


@app.route("/dailyattendancelog")
def displayDailyAttendanceLogs():
    DailyAttendanceLogs = DailyAttendanceLog.query.order_by(
        DailyAttendanceLog.absenceDate.desc()
    )
    return render_template(
        "dailyattendancelog.html",
        title="Daily Attendance Log",
        DailyAttendanceLogs=DailyAttendanceLogs,
    )


@app.route("/dailyattendancelog/<int:log_id>/delete", methods=["POST"])
def delete_DailyAttendanceLog(log_id):
    log = DailyAttendanceLog.query.get_or_404(log_id)
    db.session.delete(log)
    db.session.commit()
    flash("Daily attendance log has been deleted!", "success")
    return redirect(url_for("displayDailyAttendanceLogs"))


@app.route("/interventionlog")
def displayInterventionLogs():
    InterventionLogs = InterventionLog.query.order_by(InterventionLog.endDate.desc())
    return render_template(
        "interventionlog.html",
        title="Intervention Log",
        InterventionLogs=InterventionLogs,
    )


@app.route("/interventionlog/<int:log_id>/delete", methods=["POST"])
def delete_InterventionLog(log_id):
    log = InterventionLog.query.get_or_404(log_id)
    db.session.delete(log)
    db.session.commit()
    flash("Intervention log has been deleted!", "success")
    return redirect(url_for("displayInterventionLogs"))


@app.route("/masterschedule")
def displayMasterSchedule():
    ClassSchedules = ClassSchedule.query.order_by(
        ClassSchedule.chattStateANumber.desc()
    )
    return render_template(
        "masterschedule.html", title="Master Schedule", ClassSchedules=ClassSchedules,
    )


@app.route("/masterschedule/<int:log_id>/delete", methods=["POST"])
def delete_ClassSchedule(log_id):
    log = ClassSchedule.query.get_or_404(log_id)
    db.session.delete(log)
    db.session.commit()
    flash("Class schedule has been deleted!", "success")
    return redirect(url_for("displayMasterSchedule"))


@app.route("/scheduleadmin", methods=["GET", "POST"])
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


@app.route("/bootstraptest")
def displayBootstrapTest():
    DailyAttendanceLogs = DailyAttendanceLog.query.all()
    return render_template(
        "bootstraptest.html",
        title="Bootstrap Test",
        DailyAttendanceLogs=DailyAttendanceLogs,
    )

@app.route("/about")
def displayAbout():
    return render_template(
        "about.html",
        title="About"
    )


@app.route("/analytics")
def displayAnalyticsTest():
    return render_template("analytics.html")


@app.route("/sidebar")
def displaySidebar():
    return render_template("sidebar.html")


@app.route("/analytics2")
def displayAnalyticsTest2():
    return render_template("layout2.html")


@app.route("/classattendancelog", methods=["GET", "POST"])
def displayClassAttendanceLog():
    print("\n---THIS IS displayClassAttendanceLog()---")
    classAttendanceForm = updateClassAttendanceForm()
    classAttendanceForm.teacherName.choices = getTeachers()
    classAttendanceForm.className.choices = getClassNames()

    classDateTime = date.today()
    # classDateTime = datetime(
    #     datetime.today().year, datetime.today().month, datetime.today().day, 0, 0, 0, 0
    # )
    # print(
    #     "\nclassAttendanceForm.identifier.data = ", classAttendanceForm.identifier.data
    # )
    print(
        "classAttendanceForm.updateFiltersFlag.data =",
        classAttendanceForm.updateFiltersFlag.data,
    )

    print("request.method =", request.method)

    if classAttendanceForm.validate_on_submit():
        print(
            "classAttendanceForm.validate_on_submit() =",
            classAttendanceForm.validate_on_submit(),
        )
    print("classAttendanceForm.errors =", classAttendanceForm.errors)

    # if classAttendanceForm.identifier.data is None:
    if request.method == "GET":

        if classAttendanceForm.classDate.data:
            classDateTime = classAttendanceForm.classDate.data
            classAttendanceForm.classDate.default = classDateTime
        else:
            classDateTime = date.today()
            # classDateTime = datetime.now()
            # classDateTime = classDateTime.replace(
            #     hour=0, minute=0, second=0, microsecond=0
            # )
            classAttendanceForm.classDate.data = classDateTime
            # classAttendanceForm.classDate.data = classDateTime.date()

        classAttendanceForm.className.default = classAttendanceForm.className.data
        classAttendanceForm.teacherName.default = classAttendanceForm.teacherName.data
        classAttendanceForm.updateFiltersFlag.data = ""

    if classAttendanceForm.validate_on_submit():

        # Update default values for teacher name and class name
        classAttendanceForm.className.default = classAttendanceForm.className.data
        classAttendanceForm.teacherName.default = classAttendanceForm.teacherName.data

        # Format class date for compatibility with database
        classDate = classAttendanceForm.classDate.data
        classDateTime = classDate
        print(classDate, classDateTime)
        # classDateTime = datetime(
        #     classDate.year, classDate.month, classDate.day, 0, 0, 0, 0
        # )
        print(
            "classAttendanceForm.updateFiltersFlag.data =",
            classAttendanceForm.updateFiltersFlag.data,
        )

        # Update database with attendance updates
        if (
            classAttendanceForm.classMembers
            and classAttendanceForm.updateFiltersFlag.data != "updated"
        ):
            print("Class attendance submitted")
            print(len(classAttendanceForm.classMembers.data))
            for studentForm in classAttendanceForm.classMembers.data:
                if studentForm["updateFlag"] == "updated":
                    log_id = studentForm["log_id"]
                    print("log_id = ", log_id)
                    classAttendanceLog = ClassAttendanceLog.query.get_or_404(log_id)
                    classAttendanceLog.attendanceCode = studentForm["attendanceCode"]
                    classAttendanceLog.comment = studentForm["comment"]
                    db.session.commit()

        # Need to run the next statement [classAttendanceForm.process()]
        # or the updated values for the studentAttendanceForm won't display
        classAttendanceForm.process()

    # Retrive updated fixed-value attendance fields from database
    classAttendanceFixedFields = (
        ClassAttendanceLog.query.filter(ClassAttendanceLog.classDate == classDateTime)
        .join(ClassSchedule)
        .join(ClassSchedule.Student)
        .filter(
            ClassSchedule.teacherLastName == classAttendanceForm.teacherName.default
        )
        .filter(ClassSchedule.className == classAttendanceForm.className.default)
        .order_by(ClassSchedule.startTime)
        .order_by(ClassSchedule.className)
        .order_by(Student.lastName)
        .all()
    )

    # Retrieve updated student attendance fields from database
    for studentAttendance in classAttendanceFixedFields:
        studentAttendanceForm = updateStudentAttendanceForm()
        studentAttendanceForm.log_id = studentAttendance.id
        studentAttendanceForm.attendanceCode = studentAttendance.attendanceCode
        studentAttendanceForm.comment = studentAttendance.comment
        studentAttendanceForm.updateFlag = ""
        print(
            "ROSTER ",
            studentAttendanceForm.log_id,
            studentAttendance.ClassSchedule.className,
            studentAttendance.ClassSchedule.startTime,
            studentAttendance.ClassSchedule.endTime,
            studentAttendance.ClassSchedule.Student.firstName,
            studentAttendance.ClassSchedule.Student.lastName,
            studentAttendanceForm.attendanceCode,
            studentAttendanceForm.comment,
        )
        classAttendanceForm.classMembers.append_entry(studentAttendanceForm)

    # Reset the updateFiltersFlag before rendering page
    classAttendanceForm.updateFiltersFlag.data = ""

    print("Final before render_template")
    print(
        "classAttendanceForm.classDate.default =",
        classAttendanceForm.classDate.default,
    )
    print(
        "classAttendanceForm.classDate.data =", classAttendanceForm.classDate.data,
    )
    return render_template(
        "classattendancelog.html",
        title="Class Attendance Log",
        classAttendanceForm=classAttendanceForm,
        classAttendanceFixedFields=classAttendanceFixedFields,
    )

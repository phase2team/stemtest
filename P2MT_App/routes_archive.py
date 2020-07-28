@app.route("/classattendancelogtest", methods=["GET", "POST"])
def displayClassAttendanceLogTest():
    logFilters = classAttendanceLogFilters()
    logFilters.teacherName.choices = getTeachers()
    logFilters.className.choices = getClassNames()
    classDateTime = datetime(
        datetime.today().year, datetime.today().month, datetime.today().day, 0, 0, 0, 0
    )

    classAttendanceForm = updateClassAttendanceForm()
    if (
        classAttendanceForm.identifier.data == "classAttendanceForm"
        and classAttendanceForm.validate_on_submit()
    ):
        log_id = classAttendanceForm.classMembers.data[0]["log_id"]
        classAttendanceLog = ClassAttendanceLog.query.get_or_404(log_id)
        classAttendanceLog.attendanceCode = classAttendanceForm.classMembers.data[0][
            "attendanceCode"
        ]
        classAttendanceLog.comment = classAttendanceForm.classMembers.data[0]["comment"]
        db.session.commit()

    if logFilters.identifier.data == "logFilters":
        logFilters.classDate.default = logFilters.classDate.data
        classDate = logFilters.classDate.data
        logFilters.className.default = logFilters.className.data
        logFilters.teacherName.default = logFilters.teacherName.data

        # print(type(classDate))
        classDateTime = datetime(
            classDate.year, classDate.month, classDate.day, 0, 0, 0, 0
        )
        # print(type(classDate), classDateTime)
        # print(logFilters.className.data)
        # print(logFilters.teacherName.data)

        classAttendanceFixedFields = ClassAttendanceLog.query.filter(
            ClassAttendanceLog.classDate == classDateTime
        ).all()
        classAttendanceForm = updateClassAttendanceForm()
        for studentAttendance in ClassAttendanceLog.query.filter(
            ClassAttendanceLog.classDate == classDateTime
        ).all():
            studentAttendanceForm = updateStudentAttendanceForm()
            studentAttendanceForm.log_id = studentAttendance.id
            studentAttendanceForm.attendanceCode = studentAttendance.attendanceCode
            studentAttendanceForm.comment = studentAttendance.comment
            classAttendanceForm.classMembers.append_entry(studentAttendanceForm)
    else:
        # classDate = datetime(
        #     datetime.today().year, datetime.today().month, datetime.today().day
        # )

        classAttendanceFixedFields = ClassAttendanceLog.query.filter(
            ClassAttendanceLog.classDate == classDateTime
        ).all()
        # classAttendanceForm = updateClassAttendanceForm()

        for studentAttendance in ClassAttendanceLog.query.filter(
            ClassAttendanceLog.classDate == classDateTime
        ).all():
            studentAttendanceForm = updateStudentAttendanceForm()
            studentAttendanceForm.log_id = studentAttendance.id
            studentAttendanceForm.attendanceCode = studentAttendance.attendanceCode
            studentAttendanceForm.comment = studentAttendance.comment
            classAttendanceForm.classMembers.append_entry(studentAttendanceForm)

    return render_template(
        "classattendancelog.html",
        title="Class Attendance Log",
        classAttendanceForm=classAttendanceForm,
        classAttendanceFixedFields=classAttendanceFixedFields,
        logFilters=logFilters,
    )


@app.route("/classattendancelog", methods=["GET", "POST"])
def displayClassAttendanceLog():
    logFilters = classAttendanceLogFilters()
    logFilters.teacherName.choices = getTeachers()
    logFilters.className.choices = getClassNames()
    if logFilters.identifier.data == "logFilters" and logFilters.is_submitted():
        classDate = logFilters.classDate.data
        print(logFilters.className.data)
        print(logFilters.teacherName.data)
        # print("Log filters submitted")
        # print("logFilters.validate_on_submit = ", logFilters.validate_on_submit())
        # print("logFilters.errors =", logFilters.errors)
    else:
        classDate = datetime(
            datetime.today().year, datetime.today().month, datetime.today().day
        )
        # print("Log filters not submitted")
    print("classDate = ", classDate)
    classAttendanceFixedFields = ClassAttendanceLog.query.filter(
        ClassAttendanceLog.classDate == classDate
    ).all()
    classAttendanceForm = updateClassAttendanceForm()
    if request.method == "GET":
        for studentAttendance in ClassAttendanceLog.query.filter(
            ClassAttendanceLog.classDate == classDate
        ).all():
            studentAttendanceForm = updateStudentAttendanceForm()
            studentAttendanceForm.log_id = studentAttendance.id
            studentAttendanceForm.attendanceCode = studentAttendance.attendanceCode
            studentAttendanceForm.comment = studentAttendance.comment
            classAttendanceForm.classMembers.append_entry(studentAttendanceForm)
        return render_template(
            "classattendancelog.html",
            title="Class Attendance Log",
            classAttendanceForm=classAttendanceForm,
            classAttendanceFixedFields=classAttendanceFixedFields,
            logFilters=logFilters,
        )

    if request.method == "POST":

        if (
            classAttendanceForm.identifier.data == "classAttendanceForm"
            and classAttendanceForm.validate_on_submit()
        ):
            log_id = classAttendanceForm.classMembers.data[0]["log_id"]
            classAttendanceLog = ClassAttendanceLog.query.get_or_404(log_id)
            classAttendanceLog.attendanceCode = classAttendanceForm.classMembers.data[
                0
            ]["attendanceCode"]
            classAttendanceLog.comment = classAttendanceForm.classMembers.data[0][
                "comment"
            ]
            db.session.commit()
        # print(
        #     "classAttendanceForm.validate_on_submit =",
        #     classAttendanceForm.validate_on_submit(),
        # )
        # print("classAttendanceForm.errors =", classAttendanceForm.errors)
        flash("Class attendance log has been updated!", "success")
        return redirect(url_for("displayClassAttendanceLog"))


@app.route("/classattendancelog/<int:id>/update", methods=["POST"])
def update_ClassAttendanceLog(id):
    print("update_ClassAttendanceLog triggered")
    print("ID =", id)
    classAttendanceLog = ClassAttendanceLog.query.get_or_404(id)
    classAttendanceForm = updateClassAttendanceForm()
    if classAttendanceForm.is_submitted():
        classAttendanceLog.attendanceCode = classAttendanceForm.classMembers.data[0][
            "attendanceCode"
        ]
        classAttendanceLog.comment = classAttendanceForm.classMembers.data[0]["comment"]
        db.session.commit()
    flash("Class attendance log has been updated!", "success")
    return redirect(url_for("displayClassAttendanceLog"))

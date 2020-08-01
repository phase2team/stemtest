@app.route("/classattendancelognew", methods=["GET", "POST"])
def displayClassAttendanceLogNew():
    classAttendanceForm = updateClassAttendanceForm()
    classAttendanceForm.teacherName.choices = getTeachers()
    classAttendanceForm.className.choices = getClassNames()

    classDateTime = datetime(
        datetime.today().year, datetime.today().month, datetime.today().day, 0, 0, 0, 0
    )
    print(
        "\nclassAttendanceForm.identifier.data = ", classAttendanceForm.identifier.data
    )
    # if request.method == "POST":

    if request.method == "POST":
        print("request.form =", request.form)

    # if classAttendanceForm.validate_on_submit():
    #     print("classAttendanceForm.validate_on_submit() =", classAttendanceForm.validate_on_submit())
    # print("classAttendanceForm.errors =", classAttendanceForm.errors)

    if (
        classAttendanceForm.identifier.data == "classAttendanceForm"
        and classAttendanceForm.is_submitted()
    ):

        log_id = classAttendanceForm.classMembers.data[0]["log_id"]
        classAttendanceLog = ClassAttendanceLog.query.get_or_404(log_id)
        classAttendanceLog.attendanceCode = classAttendanceForm.classMembers.data[0][
            "attendanceCode"
        ]
        classAttendanceLog.comment = classAttendanceForm.classMembers.data[0]["comment"]
        db.session.commit()

        print(
            "CAF log filter data:",
            classAttendanceForm.classDate.data,
            classAttendanceForm.className.data,
            classAttendanceForm.teacherName.data,
        )
        parsedDate = datetime.strptime(
            classAttendanceForm.classMembers.data[0]["classDate"], "%Y-%m-%d"
        )
        print(
            "CAF classAttendanceFormLogFilters data:",
            classAttendanceForm.classMembers.data[0]["className"],
            classAttendanceForm.classMembers.data[0]["teacherName"],
            classAttendanceForm.classMembers.data[0]["classDate"],
            parsedDate,
        )
        logFilterData = classAttendanceForm.classMembers.data
        className = logFilterData[0]["className"]
        teacherName = logFilterData[0]["teacherName"]
        classDate = datetime.strptime(logFilterData[0]["classDate"], "%Y-%m-%d")

        # classAttendanceForm = updateClassAttendanceForm()
        # classAttendanceForm.teacherName.choices = getTeachers()
        # classAttendanceForm.className.choices = getClassNames()

        classAttendanceForm.className.default = className
        classAttendanceForm.teacherName.default = teacherName
        classAttendanceForm.classDate.default = classDate

        # classAttendanceForm.className.default = classAttendanceForm.classMembers.data[
        #     0
        # ]["className"]

        # classAttendanceForm.teacherName.default = classAttendanceForm.classMembers.data[
        #     0
        # ]["teacherName"]

        # classAttendanceForm.classDate.default = datetime.strptime(
        #     classAttendanceForm.classMembers.data[0]["classDate"], "%Y-%m-%d"
        # )
        # classAttendanceForm.process()

        print(
            "CAF log filter default:",
            classAttendanceForm.classDate.default,
            classAttendanceForm.className.default,
            classAttendanceForm.teacherName.default,
        )

        classAttendanceForm.process()

        classAttendanceFixedFields = ClassAttendanceLog.query.filter(
            ClassAttendanceLog.classDate == parsedDate
        ).all()
        # classAttendanceForm = updateClassAttendanceForm()

        for studentAttendance in ClassAttendanceLog.query.filter(
            ClassAttendanceLog.classDate == parsedDate
        ).all():
            studentAttendanceForm = updateStudentAttendanceForm()
            studentAttendanceForm.log_id = studentAttendance.id
            studentAttendanceForm.attendanceCode = studentAttendance.attendanceCode
            studentAttendanceForm.comment = studentAttendance.comment
            studentAttendanceForm.teacherName = ""
            studentAttendanceForm.className = ""
            studentAttendanceForm.classDate = ""
            # studentAttendanceForm.process()
            classAttendanceForm.classMembers.append_entry(studentAttendanceForm)
            print(
                "SAF ",
                studentAttendanceForm.log_id,
                studentAttendanceForm.attendanceCode,
                studentAttendanceForm.comment,
            )
        print("classAttendanceForm =", classAttendanceForm)

    elif classAttendanceForm.identifier.data == "logFilters":
        print(
            "LF log filter data:",
            classAttendanceForm.classDate.data,
            classAttendanceForm.className.data,
            classAttendanceForm.teacherName.data,
        )

        classAttendanceForm.classDate.default = classAttendanceForm.classDate.data
        classDate = classAttendanceForm.classDate.data
        classAttendanceForm.className.default = classAttendanceForm.className.data
        classAttendanceForm.teacherName.default = classAttendanceForm.teacherName.data

        print(
            "LF log filter default:",
            classAttendanceForm.classDate.default,
            classAttendanceForm.className.default,
            classAttendanceForm.teacherName.default,
        )

        print(
            "LF log filter choices:",
            classAttendanceForm.className.choices,
            classAttendanceForm.teacherName.choices,
        )

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
        # classAttendanceForm = updateClassAttendanceForm()
        for studentAttendance in ClassAttendanceLog.query.filter(
            ClassAttendanceLog.classDate == classDateTime
        ).all():
            studentAttendanceForm = updateStudentAttendanceForm()
            studentAttendanceForm.log_id = studentAttendance.id
            studentAttendanceForm.attendanceCode = studentAttendance.attendanceCode
            studentAttendanceForm.comment = studentAttendance.comment
            studentAttendanceForm.teacherName = ""
            studentAttendanceForm.className = ""
            studentAttendanceForm.classDate = ""
            classAttendanceForm.classMembers.append_entry(studentAttendanceForm)

        print(
            "LF log filter default:",
            classAttendanceForm.classDate.default,
            classAttendanceForm.className.default,
            classAttendanceForm.teacherName.default,
        )

        print(
            "LF log filter choices:",
            classAttendanceForm.className.choices,
            classAttendanceForm.teacherName.choices,
        )
    elif classAttendanceForm.identifier.data is None:
        print(
            "classAttendanceForm.identifier.data =", classAttendanceForm.identifier.data
        )
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
            studentAttendanceForm.teacherName = ""
            studentAttendanceForm.className = ""
            studentAttendanceForm.classDate = ""
            classAttendanceForm.classMembers.append_entry(studentAttendanceForm)

        print(
            "NONE log filter default:",
            classAttendanceForm.classDate.default,
            classAttendanceForm.className.default,
            classAttendanceForm.teacherName.default,
        )
        print(
            "NONE log filter choices:",
            classAttendanceForm.className.choices,
            classAttendanceForm.teacherName.choices,
        )
    print("Final before render_template")
    return render_template(
        "classattendancelog.html",
        title="Class Attendance Log",
        classAttendanceForm=classAttendanceForm,
        classAttendanceFixedFields=classAttendanceFixedFields,
    )


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

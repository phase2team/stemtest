from flask import flash
from P2MT_App import db
from P2MT_App.models import Student, FacultyAndStaff, Parents
from datetime import datetime, date, time
from P2MT_App.main.utilityfunctions import printLogEntry
import csv


# ###################
#    Student Info   #
# ###################

#  Add student info to database
def addStudentToDatabase(
    chattStateANumber,
    firstName,
    lastName,
    email,
    house,
    yearOfGraduation,
    googleCalendarId,
):
    printLogEntry("addStudentToDatabase() function called")
    # Only add the student if chattStateANumber is not already in the database
    if len(Student.query.filter_by(chattStateANumber=chattStateANumber).all()) == 0:
        student = Student(
            chattStateANumber=chattStateANumber,
            firstName=firstName,
            lastName=lastName,
            email=email,
            house=house,
            yearOfGraduation=int(yearOfGraduation),
            googleCalendarId=googleCalendarId,
        )
        print(student)
        db.session.add(student)
        db.session.commit()
    else:
        print("Student with chattStateANumber =", chattStateANumber, "already exists")
    return


def uploadStudentList(fname):
    printLogEntry("uploadStudentList() function called")
    csvFile = open(fname, "r")
    importCSV = csv.reader(csvFile)
    for row in importCSV:
        # Skip the first row if it has header row data
        if "Chatt_State_A_Number" in row:
            continue
        print("row=", row)
        chattStateANumber = row[0].strip()
        firstName = row[1].strip()
        lastName = row[2].strip()
        email = row[3].strip()
        yearOfGraduation = int(row[4].strip())
        house = row[5].strip()
        googleCalendarId = row[6].strip()
        addStudentToDatabase(
            chattStateANumber,
            firstName,
            lastName,
            email,
            house,
            yearOfGraduation,
            googleCalendarId,
        )
    return


def deleteStudent(chattStateANumber):
    printLogEntry("deleteStudent() function called")
    student = Student.query.filter_by(chattStateANumber=chattStateANumber).first()
    firstName = student.firstName
    lastName = student.lastName
    db.session.delete(student)
    db.session.commit()
    print("Student deleted from P2MT database:", chattStateANumber, firstName, lastName)
    flash("Student has been deleted!", "success")
    return


def downloadStudentListTemplate():
    printLogEntry("downloadStudentListTemplate() function called")
    # Create a CSV output file
    output_file_path = os.path.join(current_app.root_path, "static/download")
    csvFilename = output_file_path + "/" + "student_list_template.csv"
    csvOutputFile = open(csvFilename, "w")
    # Write header row for CSV file
    csvOutputWriter = csv.writer(
        csvOutputFile, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
    )
    csvOutputWriter.writerow(
        [
            "Chatt_State_A_Number",
            "First_Name",
            "Last_Name",
            "Student_Email",
            "Year_of_Graduation",
            "House",
            "googleCalendarID",
        ]
    )
    return send_file(csvFilename, as_attachment=True, cache_timeout=0)


def downloadStudentList():
    printLogEntry("downloadStudentList() function called")
    # Create a CSV output file and append with a timestamp
    output_file_path = os.path.join(current_app.root_path, "static/download")
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    csvFilename = output_file_path + "/" + "class_schedule_" + timestamp + ".csv"
    csvOutputFile = open(csvFilename, "w")
    # Write header row for CSV file
    csvHeaderRow = "year,semester,Chatt_State_A_Number,CSname,firstName,lastName,HSclass,campus,courseNumber,courseName,sectionID,teacher,online,indStudy,days,times,startTime,endTime,comment,googleCalendarEventID\n"
    csvOutputFile.write(csvHeaderRow)
    csvOutputFileRowCount = 0
    # Query the ClassSchedule with a join to include student information
    ClassSchedules = ClassSchedule.query.filter(
        ClassSchedule.schoolYear == schoolYear, ClassSchedule.semester == semester
    ).order_by(ClassSchedule.chattStateANumber.desc())
    # Process each record in the query and write to the output file
    for classSchedule in ClassSchedules:
        chattStateANumber = classSchedule.chattStateANumber
        lastName = classSchedule.Student.lastName
        firstName = classSchedule.Student.firstName
        CSname = lastName + " " + firstName
        HSclass = classSchedule.Student.yearOfGraduation
        campus = classSchedule.campus
        courseNumber = ""
        courseName = classSchedule.className
        sectionID = ""
        teacher = classSchedule.teacherLastName
        online = classSchedule.online
        if online:
            online = "1"
        else:
            online = "0"
        indStudy = classSchedule.indStudy
        if indStudy:
            indStudy = "1"
        else:
            indStudy = "0"
        days = classSchedule.classDays
        startTime = classSchedule.startTime
        endTime = classSchedule.endTime
        comment = classSchedule.comment
        googleCalendarEventID = classSchedule.googleCalendarEventID

        csvRowPrefix = [
            str(schoolYear),
            semester,
            chattStateANumber,
            CSname,
            firstName,
            lastName,
            str(HSclass),
        ]

        csvRow = csvRowPrefix + [
            campus,
            courseNumber,
            courseName,
            str(sectionID),
            teacher,
            online,
            indStudy,
            days,
            startTime.strftime("%-I:%M") + " - " + endTime.strftime("%-I:%M"),
            startTime.strftime("%-I:%M %p"),
            endTime.strftime("%-I:%M %p"),
            comment,
            googleCalendarEventID,
        ]
        csvElementCounter = 1
        for element in csvRow:
            if element is None:
                element = ""
            if csvElementCounter < len(csvRow):
                csvOutputFile.write(element + ",")
                csvElementCounter += 1
            else:
                csvOutputFile.write(element + "\n")
        csvOutputFileRowCount = csvOutputFileRowCount + 1
    csvOutputFile.close()
    return send_file(csvFilename, as_attachment=True, cache_timeout=0)


# ###################
#    Staff Info     #
# ###################

# Add staff to database
def addStaffToDatabase(
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
):
    printLogEntry("addStaffToDatabase() function called")
    # Only add the staff member if the name is not already in the database
    if (
        len(
            FacultyAndStaff.query.filter_by(
                firstName=firstName, lastName=lastName
            ).all()
        )
        == 0
    ):
        # Set empty strings to None (i.e. Null) for better data type management in database
        if len(phoneNumber) == 0:
            phoneNumber = None
        if len(chattStateANumber) == 0:
            chattStateANumber = None
        if len(myersBriggs) == 0:
            myersBriggs = None
        if len(house) == 0:
            house = None
        if len(twitterAccount) == 0:
            twitterAccount = None
        if len(houseGrade) == 0:
            houseGrade = None
        # Convert houseGrade from string to integer as required by database typing
        if isinstance(houseGrade, str):
            houseGrade = int(houseGrade)
        staff = FacultyAndStaff(
            firstName=firstName,
            lastName=lastName,
            position=position,
            email=email,
            phoneNumber=phoneNumber,
            chattStateANumber=chattStateANumber,
            myersBrigg=myersBriggs,
            house=house,
            houseGrade=houseGrade,
            twitterAccount=twitterAccount,
        )
        print(staff)
        db.session.add(staff)
        db.session.commit()
    else:
        print("Staff member", firstName, lastName, "already exists")
    return


def uploadStaffList(fname):
    printLogEntry("uploadStaffList() function called")
    csvFile = open(fname, "r")
    importCSV = csv.reader(csvFile)
    for row in importCSV:
        # Skip the first row if it has header row data
        if "chattStateANumber" in row:
            continue
        print("row=", row)
        firstName = row[0].strip()
        lastName = row[1].strip()
        position = row[2].strip()
        email = row[3].strip()
        phoneNumber = row[4].strip()
        chattStateANumber = row[5].strip()
        myersBriggs = row[6].strip()
        house = row[7].strip()
        houseGrade = row[8].strip()
        # Set houseGrade=0 if undefined to avoid errors with integer conversions
        if len(houseGrade) > 0:
            houseGrade = int(houseGrade)
        else:
            houseGrade = 0
        twitterAccount = row[9].strip()
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
    return


def deleteStaff(log_id):
    printLogEntry("deleteStaff() function called")
    staff = FacultyAndStaff.query.filter_by(id=log_id).first()
    firstName = staff.firstName
    lastName = staff.lastName
    db.session.delete(staff)
    db.session.commit()
    print("Staff deleted from P2MT database:", firstName, lastName)
    flash("Staff member has been deleted!", "success")
    return


# ###################
#    Parent Info    #
# ###################


def addParentsToDatabase(
    chattStateANumber,
    guardianship,
    motherName,
    motherEmail,
    motherHomePhone,
    motherDayPhone,
    fatherName,
    fatherEmail,
    fatherHomePhone,
    fatherDayPhone,
    guardianEmail,
    comment,
):
    printLogEntry("addParentToDatabase() function called")
    # Only add the parent info if chattStateANumber is not already in the database
    if len(Parents.query.filter_by(chattStateANumber=chattStateANumber).all()) == 0:
        if len(Student.query.filter_by(chattStateANumber=chattStateANumber).all()) != 0:
            parents = Parents(
                chattStateANumber=chattStateANumber,
                guardianship=guardianship,
                motherName=motherName,
                motherEmail=motherEmail,
                motherHomePhone=motherHomePhone,
                motherDayPhone=motherDayPhone,
                fatherName=fatherName,
                fatherEmail=fatherEmail,
                fatherHomePhone=fatherHomePhone,
                fatherDayPhone=fatherDayPhone,
                guardianEmail=guardianEmail,
                comment=comment,
            )
            print(parents)
            db.session.add(parents)
            db.session.commit()
            print("Adding parents for chattStateANumber =", chattStateANumber)
        else:
            print("No student with chattStateANumber =", chattStateANumber, " exists")
    else:
        # If parent reccord exists, update the record with the new information
        print("Updating parents for chattStateANumber =", chattStateANumber)
        parents = Parents.query.filter_by(chattStateANumber=chattStateANumber).first()
        parents.chattStateANumber = chattStateANumber
        parents.guardianship = guardianship
        parents.motherName = motherName
        parents.motherEmail = motherEmail
        parents.motherHomePhone = motherHomePhone
        parents.motherDayPhone = motherDayPhone
        parents.fatherName = fatherName
        parents.fatherEmail = fatherEmail
        parents.fatherHomePhone = fatherHomePhone
        parents.fatherDayPhone = fatherDayPhone
        parents.guardianEmail = guardianEmail
        parents.comment = None
        db.session.commit()
    return


def uploadParentsList(fname):
    printLogEntry("uploadParentList() function called")
    csvFile = open(fname, "r")
    importCSV = csv.reader(csvFile)
    for row in importCSV:
        # Skip the first row if it has header row data
        if "Chatt_State_A_Number" in row:
            continue
        print("row=", row)
        chattStateANumber = row[0].strip()
        guardianship = row[1].strip()
        motherName = row[2].strip()
        motherEmail = row[3].strip()
        motherHomePhone = row[4].strip()
        motherDayPhone = row[5].strip()
        fatherName = row[6].strip()
        fatherEmail = row[7].strip()
        fatherHomePhone = row[8].strip()
        fatherDayPhone = row[9].strip()
        guardianEmail = row[10].strip()
        comment = None
        addParentsToDatabase(
            chattStateANumber,
            guardianship,
            motherName,
            motherEmail,
            motherHomePhone,
            motherDayPhone,
            fatherName,
            fatherEmail,
            fatherHomePhone,
            fatherDayPhone,
            guardianEmail,
            comment,
        )
    return


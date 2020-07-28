from P2MT_App import db
from P2MT_App.models import (
    Student,
    ClassSchedule,
    DailyAttendanceLog,
    FacultyAndStaff,
    InterventionLog,
    InterventionType,
    ClassAttendanceLog,
)
from datetime import datetime

print("\n=========", __file__, "=========\n")

# students = {
#     "student1": {
#         "chattStateANumber": "A1234",
#         "firstName": "Bugsy",
#         "lastName": "Tester",
#         "email": "testy@students.hcde.org",
#         "house": "Staupers",
#         "yearOfGraduation": 2021,
#     },
#     "student2": {
#         "chattStateANumber": "A12345",
#         "firstName": "Duke",
#         "lastName": "Tester",
#         "email": "testy@students.hcde.org",
#         "house": "Staupers",
#         "yearOfGraduation": 2021,
#     },
# }
# print(students)


def test_importStudents():
    importCSV = open("students_export.csv", "r")
    for row in importCSV:
        print("row=", row)
        column = row.split(",")
        print("column=", column)
        chattStateANumber = column[0].strip()
        firstName = column[1].strip()
        lastName = column[2].strip()
        email = column[3].strip()
        yearOfGraduation = column[4].strip()
        house = column[5].strip()
        googleCalendarId = column[6].strip()
        test_addStudent(
            chattStateANumber,
            firstName,
            lastName,
            email,
            house,
            yearOfGraduation,
            googleCalendarId,
        )


def test_importGoogleCalendarIds():
    importCSV = open("Schedules for Google Calendar - Students.csv", "r")
    for row in importCSV:
        print("row=", row)
        column = row.split(",")
        chattStateANumber = column[0].strip()
        googleCalendarId = column[1].strip()
        print(chattStateANumber, googleCalendarId)
        test_addGoogleCalendarId(chattStateANumber, googleCalendarId)


def test_importSchedules(fname):
    importCSV = open(fname, "r")
    for row in importCSV:
        print("row=", row)
        column = row.split(",")
        print("column=", column)
        schoolYear = column[0].strip()
        if schoolYear == "year":
            continue
        semester = column[1].strip()
        chattStateANumber = column[2].strip()
        campus = column[7].strip()
        className = column[9].strip()
        staffID = 1
        online = column[12].strip()
        if online == "1":
            online = True
        else:
            online = False
        indStudy = column[13].strip()
        if indStudy == "1":
            indStudy = True
        else:
            indStudy = False
        classDays = column[14].strip()
        print(column[16].strip())
        startTime = datetime.strptime(column[16].strip(), "%I:%M %p")
        endTime = datetime.strptime(column[17].strip(), "%I:%M %p")
        comment = column[18].strip()
        googleCalendarEventID = ""
        test_addClassSchedule(
            schoolYear,
            semester,
            chattStateANumber,
            campus,
            className,
            staffID,
            online,
            indStudy,
            classDays,
            startTime,
            endTime,
            comment,
            googleCalendarEventID,
        )


#  Add googleCalendarId to a student record
def test_addGoogleCalendarId(chattStateANumber, googleCalendarId):
    student = Student.query.filter_by(chattStateANumber=chattStateANumber).first()
    if student:
        print(student)
        student.googleCalendarId = googleCalendarId
        db.session.commit()
    else:
        print("Unable to update googleCalendarId for", chattStateANumber)
    return


# test_importGoogleCalendarIds()


#  Add student info to database
def test_addStudent(
    chattStateANumber,
    firstName,
    lastName,
    email,
    house,
    yearOfGraduation,
    googleCalendarId,
):
    if len(Student.query.filter_by(chattStateANumber=chattStateANumber).all()) == 0:
        student1 = Student(
            chattStateANumber=chattStateANumber,
            firstName=firstName,
            lastName=lastName,
            email=email,
            house=house,
            yearOfGraduation=yearOfGraduation,
            googleCalendarId=googleCalendarId,
        )
        print(student1)
        db.session.add(student1)
        db.session.commit()
    else:
        print("Student with chattStateANumber =", chattStateANumber, "already exists")


# # print(Student.query.all())

# Add class schedule information to database
def test_addClassSchedule(
    schoolYear,
    semester,
    chattStateANumber,
    campus,
    className,
    staffID,
    online,
    indStudy,
    classDays,
    startTime,
    endTime,
    comment,
    googleCalendarEventID,
):
    classSchedule1 = ClassSchedule(
        schoolYear=schoolYear,
        semester=semester,
        chattStateANumber=chattStateANumber,
        campus=campus,
        className=className,
        staffID=staffID,
        online=online,
        indStudy=indStudy,
        classDays=classDays,
        startTime=startTime,
        endTime=endTime,
        comment=comment,
        googleCalendarEventID=googleCalendarEventID,
    )
    print(classSchedule1)
    db.session.add(classSchedule1)
    db.session.commit()


# Add staff to database
def test_addStaff(firstName, lastName, position, email, phoneNumber, chattStateANumber):
    staff1 = FacultyAndStaff(
        firstName=firstName,
        lastName=lastName,
        position=position,
        email=email,
        phoneNumber=phoneNumber,
        chattStateANumber=chattStateANumber,
    )
    print(staff1)
    db.session.add(staff1)
    db.session.commit()


# Add daily attendance log to database
def test_addDailyAttendanceLog():
    dailyAttendanceLog1 = DailyAttendanceLog(
        absenceDate=datetime(2020, 9, 15),
        attendanceCode="E",
        comment="Sick",
        staffID=2,
        student_id=1,
    )
    print(dailyAttendanceLog1)
    db.session.add(dailyAttendanceLog1)
    db.session.commit()


def test_addInterventionType(interventionType, maxLevel):
    interventionType = InterventionType(
        interventionType=interventionType, maxLevel=maxLevel
    )
    print(interventionType)
    db.session.add(interventionType)
    db.session.commit()


def test_addInterventionLog(
    student_id, interventionType, interventionLevel, startDate, endDate, comment
):
    interventionLog = InterventionLog(
        intervention_id=interventionType,
        interventionLevel=interventionLevel,
        startDate=startDate,
        endDate=endDate,
        comment=comment,
        staffID=2,
        student_id=student_id,
    )
    print(interventionLog)
    db.session.add(interventionLog)
    db.session.commit()


def test_addClassAttendanceLog(
    classSchedule_id, classDate, attendanceCode, comment, assignTmi
):
    classAttendanceLog = ClassAttendanceLog(
        classSchedule_id=classSchedule_id,
        classDate=classDate,
        attendanceCode=attendanceCode,
        comment=comment,
        assignTmi=assignTmi,
    )
    print(classAttendanceLog)
    db.session.add(classAttendanceLog)
    db.session.commit()


db.create_all()
# test_addInterventionType("Conduct Behavior", 6)
# test_addInterventionType("Academic Behavior", 4)
# test_addInterventionType("Attendance", 3)
# test_addInterventionType("Dress Code", 6)
# test_addInterventionType("Bullying / Harassment", 4)
# test_addInterventionType("Extended Remediation", 1)

# test_addInterventionLog(1, 1, 1, datetime(2020, 1, 1), datetime(2020, 1, 15), "comment")
# test_addStudent(
#     "A12345678", "Testy", "Tester", "tester@students.hcde.org", "Staupers", 2021
# )
# test_addStudent(
#     "A87654321", "Max", "Tester", "tester@students.hcde.org", "Einstein", 2021
# )
# test_addStudent(
#     "A86427531", "Bugsy", "Tester", "tester@students.hcde.org", "Tesla", 2021
# )
# test_addStudent(
#     "A75318642", "Jane", "Tester", "tester@students.hcde.org", "Mirzakhani", 2021
# )
# test_addStaff("Ken", "Kranz", "Guru", "guru@demo.com", "423-555-1212", "A1")
# test_addStaff(
#     "Andy", "Able", "Gym Teacher", "seamstress@demo.com", "423-555-1212", "A3"
# )

# test_addClassSchedule(
#     "English",
#     datetime(2020, 8, 15, 9, 30, 0),
#     datetime(2020, 8, 15, 10, 30, 0),
#     "MW",
#     1,
# )
# test_addClassSchedule(
#     "Science",
#     datetime(2020, 8, 15, 9, 30, 0),
#     datetime(2020, 8, 15, 10, 30, 0),
#     "MW",
#     1,
# )
# test_addClassSchedule(
#     "Math", datetime(2020, 8, 15, 9, 30, 0), datetime(2020, 8, 15, 10, 30, 0), "MW", 2
# )
# test_addClassSchedule(
#     "Art", datetime(2020, 8, 15, 9, 30, 0), datetime(2020, 8, 15, 10, 30, 0), "MW", 2
# )
# test_importStudents()

# test_importSchedules("FET Python Testing - outputFile.csv")

# test_addClassAttendanceLog(24, datetime(2020, 7, 25), "T", "late", False)
# test_addClassAttendanceLog(25, datetime(2020, 7, 25), "T", "late", False)
# test_addClassAttendanceLog(26, datetime(2020, 7, 25), "T", "late", False)
# test_addClassAttendanceLog(27, datetime(2020, 7, 25), "T", "late", False)


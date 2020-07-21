from P2MT_App import db
from P2MT_App.models import (
    Student,
    ClassSchedule,
    DailyAttendanceLog,
    FacultyAndStaff,
    InterventionLog,
    InterventionType,
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
        test_addStudent(
            chattStateANumber, firstName, lastName, email, house, yearOfGraduation
        )


#  Add student info to database
def test_addStudent(
    chattStateANumber, firstName, lastName, email, house, yearOfGraduation
):
    if len(Student.query.filter_by(chattStateANumber=chattStateANumber).all()) == 0:
        student1 = Student(
            chattStateANumber=chattStateANumber,
            firstName=firstName,
            lastName=lastName,
            email=email,
            house=house,
            yearOfGraduation=yearOfGraduation,
        )
        print(student1)
        db.session.add(student1)
        db.session.commit()
    else:
        print("Student with chattStateANumber =", chattStateANumber, "already exists")


# # print(Student.query.all())

# Add class schedule information to database
def test_addClassSchedule(className, startTime, endTime, classDays, student_id):
    classSchedule1 = ClassSchedule(
        className=className,
        startTime=startTime,
        endTime=endTime,
        classDays=classDays,
        student_id=student_id,
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


# db.create_all()
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
#     "Betsy", "Ross", "Sewing Teacher", "seamstress@demo.com", "423-555-1212", "A2"
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

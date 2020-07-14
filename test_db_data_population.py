from P2MT_App import db
from P2MT_App.models import Student, ClassSchedule, DailyAttendanceLog, FacultyAndStaff
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

#  Add student info to database
chattStateANumber = "A12"
if len(Student.query.filter_by(chattStateANumber=chattStateANumber).all()) == 0:
    student1 = Student(
        chattStateANumber=chattStateANumber,
        firstName="Max",
        lastName="Tester",
        email="testy@students.hcde.org",
        house="Staupers",
        yearOfGraduation=2021,
    )
    print(student1)
    db.session.add(student1)
    db.session.commit()
else:
    print("Student with chattStateANumber =", chattStateANumber, "already exists")

# # print(Student.query.all())

# Add class schedule information to database
# classSchedule1 = ClassSchedule(
#     className="English",
#     startTime=datetime(2020, 8, 15, 9, 30, 0),
#     endTime=datetime(2020, 8, 15, 10, 30, 0),
#     classDays="MW",
#     student_id=1,
# )
# print(classSchedule1)
# db.session.add(classSchedule1)
# db.session.commit()

# Add staff to database
# staff1 = FacultyAndStaff(
#     firstName="Betsy",
#     lastName="Ross",
#     position="Art Teacher",
#     email="test@demo.com",
#     phoneNumber="423-555-1212",
#     chattStateANumber="A2",
# )
# print(staff1)
# db.session.add(staff1)
# db.session.commit()

# dailyAttendanceLog1 = DailyAttendanceLog(
#     absenceDate=datetime(2020, 9, 20),
#     attendanceCode="E",
#     comment="Sick",
#     staffID=2,
#     student_id=1,
# )
# print(dailyAttendanceLog1)
# db.session.add(dailyAttendanceLog1)
# db.session.commit()

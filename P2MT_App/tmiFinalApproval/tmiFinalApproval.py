from P2MT_App import db
from datetime import date
from sqlalchemy import func
from P2MT_App.models import ClassAttendanceLog, InterventionLog, ClassSchedule, Student
from P2MT_App.main.utilityfunctions import printLogEntry


def findTardyClassesForStudent(startTmiPeriod, endTmiPeriod, chattStateANumber):
    tardyClasses = (
        db.session.query(ClassAttendanceLog.id)
        .join(ClassSchedule)
        .filter(
            ClassAttendanceLog.classDate >= startTmiPeriod,
            ClassAttendanceLog.classDate <= endTmiPeriod,
            ClassAttendanceLog.attendanceCode == "T",
            ClassSchedule.chattStateANumber == chattStateANumber,
        )
    ).all()
    return tardyClasses


def updateTmiForClasses(tardyClassesIds, assignTmi):
    for tardyClassId in tardyClassesIds:
        log = ClassAttendanceLog.query.get(tardyClassId)
        log.assignTmi = assignTmi
        # print("db.session.dirty =", db.session.dirty)
    return


def assignTmiForTardy(startTmiPeriod, endTmiPeriod):
    # print("db.session.dirty =", db.session.dirty)
    tardyStudents = (
        db.session.query(
            Student.chattStateANumber,
            Student.firstName,
            Student.lastName,
            func.count(Student.chattStateANumber),
        )
        .select_from(Student)
        .join(ClassSchedule)
        .join(ClassSchedule.ClassAttendanceLog)
        .filter(
            ClassAttendanceLog.classDate >= startTmiPeriod,
            ClassAttendanceLog.classDate <= endTmiPeriod,
            ClassAttendanceLog.attendanceCode == "T",
        )
        .group_by(Student.chattStateANumber)
    ).all()

    # print(str(tardyStudents))
    print(tardyStudents)
    for tardyStudent in tardyStudents:
        chattStateANumber = tardyStudent[0]
        firstName = tardyStudent[1]
        lastName = tardyStudent[2]
        tardyCount = tardyStudent[3]
        tardyClassesIds = findTardyClassesForStudent(
            startTmiPeriod, endTmiPeriod, chattStateANumber
        )
        if tardyCount >= 3:
            print("assign Tardy TMI for", chattStateANumber, firstName, lastName)
            updateTmiForClasses(tardyClassesIds, assignTmi=True)
        else:
            print("remove Tardy TMI for", chattStateANumber, firstName, lastName)
            updateTmiForClasses(tardyClassesIds, assignTmi=False)
    return


def getTmiInterventions(tmiDate):
    tmiInterventionLog = InterventionLog.query.filter(
        InterventionLog.student_id == tmiDate
    ).all()

    return


def calculateTmi(classAttendanceLogForTmiCalculations):
    printLogEntry("calculateTMI() function called")
    tmiMinutes = 0
    tardyFlag = False
    classAttendanceLogIDList = []
    for log in classAttendanceLogForTmiCalculations:
        attendanceCode = log.attendanceCode
        classAttendanceLogID = log.id
        className = log.ClassSchedule.className
        classDate = log.classDate
        teacherLastName = log.ClassSchedule.teacherLastName
        chattStateANumber = log.ClassSchedule.chattStateANumber
        if attendanceCode == "T" and tardyFlag == True:
            classAttendanceArrayItem = {
                "Date": classDate,
                "Class": className,
                "AttendanceType": "Tardy",
                "Teacher": teacherLastName,
            }
            classAttendanceLogIDList.append(classAttendanceArrayItem)

        elif attendanceCode == "T" and tardyFlag == False:
            tmiMinutes = tmiMinutes + 90
            tardyFlag = True
            classAttendanceArrayItem = {
                "Date": classDate,
                "Class": className,
                "AttendanceType": "Tardy",
                "Teacher": teacherLastName,
            }
            classAttendanceLogIDList.append(classAttendanceArrayItem)

        elif attendanceCode == "E":
            tmiMinutes = tmiMinutes + 120
            classAttendanceArrayItem = {
                "Date": classDate,
                "Class": className,
                "AttendanceType": "Excused Absence (But Missing Work)",
                "Teacher": teacherLastName,
            }
            classAttendanceLogIDList.append(classAttendanceArrayItem)

        elif attendanceCode == "U":
            tmiMinutes = tmiMinutes + 120
            classAttendanceArrayItem = {
                "Date": classDate,
                "Class": className,
                "AttendanceType": "Unexcused Absence",
                "Teacher": teacherLastName,
            }
            classAttendanceLogIDList.append(classAttendanceArrayItem)

        # print(
        #     "ChattStateANumber="
        #     + chattStateANumber
        #     + " attendance code="
        #     + attendanceCode
        #     + " classAttendanceLog ID="
        #     + classAttendanceLogID
        #     + " tmiMinutes="
        #     + tmiMinutes
        # )
        # print(chattStateANumber, attendanceCode, classAttendanceLogID, tmiMinutes)
    return


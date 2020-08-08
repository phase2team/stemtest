from P2MT_App.models import InterventionType, FacultyAndStaff, ClassSchedule, Student
from P2MT_App import db
from sqlalchemy import distinct


def getInterventionTypes():
    interventionValueLabelTupleList = db.session.query(
        InterventionType.id, InterventionType.interventionType
    ).all()
    return interventionValueLabelTupleList


def getStaffFromFacultyAndStaff():
    teacherTupleList = (
        db.session.query(
            FacultyAndStaff.id, FacultyAndStaff.firstName, FacultyAndStaff.lastName
        )
        .distinct()
        .order_by(FacultyAndStaff.lastName)
        .all()
    )
    teacherValueLabelTupleList = [
        (item[0], item[1] + " " + item[2]) for item in teacherTupleList
    ]
    return teacherValueLabelTupleList


def getTeachers():
    teacherValueLabelTupleList = (
        db.session.query(ClassSchedule.teacherLastName, ClassSchedule.teacherLastName)
        .filter(ClassSchedule.campus == "STEM School")
        .distinct()
        .order_by(ClassSchedule.teacherLastName)
        .all()
    )
    return teacherValueLabelTupleList


def getClassNames():
    classNameValueLabelTupleList = (
        db.session.query(ClassSchedule.className, ClassSchedule.className)
        .filter(ClassSchedule.campus == "STEM School")
        .distinct()
        .order_by(ClassSchedule.className)
        .all()
    )
    return classNameValueLabelTupleList


def getCampusChoices():
    campusValueLabelTupleList = (
        db.session.query(ClassSchedule.campus, ClassSchedule.campus)
        .distinct()
        .order_by(ClassSchedule.campus.desc())
        .all()
    )
    return campusValueLabelTupleList


def getStudents():
    studentTupleList = (
        db.session.query(Student.chattStateANumber, Student.firstName, Student.lastName)
        .distinct()
        .order_by(Student.lastName)
        .all()
    )
    studentValueLabelTupleList = [
        (item[0], item[1] + " " + item[2]) for item in studentTupleList
    ]
    return studentValueLabelTupleList


def getStudentsById():
    studentTupleList = (
        db.session.query(Student.id, Student.firstName, Student.lastName)
        .distinct()
        .order_by(Student.lastName)
        .all()
    )
    studentValueLabelTupleList = [
        (item[0], item[1] + " " + item[2]) for item in studentTupleList
    ]
    return studentValueLabelTupleList


def getSchoolYear():
    schoolYearValueLabelTupleList = (
        db.session.query(ClassSchedule.schoolYear, ClassSchedule.schoolYear)
        .distinct()
        .order_by(ClassSchedule.schoolYear.desc())
        .all()
    )
    return schoolYearValueLabelTupleList


def getYearOfGraduation():
    yearOfGraduationValueLabelTupleList = (
        db.session.query(Student.yearOfGraduation, Student.yearOfGraduation)
        .distinct()
        .order_by(Student.yearOfGraduation.desc())
        .all()
    )
    return yearOfGraduationValueLabelTupleList


def getSemester():
    semesterValueLabelTupleList = (
        db.session.query(ClassSchedule.semester, ClassSchedule.semester)
        .distinct()
        .order_by(ClassSchedule.semester.desc())
        .all()
    )
    return semesterValueLabelTupleList

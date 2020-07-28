from P2MT_App.models import InterventionType, FacultyAndStaff, ClassSchedule
from P2MT_App import db
from sqlalchemy import distinct


def getInterventionTypes():
    interventionTypes = InterventionType.query.all()
    interventionValueLabelTupleList = []
    for interventionType in interventionTypes:
        value = str(interventionType.id)
        label = interventionType.interventionType
        interventionValueLabelTupleList.append((value, label))
    return interventionValueLabelTupleList


def getTeachers():
    teachers = FacultyAndStaff.query.order_by(FacultyAndStaff.lastName).all()
    choicePrompt = "--Choose Teacher--"
    teacherValueLabelTupleList = [(choicePrompt, choicePrompt)]
    for teacher in teachers:
        value = str(teacher.id)
        label = teacher.lastName
        # teacherValueLabelTupleList.append((value, label))
        teacherValueLabelTupleList.append((label, label))
    return teacherValueLabelTupleList


def getClassNames():
    classSchedules = ClassSchedule.query.filter(
        ClassSchedule.campus == "STEM School"
    ).order_by(ClassSchedule.className)
    choicePrompt = "--Choose Class--"
    classNameValueLabelTupleList = [(choicePrompt, choicePrompt)]
    for classSchedule in classSchedules:
        className = classSchedule.className
        if (className, className) not in classNameValueLabelTupleList:
            classNameValueLabelTupleList.append((className, className))
    return classNameValueLabelTupleList

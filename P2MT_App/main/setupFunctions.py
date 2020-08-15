from P2MT_App import db
from P2MT_App.models import InterventionType, SchoolCalendar
from P2MT_App.main.utilityfunctions import printLogEntry
import pandas as pd


def addInterventionType(interventionType, maxLevel):
    printLogEntry("Running addInterventionType()")
    interventionTypeExists = InterventionType.query.filter(
        InterventionType.interventionType == interventionType
    ).first()
    if interventionTypeExists == None:
        interventionType = InterventionType(
            interventionType=interventionType, maxLevel=maxLevel
        )
        db.session.add(interventionType)
        print("Intervention type", interventionType, "added to the database.")
    else:
        print(
            "Intervention type",
            interventionType,
            "not added to the database (already exists).",
        )
    return


def initializeInterventionTypes():
    addInterventionType("Conduct Behavior", 6)
    addInterventionType("Academic Behavior", 4)
    addInterventionType("Attendance", 3)
    addInterventionType("Dress Code", 6)
    addInterventionType("Bullying / Harassment", 4)
    addInterventionType("Extended Remediation", 1)
    return


def addSchoolCalendarDays(startDate, endDate):
    printLogEntry("Running addSchoolCalendarDays()")
    calendarDays = pd.date_range(start=startDate, end=endDate, freq="D")
    for calendarDay in calendarDays:
        classDate = calendarDay.date()
        dayNumber = calendarDay.weekday()
        dayNumberList = ("M", "T", "W", "R", "F", "S", "S")
        if (
            dayNumber == 0
            or dayNumber == 1
            or dayNumber == 2
            or dayNumber == 3
            or dayNumber == 4
        ):
            stemSchoolDay = True
            phaseIISchoolDay = True
        else:
            stemSchoolDay = False
            phaseIISchoolDay = False
        if dayNumber == 2:
            startTmiPeriod = True
        else:
            startTmiPeriod = False
        if dayNumber == 4:
            tmiDay = True
        else:
            tmiDay = False
        schoolCalendarDateExists = SchoolCalendar.query.filter(
            SchoolCalendar.classDate == classDate
        ).first()
        if schoolCalendarDateExists == None:
            schoolCalendar = SchoolCalendar(
                classDate=classDate,
                day=dayNumberList[dayNumber],
                dayNumber=dayNumber,
                stemSchoolDay=stemSchoolDay,
                phaseIISchoolDay=phaseIISchoolDay,
                startTmiPeriod=startTmiPeriod,
                tmiDay=tmiDay,
            )
            print(
                classDate,
                dayNumber,
                dayNumberList[dayNumber],
                stemSchoolDay,
                phaseIISchoolDay,
                startTmiPeriod,
                tmiDay,
            )
            db.session.add(schoolCalendar)
        else:
            print("Class date", classDate, "is already in the School Calendar")
    return

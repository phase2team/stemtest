from flask import flash
from P2MT_App import db
from P2MT_App.models import Student
from datetime import datetime, date, time
from P2MT_App.main.utilityfunctions import printLogEntry

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
    importCSV = open(fname, "r")
    for row in importCSV:
        # Skip the first row if it has header row data
        if "Chatt_State_A_Number" in row:
            continue
        print("row=", row)
        column = row.split(",")
        print("column=", column)
        chattStateANumber = column[0].strip()
        firstName = column[1].strip()
        lastName = column[2].strip()
        email = column[3].strip()
        yearOfGraduation = int(column[4].strip())
        house = column[5].strip()
        googleCalendarId = column[6].strip()
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

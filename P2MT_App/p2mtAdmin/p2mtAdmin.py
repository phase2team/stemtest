from flask import flash
from P2MT_App import db
from P2MT_App.models import Student, FacultyAndStaff
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
        staff = FacultyAndStaff(
            firstName=firstName,
            lastName=lastName,
            position=position,
            email=email,
            phoneNumber=phoneNumber,
            chattStateANumber=chattStateANumber,
            myersBrigg=myersBriggs,
            house=house,
            houseGrade=int(houseGrade),
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
    importCSV = open(fname, "r")
    for row in importCSV:
        # Skip the first row if it has header row data
        if "chattStateANumber" in row:
            continue
        print("row=", row)
        column = row.split(",")
        print("column=", column)
        firstName = column[0].strip()
        lastName = column[1].strip()
        position = column[2].strip()
        email = column[3].strip()
        phoneNumber = column[4].strip()
        chattStateANumber = column[5].strip()
        myersBriggs = column[6].strip()
        house = column[7].strip()
        houseGrade = column[8].strip()
        # Set houseGrade=0 if undefined to avoid errors with integer conversions
        if len(houseGrade) > 0:
            houseGrade = int(houseGrade)
        else:
            houseGrade = 0
        twitterAccount = column[9].strip()
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


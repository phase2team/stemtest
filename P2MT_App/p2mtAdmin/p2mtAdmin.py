from flask import flash
from P2MT_App import db
from P2MT_App.models import Student, FacultyAndStaff, Parents
from datetime import datetime, date, time
from P2MT_App.main.utilityfunctions import printLogEntry
import csv

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
            )
            print(parents)
            db.session.add(parents)
            db.session.commit()
        else:
            print("No student with chattStateANumber =", chattStateANumber, " exists")
    else:
        print("Parents with chattStateANumber =", chattStateANumber, "already exists")
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
        )
    return


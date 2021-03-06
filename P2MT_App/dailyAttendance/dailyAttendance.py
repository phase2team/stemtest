from flask import flash, current_app, send_file
from P2MT_App import db
from P2MT_App.models import DailyAttendanceLog, Student, FacultyAndStaff
from P2MT_App.main.utilityfunctions import printLogEntry
import csv
import os
from datetime import datetime


def add_DailyAttendanceLog(chattStateANumber, absenceDate, attendanceCode, comment):
    printLogEntry("add_DailyAttendanceLog() function called")
    print(chattStateANumber, attendanceCode, comment, absenceDate)
    dailyAttendanceLog = DailyAttendanceLog(
        absenceDate=absenceDate,
        attendanceCode=attendanceCode,
        comment=comment,
        staffID=1,
        chattStateANumber=chattStateANumber,
    )
    db.session.add(dailyAttendanceLog)
    return


def downloadDailyAttendanceLog():
    printLogEntry("downloadDailyAttendanceLog() function called")
    # Create a CSV output file and append with a timestamp
    output_file_path = os.path.join(current_app.root_path, "static/download")
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    output_file_path = "/tmp"
    csvFilename = output_file_path + "/" + "daily_attendance_log_" + timestamp + ".csv"
    csvOutputFile = open(csvFilename, "w")
    csvOutputWriter = csv.writer(
        csvOutputFile, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
    )
    # Write header row for CSV file
    csvOutputWriter.writerow(
        [
            "chattStateANumber",
            "firstName",
            "lastName",
            "absenceDate",
            "attendanceCode",
            "comment",
            "logEntryDate",
            "staffLastName",
        ]
    )
    csvOutputFileRowCount = 0
    # Query for information
    dailyAttendanceLogs = (
        DailyAttendanceLog.query.join(Student)
        .join(FacultyAndStaff)
        .order_by(Student.lastName)
        .all()
    )
    # Process each record in the query and write to the output file
    for log in dailyAttendanceLogs:
        csvOutputWriter.writerow(
            [
                log.Student.chattStateANumber,
                log.Student.firstName,
                log.Student.lastName,
                log.absenceDate,
                log.attendanceCode,
                log.comment,
                log.createDate,
                log.FacultyAndStaff.lastName,
            ]
        )
        csvOutputFileRowCount = csvOutputFileRowCount + 1
    csvOutputFile.close()
    return send_file(csvFilename, as_attachment=True, cache_timeout=0)

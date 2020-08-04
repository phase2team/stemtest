from flask import flash
from P2MT_App import db
from P2MT_App.models import DailyAttendanceLog


def add_DailyAttendanceLog(student_id, absenceDate, attendanceCode, comment):
    print(student_id, attendanceCode, comment, absenceDate)
    dailyAttendanceLog = DailyAttendanceLog(
        absenceDate=absenceDate,
        attendanceCode=attendanceCode,
        comment=comment,
        staffID=5,
        student_id=student_id,
    )
    db.session.add(dailyAttendanceLog)
    db.session.commit()
    flash("Daily attendance log has been added!", "success")
    return

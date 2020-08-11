from P2MT_App import db
from datetime import date
from P2MT_App.models import ClassAttendanceLog


def test_setAttendanceForTmiTesting(startDate, endDate):
    logs = ClassAttendanceLog.query.filter(
        ClassAttendanceLog.classDate >= startDate,
        ClassAttendanceLog.classDate <= endDate,
    )
    for log in logs:
        if log.attendanceCode == None:
            log.attendanceCode = "P"
            db.session.commit()
            print(log)
    return


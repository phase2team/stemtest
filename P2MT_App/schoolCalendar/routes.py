from flask import render_template, request, redirect, url_for, flash, Blueprint
from P2MT_App import db
from P2MT_App.models import SchoolCalendar
from P2MT_App.schoolCalendar.forms import (
    updateSchoolCalendarFieldListForm,
    updateSchoolCalendarContainerForm,
)

schoolCalendar_bp = Blueprint("schoolCalendar_bp", __name__)


@schoolCalendar_bp.route("/schoolcalendar", methods=["GET", "POST"])
def displaySchoolCalendar():
    # Create top level form for school calendar
    updateSchoolCalendarContainerFormDetails = updateSchoolCalendarContainerForm()

    if request.method == "POST":
        print("request.method == POST")
        # print(request.form)

    if updateSchoolCalendarContainerFormDetails.validate_on_submit():
        print("Form submitted!")
        if updateSchoolCalendarContainerFormDetails.schoolCalendarDays:
            print("School days update submitted")
            print(len(updateSchoolCalendarContainerFormDetails.schoolCalendarDays.data))
            for (
                schoolCalendarDay
            ) in updateSchoolCalendarContainerFormDetails.schoolCalendarDays.data:
                if schoolCalendarDay["updateFlag"] == "updated":
                    log_id = schoolCalendarDay["log_id"]
                    print("log_id = ", log_id)
                    schoolCalendar = SchoolCalendar.query.get_or_404(log_id)
                    schoolCalendar.stemSchoolDay = schoolCalendarDay["stemSchoolDay"]
                    schoolCalendar.phaseIISchoolDay = schoolCalendarDay[
                        "phaseIISchoolDay"
                    ]
                    schoolCalendar.chattStateSchoolDay = schoolCalendarDay[
                        "chattStateSchoolDay"
                    ]
                    schoolCalendar.seniorErDay = schoolCalendarDay["seniorErDay"]
                    schoolCalendar.juniorErDay = schoolCalendarDay["juniorErDay"]
                    schoolCalendar.seniorUpDay = schoolCalendarDay["seniorUpDay"]
                    schoolCalendar.juniorUpDay = schoolCalendarDay["juniorUpDay"]
                    db.session.commit()

    print(updateSchoolCalendarContainerFormDetails.errors)

    # Query database for school calendar day info
    schoolCalendarDays = SchoolCalendar.query.filter(SchoolCalendar.day != "S").all()
    schoolCalendarDates = (
        db.session.query(SchoolCalendar.classDate)
        .filter(SchoolCalendar.day != "S")
        .all()
    )
    # print(schoolCalendarDates)
    # Populate form info with database values
    for schoolCalendarDay in schoolCalendarDays:
        # Create sub-form for school calendar day details
        updateSchoolCalendarFieldListFormDetails = updateSchoolCalendarFieldListForm()
        updateSchoolCalendarFieldListFormDetails.log_id = schoolCalendarDay.id
        updateSchoolCalendarFieldListFormDetails.classDate = schoolCalendarDay.classDate
        updateSchoolCalendarFieldListFormDetails.stemSchoolDay = (
            schoolCalendarDay.stemSchoolDay
        )
        updateSchoolCalendarFieldListFormDetails.phaseIISchoolDay = (
            schoolCalendarDay.phaseIISchoolDay
        )
        updateSchoolCalendarFieldListFormDetails.chattStateSchoolDay = (
            schoolCalendarDay.chattStateSchoolDay
        )
        updateSchoolCalendarFieldListFormDetails.seniorErDay = (
            schoolCalendarDay.seniorErDay
        )
        updateSchoolCalendarFieldListFormDetails.juniorErDay = (
            schoolCalendarDay.juniorErDay
        )
        updateSchoolCalendarFieldListFormDetails.seniorUpDay = (
            schoolCalendarDay.seniorUpDay
        )
        updateSchoolCalendarFieldListFormDetails.juniorUpDay = (
            schoolCalendarDay.juniorUpDay
        )
        updateSchoolCalendarFieldListFormDetails.updateFlag = ""
        # Append school day details to top level form
        updateSchoolCalendarContainerFormDetails.schoolCalendarDays.append_entry(
            updateSchoolCalendarFieldListFormDetails
        )

    return render_template(
        "schoolcalendar.html",
        title="School Calendar",
        schoolCalendarForm=updateSchoolCalendarContainerFormDetails,
        schoolCalendarDates=schoolCalendarDates,
    )

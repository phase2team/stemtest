from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired


class editSchoolCalendar(FlaskForm):
    classDate = DateField("Start Date", validators=[DataRequired()])
    stemSchoolDay = BooleanField("STEM School Day")
    phaseIIDay = BooleanField("Phase II Day")
    chattStateSchoolDay = BooleanField("Chatt State School Day")
    seniorErDay = BooleanField("Senior ER Day")
    juniorErDay = BooleanField("Junior ER Day")
    seniorUpDay = BooleanField("Senior UP Day")
    juniorUpDay = BooleanField("Junior UP Day")

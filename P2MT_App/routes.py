from flask import render_template
from P2MT_App import app
from P2MT_App.models import Student, ClassSchedule


@app.route('/')
def home():
    return render_template('home.html',title='Home')


@app.route('/students')
def students():
    students = Student.query.all()
    for student in students :
        print(student.firstName)
    return render_template('students.html',title='Home',students=students)

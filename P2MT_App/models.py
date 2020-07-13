from P2MT_App import db

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chattStateANumber = db.Column(db.Integer,unique=True, nullable=False)
    firstName = db.Column(db.String(50),nullable=False)
    lastName = db.Column(db.String(50),nullable=False)
    email = db.Column(db.String(120),nullable=False)
    yearOfGraduation = db.Column(db.Integer, nullable=False)
    house = db.Column(db.String(20),nullable=False)
    classSchedule = db.relationship('ClassSchedule',backref='student',lazy=True)

    def __repr__(self):
        return f"Students('{self.chattStateANumber}','{self.firstName}','{self.lastName}')"

class ClassSchedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    className = db.Column(db.String(50),nullable=False)
    startTime = db.Column(db.DateTime,nullable=False)
    endTime = db.Column(db.DateTime,nullable=False)
    classDays = db.Column(db.String(10), nullable=False)
    student_id = db.Column(db.Integer,db.ForeignKey('student.id'),nullable=False)

    def __repr__(self):
        return f"ClassSchedule('{self.className}','{self.startTime}','{self.endTime}','{self.classDays}')"

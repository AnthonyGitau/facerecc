from datetime import datetime
from database import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

class Unit(Base):
    __tablename__ = "units"

    id = Column('student_id',Integer , primary_key=True)
    name = Column('first_name', String(50), unique=False , index=False)
    code = Column('last_name' , String(50))
    lecturer = Column('email',String(50),unique=True , index=True)
    registered_on = Column('registered_on' , DateTime)
 
    def __init__(self , name ,code , lecturer):
        self.name = name
        self.code = code
        self.lecturer = lecturer
        self.registered_on = datetime.utcnow()

    def __str__(self):
        return "Unit - %s" % (self.name)


class Student(Base):
    __tablename__ = "students"

    id = Column('student_id',Integer , primary_key=True)
    first_name = Column('first_name', String(50), unique=False , index=False)
    last_name = Column('last_name' , String(50))
    email = Column('email',String(50),unique=True , index=True)
    password = Column('password' , String(200))
    registered_on = Column('registered_on' , DateTime)
 
    def __init__(self , first_name ,last_name , email):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.registered_on = datetime.utcnow()

    def __repr__(self):
        return "Student - %s" % (self.first_name)


class Attendance(Base):
    __tablename__ = "attendance"
    
    id = Column('attendance_id',Integer , primary_key=True)
    unit_id = Column(Integer, ForeignKey(Unit.id))
    student_id = Column(Integer, ForeignKey(Student.id))
    attended_on = Column('registered_on' , DateTime)

    def __init__(self, unit_id, student_id):
        self.unit_id = unit_id
        self.student_id = student_id
        self.attended_on = datetime.utcnow()

    def __repr__(self):
        return "Student %s - Attended %s on %s" % (
            self.student_id, self.unit_id, self.attended_on)

class UnitRegistration(Base):
    __tablename__ = "unit_registration"

    id = Column('unit_registration',Integer , primary_key=True)
    unit_id = Column(Integer, ForeignKey(Unit.id))
    student_id = Column(Integer, ForeignKey(Student.id))

    def __init__(self, unit_id, student_id):
        self.unit_id = unit_id
        self.student_id = student_id

    def __repr__(self):
        return "Student %s taking course %s" % (self.student_id, self.unit_id)


class User(Base):
    __tablename__ = "user"

    id = Column('user_id',Integer , primary_key=True)
    first_name = Column('first_name', String(50), unique=False , index=False)
    last_name = Column('last_name' , String(50))
    password = Column('password' , String(200))
    email = Column('email',String(50),unique=True , index=True)
    registered_on = Column('registered_on' , DateTime)
 
    def __init__(self , first_name ,last_name, password , email):
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.email = email
        self.registered_on = datetime.utcnow()

    def is_authenticated(self):
        return True
 
    def is_active(self):
        return True
 
    def is_anonymous(self):
        return False
 
    def get_id(self):
        return unicode(self.id)
 
    def __repr__(self):
        return '<User %r>' % (self.email)
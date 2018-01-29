import subprocess
import threading
from flask import jsonify
from flask import Flask,session, request, flash, url_for, redirect, render_template, abort ,g
from flask_login import login_user , logout_user , current_user , login_required, LoginManager

from sqlalchemy import exists

from database import db_session
from models import User, Student, Unit, Attendance

app= Flask(__name__)
app.secret_key = 'sakjdvayusdq873dvhavsmdhna(&09hajdhsa9d7asdmdhascdasjd'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.before_request
def before_request():
    g.user = current_user


@app.route('/')
@login_required
def index():
    return render_template('dashboard.html')

@app.route('/register' , methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    user = User(request.form['name'], request.form['password'],request.form['email'])
    db_session.add(user)
    db_session.commit()
    flash('User successfully registered')
    return redirect(url_for('login'))
 

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    email = request.form['email']
    password = request.form['password']
    registered_user = User.query.filter_by(email=email,password=password).first()
    if registered_user is None:
        flash('Username or Password is invalid' , 'error')
        return redirect(url_for('login'))
    login_user(registered_user)
    flash('Logged in successfully')
    return redirect(request.args.get('next') or url_for('index'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index')) 


@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'GET':
        return render_template('add_student.html')

    firstName = request.form['firstName']
    lastName = request.form['lastName']
    emailAddress = request.form['emailAddress']

    student_exists = db_session.query(exists().where(Student.email==emailAddress)).scalar()
    if student_exists:
        student=Student.query.filter_by(Id=id).first()
        student.first_name = first_name
        student.last_name = last_name
        db_session.commit()

    new_student = Student(first_name=firstName, last_name=lastName, email=emailAddress)
    db_session.add(new_student)
    db_session.commit()

    flash('Student added and updated to the system.')
    return redirect(url_for('add_student'))


@app.route('/train_student', methods=['GET', 'POST'])
def train_student():
    if request.method == 'GET':
        students = db_session.query(Student).all()
        print(students)
        return render_template('train_student.html', students=students)

@app.route('/train/<student_id>', methods=['GET', 'POST'])
def train(student_id):
    import face_acquire

    thread = threading.Thread(target=face_acquire.capture(student_id))
    thread.start()
    return jsonify({'status': 200})


@app.route('/train_dataset')
def train_dataset():
    return render_template('train_dataset.html')

@app.route('/train_dataset_process')
def train_dataset_process():
    subprocess.call(['python', 'face_training.py'])
    return jsonify({'status': 200, 'trained': True})

@app.route('/add_unit', methods=['GET', 'POST'])
def add_unit():
    if request.method == 'GET':
        return render_template('add_unit.html')

    unitName = request.form['unitName']
    unitCode = request.form['unitCode']
    lecturerName = request.form['lecturerName']

    print(unitName, unitCode, lecturerName)
    unit_exists = db_session.query(exists().where(Unit.code==unitCode)).scalar()
    if unit_exists:
        unit=Unit.query.filter_by(code=unitCode).first()
        unit.name = unitName
        unit.code = unitCode
        unit.lecturer = lecturerName
        db_session.commit()

    new_unit = Unit(name=unitName, code=unitCode, lecturer=lecturerName)
    db_session.add(new_unit)
    db_session.commit()

    flash('Unit added and updated to the system.')
    return redirect(url_for('add_unit'))

@app.route('/attendance_track')
def attendance_track():
    units = Unit.query.all()
    return render_template('attendance_track.html', units=units)


@app.route('/attendance_track/<unit_id>')
def attendance_track_unit(unit_id):
    import face_recognition
    unit = Unit.query.get(unit_id)

    face_recognition.attendanceRecord(unit.id)
    return jsonify({'status': 200})

@app.route('/charts')
def charts():
    units = Unit.query.all()
    return render_template('charts.html', units=units)

if __name__ == '__main__':
    app.run(debug=True)
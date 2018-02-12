import datetime
import subprocess
import threading
import bcrypt

from flask import jsonify, send_from_directory
from flask import Flask,session, request, flash, url_for, redirect, render_template, abort ,g
from flask_login import login_user , logout_user , current_user , login_required, LoginManager
from sqlalchemy import exists, Date, cast, extract

from database import db_session
from models import User, Student, Unit, Attendance, UnitRegistration

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

    pw_hash = bcrypt.hashpw(request.form['password'].encode(), bcrypt.gensalt())

    user = User(request.form['first_name'], 
        request.form['last_name'], pw_hash,request.form['email'])
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
    registered_user = User.query.filter_by(email=email).first()
    if registered_user is None or not bcrypt.checkpw(password.encode(), registered_user.password.encode()):
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
        student=Student.query.filter_by(email=emailAddress).first()
        student.first_name = first_name
        student.last_name = last_name
        db_session.commit()

    new_student = Student(first_name=firstName, last_name=lastName, email=emailAddress)
    db_session.add(new_student)
    db_session.commit()

    flash('Student added and updated to the system.')
    return redirect(url_for('add_student'))


@app.route('/all_students', methods=['GET', 'POST'])
def all_students():
    students = db_session.query(Student).all()
    return render_template('all_students.html', students=students)


@app.route('/all_students/delete/<id>', methods=['GET', 'POST'])
def delete_student(id):
    if request.method == 'GET':
        student = db_session.query(Student).get(id)
        return render_template('delete_student.html', student=student)

    student = Student.query.get(id)
    db_session.delete(student)
    db_session.commit()

    flash('Student deleted from the system.')
    return redirect(url_for('all_students'))

@app.route('/all_students/update/<id>', methods=['GET', 'POST'])
def update_student(id):
    if request.method == 'GET':
        student = db_session.query(Student).get(id)
        return render_template('edit_student.html', student=student)

    firstName = request.form['firstName']
    lastName = request.form['lastName']
    emailAddress = request.form['emailAddress']

    student_exists = db_session.query(exists().where(Student.email==emailAddress)).scalar()
    if student_exists:
        student=Student.query.filter_by(id=id).first()
        student.first_name = firstName
        student.last_name = lastName
        student.email = emailAddress
        db_session.commit()

    flash('Student Updated In system.')
    return redirect(url_for('all_students'))

@app.route('/image/<path:path>')
def send_image(path):
    return send_from_directory('dataset', path)





@app.route('/train_student', methods=['GET', 'POST'])
def train_student():
    if request.method == 'GET':
        students = db_session.query(Student).all()
        print(students)
        return render_template('train_student.html', students=students)


@app.route('/train/<student_id>', methods=['GET', 'POST'])
def train(student_id):
    import face_acquire
    print('Face Acquire Starting for Student {}'.format(student_id))
    thread = threading.Thread(target=face_acquire.capture, args=(student_id,))
    thread.start()
    print('Face Acquire Ending for Student {}'.format(student_id))
    return jsonify({'status': 200})


@app.route('/train_dataset')
def train_dataset():
    return render_template('train_dataset.html')

@app.route('/train_dataset_process')
def train_dataset_process():
    print('Training the dataset at {}'.format(datetime.datetime.now()))
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

@app.route('/manage_units', methods=['GET', 'POST'])
def manage_units():
    units = Unit.query.all()
    return render_template('manage_units.html', units=units)


@app.route('/manage_units/delete/<id>', methods=['GET', 'POST'])
def delete_unit(id):
    if request.method == 'GET':
        unit = db_session.query(Unit).get(id)
        return render_template('delete_unit.html', unit=unit)
    unit = Unit.query.get(id)
    db_session.delete(unit)
    db_session.commit()

    flash('Unit delete from the system.')
    return redirect(url_for('manage_units'))


@app.route('/manage_units/update/<id>', methods=['GET', 'POST'])
def update_unit(id):
    if request.method == 'GET':
        unit = db_session.query(Unit).get(id)
        return render_template('edit_unit.html', unit=unit)

    code = request.form['code']
    name = request.form['name']
    lecturer = request.form['lecturer']

    student_exists = db_session.query(exists().where(Unit.id==id)).scalar()
    if student_exists:
        unit=Unit.query.filter_by(id=id).first()
        unit.code = code
        unit.name = name
        unit.lecturer = lecturer
        db_session.commit()

    flash('Unit Updated In system.')
    return redirect(url_for('manage_units'))



@app.route('/register_units/<id>', methods=['GET', 'POST'])
def register_units(id):
    student = Student.query.get(id)

    if request.method == 'GET':
        units = Unit.query.all()
        return render_template('register_units.html', units=units, student=student)

    courses = request.form.getlist('courses')
    for course in courses:
        ur = UnitRegistration(int(course), student.id)
        db_session.add(ur)
        db_session.commit()

    flash('Courses Registered In system.')
    return redirect(url_for('all_students'))

@app.route('/unit_data', methods=['GET', 'POST'])
def unit_data():
    units = Unit.query.all()
    return render_template('unit_data.html', units=units)

@app.route('/get_unit_students/<unit_id>')
def get_unit_students(unit_id):

    attendance = db_session.query(Attendance).filter(Attendance.unit_id == unit_id).all()
    dates = [d.attended_on.strftime('%d-%m-%Y') for d in attendance]
    dates = list(set(dates))
    attendance_data = {}
    for d in dates:
        date = d.split('-')
        date = datetime.datetime(int(date[2]), int(date[1]), int(date[0]))
        attendances = db_session.query(Attendance).filter(Attendance.unit_id == unit_id) \
                                .filter(extract('year', Attendance.attended_on) == date.year) \
                                .filter(extract('month', Attendance.attended_on) == date.month) \
                                .filter(extract('day', Attendance.attended_on) == date.day).all()

        label = date.strftime('%d-%m-%Y')
        if not attendance_data.get(label, None):
            attendance_data[label] = len(attendances)
        else:
            attendance_data[label] = attendance_data[label] + len(attendances)

    chart_labels, chart_data = [], []
    for key in sorted(attendance_data.keys()):
        chart_labels.append(key)
        chart_data.append(attendance_data[key])

    unit_registration = db_session.query(UnitRegistration).filter(UnitRegistration.unit_id==unit_id).all()
    student_number = len(unit_registration)
    students = []
    for u in unit_registration:
        student = Student.query.get(u.student_id)
        if student:
            students.append(
                {
                 'student_id': student.id, 'first_name':student.first_name, 
                 'last_name': student.last_name, 'email': student.email
                }
            )
    response = {
        'student_number': student_number,
        'students':students,
        'attendance_data': {'labels': chart_labels, 'data': chart_data},
    }
    return jsonify(response)


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

@app.route('/attendance_computation')
def attendance_computation():
    students = Student.query.all()
    units = Unit.query.all()
    return render_template('attendance_computation.html', students=students, units=units)


@app.route('/get_unit_registered_students/<unit_id>')
def get_unit_registered_students(unit_id):
    student_ids = db_session.query(UnitRegistration).with_entities(UnitRegistration.student_id) \
            .filter(UnitRegistration.unit_id == unit_id).all()
    student_ids = [s[0] for s in student_ids]
    students = db_session.query(Student).filter(Student.id.in_(student_ids)).all()

    response = []
    for student in students:
        response.append({
            'id': student.id,
            'email': student.email,
            'first_name': student.first_name,
            'last_name': student.last_name,

    })
    return jsonify(response)



@app.route('/get_unit_dates/<unit_id>')
def get_unit_dates(unit_id):
    attendance = db_session.query(Attendance).filter(Attendance.unit_id == unit_id).all()

    dates = [d.attended_on.strftime('%d-%m-%Y') for d in attendance]
    dates = list(set(dates))
    return jsonify({'dates':dates})

@app.route('/get_attendance_dates/<unit_id>/<date>')
def get_attendance_dates(unit_id, date):
    date = date.split('-')
    print(date)
    print(int(date[0]), int(date[1]), int(date[2]))
    date = datetime.datetime(int(date[2]), int(date[1]), int(date[0]))

    
    attendances = db_session.query(Attendance).filter(Attendance.unit_id == unit_id) \
                            .filter(extract('year', Attendance.attended_on) == date.year) \
                            .filter(extract('month', Attendance.attended_on) == date.month) \
                            .filter(extract('day', Attendance.attended_on) == date.day).all()

    print('ATTENDANCES ', attendances)
    students_attendance = []
    for a in attendances:
        student = Student.query.get(a.student_id)
        if student:
            students_attendance.append(
                {
                 'student_id': student.id, 'first_name':student.first_name, 
                 'last_name': student.last_name, 'attended_on':a.attended_on 
                }
            )


    months = [a.attended_on.strftime('%B') for a in attendances]
    res = {}
    for m in months:
        if not res.get(m, None):
            res[m] = 1
        else:
            res[m] += 1

    return jsonify({
        'labels': list(res.keys()),
        'data': list(res.values()),
        'students_attendance': students_attendance,
    })


if __name__ == '__main__':
    app.run(debug=True)
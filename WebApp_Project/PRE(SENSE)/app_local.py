# Step 01: import necessary libraries/modules
from flask import Flask, jsonify, request, render_template, url_for, redirect, send_file
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from PIL import Image, ImageDraw, ImageFont
from ast import literal_eval
import numpy as np
import face_recognition
import os
import csv
import datetime
from datetime import date
from datetime import datetime


app = Flask(__name__, template_folder='templates', static_folder='static')
app.debug=True

#configurations
UPLOAD_FOLDER = "./app_storage"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
student_jpg = "./student_photo"
app.config['students'] = student_jpg
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://kinmeng:password@localhost:5432/attendance_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
base_url = "http://localhost:5000"
# base_url = "http://presenseapp.herokuapp.com"


from models_local import Photo, Student, Attendance

@app.route('/')
def home():
   return render_template('home.html')


@app.route('/uploader/', methods=['POST','GET'])
def uploader():
    if request.method == 'GET':
           return render_template('upload.html')
    if request.method == 'POST':
        os.makedirs('app_storage', exist_ok=True)
        photo_objects = request.files.getlist('file')
        week_number = request.form.get('week_number')
        for photo in photo_objects:
            new_image = Photo(img_filename=photo.filename, week=week_number, timestamp=datetime.now())
            db.session.add(new_image)
            db.session.commit()    
            print("image saved")
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(photo.filename)))
            url = base_url + '/processPhoto/'
            return redirect(url)

# @app.route('/uploader/', methods=['POST','GET'])
# def upload_photo():
# 	if request.method == 'POST':
# 		os.makedirs('app_storage', exist_ok=True)
# 		photo_objects = request.files.getlist('file')
# 		for photo in photo_objects:
# 			photo.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(photo.filename)))
# 			# print(photo.filename)
# 			# new_image = Photo(name=7, img_filename=photo.filename, img_data=photo.read())
# 			# db.session.add(new_image)
# 			# db.session.commit()    
            
# 			print(photo)
# 			photo.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(photo.filename)))
# 			return "you uploaded successfully"
# 	if request.method == 'GET':
# 		returned_photos = Photo.query.all()
# 		return jsonify([m.serialize() for m in returned_photos])

@app.route('/student/', methods=['POST', 'GET'])
def student():
    if request.method == 'POST':
        student_name = request.form.get('student_name')
        student_id = request.form.get('student_id')
        student_section = request.form.get('student_section')
        student_photo = request.files['file']
        try:
            filepath = os.path.join(app.config['students'], secure_filename(student_photo.filename))
            student_photo.save(filepath)
            picture_of_student = face_recognition.load_image_file(filepath)
            face_encoding = face_recognition.face_encodings(picture_of_student)[0]
            face_encoding = face_encoding.tolist()
            face_encoding = str(face_encoding)
    
            new_student = Student(student_name= student_name, student_photo=student_photo.filename, student_id=student_id, student_section=student_section, encodings=face_encoding) #based on init function
            db.session.add(new_student)
            db.session.commit()
            
            return jsonify('{} was created'.format(new_student))
        except Exception as e:
            return (str(e))
    if request.method == 'GET':
        return render_template('student_reg.html')



@app.route('/processPhoto/', methods=['GET'])
def processPhoto():
    if request.method == 'GET':
        att_list = []

        today = date.today()
        start_date = datetime(year=today.year,month=today.month, day=today.day, hour=0, minute=0, second=0, microsecond=0)
        end_date = datetime(year=today.year,month=today.month, day=today.day, hour=23, minute=59, second=59, microsecond=59)
        
        class_photos = Photo.query.filter(Photo.week==1, Photo.timestamp >= start_date, Photo.timestamp <= end_date).all()[-1]

        image = class_photos.serialize()
        path = './app_storage/'+ image['img_filename']
        print(path)
        class_photo = face_recognition.load_image_file(path)
        face_encodings_class = face_recognition.face_encodings(class_photo, num_jitters=2)

        

        returned_students = Student.query.filter_by(student_section='G1')	
        for student in returned_students:
            student = student.serialize()
            face_encoding_student = student['encodings']
            face_encoding_student = literal_eval(face_encoding_student)
            face_encoding_student = np.asarray(face_encoding_student)
            results = face_recognition.compare_faces(face_encodings_class, face_encoding_student, tolerance=0.4)
            print(results)
            name = student['name']
            if True in results:
                att_list.append({'name': name, 'attendance':'present'})
                stu_id = Student.query.filter_by(student_name= name).first().student_id
                if id is not None:
                    new_attendance = Attendance(student_id= stu_id, present=1, timestamp=datetime.now())
                    db.session.add(new_attendance)
                    db.session.commit()
            else: 
                att_list.append({'name': name, 'attendance':'absent'})
                stu_id = Student.query.filter_by(student_name= name).first().student_id
                if id is not None:
                    new_attendance = Attendance(student_id= stu_id, present=0, timestamp=datetime.now())
                    db.session.add(new_attendance)
                    db.session.commit()
        
        return render_template('displayer.html', att_list=att_list)



@app.route('/download/', methods=['GET'])
def downloadexcel():
    a_file = open("attendance.csv","w")
    content = {}    
    today = date.today()
    start_date = datetime(year=today.year,month=today.month, day=today.day, hour=0, minute=0, second=0, microsecond=0)
    end_date = datetime(year=today.year,month=today.month, day=today.day, hour=23, minute=59, second=59, microsecond=59)
    attendance = Attendance.query.filter(Attendance.timestamp >= start_date, Attendance.timestamp <= end_date).all()[-5:]
    print(attendance)
    for student in attendance:
        print(Attendance.query.filter_by(id=student.student_id).first())
        content[Student.query.filter_by(student_id=student.student_id).first().student_name] = student.present
    
    print(content)
    writer = csv.writer(a_file)
    for key, value in content.items():
        writer.writerow([key, value])
    a_file.close()
    return send_file(filename_or_fp= 'attendance.csv',mimetype='text/csv', attachment_filename='attendance.csv', as_attachment=True)
    

if __name__ == '__main__':
   app.run(debug = True)
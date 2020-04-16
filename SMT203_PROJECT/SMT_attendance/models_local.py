from app_local import db
from flask_sqlalchemy import SQLAlchemy
import datetime


class Photo(db.Model):
	__tablename__ = 'class_photos'

	id = db.Column(db.Integer, primary_key=True)
	# name = db.Column(db.String(80), unique = True, nullable=False)
	img_filename =  db.Column(db.String())
	week = db.Column(db.Integer)
	timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
	
	def __init__(self, img_filename, week, timestamp): #do not initialize pri key
		self.img_filename = img_filename
		self.week = week
		self.timestamp = timestamp
	def __repr__(self):
		return '<id {}>'.format(self.id)
	
	def serialize(self):
		return {
		'id': self.id,
		'img_filename': self.img_filename,
		'week': self.week,     
		'timestamp':self.timestamp
		}

class Student(db.Model):
	__tablename__ = 'student_photos'

	student_id = db.Column(db.Integer, primary_key=True)
	student_name = db.Column(db.String(80), unique = True, nullable=False)
	student_photo = db.Column(db.String())
	student_section = db.Column(db.String())
	encodings = db.Column(db.String())

	student_attendance = db.relationship('Attendance', back_populates='attendance_student', uselist=True)

	def __init__(self, student_id, student_name, student_photo, student_section, encodings): #do not initialize pri key
		self.student_id = student_id
		self.student_name = student_name
		self.student_photo = student_photo
		self.student_section = student_section
		self.encodings = encodings

	def __repr__(self):
		return '<id {}>'.format(self.student_id)
	
	def serialize(self):
		return {
		'id': self.student_id,
		'name': self.student_name,
		'photo': self.student_photo,
		'encodings': self.encodings,
		'section': self.student_section
		}

class Attendance(db.Model):
	__tablename__	= 'student_attendance'

	id = db.Column(db.Integer, primary_key=True)
	student_id = db.Column(db.Integer, db.ForeignKey('student_photos.student_id'), nullable=False)
	present = db.Column(db.Integer, unique=False, nullable=False)
	attendance_student = db.relationship('Student', back_populates='student_attendance')
	timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

	def __init__(self, student_id, present, timestamp): #do not initialize pri key
		self.student_id = student_id,
		self.present = present,
		self.timestamp = timestamp
	
	def serialize(self):
		return {
			'student_id': self.student_id,
			'name': self.attendance_student.name,
			'present': self.present
		}
		
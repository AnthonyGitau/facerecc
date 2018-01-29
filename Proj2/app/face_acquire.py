import cv2
import numpy as numpy

face_detect=cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')
cam=cv2.VideoCapture(0)

from database import db_session
from models import Student

def insertOrUpdate(Id, first_name, last_name, email):
	exists = db_session.query(exists().where(Student.id==Id)).scalar()

	if exists:
		student=Student.query.filter_by(Id=id).first()
		student.first_name = first_name
		student.last_name = last_name
		db_session.commit()
	new_student = Student(first_name=first_name, last_name=last_name)
	db_session.add(new_student)
	db_session.flush()

	return True

def capture(Id):
	sampleNum=0
	while(True):
		ret,img=cam.read()
		if img is not None:
			gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
			faces=face_detect.detectMultiScale(gray,1.3,5)
			for(x,y,w,h) in faces:
				sampleNum=sampleNum+1
				cv2.imwrite("/home/fynch/Proj2/app/dataset/User."+str(Id)+"."+str(sampleNum)+".jpg",img[y:y+h,x:x+w])
				cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
			print("no of faces found {}".format(len(faces)))
			cv2.imshow("Face",img)
			if cv2.waitKey(50) & 0xFF == ord('q'):
				end()
			elif sampleNum>20:
				end()
	return

def end():
	cam.release()
	cv2.destroyAllWindows()
	return None
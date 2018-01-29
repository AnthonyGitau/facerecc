#! /usr/bin/python
import cv2
import numpy as np
import sqlite3
import time

LESSON_TIME = 2400
LESSON_STUDENTS = {}

from database import db_session
from models import Student, Attendance, Unit

faceDetect=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
# faceDetect=cv2.CascadeClassifier('./haarcascades/haarcascade_frontalface_alt2.xml')
#faceDetect=cv2.CascadeClassifier('./haarcascades/haarcascade_eye.xml')

cam=cv2.VideoCapture(0)
rec=cv2.face.createLBPHFaceRecognizer()
rec.load('trainer/trainingdata.yml')
font=cv2.FONT_HERSHEY_COMPLEX

def getProfile(id):
    return db_session.query(Student).get(id)

def attendanceRecord(unit_id):
    start_time = time.time()
    while(True):
        date_string = time.strftime('%Y-%m-%d-%H:%M')
        ret, img = cam.read()
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        faces = faceDetect.detectMultiScale(gray, 1.3, 5)
        for(x, y, w, h)in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
            id, conf = rec.predict(gray[y:y+h,x:x+w])
            print('Predicted Id = ', id, ' ', conf)
            profile = getProfile(id)
            if(profile != None):
                cv2.putText(img, profile.first_name,(x,y+h+20),font,1, (0,255,0))
                print(profile.first_name)
                now = time.time()
                if (now - start_time) < LESSON_TIME:
                    if not LESSON_STUDENTS.get(profile.id, None):
                        LESSON_STUDENTS[profile.id] = profile.first_name
                        attendance = Attendance(unit_id=unit_id, student_id=profile.id)
                        db_session.add(attendance)
                        db_session.commit()
                    else:
                        print('Student [%s] attendance recorded' % profile.id)
                
            else:
                cv2.putText(img, 'New Student',(x-10,y-10),font,1,(0,255,0))
            image_path = "output/User."+str(id)+"\t"+ date_string +".jpg"
            print(image_path)
            cv2.imwrite(image_path,img[y:y+h,x:x+w])
        cv2.imshow("face",img)
        if(cv2.waitKey(1)==ord('q')):
            break

    cam.release()
    cv2.destroyAllWindows()
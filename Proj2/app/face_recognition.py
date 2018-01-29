#! /usr/bin/python
import cv2
import numpy as np
import sqlite3
import time

from database import db_session
from models import Student

faceDetect=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
# faceDetect=cv2.CascadeClassifier('./haarcascades/haarcascade_frontalface_alt2.xml')
#faceDetect=cv2.CascadeClassifier('./haarcascades/haarcascade_eye.xml')

cam=cv2.VideoCapture(0)
rec=cv2.face.createLBPHFaceRecognizer()
rec.load('trainer/trainingdata.yml')
font=cv2.FONT_HERSHEY_COMPLEX

def getProfile(id):
    return db_session.query(Student).get(id)

# def getProfile(id):
#     conn=sqlite3.connect('facedb.db')
#     cmd="SELECT * FROM Students WHERE Id="+str(id)+";"
#     cursor=conn.execute(cmd)
#     profile=None
#     for row in cursor:
#         profile=row
#     print(cursor, ' cursor')
#     conn.close()

#     print("Detected this fool {}".format(id))
#     return profile
# print('Starting System ......')

while(True):
    date_string = time.strftime('%Y-%m-%d-%H:%M')
    ret, img = cam.read()
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces = faceDetect.detectMultiScale(gray, 1.3, 5)
    for(x,y,w,h)in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
        id, conf = rec.predict(gray[y:y+h,x:x+w])
        print('Predicted Id=', id, ' ', conf)
        profile = getProfile(id)
        if(profile != None):
            cv2.putText(img, profile.first_name,(x,y+h+20),font,1, (0,255,0))
            print(profile.first_name)
        else:
            cv2.putText(img, 'Unknown Student',(x-10,y-10),font,1,(0,255,0))

        image_path = "output/User."+str(id)+"\t"+ date_string+".jpg"
        print(image_path)
        cv2.imwrite(image_path,img[y:y+h,x:x+w])
    cv2.imshow("face",img)
    if(cv2.waitKey(1)==ord('q')):
        break

cam.release()
cv2.destroyAllWindows()

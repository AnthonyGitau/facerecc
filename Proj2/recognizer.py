import cv2
import numpy as np
import sqlite3
import time


faceDetect=cv2.CascadeClassifier('./haarcascades/haarcascade_frontalface_default.xml')
cam=cv2.VideoCapture(0)
rec=cv2.face.createLBPHFaceRecognizer()
rec.load('trainer/trainingdata.yml')
font=cv2.FONT_HERSHEY_COMPLEX

def getProfile(id):
    	
    	conn=sqlite3.connect('facedb.db')
    	cmd="SELECT * FROM Students WHERE Id="+str(id)+";"
    	cursor=conn.execute(cmd)
    	profile=None
    	for row in cursor:	
    			profile=row
    	print(cursor, ' cursor')
    	conn.close()

    	print("Detected this fool {}".format(id))
    	return profile
print('Starting System ......')


import cv2
import numpy as numpy
import sqlite3

face_detect=cv2.CascadeClassifier('./haarcascades/haarcascade_frontalface_default.xml')
cam=cv2.VideoCapture(0)

conn = sqlite3.connect("facedb.db")

def insertorUpdate(Id,Name):
	cmd = "SELECT * FROM Students WHERE Id={0}".format(Id)
	cursor = conn.execute(cmd)
	isRecordExist=0
	for row in cursor:
		isRecordExist=1
	if(isRecordExist==1):
		cmd="UPDATE Students SET Names={0} WHERE Id={1}".format(Name, Id)
	else:
		cmd="INSERT INTO Students(Id, Names) Values('{0}', '{1}')".format(Id, Name)

	conn.execute(cmd)
	conn.commit()
	conn.close()

Id   = int(raw_input('enter user id:'))
name = str(raw_input('enter user Name:'))

insertorUpdate(Id,name)
sampleNum=0
while(True):
	ret,img=cam.read()
	gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	faces=face_detect.detectMultiScale(gray,1.1,5)
	for(x,y,w,h) in faces:
		sampleNum=sampleNum+1
		cv2.imwrite("dataset/User."+str(Id)+"."+str(sampleNum)
+".jpg",img[y:y+h,x:x+w])
		cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)

	print("no of faces found {}".format(len(faces)))
	cv2.imshow("Face",img)
	if cv2.waitKey(50) & 0xFF == ord('q'):
		break
	elif sampleNum>20:
		break
	
cam.release()
cv2.destroyAllWindows()

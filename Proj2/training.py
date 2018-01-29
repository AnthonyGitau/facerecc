import os
import cv2
import numpy as np
from PIL import Image

recognizer=cv2.face.createLBPHFaceRecognizer()
detector = cv2.CascadeClassifier('./haarcascades/haarcascade_frontalface_default.xml')
path='dataset'

def get_images_and_ID(path):
	imagePaths=[os.path.join(path,f) for f in os.listdir(path)]
	faces=[]
	IDs=[]
	for imagePath in imagePaths:
		faceImg=Image.open(imagePath).convert('L')
		faceNp=np.array(faceImg,'uint8')
#get the label of the image
		ID=int(os.path.split(imagePath)[-1].split('.')[1])
		faces.append(faceNp)
		print ID
		IDs.append(ID)
		cv2.imshow('training',faceNp)
		cv2.waitKey(10)
	return np.array(IDs),faces

Ids,faces=get_images_and_ID(path)
recognizer.train(faces,np.array(Ids))
recognizer.save('trainer/trainingdata.yml')
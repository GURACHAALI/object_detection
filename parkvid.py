import cv2 as cv
import pickle
import cvzone
import numpy as np


#video feed
cap=cv.VideoCapture('carPark.mp4')
      
with open('carparkpos','rb') as f:
        posList=pickle.load(f)
                
width,height=107,48

def CheckParkingSpace(imgpro):
    spaceCounter = 0
    
    for pos in posList:
        x,y=pos
    
        
        imgcrop=imgpro[y:y+height,x:x+width]
        #cv.imshow(str(x*y),imgcrop)
        count=cv.countNonZero(imgcrop)
        
        
        if count<800:
            color=(255,255,255)
            thickness=5
            spaceCounter += 1
            
        else:
            color=(0,0,255)
            thickness=2
        cv.rectangle(img,pos,(pos[0]+width,pos[1]+height),color,thickness)        
    cvzone.putTextRect(img, str(count), (x, y + height - 3), scale=1,
                           thickness=2, offset=0, colorR=color)

    cvzone.putTextRect(img, f'emptyslots: {spaceCounter}/{len(posList)}', (100, 50), scale=2,
                           thickness=4, offset=25, colorR=(0,200,0))

while True:
    if cap.get(cv.CAP_PROP_POS_FRAMES)==cap.get(cv.CAP_PROP_FRAME_COUNT):
        cap.set(cv.CAP_PROP_POS_FRAMES,0)
        
    success,img=cap.read()
    imgGray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    imgBlur = cv.GaussianBlur(imgGray, (3, 3), 1)
    imgThreshold = cv.adaptiveThreshold(imgBlur, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY_INV, 25, 16) 
    
    
    imgMedian = cv.medianBlur(imgThreshold, 5)
    kernel = np.ones((3, 3), np.uint8)
    imgDilate = cv.dilate(imgMedian, kernel, iterations=1)

    CheckParkingSpace(imgDilate)  
    
        
            
    
    cv.imshow('image',img)
    #cv.imshow('imgthres',imgThreshold)
    #cv.imshow('imgts',imgMedian)
    cv.waitKey(10)
import cv2 as cv
import pickle


width,height=107,48

try:
    with open('carparkpos','rb') as f:
        posList=pickle.load(f)
except:        
        
  posList=[]

def mouseClick(events,x,y,flags,params):
    if events==cv.EVENT_LBUTTONDOWN:
        posList.append((x,y))
    if events==cv.EVENT_RBUTTONDOWN:
        for i,pos in enumerate(posList):
            x1,y1=pos
            if x1<x<x1+width and y1<y<y1+height:
                posList.pop(i)
                
    
    with open('carparkpos','wb') as f:
        pickle.dump(posList,f)            
 
                  
#create a while loop
while True:
    img=cv.imread("carParkImg.png")
    for pos in posList:
        cv.rectangle(img,pos,(pos[0]+width,pos[1]+height),(0,0,255),2)
    #cv.rectangle(img,(50,192),(157,240),(0,0,255),2)
    cv.imshow('image',img)
    cv.setMouseCallback('image',mouseClick)
    cv.waitKey(1)
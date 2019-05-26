import cv2
import numpy as np
from pynput.mouse import Button, Controller
import keyboard
import wx
mouse=Controller()

app=wx.App(False)
(sx,sy)=wx.GetDisplaySize()
(camx,camy)=(320,240)

lowerBound=np.array([33,80,40])
upperBound=np.array([102,255,255])
#test1
lowerBound1=np.array([79,168,119])
upperBound1=np.array([238,256,256])
#
cam= cv2.VideoCapture(0)

kernelOpen=np.ones((5,5))
kernelClose=np.ones((20,20))
pinchFlag=0
#test2
pinchFlag1=0
#
while True:
    ret, img=cam.read()
    img=cv2.resize(img,(340,220))

    #convert BGR to HSV
    imgHSV= cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    # create the Mask
    mask=cv2.inRange(imgHSV,lowerBound,upperBound)
    #morphology
    maskOpen=cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernelOpen)
    maskClose=cv2.morphologyEx(maskOpen,cv2.MORPH_CLOSE,kernelClose)

    maskFinal=maskClose
    conts,h=cv2.findContours(maskFinal.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
#test3
    mask1=cv2.inRange(imgHSV,lowerBound1,upperBound1)
    #morphology
    maskOpen1=cv2.morphologyEx(mask1,cv2.MORPH_OPEN,kernelOpen)
    maskClose1=cv2.morphologyEx(maskOpen1,cv2.MORPH_CLOSE,kernelClose)

    maskFinal1=maskClose1
    conts1,h1=cv2.findContours(maskFinal1.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

    if(len(conts1)==1):
        x3,y3,w3,h3=cv2.boundingRect(conts1[0])
        keyboard.press('w')
        #if(pinchFlag1==0):
            #pinchFlag1=1
            #print("Hello im keyboard")
            

    elif(len(conts1)==0):
        keyboard.release('w')
       # if(pinchFlag1==1):
            #pinchFlag1=0
            #print("GOODBYE")
            
#
    if(len(conts)==2):
        if(pinchFlag==1):
            pinchFlag=0
            mouse.release(Button.left)
        x1,y1,w1,h1=cv2.boundingRect(conts[0])
        x2,y2,w2,h2=cv2.boundingRect(conts[1])
        cv2.rectangle(img,(x1,y1),(x1+w1,y1+h1),(255,0,0),2)
        cv2.rectangle(img,(x2,y2),(x2+w2,y2+h2),(255,0,0),2)
        cx1=x1+w1//2
        cy1=y1+h1//2
        cx2=x2+w2//2
        cy2=y2+h2//2
        cx=(cx1+cx2)//2
        cy=(cy1+cy2)//2
        cv2.line(img, (cx1,cy1),(cx2,cy2),(255,0,0),2)
        cv2.circle(img, (cx,cy),2,(0,0,255),2)
        mouseLoc=(sx-(cx*sx//camx), cy*sy//camy)
        mouse.position=mouseLoc 
        while mouse.position!=mouseLoc:
            pass
    elif(len(conts)==1):
        x,y,w,h=cv2.boundingRect(conts[0])
        if(pinchFlag==0):
            pinchFlag=1
            mouse.press(Button.left)
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        cx=x+w//2
        cy=y+h//2
        cv2.circle(img,(cx,cy),(w+h)//4,(0,0,255),2)
        mouseLoc=(sx-(cx*sx//camx), cy*sy//camy)
        mouse.position=mouseLoc 
        while mouse.position!=mouseLoc:
            pass
    cv2.imshow("mask1",mask1)   
    cv2.imshow("mask",mask)    
    cv2.imshow("cam",img)
    cv2.waitKey(5)

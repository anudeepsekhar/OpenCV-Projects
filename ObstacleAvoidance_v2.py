import cv2
import numpy as np
import math


def calc_dist(p1,p2):
    x1 = p1[0]
    y1 = p1[1]
    x2 = p2[0]
    y2 = p2[1]
    
    dist = np.sqrt((x2-x1)**2 + (y2-y1)**2)
    return dist

def getChunks(l, n):
    """Yield successive n-sized chunks from l."""
    a = []
    for i in range(0, len(l), n):
        
        a.append(l[i:i + n])
    return a

cap = cv2.VideoCapture(0)
StepSize = 5

while(1):
    _,frame = cap.read()
    # print(frame.shape)

    img = frame.copy()
    hsv = cv2.cvtColor(img,cv2.COLOR_RGB2HSV)
    gray = cv2.cvtColor(hsv,cv2.COLOR_RGB2GRAY)
    blur = cv2.bilateralFilter(img,9,40,40)
    edges = cv2.Canny(blur,50,100)
    # kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(2,2))
    # edges = cv2.erode(edges,(2,2),iterations = 1)

    img_h = img.shape[0] - 1
    img_w = img.shape[1] - 1
    EdgeArray = []
    for j in range(0,img_w,StepSize):
        for i in range(img_h-5,0,-1):
            if edges.item(i,j) == 255:
                pixel = (j,i)
                break
            else:
                pixel = (j,0)
        EdgeArray.append(pixel)

    for x in range(len(EdgeArray)-1):
        cv2.line(img, EdgeArray[x], EdgeArray[x+1], (0,255,0), 1)

    for x in range(len(EdgeArray)):
        cv2.line(img, (x*StepSize, img_h), EdgeArray[x],(0,255,0),1)
    
    chunks = getChunks(EdgeArray,int(len(EdgeArray)/5))
    max_dist = 0
    
    for i in range(len(chunks)):        
        x_vals = []
        y_vals = []
        for (x,y) in chunks[i]:
            x_vals.append(x)
            y_vals.append(y)

        avg_x = int(np.average(x_vals))
        avg_y = int(np.average(y_vals))
        cv2.line(frame,(320,480),(avg_x,avg_y),(255,0,0),2)
        dist = calc_dist([320,480],[avg_x,avg_y])
        
        if(dist>max_dist):
            max_dist = dist
            max_point = (avg_x,avg_y)
            
    cv2.line(frame,(320,480),max_point,(0,255,0),3)

    arg = math.degrees(math.atan2(480-max_point[1],320-max_point[0]))-90
    print arg
    
    if(max_dist < 1000):
        if(arg>-20 and arg<20):
            print("go straight")
        elif(arg>= 20):
            print("turn right")
        elif(arg<=-20):
            print("turn left")
    else:
        print("stop")

    cv2.imshow("frame",frame)
    cv2.imshow("Canny",edges)
    cv2.imshow("result",img)


    k = cv2.waitKey(0) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows

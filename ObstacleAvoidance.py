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
    

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    a = []
    for i in range(0, len(l), n):
        
        a.append(l[i:i + n])
    return a


cap = cv2.VideoCapture(0)
while(1):
    _,frame = cap.read()
    # print(frame.shape)

    img = frame.copy()

    hsv = cv2.cvtColor(img,cv2.COLOR_RGB2HSV)

    gray = cv2.cvtColor(hsv,cv2.COLOR_RGB2GRAY)

    blur = cv2.GaussianBlur(gray,(5,5),0)

    edges = cv2.Canny(blur,100,150)
    kerneld = np.ones((2, 2), np.uint8)
    edges = cv2.dilate(edges, kerneld)
    
    h,w = img.shape[:2]
    row_inds = np.indices((h,w))[0] # gives row indices in shape of img
    row_inds_at_edges = row_inds.copy()
    row_inds_at_edges[edges==0] = 0 # only get indices at edges, 0 elsewhere
    max_row_inds = np.amax(row_inds_at_edges, axis=0) # find the max row ind over each co
    inds_after_edges = row_inds >= max_row_inds
    filled_from_bottom = np.zeros((h, w))
    filled_from_bottom[inds_after_edges] = 255
    
    cords = []
    for i in range(len(max_row_inds)):
        cord = [i, max_row_inds[i]]
        cords.append(cord)
    p = chunks(cords,int(len(cords)/5))
    c = []
    max_dist = 0
    
    for i in range(5):        
        x_vals = []
        y_vals = []
        for j in range(len(p[i])):
            x_vals.append(p[i][j][0])
            y_vals.append(p[i][j][1])

        avg_x = sum(x_vals)/len(x_vals)
        avg_y = sum(y_vals)/len(y_vals)
        cv2.line(frame,(320,480),(int(avg_x),int(avg_y)),(255,0,0),2)
        dist = calc_dist([320,480],[avg_x,avg_y])
        
        if(dist>max_dist):
            max_dist = dist
            max_point = (avg_x,avg_y)
            
    cv2.line(frame,(320,480),max_point,(0,255,0),3)
    arg = math.degrees(math.atan2(480-max_point[1],320-max_point[0]))-90
    print arg
    
    kernele = np.ones((5, 5), np.uint8)
    filled_from_bottom = cv2.erode(filled_from_bottom, kernele)
    
    cv2.imshow('frame',frame)
    cv2.imshow('hsv',filled_from_bottom)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows

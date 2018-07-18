import cv2
import numpy as np


cap = cv2.VideoCapture(1)

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    a = []
    for i in range(0, len(l), n):
        
        a.append(l[i:i + n])
    return a

while(1):
    _,frame = cap.read()
    print(frame.shape)

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
    max_row_inds = np.amax(row_inds_at_edges, axis=0) # find the max row ind over each col
    cords = []

    for i in range(len(max_row_inds)):
        cord = [i, max_row_inds[i]]
        cords.append(cord)

##    print(cords) 
##    print(len(cords))

    p = chunks(cords,int(len(cords)/5))
##    print(p[0])
    c = []
    for i in range(5):
        
        x_vals = []
        y_vals = []
        for j in range(len(p[i])):
            x_vals.append(p[i][j][0])
            y_vals.append(p[i][j][1])

        avg_x = sum(x_vals)/len(x_vals)
        avg_y = sum(y_vals)/len(y_vals)
        cv2.line(frame,(320,480),(int(avg_x),int(avg_y)),(255,0,0),2)
        cx = avg_x - 320
        cy = 480 - avg_y
        c.append([cx,cy])
    print(c)
    res_x = 320
    res_y = 480
    for i in range(c):
        res_x += c[i][0]
        res_y -= c[i][1]
        
    if(res_y > 0):
        res_y = 0
    cv2.line(frame,(320,480),(int(res_x),int(res_y)),(0,255,0),3)
    ##    print (max_row_inds) 
    inds_after_edges = row_inds >= max_row_inds
    # print(inds_after_edges) 

    filled_from_bottom = np.zeros((h, w))
    filled_from_bottom[inds_after_edges] = 255

##    print(filled_from_bottom)
    
  
    kernele = np.ones((5, 5), np.uint8)
    filled_from_bottom = cv2.erode(filled_from_bottom, kernele)


    cv2.imshow('frame',frame)
    
    cv2.imshow('hsv',filled_from_bottom)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows

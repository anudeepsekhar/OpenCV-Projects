import cv2
import numpy as np 

img = cv2.imread('hh.jpg')

im = cv2.cvtColor(img,cv2.COLOR_BGR2YCrCb)
gray = cv2.equalizeHist(im[0])
gray = cv2.equalizeHist(im[3])
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
gray = cv2.equalizeHist(gray)
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
gray = clahe.apply(gray)
blur = cv2.GaussianBlur(gray,(5,5),0)
sobelx = cv2.Sobel(gray,cv2.CV_64F,1,0,ksize=3)
abs_sobelx = cv2.convertScaleAbs(sobelx)
sobely = cv2.Sobel(gray,cv2.CV_64F,0,1,ksize=3)
abs_sobely = cv2.convertScaleAbs(sobely)
res = cv2.addWeighted(abs_sobelx,0.5,abs_sobely,0.5,0)
res_norm = np.zeros_like(res)
res_norm = cv2.normalize(res,res_norm,0,255,cv2.NORM_MINMAX)
final = cv2.bilateralFilter(res_norm,3,10,10)
inv = cv2.bitwise_not(final)


cv2.imshow('Original',img)
cv2.imshow('res',inv)




cv2.waitKey(0)
cv2.destroyAllWindows()
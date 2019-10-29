# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 16:55:32 2019

@author: Artem
"""

import numpy as np
import cv2


cap = cv2.VideoCapture('test_images\\SampleVideo_1280x720_20mb.mp4')

while(True): 
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #cv2.imshow('Video', frame)

    ret, frame = cap.read()
    frame = np.asarray(frame)
    if (ret is False):
        exit
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()
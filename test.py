from picamera import PiCamera
from time import sleep
from time import time
from scipy.io import savemat
import os
import cv2
from fnc.extractFeature import extractFeature
from pygame import mixer
##
mixer.init()
d=input("enter your name")
sound = mixer.Sound('/home/pi/Downloads/enroll1.wav')
sound.play()
camera = PiCamera()
n=0
while n<7:
    n+=1
    m=str(n)
   #print(n)
    file_name="/home/pi/Downloads/python/data/"+d+m+".jpg"
    temp="/home/pi/Downloads/python/templates/"+d+m+".jpg"
    print(file_name)
    camera.start_preview()
    camera.brightness=60
    sleep(10)
               
    camera.stop_preview()

    #a='/home/pi/Downloads/Iris-RecextractFeatureognition-master/python/img'+d+'jpg'
    camera.capture(file_name)
    print("k")
    img=cv2.imread(file_name)
    #cv2.imwrite('/home/pi/Downloads/Iris-Recognition-master/python/data7/img1.png',img)
    cv2.imshow('image',img)
    cv2.waitKey(0)
    file=file_name
    print('>>> Enroll for the file ', file)
    template, mask, file = extractFeature(file)
##    cv2.imshow('imag1',template)
##    cv2.imshow('image',mask)
    print("d")

    # Save extracted feature
    basename = os.path.basename(file)

    out_file = os.path.join('/home/pi/Downloads/python/templates/', "%s.mat" % (basename))
    savemat(out_file, mdict={'template':template, 'mask':mask})
    print('>>> Template is saved in %s' % (out_file))
    cv2.destroyAllWindows()
sound = mixer.Sound('/home/pi/Downloads/enroll2.wav')
sound.play()

#cv2.waitKey(0)

#
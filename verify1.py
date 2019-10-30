##-----------------------------------------------------------------------------
##  Import
##-----------------------------------------------------------------------------
import argparse
from time import time
#from picamera import PiCamera
from time import sleep

from fnc.extractFeature import extractFeature
from fnc.matching import matching
import RPi.GPIO as gpio

import serial
import cv2
from pygame import mixer
from threading import *

mixer.init()



gpio.setwarnings(False)
gpio.setmode(gpio.BOARD)
gpio.setup(16,gpio.OUT)




ser=serial.Serial('/dev/ttyACM0',9600)

#camera = PiCamera()

parser = argparse.ArgumentParser()

##parser.add_argument("--file", type=str,
##                    help="Path to the file that you want to verify.")

parser.add_argument("--temp_dir", type=str, default="./templates/",
                                        help="Path to the directory containing templates.")

parser.add_argument("--thres", type=float, default=0.38,
                                        help="Threshold for matching.")

args = parser.parse_args()
a=input("fdb")
print(a)
if a=="b":
    print("k")
    gpio.output(16,True)

##-----------------------------------------------------------------------------
##  Execution
##-----------------------------------------------------------------------------
# Extract feature
##            camera.start_preview()
##            camera.brightness=60
##            sleep(20)
##                       
##            camera.stop_preview()
##
##            #a='/home/pi/Downloads/Iris-RecextractFeatureognition-master/python/img'+d+'jpg'
##            camera.capture('/home/pi/Downloads/img1.jpg')
file='/home/pi/Downloads/img1.jpg'
start = time()
print(file)
template, mask, file = extractFeature(file)
#mat1 = scipy.io.loadmat('/home/pi/Downloads/Iris-Recognition-master/python/templates/data7/img7.jpg.mat')
#mat2 = scipy.io.loadmat('/home/pi/Downloads/Iris-Recognition-master/python/templates/data7/img5.jpg.mat')
#c=mat1['template']
#b=mat2['template']
#c1=mat1['mask']
#b1=mat2['mask']

# Matching
result = matching(template, mask, args.temp_dir, args.thres)
##cv2.imshow('segment9',imageiris)
##cv2.waitKey(0)
##cv2.imshow('normalize',image)
##cv2.waitKey(0)
##cv2.imshow('encode1',template)
##cv2.waitKey(0)
##cv2.imshow('encode2',mask)
##cv2.waitKey(0)
##cv2.imshow('enco2',im)
##cv2.waitKey(0)
##cv2.imshow('ene2',im)
##cv2.waitKey(0)

if result == -1:
    print('>>> No registered sample.')
    ser.write("<Not Authenticated>".encode())
##    sound = mixer.Sound('/home/pi/Downloads/not authenticated.wav')
##    sound.play()
        

elif result == 0:
    print('>>> No sample matched.')
    ser.write("<Not Authenticated>".encode())
    sound = mixer.Sound('/home/pi/Downloads/not authenticated.wav')
    sound.play()

    gpio.output(16,False)
    

else:
    print('>>> {} samples matched (descending reliability):'.format(len(result)))
    for res in result:
            print("\t", res)
    ser.write("<Authenticated>".encode())
    sound = mixer.Sound('/home/pi/Downloads/authenticated.wav')
    sound.play()

    gpio.output(16,True)
        


# Time measure
end = time()
print('\n>>> Verification time: {} [s]\n'.format(end - start))
sleep(6)
gpio.cleanup()



from tkinter import *
from tkinter import messagebox
from picamera import PiCamera
from time import sleep
from time import time
from scipy.io import savemat
import os
import cv2
from fnc.extractFeature import extractFeature
import argparse
from fnc.matching import matching
import serial
import RPi.GPIO as gpio
from pygame import mixer

mixer.init()

top=Tk()
top.geometry('2000x1000')
top.configure(background="#5c6268")

B_c="#14cece"

ser=serial.Serial('/dev/ttyACM0',9600)

gpio.setwarnings(False)
gpio.setmode(gpio.BOARD)
gpio.setup(16,gpio.OUT)


def rpm():
    pass

def verification():
    top=Tk()
    top.geometry('2000x1000')
    top.configure(background="#5c6268")
    def verify():
        camera = PiCamera()

        #------------------------------------------------------------------------------
        #	Argument parsing
        #------------------------------------------------------------------------------
        parser = argparse.ArgumentParser()

        ##parser.add_argument("--file", type=str,
        ##                    help="Path to the file that you want to verify.")

        parser.add_argument("--temp_dir", type=str, default="./templates/",
                                                help="Path to the directory containing templates.")

        parser.add_argument("--thres", type=float, default=0.38,
                                                help="Threshold for matching.")

        args = parser.parse_args()


        ##-----------------------------------------------------------------------------
        ##  Execution
        ##-----------------------------------------------------------------------------
        # Extract feature
        camera.start_preview()
        camera.brightness=60
        sleep(10)
                   
        camera.stop_preview()

        #a='/home/pi/Downloads/Iris-RecextractFeatureognition-master/python/img'+d+'jpg'
        camera.capture('/home/pi/Downloads/img1.jpg')
        file='/home/pi/Downloads/img1.jpg'
        E2.delete(0,'end')
        E2.insert(0,file)
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

        if result == -1:
                print('>>> No registered sample.')
                E1.delete(0,'end')
                E1.insert(0,'FINISHED!!!')
                ser.write("<Not Authenticated>".encode())
                gpio.output(16,False)

        elif result == 0:
                ser.write("<Not Authenticated>".encode())
                print('>>> No sample matched.')
                E1.delete(0,'end')
                E1.insert(0,'No sample matched.')
                sound = mixer.Sound('/home/pi/Downloads/not authenticated.wav')
                sound.play()
                gpio.output(16,False)

        else:
                print('>>> {} samples matched (descending reliability):'.format(len(result)))
                for res in result:
                        print("\t", res)
                E1.delete(0,'end')
                E1.insert(0,' sample matched.')
                ser.write("<Authenticated>".encode())
                gpio.output(16,True)
                sound = mixer.Sound('/home/pi/Downloads/authenticated.wav')
                sound.play()


        # Time measure
        end = time()
        print('\n>>> Verification time: {} [s]\n'.format(end - start))
        E2.delete(0,'end')
        E2.insert(0,end-start)
        sleep(10)
        gpio.output(16,False)

        
    L1 = Label(top, text="VERIFICATION",fg="#14cece",bg="#5c6268",font=('Times',35,"bold"))
    L1.pack( side = LEFT)
    L1.place(x=500,y=100)
    
    B_10=Button(top,text="Veriify",command=verify,bg="black",fg=B_c,activebackground="green")
    B_10.place(x=600,y=500)
    
    L1 = Label(top, text="result",fg="#14cece",bg="#5c6268",font=('Times',15,"bold"))
    L1.pack( side = LEFT)
    L1.place(x=600,y=250)
    
    L1 = Label(top, text="procesing time",fg="#14cece",bg="#5c6268",font=('Times',15,"bold"))
    L1.pack( side = LEFT)
    L1.place(x=870,y=250)
    
    E1 = Entry(top, bd =2)
    E1.pack(side = RIGHT)
    E1.place(x=550,y=300)
    
    E2 = Entry(top, bd =2)
    E2.pack(side = RIGHT)
    E2.place(x=850,y=300)
    
        

def enrollment():
    top=Tk()
    top.geometry('2000x1000')
    top.configure(background="#5c6268")
    def enrol(k,j):
        if k=="a" and j=="j":         
            top=Tk()
            top.geometry('2000x1000')
            top.configure(background="#5c6268")
            def enroll(d):
                print(d)
                camera = PiCamera()
                n=0
                sound = mixer.Sound('/home/pi/Downloads/enroll1.wav')
                sound.play()
                while n<7:
                    n+=1
                    m=str(n)
                   #print(n)
                    file_name="/home/pi/Downloads/python/data/"+d+m+".jpg"
                    temp="/home/pi/Downloads/python/templates/"+d+m+".jpg"
                    print(file_name)
                    E2.delete(0,'end')
                    E2.insert(0,file_name)
                    camera.start_preview()
                    camera.brightness=60
                    sleep(7)
                               
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
                    E2.delete(0,'end')
                    E2.insert(0,'>>> Enroll for the file ')
                    template, mask, file = extractFeature(file)
                    cv2.imshow('imag1',template)
                    cv2.imshow('image',mask)
                    print("d")
            
                    # Save extracted feature
                    basename = os.path.basename(file)
            
                    out_file = os.path.join('/home/pi/Downloads/python/templates/', "%s.mat" % (basename))
                    savemat(out_file, mdict={'template':template, 'mask':mask})
                    print('>>> Template is saved in %s' % (out_file))
                    E2.delete(0,'end')
                    E2.insert(0,'>>> Template is saved ')
                    cv2.destroyAllWindows()
                E2.delete(0,'end')
                E2.insert(0,'FINISHED!!!')
                sound = mixer.Sound('/home/pi/Downloads/enroll2.wav')
                sound.play()
                        
            L1 = Label(top, text="ENROLLMENT",fg="#14cece",bg="#5c6268",font=('Times',35,"bold"))
            L1.pack( side = LEFT)
            L1.place(x=500,y=100)
            
            L1 = Label(top, text="1.Enter your name",fg="#14cece",bg="#5c6268",font=('Times',15,"bold"))
            L1.pack( side = LEFT)
            L1.place(x=550,y=200)
            
            E1 = Entry(top, bd =2)
            E1.pack(side = RIGHT)
            E1.place(x=550,y=300)
            
            E2 = Entry(top, bd =2)
            E2.pack(side = RIGHT)
            E2.place(x=850,y=500)
            
            L1 = Label(top, text="2.After entering user name click th enroll button to proceed ",fg="#14cece",bg="#5c6268",font=('Times',15,"bold"))
            L1.pack( side = LEFT)
            L1.place(x=430,y=400)
            
            L1 = Label(top, text="""(Note:Press "0" after each and every image enrollment to continue the process)""",fg="#14cece",bg="#5c6268",font=('Times',15,"bold"))
            L1.pack( side = LEFT)
            L1.place(x=380,y=550)
            
            L1 = Label(top, text="Current Status",fg="#14cece",bg="#5c6268",font=('Times',15,"bold"))
            L1.pack( side = LEFT)
            L1.place(x=850,y=450)
            
            B_10=Button(top,text="ENROLL",command=lambda:enroll(E1.get()),bg="black",fg=B_c,activebackground="green")
            B_10.place(x=600,y=500)
            
            top.mainloop()
        else:
            top=Tk()
            top.geometry('400x100')
            
            
            L1 = Label(top, text="username password doesnt match",fg="#14cece",bg="#5c6268",font=('Times',12,"bold"))
            L1.pack( side = LEFT)
            L1.place(x=50,y=50)
            
    L1 = Label(top, text="SIGN IN",fg="#14cece",bg="#5c6268",font=('Times',25,"bold"))
    L1.pack( side = LEFT)
    L1.place(x=600,y=150)
    
    L1 = Label(top, text="USERNAME :",fg="#14cece",bg="#5c6268",font=('Times',15,"bold"))
    L1.pack( side = LEFT)
    L1.place(x=430,y=250)
    
    L1 = Label(top, text="PASSWORD :",fg="#14cece",bg="#5c6268",font=('Times',15,"bold"))
    L1.pack( side = LEFT)
    L1.place(x=430,y=350)
    
    E1 = Entry(top, bd =2)
    E1.pack(side = RIGHT)
    E1.place(x=750,y=250)
                
    E2 = Entry(top, bd =2,show="*")
    E2.pack(side = RIGHT)
    E2.place(x=750,y=350)

    B_10=Button(top,text="LOGIN",command=lambda:enrol(E1.get(),E2.get()),bg="black",fg=B_c,activebackground="green")
    B_10.place(x=600,y=450)
        
            
    

    

L1 = Label(top, text="IRIS RECOGNITION DOOR LOCK SYSTEM",fg="#14cece",bg="#5c6268",font=('Times',35,"bold"))
L1.pack( side = LEFT)
L1.place(x=230,y=150)

B_10=Button(top,text="ENROLLMENT",command=enrollment,bg="black",fg=B_c,activebackground="green")
B_10.place(x=600,y=300)

B_11=Button(top,text="VERIFICATION",command=verification,bg="black",fg=B_c,activebackground="green")
B_11.place(x=600,y=400)

top.mainloop()


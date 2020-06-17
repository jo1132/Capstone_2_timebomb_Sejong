#This is the work of Sejong Univ's Time Bombs.
#The subject is pedestrian detection, vehicle detection, crosssection detection
#The distinction of car types is incomplete.
#I hope it helps
#
#
#

import sys
import cv2
import numpy as np
import time
import object
import socket

#here 

HOST = '192.168.1.3'  #IP Address

PORT = 12345



client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((HOST,PORT))

msg = "C_pi"           #client name A to D

length = len(msg)

data = msg.encode()

client_socket.send(length.to_bytes(4, byteorder='big'))

client_socket.send(data)

#time.sleep(1)

#here end


#car haarcascade
car_classifier = cv2.CascadeClassifier('haarcascade_car6.xml')

#capVideo
cap = cv2.VideoCapture('video/sam2.mp4')


#Save a Video
"""
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('video/output7.mp4', fourcc, 30.0, (int(width), int(height)))
"""

#BackgroundSubtractorMOG2
fgbg = cv2.createBackgroundSubtractorMOG2(detectShadows=False, history=200, varThreshold=90)

#kernalOp
kernalOp = np.ones((3, 3), np.uint8)
kernalOp2 = np.ones((5, 5), np.uint8)
kernalCl = np.ones((11, 11), np.uint8)

#init ped_objs
font = cv2.FONT_HERSHEY_SIMPLEX
objs = []
max_p_age = 30
pid = 1

#car info
cnt_in = 0
cnt_out = 0
car_num = 0

#car Line - you need setting
line_in = 185
line_out = 322
line_invade = 330

#num
ped_cnt = 0
car_cnt = 0
car_flag= True

#car class
moto_cnt = 0
car_nomal = 0

#ped Line - you need setting
left_in = 135
left_out = 742

right_in = 745
right_out = 105

#Set the area to show in the frame
#car point init
point1 = np.array([[378,220],[472,220],[440,335],[317,335]], np.int32)

#else car point init
point2 = np.array([[280,180],[397,180],[313, 336],[150,336]], np.int32)

#ped point init
point3 = np.array([[70,340],[780,340],[780,452],[50,452]], np.int32)


#Car State
c_state1 = 'Car State : Exist'
c_state2 = 'Car State : '

#Ped State
p_state1 = 'Ped State : Exist' 
p_state2 = 'Ped State : None' 
        

while (cap.isOpened()):
    ret, frame = cap.read()
    
    #frame resize
    frame = cv2.resize(frame, (800, 480))

    #test car1 section
#	car1 = frame.copy
#	car1 = frame[300:300 + 105, 325:416]
#	car = cv2.resize(car1, dsize=(0,0), fx=2.0,fy=2.0,interpolation = cv2.INTER_LINEAR)
#	car1 = cv2.rectangle(car1, (0, 0), (91 - 1, 105 - 1), (0, 255, 255))
	
    #Car frame init
    car = frame.copy
    car = frame[220:220 + 130 , 325:475]
    #car1 = cv2.resize(car, dsize=(0,0), fx=2.0, fy=2.0, interpolation = cv2.INTER_LINEAR)
    
    #car original frame
    #car = cv2.rectangle(car, (0, 0), (130 - 1, 150 - 1), (0, 255, 255))
	    
    #car show frame
    frame = cv2.polylines(frame, [point1], True, (0,0,255),2)
    
    #Car1 frame init
    car1 = frame.copy
    car1 = frame[130:130+230, 140:360]
    
    #car1 original frame
    #car1 = cv2.rectangle(car1,(0,0), (220-1, 230-1), (255,0,0),2) 
     
    #car1 show frame
    frame = cv2.polylines(frame, [point2], True, (255,255,0),2)
    
    gray = cv2.cvtColor(car, cv2.COLOR_BGR2GRAY)
    
    #Ped frame init
    ped = frame.copy
    ped = frame[337:472, 50:790]
    
    #ped original frame
    #ped = cv2.rectangle(ped, (0, 0), (660 - 1, 80 - 1), (0, 255, 255),2)
    
    #ped rectangle show frame
    #frame = cv2.rectangle(frame, (100,302), (740, 412), (0,255,255),2)
    
    #ped show frame
    frame = cv2.polylines(frame, [point3], True, (0,255,255),2)
    
    cars = car_classifier.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=9,
        minSize=(50, 40),
        maxSize=(60,70),
    )

    #Car Section
    for (x, y, w, h) in cars:
        #car = cv2.rectangle(car, (int(x*0.7), y), (int((x + w)*0.7), y + h), (0, 255, 0), 2)    
        car = cv2.rectangle(car, (x, y), (x + w, y + h), (0, 255, 0), 2)    

        car_cnt = 1
        
        if car_cnt == 1: 
            cv2.putText(frame, c_state1 , (10, 60), font, 0.5, (0, 0, 255), 2, cv2.LINE_AA)
        #print("car")
	  
    car_flag = False
     
    if car_flag == False:    
        cv2.putText(frame, c_state2 , (10, 60), font, 0.5, (0, 0, 255), 2, cv2.LINE_AA)        
    car_flag = True
         
    for i in objs:
       i.age_one()
        
    fgmask = fgbg.apply(frame)
    
    if ret == True:
        ret, imBin = cv2.threshold(fgmask, 200, 255, cv2.THRESH_BINARY)
        mask = cv2.morphologyEx(imBin, cv2.MORPH_OPEN, kernalOp)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernalCl)

        (countours0, hierarchy) = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        for cnt in countours0:
            area = cv2.contourArea(cnt)
            
            #ped area - you need setting
            if (area > 350 and area <1400) or (area > 2100 and area< 2400): 
                  
                #image moment
                m = cv2.moments(cnt)
                cx = int(m['m10'] / m['m00'])
                cy = int(m['m01'] / m['m00'])
                x, y, w, h = cv2.boundingRect(cnt)

                new = True
				        
                #Set pedestrian recognition area
                # ped section
                if cx in range(70, 790):
                    if cy in range(345, 452):
                        #print(area)
                        
                        for i in objs:
                            if abs(x - i.getX()) <= w and abs(y - i.getY()) <= h:
                                new = False
                                i.updateCoords(cx, cy)

                                #Ped State
                                if i.going_LEFT_IN(left_in, right_in) == True:
                                    ped_cnt += 1

                                elif i.going_LEFT_OUT(left_in, left_out) == True:
                                    ped_cnt -= 1
                                    
                                elif i.going_RIGHT_IN(left_in, right_in) == True:
                                    ped_cnt += 1

                                elif i.going_RIGHT_OUT(right_out, right_in) == True:
                                    ped_cnt -= 1                               
                                break
                            
                            #Ped setDone()
                            if i.getState() == '1':
                                if i.getDir() == 'left_in' and i.getX() > left_out:
                                    i.setDone()
                                elif i.getDir() == 'right_in' and i.getX() < right_out:
                                    i.setDone()

                            if i.timedOut():
                                index = objs.index(i)
                                objs.pop(index)
                                del i
                        
                        #new_obj    
                        if new == True:
                            p = object.Obj(pid, cx, cy, max_p_age)
                            objs.append(p)
                            pid + 1
                        
                        
                        cv2.circle(frame, (cx, cy), 2, (0, 0, 255), -1)
                        img = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2)
            
            #Car section
            #Car area - you need setting
            if (area > 2400 and area < 11000) or (area > 600 and area < 1500):
                
                #image moment
                m = cv2.moments(cnt)
                cx = int(m['m10'] / m['m00'])
                cy = int(m['m01'] / m['m00'])
                x, y, w, h = cv2.boundingRect(cnt)
                
                new = True
           
                #Set car recognition area
                # car section
                if cx in range(150, 350):
                    if cy in range(180, 340):
                        #print(area)
                        
                        for i in objs:
                             if abs(x - i.getX()) <= w and abs(y - i.getY()) <= h:
                                new = False
                                i.updateCoords(cx, cy)
                                
                                if i.going_CAR_IN(line_in, line_out)==True:
                                    #if you want classify car 
                                    #this is sample code
                                    """
                                    if area > 600 and area <1500:
                                        moto_cnt+=1
                                    elif area > 2400 and area < 11000:
                                        car_nomal+=1
                                    """
                                        
                                    cnt_in+=1
                                        
                                elif i.going_CAR_OUT(line_in, line_out)==True:
                                    #if you want classify car 
                                    #this is sample code
                                    """
                                    if area > 600 and area <1500:
                                        moto_cnt-=1
                                    elif area > 2400 and area < 11000:
                                        car_nomal-=1
                                    """    

                                    cnt_out+=1
                                
                                #car invade center line or car change line                                              
                                elif i.getDir()!='in' and i.going_invade_left(line_invade, line_invade)==True:
                                
                                    cnt_in+=1 
                                 
                                elif i.getDir()=='in' and i.going_invade_right(line_invade, line_invade)==True:
                                    cnt_out+=1
                                    
                                car_num = cnt_in - cnt_out
                                break
                             
                             #state recognize       
                             if i.getState()=='1':
                                 if i.getDir()=='in' and i.getY()>line_out+10:
                                     i.setDone()
                                     
                                 elif i.getDir()=='out' and i.getY()>line_out+10:
                                     i.setDone()
                                     
                                 elif i.getDir()=='left' and i.getX()<line_invade-10:
                                     i.setDone()
                                     
                                 elif i.getDir()=='right' and i.getX()>line_invade+10:
                                     i.setDone()    
                             
                             if i.timedOut():
                                 index=objs.index(i)
                                 objs.pop(index)
                                 del i                        
                               
                        if new == True:
                            p = object.Obj(pid, cx, cy, max_p_age)
                            objs.append(p)
                            pid + 1
                            
                        cv2.circle(frame, (cx, cy), 2, (0, 0, 255), -1)
                        img = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                
        
        #text template
        str_ped = 'Ped Num : ' + str(ped_cnt)
        str_in = 'IN : ' + str(cnt_in)
        str_out = 'OUT : ' + str(cnt_out)
        
        str_car = 'Car Num : ' + str(car_num)
        str_moto = 'Moto Cycle : ' + str(moto_cnt)
        str_nomal = 'Car : ' + str(car_nomal) 
        str_title = '[Car L-Section Info]'
        str_line = '----------------' 
        
        #Ped signal
        if ped_cnt != 0:
            cv2.putText(frame, p_state1 , (10, 90), font, 0.5, (0, 255, 255), 2, cv2.LINE_AA)
            #print('ped')
        else:
            cv2.putText(frame, p_state2 , (10, 90), font, 0.5, (0, 255, 255), 2, cv2.LINE_AA)
        
        
        
        #this is car and ped line
        """
        #Ped detect line
        frame = cv2.line(frame, (left_in, 340), (left_in, 452), (0, 0, 255), 2, 8)
        frame = cv2.line(frame, (right_in, 340), (right_in, 452), (0, 0, 255), 2, 8)
        
        #Ped detect limit line
        frame = cv2.line(frame, (left_out, 340), (left_out, 452), (0,0, 255), 1,8)
        frame = cv2.line(frame, (right_out, 340), (right_out, 452), (0,0,255),1,8)
        
        #Car detect line
        frame = cv2.line(frame, (130, line_in), (350, line_in), (0,0,255),2,8)
        frame = cv2.line(frame, (130, line_out), (350, line_out), (0,0,255),2,8)
        
        #Car invasion line
        frame = cv2.line(frame, (line_invade, line_in), (line_invade, line_out), (255,255,0), 2, 8)
        """
        
        #Text
        #cv2.putText(frame, str_ped , (550, 120), font, 0.7, (255, 255, 0), 2, cv2.LINE_AA)         
        cv2.putText(frame, str_title, (10,145), font, 0.7, (255,255,0), 2, cv2.LINE_AA)
        #cv2.putText(frame, str_in , (10, 180), font, 0.5, (255,255,0) , 2, cv2.LINE_AA)
        #cv2.putText(frame, str_out , (10, 210), font, 0.5, (255,255,0) , 2, cv2.LINE_AA)
        #cv2.putText(frame, str_moto , (10, 170), font, 0.5, (255,255,0) , 2, cv2.LINE_AA)
        #cv2.putText(frame, str_nomal , (10, 200), font, 0.5, (255,255,0) , 2, cv2.LINE_AA)
        cv2.putText(frame, str_line , (10, 170), font, 0.5, (255,255,0) , 2, cv2.LINE_AA)
 
        cv2.putText(frame, str_car , (10, 200), font, 0.5, (255,255,0) , 2, cv2.LINE_AA)
         
        
        #cv2.imshow('detect', frame)
        #out.write(frame)
        
        #cv2.imshow('Car', car)
        #cv2.imshow('Car1', car1)
        #cv2.imshow('Pedestrian', ped)

        if cv2.waitKey(1) & 0xff == ord('q'):
            break

    else:
        break

        #here

    try:
        
        
        if ped_cnt==0:
            A_cro = "0"
        else:
            A_cro = "1"

        
        if car_cnt == 1:
            A_Lcar = "1"
        else:
            A_Lcar = "0"


        A_Carnum = str(car_num)
        msg = A_cro+A_Lcar+A_Carnum
        msg3 = msg.encode()

        client_socket.send(msg3)

        #time.sleep(1)

        print("sending")

    except Exception as e:

        print (e)

    finally:

 #       client_socket.close()

        print ("end")
        
    car_cnt = 0



client_socket.close()

#here end 


cap.release()
cv2.destroyAllWindows()

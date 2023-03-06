import cv2
import sys
sys.path.append("/home/pi/FR_system/cdac_employee_detection-master/")

from threading import Thread
import psycopg2
import numpy as np
from threading import Thread
import requests
import os
from datetime import datetime as dt
import fr_system_dl
from imutils.video import VideoStream
import face_recognition
import imutils
import pickle
import time


ds_factor=0.6

class VideoCamera(object):
    def __init__(self):
        #self.video = cv2.VideoCapture(2)
        
        self.video = VideoStream(src=0).start()
        time.sleep(2.0) # After starting stream, allowing camera to warm up
       
        self.recog_thresh = 1.0
        self.input_resolution = 112
        self.input_image_size  = 160
        self.margin = 0
        self.thresh = 0.8
        self.count = 1
        self.detect_multiple_faces = 0
        
        
        self.frame=None
        self.recognition_queue = ["UNKNOWN", "UNKNOWN"]#, "UNKNOWN"]
        self.result = None
        #self.start()
    
    def get_frame(self):
        image = self.video.read()
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = imutils.resize(image, width=640)
        #if dt.now().time().second%1==0:
        #    ret, jpeg = cv2.imencode('.jpg', image)
        #    print(self.recognition_queue)
        #    return jpeg.tobytes()
        
        print(type(image))
        
        image, username = fr_system_dl.main(image)
        
        
        if username != "No Face" and username != "Unknown":
            # if self.recognition_queue[0]== self.recognition_queue[1] == self.recognition_queue[2] != "NO FACE"  :
            # data = {"username":self.result}
            # requests.post("http://localhost:5010/empdet", data=data)
            # os.environ["RESULT"] = self.result
            with open("username.txt", 'w') as f:
                f.write(username)
            
        text_x = 20
        text_y = 30
        cv2.putText(image, str(username), (text_x, text_y), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (50, 205, 50),
                    thickness=2, lineType=1)
        
        ret, jpeg = cv2.imencode('.jpg', image[:,:,::-1])
        print(self.recognition_queue)
        return jpeg.tobytes()
    
    def __del__(self):
        self.video.stop()
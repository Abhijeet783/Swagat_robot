import cv2
import sys
sys.path.append("/home/pi/FR_system/cdac_employee_detection-master/")

from threading import Thread
import tensorflow as tf
#from resources import SupportMethods
from models.detector.mtcnn import detect_and_align
from models.verifier.facenet import facenet
import psycopg2
import numpy as np
from threading import Thread
import fr_system
import requests
import os
from datetime import datetime as dt

ds_factor=0.6

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(2)
        
        self.recog_thresh = 1.0
        self.input_resolution = 112
        self.input_image_size  = 160
        self.margin = 0
        self.thresh = 0.8
        self.count = 1
        self.detect_multiple_faces = 0
        
        #detector = RetinaFaceCoV('./models/detector/RetFaceCov/model/mnet_cov2', 0, gpuid, 'net3l')
        self.graph_face = tf.Graph()
        self.sess_face = tf.Session(graph=self.graph_face)
        with self.graph_face.as_default():
            with self.sess_face.as_default():
                self.pnet, self.rnet, self.onet = detect_and_align.create_mtcnn(self.sess_face, None)
        
        self.frame=None
        self.grabbed = False
        self.stopped = False
        self.recognition_queue = ["UNKNOWN", "UNKNOWN"]#, "UNKNOWN"]
        self.result = None
        #self.start()
        
    def start(self):
        # start the thread to read frames from the video stream
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        # keep looping infinitely until the thread is stopped
        while True:
            # if the thread indicator variable is set, stop the thread
            if self.stopped:
                return
            # otherwise, read the next frame from the stream
            (self.grabbed, self.frame) = self.video.read()
    
    def stop(self):
         self.stopped=True
         
    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        ret, image = self.video.read()
        #if dt.now().time().second%1==0:
        #    ret, jpeg = cv2.imencode('.jpg', image)
        #    print(self.recognition_queue)
        #    return jpeg.tobytes()
        
        print(type(image))
        
        image, username = fr_system.main(image)
        
        if username is not None:
            self.recognition_queue.pop()
            self.recognition_queue.insert(0, username)

        if self.recognition_queue[0] == self.recognition_queue[1] != "UNKNOWN":
            self.result = self.recognition_queue[0]

            text_x = 20
            text_y = 60
            cv2.putText(image, str(self.result), (text_x, text_y), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (50, 205, 50),
                        thickness=2, lineType=1)
            # Write speak out code here

        elif self.recognition_queue[0] == self.recognition_queue[1] == "UNKNOWN":
            self.result = self.recognition_queue[0]

        elif self.recognition_queue[0] != self.recognition_queue[1] != "NO FACE":
            self.result = "UNKNOWN" 

        else:
            self.result = "NO FACE"

        text_x = 20
        text_y = 60
        cv2.putText(image, str(self.result), (text_x, text_y), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (50, 205, 50),
                    thickness=2, lineType=1)

        if self.result != "NO FACE" and self.result != "UNKNOWN":
            # if self.recognition_queue[0]== self.recognition_queue[1] == self.recognition_queue[2] != "NO FACE"  :
            # data = {"username":self.result}
            # requests.post("http://localhost:5010/empdet", data=data)
            # os.environ["RESULT"] = self.result
            with open("username.txt", 'w') as f:
                f.write(self.result)

        ret, jpeg = cv2.imencode('.jpg', image)
        print(self.recognition_queue)
        return jpeg.tobytes()
        
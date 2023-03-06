from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
#import simpleaudio as sa
import cv2
import numpy as np
#from model.align import detect_face
import sys
sys.path.append("/home/pi/FR_system/cdac_employee_detection-master/")
import os
import time
import cv2
import json
import shutil
import glob
from datetime import datetime as dt
from resources import SupportMethods
#from models.detector.RetFaceCov.retinaface_cov import RetinaFaceCoV
from models.detector.mtcnn import detect_and_align
from models.verifier.facenet import facenet
from datetime import datetime as dt
import psycopg2
import tensorflow as tf
import mariadb
import traceback
import asyncio
import websockets
import requests
from threading import Thread
import time 

class VideoCamera():
    
    def __init__(self):
        
        self.cap = cv2.VideoCapture(2)
        
        self.frame=self.cap.read()[1]
        #print(self.frame)
        self.grabbed = False
        self.stopped = False
        
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
            (self.grabbed, self.frame) = self.cap.read()
            #print(self.frame)
            
             
    def stop(self):
         self.stopped=True
         
    def __del__(self):
        self.cap.release()
        

def main():

    print('Initializing application....')
    np.random.seed(1234)
    #net = SupportMethods.build_rface()

    ## Parameters
    recog_thresh = 1.0
    input_resolution = 112
    input_image_size  = 160
    margin = 0
    thresh = 0.8
    mask_thresh = 0.2
    count = 1
    gpuid = -1

    #detector = RetinaFaceCoV('./models/detector/RetFaceCov/model/mnet_cov2', 0, gpuid, 'net3l')
    graph_face = tf.Graph()
    sess_face = tf.Session(graph=graph_face)
    with graph_face.as_default():
        with sess_face.as_default():
            pnet, rnet, onet = detect_and_align.create_mtcnn(sess_face, None)
            
    recog_thresh = 0.94
    input_resolution = 112
    margin = 0
    detect_multiple_faces = 0

    print('Start Recognition.......')
    #cap = cv2.VideoCapture(2)
    cap = VideoCamera()
    cap.start()
    fr_interval = 2  
    frame_count = 0
    while (True):
        t0 = time.perf_counter()
        # Capture frame-by-frame
        #ret, frame = cap.read()
        frame = cap.frame
        #print(frame)
        #frame = cv2.imread("data/testing_image.jpg")
        #frame = cv2.resize(frame, (640,480))
        #frame_org = np.copy(frame)
        imagedata = np.copy(frame)
        imagedata = imagedata[:,:,::-1]
        
        ########### Face detection of frame #################
        t1 = time.perf_counter()
        #num_faces, face, bboxes = SupportMethods.get_aligned_face_mtcnn(pnet, rnet, onet, imagedata, detect_multiple_faces, margin, input_resolution)
        num_faces, landmarks, bboxes, face_detection_score, cropped_faces = detect_and_align.get_face(
                                                    None, pnet, rnet, onet, imagedata, detect_multiple_faces, margin)                                                                                                 

        if num_faces > 0:
            face = cropped_faces[0]
            box = np.array(bboxes[0:4]).astype(np.int)
            y1 = box[0]
            x1 = box[1]
            y2 = box[2]
            x2 = box[3]
            color = (0,255,0)
            cv2.rectangle(frame, (y1, x1), (y2, x2), color, 2)
           
        
        cv2.imshow("frame1", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        print(f"Time in Face Recognition:{(time.perf_counter()-t0)}\n")
        #break
        
    #cap.release()
    cv2.destroyAllWindows()



if __name__ == '__main__':

    main()  







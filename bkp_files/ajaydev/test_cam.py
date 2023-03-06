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
import fr_system
import requests
import os
from datetime import datetime as dt
import time 

ds_factor=0.6

class VideoCamera(object):
    def __init__(self):
        #self.video = cv2.VideoCapture("/home/pi/FR_system/cdac_employee_detection-master/data/FR_test_video.mp4")  #2
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
        
        do_flip=True
        t1 = time.perf_counter()
        imagedata = image
        #num_faces, face, bboxes = SupportMethods.get_aligned_face_mtcnn(pnet, rnet, onet, imagedata, detect_multiple_faces, margin, input_resolution)
        num_faces, landmarks, bboxes, face_detection_score, cropped_faces = detect_and_align.get_face(
                                                None, self.pnet, self.rnet, self.onet, imagedata, self.detect_multiple_faces, self.margin)                                                                                                 
        #print(num_faces, bboxes, landmarks)
        #print("Time in detect_and_align:", time.perf_counter()-t1)
        if num_faces == 0 :
            RESULT = "No FACE"

        elif num_faces > 0:
            # Write speak out code here
            #play(AudioSegment.from_file('/home/pi/SwagatNew/static/msg1.wav'))
            #play(AudioSegment.from_file('/home/pi/SwagatNew/static/msg2.wav'))
            #play(AudioSegment.from_file('/home/pi/SwagatNew/static/msg3.wav'))
            
            face = cropped_faces[0]
            box = np.array(bboxes[0:4]).astype(np.int)
            y1 = box[0]
            x1 = box[1]
            y2 = box[2]
            x2 = box[3]
            color = (0,255,0)
            cv2.rectangle(image, (y1, x1), (y2, x2), color, 2)
            
            ######### Get embedding ########

            # t11 = time.perf_counter()
            face = cv2.resize(face, (self.input_image_size, self.input_image_size), interpolation=cv2.INTER_NEAREST)
            face = facenet.prewhiten(face)
            
            #cv2.imwrite("/temp_data/face.jpg", face)
    
        ret, jpeg = cv2.imencode('.jpg', image)
        #print(self.recognition_queue)
        return jpeg.tobytes()
        
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

ds_factor=0.6

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        
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
    
    
    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        success, image = self.video.read()
        print(type(image))
        image=cv2.resize(image,None,fx=ds_factor,fy=ds_factor,interpolation=cv2.INTER_AREA)
        image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        num_faces, landmarks, bboxes, face_detection_score, cropped_faces = detect_and_align.get_face(
                                                    None, self.pnet, self.rnet, self.onet, image, self.detect_multiple_faces, self.margin)
        
        if num_faces>0:
            box = np.array(bboxes[0:4]).astype(np.int)
            y1 = box[0]
            x1 = box[1]
            y2 = box[2]
            x2 = box[3]
            color = (0,255,0)
            cv2.rectangle(image, (y1, x1), (y2, x2), color, 2)
        
        
        ret, jpeg = cv2.imencode('.jpg', image[:,:,::-1])
        return jpeg.tobytes()
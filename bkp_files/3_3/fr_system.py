from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
#import simpleaudio as sa
import cv2
import numpy as np
#from model.align import detect_face
import sys
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
import traceback
from pydub import AudioSegment
from pydub.playback import play

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
        
        modeldir = '/home/pi/FR_system/cdac_employee_detection-master/models/verifier/facenet/20170511-185253-128/20170511-185253.pb'
        facenet.load_model(modeldir)

        images_placeholder = tf.get_default_graph().get_tensor_by_name("input:0")
        embeddings = tf.get_default_graph().get_tensor_by_name("embeddings:0")
        phase_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0")
        embedding_size = embeddings.get_shape()[1]
        

enrollfolder_JSON_path = '/home/pi/FR_system/cdac_employee_detection-master/enrollment_data/'
#json_paths = glob.glob(enrollfolder_JSON_path+'/**/JSON/*.json')

features, labels, names = SupportMethods.read_json_from_paths(enrollfolder_JSON_path)

recognistion_queue = ['UNKNOWN', 'UNKNOWN', 'UNKNOWN']
recog_thresh = 0.90
input_resolution = 112
margin = 0

#print('Start Recognition.......')
#cap = cv2.VideoCapture(2)
#frame_wait_count = 200 #100
#frame_wait_duration = 100 #50
last_username = 'UNKNOWN'
recog_flag = 0
whiteheader = cv2.imread("/home/pi/FR_system/cdac_employee_detection-master//data/header.png")
detect_multiple_faces = 1
margin = 0
input_resolution = 112

fr_interval = 2  
frame_count = 0

def main(frame):
    imagedata = np.copy(frame)
    imagedata = imagedata[:,:,::-1]
    
    RESULT = None
    
    emb_array = np.zeros((1, embedding_size))
    do_flip=True
    t1 = time.perf_counter()
    #num_faces, face, bboxes = SupportMethods.get_aligned_face_mtcnn(pnet, rnet, onet, imagedata, detect_multiple_faces, margin, input_resolution)
    num_faces, landmarks, bboxes, face_detection_score, cropped_faces = detect_and_align.get_face(
                                            None, pnet, rnet, onet, imagedata, detect_multiple_faces, margin)                                                                                                 
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
        cv2.rectangle(frame, (y1, x1), (y2, x2), color, 2)
          
        
        if dt.now().time().second%20==0:
            
            ######### Get embedding ########

            # t11 = time.perf_counter()
            face = cv2.resize(face, (input_image_size, input_image_size), interpolation=cv2.INTER_NEAREST)
            face = facenet.prewhiten(face)

            feed_dict = {images_placeholder: [face], phase_train_placeholder: False}
            emb_array[0, :] = sess_face.run(embeddings, feed_dict=feed_dict)
            # predictions = model.predict_proba(emb_array)
            print(emb_array.shape)
            # t12 = time.perf_counter()
            #print("Time in Feature Extraction:", (t12-t11))

            # t3 = time.perf_counter()
            embedding = emb_array[0]
            D,I = SupportMethods.record_search1(embedding, features)
            dist = D#[0][0]
            label_idx = I#[0][0]
            
            if dist<recog_thresh:
                RESULT = labels[label_idx]
            
            else:
                RESULT = "Visitor"
            
                
            print(f"{RESULT}\t{dist}")
            # print("Time in Feature Comparision:", time.perf_counter()-t3)
    
    #text_x = 20
    #text_y = 60
    #cv2.putText(frame, str(RESULT), (text_x, text_y), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (50,205,50),thickness=2,lineType=1)
        #print("FR Update Status:", updateFrRecord(RESULT, dt.now().time().isoformat()))


    return frame, RESULT 



if __name__ == '__main__':

    main()  







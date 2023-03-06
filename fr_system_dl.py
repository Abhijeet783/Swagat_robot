from imutils.video import VideoStream
import face_recognition
import argparse
import imutils
import pickle
import time
import cv2


# load the known faces and embeddings
print("[INFO] loading encodings...")
data = pickle.loads(open("/home/pi/SwagatNew/data/enrolled_users.pkl", "rb").read())

# loop over frames from the video file stream
def main(frame):
    
    # convert the input frame from BGR to RGB then resize it to have
    # a width of 750px (to speedup processing)
    r = frame.shape[1] / float(frame.shape[1])
    # detect the (x, y)-coordinates of the bounding boxes
    # corresponding to each face in the input frame, then compute
    # the facial embeddings for each face
    boxes = face_recognition.face_locations(frame,
                                            model="hog")
    encodings = face_recognition.face_encodings(frame, boxes)
    names = []
    name = "No Face"
    # loop over the facial embeddings
    for encoding in encodings[:1]:
        # attempt to match each face in the input image to our known
        # encodings
        matches = face_recognition.compare_faces(data["encodings"],
                                                 encoding, tolerance=0.48)
        name = "Unknown"
        # check to see if we have found a match
        if True in matches:
            # find the indexes of all matched faces then initialize a
            # dictionary to count the total number of times each face
            # was matched
            matchedIdxs = [i for (i, b) in enumerate(matches) if b]
            counts = {}
            # loop over the matched indexes and maintain a count for
            # each recognized face face
            for i in matchedIdxs:
                name = data["names"][i]
                counts[name] = counts.get(name, 0) + 1
            # determine the recognized face with the largest number
            # of votes (note: in the event of an unlikely tie Python
            # will select first entry in the dictionary)
            name = max(counts, key=counts.get)

        # update the list of names
        names.append(name)

        # loop over the recognized faces
        for ((top, right, bottom, left), name) in zip(boxes, names):
            # rescale the face coordinates
            top = int(top * r)
            right = int(right * r)
            bottom = int(bottom * r)
            left = int(left * r)
            # draw the predicted face name on the image
            cv2.rectangle(frame, (left, top), (right, bottom),
                          (0, 255, 0), 2)
            y = top - 15 if top - 15 > 15 else top + 15
            cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
                        0.75, (0, 255, 0), 2)

    return frame, name


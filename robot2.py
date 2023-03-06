from flask import Flask
from flask import render_template, request, Response
from test_cam import VideoCamera 
import RPi.GPIO as GPIO
import time
import MySQLdb

import os

app = Flask(__name__)


#Motor GPIO Pin numbers for Navigation
m11=26
m12=19
m21=13
m22=21


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(m11, GPIO.OUT)
GPIO.setup(m12, GPIO.OUT)
GPIO.setup(m21, GPIO.OUT)
GPIO.setup(m22, GPIO.OUT)
GPIO.output(m11 , 0)
GPIO.output(m12 , 0)
GPIO.output(m21, 0)
GPIO.output(m22, 0)
print ("DOne")

a=1
username=" "
uid=" "
#DB Connection string and DB cursor code
conn = MySQLdb.connect("localhost","root","Swagat@123","Swagath" ) 
cursor = conn.cursor() 

@app.route("/robot")
def robot():
    return render_template('robot.html')

class Bot:

    @app.route('/left_side')
    def left_side():
        data1="LEFT"
        GPIO.output(m11 , 0)
        GPIO.output(m12 , 0)
        GPIO.output(m21 , 1)
        GPIO.output(m22 , 0)
        return 'true'

    @app.route('/right_side')
    def right_side():
       data1="RIGHT"
       GPIO.output(m11 , 1)
       GPIO.output(m12 , 0)
       GPIO.output(m21 , 0)
       GPIO.output(m22 , 0)
       return 'true'

    @app.route('/up_side')
    def up_side():
       data1="FORWARD"
       GPIO.output(m11 , 1)
       GPIO.output(m12 , 0)
       GPIO.output(m21 , 1)
       GPIO.output(m22 , 0)
       return 'true'

    @app.route('/down_side')
    def down_side():
       data1="BACK"
       GPIO.output(m11 , 0)
       GPIO.output(m12 , 1)
       GPIO.output(m21 , 0)
       GPIO.output(m22 , 1)
       return 'true'

    @app.route('/stop')
    def stop():
       data1="STOP"
       GPIO.output(m11 , 0)
       GPIO.output(m12 , 0)
       GPIO.output(m21 , 0)
       GPIO.output(m22 , 0)
       return  'true'


    @app.route("/uget", methods = ['POST'])
    def getUsername():
        
        global username
        global uid
        username = request.form["username"]
        print("Recognised User:", username)
        cursor.execute("select EmpName from Employees where EmpId="+username) 
        data = cursor.fetchall() #data from database 
        
        uid = data
        return "Success"


    @app.route("/getUsername")
    def getUser():
        global uid
        global username
        print("Global User:", username)
        return render_template('index5.html', username=uid, uid=username)

    @app.route("/")
    def index():
        cursor.execute("select news from news") 
        data = cursor.fetchall() #data from database 
        return render_template('index.html', value=data)



    def gen(cam):
        while True:
            #get camera frame
            frame = cam.get_frame()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
                         

    @app.route('/video_feed')
    def video_feed():
        cam = VideoCamera()
        return Response(gen(cam),
                        mimetype='multipart/x-mixed-replace; boundary=frame')

    if __name__ == "__main__":
        print ("Start")

        app.run(host='0.0.0.0',port=5010)

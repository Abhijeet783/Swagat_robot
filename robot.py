from flask import Flask
from flask import render_template, request
import RPi.GPIO as GPIO
import time
import MySQLdb

app = Flask(__name__)

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

conn = MySQLdb.connect("localhost","root","Swagat@123","Swagath" ) 
cursor = conn.cursor() 

@app.route("/robot")
def robot():
    return render_template('robot.html')

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

@app.route("/")
def index():
    cursor.execute("select 'EmpId', 'EmpName', 'EmpWaveFile' from Employees where 'EmpId', 'EmpName', EmpWaveFile' = "" ") 
    data = cursor.fetchall() #data from database 
    return render_template('index4.html', value=data)

if __name__ == "__main__":
 print ("Start")
 
 app.run(host='0.0.0.0',port=5011)

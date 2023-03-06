from pydub import AudioSegment
from pydub.playback import play
import os
from time import sleep
import MySQLdb
from num2words import num2words
from subprocess import call
from smbus2 import SMBus
import requests
from mlx90614 import MLX90614
import time
import RPi.GPIO as gpio

R_DIR= 8
R_STEP= 7
R_EN= 25

L_DIR= 23
L_STEP= 18
L_EN= 24

gpio.setmode(gpio.BCM)

gpio.setup(R_DIR, gpio.OUT)
gpio.setup(R_STEP, gpio.OUT)
gpio.setup(R_EN, gpio.OUT)
gpio.output(R_EN,0)

gpio.setup(L_DIR, gpio.OUT)
gpio.setup(L_STEP, gpio.OUT)
gpio.setup(L_EN, gpio.OUT)
gpio.output(L_EN,0)



conn = MySQLdb.connect("localhost","root","Swagat@123","Swagath" ) 
cursor = conn.cursor()

def tempdetect_function():
  
    print("Inside Temperature Func")
    cmd_beg= 'espeak '
    cmd_end= ' 2>/dev/null' # To dump the std errors to /dev/null

    bus = SMBus(1)
    sensor = MLX90614(bus, address=0x5A)

    x = int((sensor.get_object_1() * 1.8)+36)
    count = num2words(x) + ' Degree Fahrenheit'
    print(count)
    #Replacing ' ' with '_' to identify words in the text entered
    count = count.replace(' ', '_')
    #Calls the Espeak TTS Engine to read aloud a Text
    call([cmd_beg+count+cmd_end], shell=True)
    return x

def pose():
    sleep(1)
    gpio.output(R_DIR, 0)
    gpio.output(L_DIR, 0)
    for x in range(75):
        gpio.output(R_STEP, gpio.HIGH)
        gpio.output(L_STEP, gpio.HIGH)
        sleep(0.01)
        gpio.output(R_STEP, gpio.LOW)
        gpio.output(L_STEP, gpio.LOW)
        sleep(0.01)
    sleep(1)
    gpio.output(R_DIR, 1)
    gpio.output(L_DIR, 1)
    for x in range(75):
        gpio.output(R_STEP, gpio.HIGH)
        gpio.output(L_STEP, gpio.HIGH)
        sleep(0.01)
        gpio.output(R_STEP, gpio.LOW)
        gpio.output(L_STEP, gpio.LOW)
        sleep(0.01)
    #sleep(3)
    #gpio.output(R_DIR, 1)
    #gpio.output(L_DIR, 1)
    #for x in range(500):
     #   gpio.output(R_STEP, gpio.HIGH)
     #   gpio.output(L_STEP, gpio.HIGH)
     #   sleep(0.01)
     #   gpio.output(R_STEP, gpio.LOW)
     #   gpio.output(L_STEP, gpio.LOW)
     #   sleep(0.01)
    

def playAudio():
    while(1):
        details='none,none'
        if not os.path.exists("username.txt"):
            continue
        with open("username.txt", "r") as f:
            username = f.read().strip()
            print("username",username)
            #username = "341573"
            if username != 'No Face' and username != 'Visitor' :
#                 response = requests.post("http://localhost:5010/uget", data={"username":username})
#                 print(response.status_code)
                pose()
                play(AudioSegment.from_file('/home/pi/SwagatNew/static/msg1.wav'))
                
                
             #   play(AudioSegment.from_file('/home/pi/SwagatNew/static/msg2.wav'))
              #  play(AudioSegment.from_file('/home/pi/SwagatNew/static/msg3.wav'))
               # print(usernam#e)
                #All code
                print("username")                 
                cursor.execute("select EmpId, EmpName, EmpWavFile from Employees where EmpId="+username)
                data = cursor.fetchall() #data from database
                details = str(data[0][0]) + ',' + str(data[0][1])
                print(details)
                details_file = open('details.txt','w')
                details_file.write(details)
                details_file.close()
                    
                    
                try:
                    for row in data:
                        play(AudioSegment.from_file('/home/pi/SwagatNew/static/names/'+ row[2] ))
                        
                    play(AudioSegment.from_file('/home/pi/SwagatNew/static/temp_msg.wav')) 
                    
                #play show hand 
                # call temp function
                except:
                    print("error in paying the audio")
                #os.environ["RESULT"]="0"
                print("Environment Var Reset")
                os.remove("username.txt")
                temperature=tempdetect_function()
#                 date_time="123"
                
#                 cursor.execute("INSERT INTO Temp values('"+username+"','"+temperature+"','"+date_time+"')")
#                 conn.commit()
                details = str(data[0][0]) + ',' + str(data[0][1]) + ',' + str(temperature)
                print(details)
                details_file = open('details.txt','w')
                details_file.write(details)
                details_file.close()
                
       # os.remove("username.txt")
            else:
                details = "none,none,none"
                details_file = open('details.txt','w')
                details_file.write(details)
                details_file.close()
        print("file removed") 
        sleep(10)
        

  
playAudio()
print("out of play audio")



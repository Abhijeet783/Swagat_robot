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

def playAudio():
    while(1):
        if not os.path.exists("username.txt"):
            continue
        with open("username.txt", "r") as f:
            username = f.read().strip()
            print(username)
            #username = "341573"
            if username != 'No FACE' and username != 'Visitor' :
#                 response = requests.post("http://localhost:5010/uget", data={"username":username})
               
                
                #print(response.status_code)
                play(AudioSegment.from_file('/home/pi/SwagatNew/static/msg1.wav'))
                
             #   play(AudioSegment.from_file('/home/pi/SwagatNew/static/msg2.wav'))
              #  play(AudioSegment.from_file('/home/pi/SwagatNew/static/msg3.wav'))
               # print(usernam#e)
                #All code
                 
                cursor.execute("select EmpId, EmpName, EmpWavFile from Employees where EmpId="+username) 
                data = cursor.fetchall() #data from database
                print(data)
                for row in data:
                    play(AudioSegment.from_file('/home/pi/SwagatNew/static/names/'+ row[2] ))
                    
                play(AudioSegment.from_file('/home/pi/SwagatNew/static/temp_msg.wav')) 

                #play show hand 
                # call temp function

                #os.environ["RESULT"]="0"
                print("Environment Var Reset")
                os.remove("username.txt")
                tempdetect_function()
       # os.remove("username.txt")
        print("file removed") 
        sleep(10)
        
        



playAudio()
print("out of play audio")




from pydub import AudioSegment
from pydub.playback import play
import os
from time import sleep
import MySQLdb

conn = MySQLdb.connect("localhost","root","Swagat@123","Swagath" ) 
cursor = conn.cursor() 

def playAudio():
    while(1):
        if not os.path.exists("username.txt"):
            continue
        with open("username.txt", "r") as f:
            username = f.read()
            if username:
                play(AudioSegment.from_file('/home/pi/SwagatNew/static/msg1.wav'))
             #   play(AudioSegment.from_file('/home/pi/SwagatNew/static/msg2.wav'))
              #  play(AudioSegment.from_file('/home/pi/SwagatNew/static/msg3.wav'))
               # print(usernam#e)
                #All code
                username="341573"
                cursor.execute("select EmpId, EmpName, EmpWavFile from Employees where EmpId="+username) 
                data = cursor.fetchall() #data from database
                print(data)
                for row in data:
                  play(AudioSegment.from_file('/home/pi/SwagatNew/static/names/'+ row[2] ))                
                
            
                #play show hand file
                
                
                
                
                
                # call temp function
                
                
                
                #os.environ["RESULT"]="0"
                print("Environment Var Reset")
                
        os.remove("username.txt")
        print("file removed") 
        sleep(10)
        
playAudio()
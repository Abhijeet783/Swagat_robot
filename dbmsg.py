from flask import Flask
from flask import render_template, request
import MySQLdb

app = Flask(__name__)


conn = MySQLdb.connect("localhost","root","Swagat@123","Swagath" ) 
cursor = conn.cursor() 

@app.route('/')
def data():
    
    return render_template("index12.html")

@app.route('/v_msg')
def data2():
    cursor = conn.cursor() 
    cursor.execute("select * from Message")
    msgdata = cursor.fetchall()

    return render_template("index11.html",data=msgdata)



if __name__=='__main__':
 app.run(host='127.0.0.1', port=5012)

from flask import Flask
from flask import render_template, request
import MySQLdb

app = Flask(__name__)


conn = MySQLdb.connect("localhost","root","Swagat@123","Swagath" ) 

cursor = conn.cursor() 

@app.route('/')
def get_data():
    return render_template("index10.html")

@app.route('/', methods=['POST'])
def get_data1():
    if request.method=='POST':
     Name=request.form['name']
     Mobile_No=request.form['Mobno']
     Email_Id=request.form['emailid']
     Org=request.form['org']
     cursor = conn.cursor()
     cursor.execute("INSERT INTO Visitors values('"+Name+"','"+Mobile_No+"','"+Email_Id+"','"+Org+"')")
     conn.commit()
    return render_template("index10.html")

if __name__=='__main__':
 app.run(host='127.0.0.1', port=5011)



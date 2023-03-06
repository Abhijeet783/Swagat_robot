# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 10:58:57 2021

@author: vetur
"""

from  flask import Flask,request, session, redirect,url_for,render_template
from flaskext.mysql import MySQL 
import re

import MySQLdb

app = Flask(__name__)

app.secret_key = 'Swagat@123'

conn = MySQLdb.connect("localhost","root","Swagat@123","Swagath") 
cursor = conn.cursor() 


#http://localhost:5000/pythonlogin/ - login page
@app.route('/pythonlogin/',methods=['GET','POST'])
def login():
    cursor = conn.cursor()
    msg = ''
    #checking if username and password post requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        #checking if account already exists
        cursor.execute(f'SELECT * FROM accounts WHERE username = "{username}" AND password = "{password}"')
        #fetch one account and return the result
        account = cursor.fetchone()
        
        #if account exists in accounts table 
        if account:
            session['loggedin'] = True
            session['id'] = account[0]
            session['fullname'] = account[1]
            session['username'] = account[2]
            #redirect to home page
            #return "logged in successfully"
            return redirect(url_for('home'))
        else:
            #account doesn't exist or incorrect creds
            msg = 'Incorrect credentials'
    return render_template('msgindex.html',msg=msg)
        
 
# http://localhost:5000/register - this will be the registration page
@app.route('/register', methods=['GET', 'POST'])
def register():
 # connect
    cursor = conn.cursor()
    
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        fullname = request.form['fullname']
        username = request.form['username']
        print(username)
        password = request.form['password']
        email = request.form['email']
   
  #Check if account exists using MySQL
        cursor.execute(f'SELECT * FROM accounts WHERE username = "{username}"')
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute(f'INSERT INTO accounts VALUES (NULL, "{fullname}", "{username}", "{password}", "{email}")') 
            conn.commit()
   
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('msgregister.html', msg=msg)
  
# http://localhost:5000/home - this will be the home page, only accessible for loggedin users
@app.route('/')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        receiver = session['fullname']
        cursor.execute(f'SELECT Message,sender FROM Message WHERE receiver = "{receiver}"')
        messages = cursor.fetchall()
        # User is loggedin show them the home page
        return render_template('msghome.html', username=session['username'],messages=messages)
    
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/message',methods=['POST','GET'])
def message():
    print("in message")
    cursor = conn.cursor() 
    cursor.execute("select EmpName from Employees")
    data = cursor.fetchall()
    if request.method=='POST' and 'Sender' in request.form and 'Receiver' in request.form and 'Message' in request.form:
        Sender=str(request.form['Sender']) #replace this later
        Receiver=str(request.form['Receiver'])
        Message=str(request.form['Message'])
        cursor = conn.cursor()
        cursor.execute(f'INSERT INTO Message(Sender,Receiver,Message)values("{Sender}","{Receiver}","{Message}")')
        #cursor.execute(f'INSERT INTO accounts VALUES (NULL, "{fullname}", "{username}", "{password}", "{email}")') 
        conn.commit()
        return redirect(url_for('home'))
    if 'loggedin' in session:
        cursor.execute('SELECT * FROM accounts WHERE id = '+str(session['id']))
        account = cursor.fetchone()
    return render_template("msgform.html",data=data,account=account)


# http://localhost:5000/logout - this will be the logout page
@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))
 
# http://localhost:5000/profile - this will be the profile page, only accessible for loggedin users
@app.route('/profile')
def profile(): 
 # Check if account exists 
    cursor = conn.cursor()
    
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor.execute('SELECT * FROM accounts WHERE id = '+str(session['id']))
        account = cursor.fetchone()
        # Show the profile page with account info
        print(account)
        return render_template('msgprofile.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))
  
  
  
if __name__ == '__main__':
    app.run(debug=True)




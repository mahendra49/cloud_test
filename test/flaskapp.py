from flask import Flask,render_template,request,send_file
from werkzeug.utils import secure_filename
import sqlite3
import os
import dbcreation


app = Flask(__name__)
DATABASE = 'users.db'
UPLOAD_PATH='./myfiles'
# app.config.from_object(__name__)
app = Flask(__name__, template_folder='templates')
app.config['UPLOAD_FOLDER'] = UPLOAD_PATH


@app.route('/send_user_file/<filename>')
def return_files_tut(filename):
    file_path = app.config['UPLOAD_FOLDER'] + "/"+ filename
    return send_file(file_path, as_attachment=True, attachment_filename='')



@app.route("/filedown/<filename>", methods = ['GET'])
def download_file(filename):
        return render_template('download.html',value=filename)

@app.route('/')
def login():
        return render_template("login.html")
@app.route('/register')
def registration():
        return render_template("register.html")

@app.route('/fileupload', methods=['GET', 'POST'])
def fileupload():
        if request.method == 'POST':
                f = request.files['file']
                emailid=request.form.get('email')
                passwrd=request.form.get('password')
                firstn=request.form.get('firstname')
                lastn=request.form.get('lastname')
                usern=request.form.get('username')
                filenam=secure_filename(f.filename)
                num_words = 0
                f.save(os.path.join(app.config['UPLOAD_PATH'],secure_filename(f.filename)))

                with open(os.path.join(app.config['UPLOAD_PATH'],secure_filename(f.filename)), 'r') as f:
                        for line in f:
                                words = line.split()
                                num_words +=len(words)

                                return render_template("details.html",filename=filenam,wordlen=num_words,username=usern,firstname=firstn,lastname=lastn,email=emailid,password=passwrd)


        return render_template("details.html")

@app.route('/registrationComplete',methods=['POST'])
def registrationComplete():
        emailid=request.form.get('email')
        passwrd=request.form.get('Pass')
        firstn=request.form.get('Fname')
        lastn=request.form.get('Lname')
        usern=request.form.get('username')
        file = request.files['file']
        filename = secure_filename(file.filename)
        conn = sqlite3.connect('users.db')
        c = conn.cursor()

        c.execute("""SELECT * FROM user_details WHERE user_name=?""",(usern,))
        users= c.fetchone()
        if users!= None:
                error="try again with different username(this namename is already taken)"
                return render_template("register.html",error=error)
        else:
                successmessage= "Successfully registerd."
                c.execute("""INSERT INTO user_details (first_name,last_name,email,user_name,password,filename) VALUES (?,?,?,?,?,?)""",(firstn,lastn,emailid,usern,passwrd,filename))
                conn.commit()
                conn.close()
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                return render_template("login.html",message=successmessage)

        
@app.route('/loginValidation', methods=['POST'])
def loginValidation():
        error= None
        
        usern=request.form.get('uname')
        passwrd=request.form.get('psw')
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        
        c.execute("""SELECT * FROM user_details WHERE user_name=? AND password=?""",(usern,passwrd))
        users=c.fetchone()
        print(users)
        conn.commit()
        conn.close()
        if users != None:
                num_words = 0
                with open(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(users[5])), 'r') as f:
                        for line in f:
                                words = line.split()
                                num_words +=len(words)
                return render_template("details.html",username=usern,firstname=users[0],lastname=users[1],email=users[2],password=passwrd,words=num_words,filename=users[5])
        else:
                error="username not valid or password not correct"
                return render_template("login.html",error=error)


if __name__ == '__main__':
  app.run()

from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash
import smtplib
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import sqlite3 as sql
basedir = os.path.abspath(os.path.dirname(__file__))
currentdirectory=os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)
class Student2(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    rollnumber = db.Column(db.String(100))
    place=db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(80), unique=False, nullable=False)
    course=db.Column(db.String(100))
    phonenumber=db.Column(db.Integer)
    parentphno=db.Column(db.Integer)
    hostelname=db.Column(db.String(100))
    roomno=db.Column(db.Integer)
    outime=db.Column(db.String(100))
    intime=db.Column(db.String(100))
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    def __repr__(self):
        return f'<Student {self.firstname}>'


class std(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    def __repr__(self):
        return f'<Student {self.firstname}>'
class Student4(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    rollnumber = db.Column(db.String(100))
    homeaddress=db.Column(db.String(1000), nullable=False)
    email = db.Column(db.String(80), unique=False, nullable=False)
    course=db.Column(db.String(100))
    phonenumber=db.Column(db.Integer)
    parentphno=db.Column(db.Integer)
    hostelname=db.Column(db.String(100))
    roomno=db.Column(db.Integer)
    purpose=db.Column(db.String(1000), nullable=False)
    noofdays=db.Column(db.Integer)
    fromdate=db.Column(db.String(100))
    todate=db.Column(db.String(100))
    outime=db.Column(db.String(100))
    intime=db.Column(db.String(100))
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    def __repr__(self):
        return f'<Student {self.firstname}>'
@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('guess'))
    return render_template('index.html')
from werkzeug.security import check_password_hash


from werkzeug.security import check_password_hash
import sqlite3 as sql
from flask import Flask, render_template, request, redirect, url_for, session, flash

@app.route('/login1', methods=['POST'])
def login1():
    username = request.form['username']
    password = request.form['password']
    # Connect to the database
    con = sql.connect("data.db")
    cur = con.cursor()
    # Use parameterized query to prevent SQL injection
    cur.execute("SELECT username, password FROM std WHERE username=?", (username,))
    result = cur.fetchone()
    # Close the connection
    con.close()

    if result:
        db_username, db_password = result
        # Check if the entered password matches the hashed password
        if check_password_hash(db_password, password):
            session['username'] = username
            if username == 'hostelwarden':
                return redirect(url_for('homeadmin'))
            else:
                return redirect(url_for('guess'))
        else:
            flash('Invalid username or password')
    else:
        flash('Invalid username or password')

    return redirect(url_for('home'))



# @app.route('/dashboard')
# def dashboard():
#     if 'username' in session:
#         return render_template('index1.html', username=session['username'])
#     return redirect(url_for('home'))
@app.route('/guess')
def guess():
    if 'username' in session:
        return render_template('index1.html', username=session['username'])
    return redirect(url_for('home'))


@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out')
    return redirect(url_for('home'))
# @app.route('/guess')
# def guess():
#    return render_template('index1.html')
@app.route('/set')
def set():
    if 'username' in session:
        return render_template('home.html', username=session['username'])
    return redirect(url_for('home'))
@app.route('/outing')
def outing():
    if 'username' in session:
        return render_template('outing.html', username=session['username'])
    return redirect(url_for('home'))
@app.route('/leave')
def leave():
    if 'username' in session:
        return render_template('leave.html', username=session['username'])
    return redirect(url_for('home'))
@app.route('/rules')
def rules():
    if 'username' in session:
        return render_template('rules.html', username=session['username'])
    return redirect(url_for('home'))


@app.route('/login', methods=['POST'])
def recieve_data():
    # Check if the user is logged in
    if 'username' not in session:
        return redirect(url_for('home'))
    # Retrieve form data
    name = request.form['name']
    rollnumber = request.form['Rollnumber']
    place = request.form['place']
    course = request.form['coursem']
    hostelname = request.form['hostel']
    roomno = request.form['roomno']
    phno = request.form['phonenumber']
    parentphno = request.form['parentphoneNumber']
    email = request.form['email']
    outime = request.form['outtime']
    intime = request.form['intime']

    # Validate roll number
    if rollnumber != session['username']:
        flash('Roll number does not match the logged-in username')
        return redirect(url_for('outing'))


    # Call function to send an email
    sendemail(name, rollnumber, place, course, hostelname, roomno, phno, parentphno, email, outime, intime)

    # Create a new Student2 object and add it to the database
    user1 = Student2(name=name, rollnumber=rollnumber, place=place, course=course, hostelname=hostelname, roomno=roomno,
                     phonenumber=phno, parentphno=parentphno, email=email, outime=outime, intime=intime)
    db.session.add(user1)
    db.session.commit()

    # Render the granted page with the provided data
    return render_template('granted.html', name=name, rollnumber=rollnumber, place=place, course=course,
                           hostelname=hostelname, roomno=roomno, phno=phno, parentphno=parentphno, email=email,
                           outime=outime, intime=intime)


@app.route('/leave', methods=['POST'])
def recieves_data():
    # Check if the user is logged in
    if 'username' not in session:
        return redirect(url_for('home'))

    # Retrieve form data
    name = request.form['name']
    rollnumber = request.form['Rollnumber']
    course = request.form['coursem']
    hostelname = request.form['hostel']
    homeaddress = request.form['homeaddress']
    roomno = request.form['roomno']
    phno = request.form['phonenumber']
    parentphno = request.form['parentphoneNumber']
    email = request.form['email']
    purpose = request.form['purposeof']
    noofdays = request.form['noofdays']
    fromdate = request.form['From']
    todate = request.form['To']
    file = request.form['file']
    outime = request.form['outtime']
    intime = request.form['intime']

    # Validate roll number
    if rollnumber != session['username']:
        flash('Roll number does not match the logged-in username')
        return redirect(url_for('outing'))
    # Call function to send an email
    sendemailleave(name=name, rollnumber=rollnumber, course=course, homeaddress=homeaddress, hostelname=hostelname,
                   roomno=roomno, phno=phno, parentphno=parentphno, purpose=purpose, noofdays=noofdays,
                   fromdate=fromdate, todate=todate, email=email, outime=outime, intime=intime)

    # Create a new Student4 object and add it to the database
    user1 = Student4(name=name, rollnumber=rollnumber, course=course, hostelname=hostelname, homeaddress=homeaddress,
                     roomno=roomno, phonenumber=phno, parentphno=parentphno, purpose=purpose, noofdays=noofdays,
                     email=email, fromdate=fromdate, todate=todate, outime=outime, intime=intime)
    db.session.add(user1)
    db.session.commit()

    # Render the granted leave page with the provided data
    return render_template('grantedleave.html', name=name, rollnumber=rollnumber, course=course,
                           hostelname=hostelname, homeaddress=homeaddress, roomno=roomno, phno=phno,
                           parentphno=parentphno, email=email, purpose=purpose, noofdays=noofdays,
                           fromdate=fromdate, todate=todate, outime=outime, intime=intime)


@app.route('/admin')
def admin():
    if 'username' in session:
        return render_template('admin.html', username=session['username'])
    return redirect(url_for('home'))
@app.route('/outingadmin')
def outingadmin():
    if 'username' not in session:
        return redirect(url_for('home'))
    students = Student2.query.all()
    return render_template('outingadmin.html', students=students)

@app.route('/leaveadmin')
def leaveadmin():
    if 'username' not in session:
        return redirect(url_for('home'))
    students = Student4.query.all()
    return render_template('leaveadmin.html', students=students)

@app.route('/homeadmin')
def homeadmin():
    if 'username' in session:
        return render_template('homeadmin.html', username=session['username'])
    return redirect(url_for('home'))


def sendemail(name, rollnumber, place, course, hostelname, roomno, phno, parentphno, email, outime, intime):
    my_email = "iiitkottayamcoms@gmail.com"
    password = "qwyxksuejdmsglin"

    # Create the HTML email content
    email_message = f"""\
    <html>
    <body>
        <p>Dear {name},</p>
        <p>Your outing to {place} from {outime} to {intime} has been approved by the Hostel Warden.</p>
        <table border="1" cellpadding="5" cellspacing="0">
            <tr>
                <th>Name</th>
                <td>{name}</td>
            </tr>
            <tr>
                <th>Roll Number</th>
                <td>{rollnumber}</td>
            </tr>
            <tr>
                <th>Place to Visit</th>
                <td>{place}</td>
            </tr>
            <tr>
                <th>Course and Semester</th>
                <td>{course}</td>
            </tr>
            <tr>
                <th>Hostel Name</th>
                <td>{hostelname}</td>
            </tr>
            <tr>
                <th>Room Number</th>
                <td>{roomno}</td>
            </tr>
            <tr>
                <th>Phone Number</th>
                <td>{phno}</td>
            </tr>
            <tr>
                <th>Parent Phone Number</th>
                <td>{parentphno}</td>
            </tr>
            <tr>
                <th>Out Time</th>
                <td>{outime}</td>
            </tr>
            <tr>
                <th>In Time</th>
                <td>{intime}</td>
            </tr>
        </table>
    </body>
    </html>
    """

    # Send the email
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(
                from_addr=my_email,
                to_addrs=email,
                msg=f"Subject: College Outing Management System (COMS)\nContent-Type: text/html\n\n{email_message}"
            )
        print(f"Email sent to {email}")  # Debug output
    except Exception as e:
        print(f"Failed to send email: {e}")  # Debug output


def sendemailleave(name,rollnumber,course,hostelname,homeaddress,roomno,phno,parentphno,email,purpose,noofdays,fromdate,todate,outime,intime):
   my_email = "iiitkottayamcoms@gmail.com"
   password = "qwyxksuejdmsglin"
   with smtplib.SMTP('smtp.gmail.com') as connection:
      connection.starttls()
      connection.login(user=my_email, password=password)
      email_message = f"""\
          <html>
          <body>
              <p>Dear {name},</p>
              <p>Your leave has been approved by our institution head.</p>
              <table border="1" cellpadding="5" cellspacing="0">
                  <tr>
                      <th>Name</th>
                      <td>{name}</td>
                  </tr>
                  <tr>
                      <th>Roll Number</th>
                      <td>{rollnumber}</td>
                  </tr>
                  <tr>
                      <th>Course and Semester</th>
                      <td>{course}</td>
                  </tr>
                  <tr>
                      <th>Hostel Name</th>
                      <td>{hostelname}</td>
                  </tr>
                  <tr>
                      <th>Home Address</th>
                      <td>{homeaddress}</td>
                  </tr>
                  <tr>
                      <th>Room Number</th>
                      <td>{roomno}</td>
                  </tr>
                  <tr>
                      <th>Phone Number</th>
                      <td>{phno}</td>
                  </tr>
                  <tr>
                      <th>Parent Phone Number</th>
                      <td>{parentphno}</td>
                  </tr>
                  <tr>
                      <th>Purpose of Leave</th>
                      <td>{purpose}</td>
                  </tr>
                  <tr>
                      <th>No. of Days</th>
                      <td>{noofdays}</td>
                  </tr>
                  <tr>
                      <th>From</th>
                      <td>{fromdate}</td>
                  </tr>
                  <tr>
                      <th>To</th>
                      <td>{todate}</td>
                  </tr>
                  <tr>
                      <th>Out Time</th>
                      <td>{outime}</td>
                  </tr>
                  <tr>
                      <th>In Time</th>
                      <td>{intime}</td>
                  </tr>
              </table>
          </body>
          </html>
          """
      connection.sendmail(from_addr=my_email, to_addrs=email, msg=email_message)
if __name__ == '__main__':
   app.run(debug=True)


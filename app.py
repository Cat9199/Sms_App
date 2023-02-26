import os
from flask import Flask, render_template, request, url_for, redirect,send_file
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from sqlalchemy.sql import func
global ui
from io import BytesIO
from werkzeug.datastructures import  FileStorage
uname = 'gest'
from werkzeug.exceptions import HTTPException

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
redirect('/register')
# ...

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    useradd = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    age = db.Column(db.Integer)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    bio = db.Column(db.Text)

    def __repr__(self):
        return f'<Student {self.firstname}>'

class user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(120))
    password = db.Column(db.String(80))
    smsn=db.Column(db.Integer)
    whatsappn=db.Column(db.Integer)
    emailn=db.Column(db.Integer)
class plan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sms = db.Column(db.String(80))
    whatsapp = db.Column(db.String(80))
    email = db.Column(db.String(80))
    cost=db.Column(db.String(80))
class Messg(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    MessName = db.Column(db.String(10000), nullable=False)
    useradd = db.Column(db.String(100), nullable=False)
    MessCon = db.Column(db.String(10000), nullable=False)
    Messphons = db.Column(db.String(1000000), nullable=False)
    mesline = db.Column(db.String(40))
    stat = db.Column(db.String(40))
    conum = db.Column(db.String(40))
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
class payac(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cardname = db.Column(db.String(10000), nullable=False)
    useradd = db.Column(db.String(100), nullable=False)
    cardnum = db.Column(db.String(10000), nullable=False)
    cvv = db.Column(db.String(3), nullable=False)
    expiration = db.Column(db.String(40))
    cost = db.Column(db.String(40))
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())  
    stat=db.Column(db.String(30))
 
	
@app.route("/register", methods=["GET", "POST"])
def register():
    global uname
    if request.method == "POST":
        uname = request.form['uname']
        mail = request.form['mail']
        passw = request.form['passw']

        register = user(username = uname, email = mail, password = passw,smsn=0,whatsappn=0,emailn=0)
        db.session.add(register)
        db.session.commit()

        return redirect(url_for("login"))
    if uname == 'gest':
        return render_template("register.html")
    else:
        return redirect('/login')

@app.route("/login",methods=["GET", "POST"])
def login():
    global uname
    if request.method == "POST":
        un = request.form["uname"]
        passw = request.form["passw"]
        
        login = user.query.filter_by(username=un, password=passw).first()
        if login is not None:
            uname = un
            print(login)
               
            return redirect('/')
        elif un == None:
           uname = 'gest'
           print('this')
        #    disabled
    if uname == 'gest':
        return render_template("login.html")
    else :
        return redirect('/loginfo')
@app.route('/loginfo')
def loginfo():
    global uname
    return render_template('loginfo.html',user=uname)

# =================================
# @app.route('/test')
# def test():
#     peter =Student.query.filter_by(useradd='123').all()
#     return render_template('i.html', students=peter,uname=uname,stat="disabled")
#     return 'ok'
# =========================


@app.route('/addmes' ,methods=('GET', 'POST'))
def addmas():
    global uname
    global idm
    if uname != 'gest':
        if request.method == "POST":
            mn = request.form["Mname"]
            cn = request.form["con"]
            mm = request.form["Mmess"]
            tc = cn.split(',')
            pc = str(len(tc))
            t = Messg(MessName=mn,useradd=uname,MessCon=mm,Messphons=cn,stat='processing',conum=pc)
            db.session.add(t)
            db.session.commit()
            idm = str(t.id)
            return redirect('/mesms')
            
        return render_template('messform.html',messavel=3000)
    else:
        return redirect('/login')


@app.route('/mesms')
def mesms():
    global idm
    f = Messg.query.get_or_404(int(idm))
    
    return render_template('methedsms.html',messagname=f.MessName,id=f.id,avmess='3000',phnum=f.conum,time=f.created_at)


@app.route('/')

def index():
    students = Student.query.all()
    return render_template('index.html', students=students ,uname=uname)

# ...

@app.route('/<int:student_id>/')
def student(student_id):
    student = Student.query.get_or_404(student_id)
    return render_template('student.html', student=student)
@app.route("/control")
def control():
    global uname
    if uname != 'gest':
        mess = Messg.query.filter_by(useradd=uname, stat='processing')
        return render_template('control.html',mes=mess)
    elif uname == 'gest':
        return redirect('/login')
# ...
@app.route("/logout")
def logout():
    global uname
    uname = 'gest'
    return redirect('/login')

@app.route('/create/')
def create():
    return render_template('create.html')

@app.route('/create/', methods=('GET', 'POST'))
def create2():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        age = int(request.form['age'])
        bio = request.form['bio']
        student = Student(firstname=firstname,
                          lastname=lastname,
                          email=email,
                          age=age,
                          useradd=uname,
                          bio=bio)
        db.session.add(student)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('create.html')

# ...


@app.route('/<int:student_id>/viwemess/', methods=('GET', 'POST'))
def vm(student_id):
    student = Messg.query.get_or_404(student_id)


    return render_template('edit.html', id=str(student.id))
@app.route('/<int:student_id>/viwepay/', methods=('GET', 'POST'))
def vp(student_id):
    student = payac.query.get_or_404(student_id)


    return render_template('edit.html', id=str(student.id))
# ...
@app.route("/2000pl", methods=('GET', 'POST'))
def p20000():
    global uname
    global st
    if uname != 'gest':
        if request.method == 'POST':
            cardname = request.form['cardname']
            cardnumber = request.form['creditcard']
            cvv = request.form['cvv']
            expiration = request.form['expiration']
            g = payac(cardname=cardname,useradd=uname,cardnum= cardnumber,cvv=cvv,cost='5',stat='send')
            db.session.add(g)
            db.session.commit()
            st = g.id
            return redirect('/ok')
            
        return render_template('pay.html',sms='2000',Whatsapp='10000',email='15000')
    elif uname == 'gest':
        return redirect('/login')
 
 
 
@app.route('/<int:user_id>/viwem/', methods=('GET', 'POST'))
def viwem(user_id):
    return render_template('mev.html',user_id=user_id)
@app.route('/<int:user_id>/dac/', methods=('GET', 'POST'))
def dac(user_id):
    import pywhatkit
    from datetime import datetime
    numlest=["+201069324895","+201069324895","+201069324895"]
    for x in numlest :
        currentDateAndTime = datetime.now()
        h = currentDateAndTime.strftime("%H")
        m = currentDateAndTime.strftime("%M")
        s = currentDateAndTime.strftime("%S")
        
        print(h,m,s)
    # Send a WhatsApp Message to a Contact at 1:30 PM
        pywhatkit.sendwhatmsg(x, "Hiiii", int(h),int(m)+1)
    return 'ok'
    # pid = payac.query.get_or_404(user_id)
    # return render_template('mep.html',user_id=pid)
@app.route('/<int:user_id>/aac/', methods=('GET', 'POST'))
def aac(user_id):
    pid = payac.query.get_or_404(user_id)
    userr = pid.useradd
    print(userr)
    pd = user.query.filter_by(username=userr).first()
    if pid.cost == '5':
        # pd.smsn = int(pd.sms)+ 5000
        pd.whatsappn = int(pd.whatsappn)+ 7000
        pd.emailn = int(pd.emailn)+ 15000
        db.session.delete(pid)
        
        db.session.add(pd)
        db.session.commit()
    # pd.smsn = 500
    return render_template('mep.html',user_id=pid)
@app.route('/ok')
def ok():
    global st
    return render_template('pross.html',method_id=str(st))
@app.route("/5000pl")
def p5000():
    return render_template('pay.html',sms='5000',Whatsapp='20000',email='25000')
@app.route("/7000pl")
def p70000():
    return render_template('pay.html',sms='7000',Whatsapp='30000',email='35000')
@app.post('/<int:student_id>/delete/')
def delete(student_id):
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('index'))
@app.route("/sms")
def sms():
    global idm
    f = Messg.query.get_or_404(int(idm))
    f.mesline = 'sms'
    db.session.add(f)
    db.session.commit() 
    return ' ok'
@app.route("/whatsapp")
def whatsapp():
    global idm
    f = Messg.query.get_or_404(int(idm))
    f.mesline = 'whatsapp'
    db.session.add(f)
    db.session.commit()
    return ' ok'
@app.route("/telgram")
def telgram():
    global idm
    f = Messg.query.get_or_404(int(idm))
    f.mesline = 'telgram'
    db.session.add(f)
    db.session.commit()
    return ' ok'
@app.route('/admin')
def admin():

    pays = payac.query.all()
    messgs = Messg.query.all()
    if uname == 'admin@sms':
        
        return render_template('admin.html',payss=pays,messs=messgs)
    else:
        return render_template('404.html')
@app.errorhandler(404) 
def invalid_route(e): 
    return render_template('404.html')

@app.route('/admin/plans')
def planss():
    if uname == 'admin@sms':
        return 'this is plans page'
    else:
        return render_template('404.html')
@app.errorhandler(Exception)
def handle_exception(e):
    # pass through HTTP errors
    if isinstance(e, HTTPException):
        return e

    # now you're handling non-HTTP exceptions only
    return render_template("500_generic.html", e=e), 500

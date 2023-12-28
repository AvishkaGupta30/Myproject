from flask import Flask, redirect, render_template,request,flash,url_for,session
from flask_mail import *
from user import user_operation
from provider import provider_operation
from captcha.image import ImageCaptcha
import random
import hashlib
import speech_recognition as sr

app = Flask(__name__)

app.secret_key = "hkldsjfklds78784hdsy787i"
#-------------------mail configuration---------------------------
app.config["MAIL_SERVER"]='smtp.office365.com'
app.config["MAIL_PORT"] = '587'
app.config["MAIL_USERNAME"] = 'avisha01@outlook.com'
app.config["MAIL_PASSWORD"]= '@Pinks@10'
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False
mail = Mail(app)
#----------------------------------------------------------

@app.route('/')
def index():
    return render_template('index.html')


#------------------user sign up pages--------------------------------------------------
@app.route('/user_signup')
def user_signup():
    num=random.randrange(1000,9999)
    # Create an image instance of the given size
    img = ImageCaptcha(width = 280, height = 90)

    # Image captcha text
    global CAPTCHA_text
    CAPTCHA_text = str(num)
 
    # write the image on the given file and save it
    img.write(CAPTCHA_text, 'static/images/CAPTCHA.png')
    return render_template('user_signup.html')

@app.route('/user_signup_insert',methods=['GET','POST'])
def user_signup_insert():
    if request.method=='POST': 
        if CAPTCHA_text!=request.form["CAPTCHA"]:
                        flash("invalid captcha!!!")
                        return render_template('user_signup.html')

        name=request.form["name"]
        email=request.form["email"]
        mobile=request.form["mobile"]
        password=request.form["password"]
        #--- password hashing----------------
        pas = hashlib.md5(password.encode())
        password = pas.hexdigest()
        #---------user insert-----------------
        op = user_operation()  # object create
        op.user_signup_insert(name,email,mobile,password)
        #------- email verification--------------------------------
        global otp
        otp = random.randint(100000,999999)
        msg = Message('Email verification',sender = 'avisha01@outlook.com', recipients = [email])
        msg.body = "Hi "+ name + "\nYour email OTP is: " + str(otp)
        mail.send(msg)
        return render_template('email_verify.html',email=email)

@app.route('/email_verify',methods=['GET','POST'])
def email_verify():
    user_otp = request.form['otp']
    if otp == int(user_otp):
        flash("Your Email is Verified.. You can Login Now!!!")
        return redirect(url_for('user_login'))
    email=request.form['email']
    op = user_operation()  # object create
    op.user_delete(email)
    flash("Your Email verification is failed... Register with Valid Email!!!")
    return redirect(url_for('user_signup'))

#------------------user login pages--------------------------------------------------
@app.route('/user_login')
def user_login():
    return render_template('user_login.html')

@app.route('/user_login_verify',methods=['GET','POST'])
def user_login_verify():
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']
        op = user_operation()
        r=op.user_login_verify(email,password)
        if r==0:
            flash("Invalid Email or Password")
            return redirect(url_for('user_login'))
        else:
            return redirect(url_for('user_dashboard'))


@app.route('/user_logout')
def user_logout():
    session.clear()
    return redirect(url_for('user_login'))

@app.route('/user_dashboard')
def user_dashboard():
    if 'user_email' in session:
        return render_template('user_dashboard.html')
    else:
        flash("you are not logged in .. login now!!!")
        return redirect(url_for('user_login'))

@app.route('/user_profile')
def user_profile():
    if 'user_email' in session:
        op = user_operation()
        r=op.user_profile()
        return render_template('user_profile.html',rec=r)
    else:
        flash("you are not logged in .. login now!!!")
        return redirect(url_for('user_login'))

@app.route('/user_profile_update',methods=['GET','POST'])
def user_profile_update():
    if 'user_email' in session:
        if request.method=='POST':
            name=request.form['name']
            mobile=request.form['mobile']
            op = user_operation()
            op.user_profile_update(name,mobile)
            flash("your profile is updated successfully!!!")
            return redirect(url_for('user_profile'))
    else:
        flash("you are not logged in .. login now!!!")
        return redirect(url_for('user_login'))

#--------------------------------------------------------------------------------------
#------------------------------- provider routing--------------------------------------
#--------------------------------------------------------------------------------------
@app.route('/provider_signup')
def provider_signup():
    num=random.randrange(1000,9999)
    # Create an image instance of the given size
    img = ImageCaptcha(width = 280, height = 90)

    # Image captcha text
    global captcha_text1
    captcha_text1 = str(num)
 
    # write the image on the given file and save it
    img.write(captcha_text1, 'static/images/CAPTCHA1.png')
    return render_template('provider_signup.html')

@app.route('/provider_signup_insert',methods=['GET','POST'])
def provider_signup_insert():
    if request.method=='POST': 
        if captcha_text1!=request.form["captcha"]:
                        flash("invalid captcha!!!")
                        return render_template('provider_signup.html')

        name=request.form["name"]
        email=request.form["email"]
        mobile=request.form["mobile"]
        address=request.form["address"]
        city=request.form["city"]
        password=request.form["password"]
        #--- password hashing----------------
        pas = hashlib.md5(password.encode())
        password = pas.hexdigest()
        #---------provider insert-----------------
        op = provider_operation()  # object create
        rec=op.provider_signup_insert(name,email,mobile,address,city,password)
        for r in rec:
            flash("Your Provider ID is: "+ str(r[0])+"   login now..")
        return render_template('provider_login.html')

#------------------provider login pages--------------------------------------------------
@app.route('/provider_login')
def provider_login():
    return render_template('provider_login.html')

@app.route('/provider_login_verify',methods=['GET','POST'])
def provider_login_verify():
    if request.method=='POST':
        provider_id=request.form['provider_id']
        password=request.form['password']
        op = provider_operation()
        r=op.provider_login_verify(provider_id,password)
        if r==0:
            flash("Invalid ID or Password")
            return redirect(url_for('provider_login'))
        else:
            return redirect(url_for('provider_dashboard'))


@app.route('/provider_logout')
def provider_logout():
    session.clear()
    return redirect(url_for('provider_login'))

@app.route('/provider_dashboard')
def provider_dashboard():
    if 'provider_id' in session:
        return render_template('provider_dashboard.html')
    else:
        flash("you are not logged in .. login now!!!")
        return redirect(url_for('provider_login'))

@app.route('/provider_profile')
def provider_profile():
    if 'provider_id' in session:
        op = provider_operation()
        r=op.provider_profile()
        return render_template('provider_profile.html',rec=r)
    else:
        flash("you are not logged in .. login now!!!")
        return redirect(url_for('provider_login'))

@app.route('/provider_profile_update',methods=['GET','POST'])
def provider_profile_update():
    if 'provider_id' in session:
        if request.method=='POST':
            email=request.form['email']
            mobile=request.form['mobile']
            address=request.form['address']
            op = provider_operation()
            op.provider_profile_update(email,mobile,address)
            flash("your profile is updated successfully!!!")
            return redirect(url_for('provider_profile'))
    else:
        flash("you are not logged in .. login now!!!")
        return redirect(url_for('provider_login'))


@app.route('/provider_bike')
def provider_bike():
    if 'provider_id' in session:
        return render_template('provider_bike.html')
    else:
        flash("you are not logged in .. login now!!!")
        return redirect(url_for('provider_login'))

@app.route('/provider_bike_insert',methods=['GET','POST'])
def provider_bike_insert():
    if 'provider_id' in session:
        if request.method=='POST':
            model_name=request.form['model_name']
            reg_no=request.form['reg_no']
            charge=request.form['charge']
            mfg_date=request.form['mfg_date']
            descp=request.form['descp']
            #------photo upload-------------
            photo=request.files["photo"]
            photo_name = photo.filename
            photo.save("static/bike/" + photo_name)
            #-----------------------------------------------------------------------
            op = provider_operation()
            op.provider_bike_insert(model_name,reg_no,charge,mfg_date,descp,photo_name)
            flash("your bike is inserted successfully!!!")
            return redirect(url_for('provider_bike'))
    else:
        flash("you are not logged in .. login now!!!")
        return redirect(url_for('provider_login'))

        
@app.route('/provider_bike_view')
def provider_bike_view():
    if 'provider_id' in session:
        op = provider_operation()
        r=op.provider_bike_view()
        return render_template('provider_bike_view.html', rec=r)
    else:
        flash("you are not logged in .. login now!!!")
        return redirect(url_for('provider_login'))

@app.route('/provider_bike_delete',methods=['GET','POST'])
def provider_bike_delete():
    if 'provider_id' in session:
        if request.method=='GET':
            bike_id=request.args.get('bike_id')
            op = provider_operation()
            op.provider_bike_delete(bike_id)
            flash("bike is deleted successfully!!!")
            return redirect(url_for('provider_bike_view'))
    else:
        flash("you are not logged in .. login now!!!")
        return redirect(url_for('provider_login'))

@app.route('/provider_bike_voice_search',methods=['GET','POST'])
def user_bike_voice_search():
    if 'user_email' in session:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio_data = r.record(source, duration=5)

            city = r.recognize_google(audio_data)


            op = user_operation()
            op = op.user_bike_search(city)
            return render_template(url_for('user_bike.html', rec=r))
    else:
        flash("You are not logged in .. login now!!!")
        return redirect(url_for('user_login'))        

        


@app.route('/provider_bike_profile',methods=['GET','POST'])
def provider_bike_profile():
    if 'provider_id' in session:
        if request.method=='GET':
            bike_id=request.args.get('Bike ID')
            op = provider_operation()
            r=op.provider_bike_profile('Bike ID')
            return render_template ('provider_bike_profile.html',rec=r)
    else:
        flash("You are not logged in .. login now!!!")
        return redirect(url_for('provider_login'))



@app.route('/provider_bike_profile_update',methods=['GET','POST'])
def provider_bike_profile_update():
    if 'provider_id' in session:
        if request.method=='POST':
            bike_id=request.args.get('bike_id')
            model_name=request.form['model_name']
            reg_no=request.form['reg_no']
            charge=request.form['charge']
            mfg_date=request.form['mfg_date']
            descp=request.form['descp']
            op = provider_operation()
            op.provider_bike_profile_update(bike_id,model_name,reg_no,charge,mfg_date,descp)
            flash("Your Bike Details are Updated Successfully!!!")
            return redirect(url_for('provider_bike_profile',bike_id=bike_id))
    else:
        flash("you are not logged in .. login now!!!")
        return redirect(url_for('provider_login'))

@app.route('/provider_bike_rent')
def provider_bike_rent():
    if 'provider_id' in session:
        op = provider_operation()
        r=op.provider_bike_rent()
        return render_template('provider_bike_rent.html',rec=r)
    else:
        flash("you are not logged in .. login now!!!")
        return redirect(url_for('provider_login'))
        
if __name__=="__main__":
	app.run(debug =  True)

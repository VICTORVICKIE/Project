from flask import render_template,url_for,session,request,logging,redirect,flash
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from passlib.hash import sha256_crypt
from cc.send import send
from cc.otp_gen import otp_gen
from functools import wraps
from cc.sqlhelpers import *
from cc.forms import *
import time, os
from cc import app

s = URLSafeTimedSerializer(os.urandom(24))



def is_logged_in(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			
			return f(*args,**kwargs)
		else:
			flash("Unauthorized!! Please Login","danger")
			return redirect(url_for('login'))
	return wrap

def is_logged_out(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            flash('You are already logged in.', 'danger')
            return redirect(url_for('dashboard'))
        else:
            return f(*args, **kwargs)
    return wrap

def special_trans(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if ('recepient' in session) and ('otp' in session) and ('amount' in session):
        	
        	return f(*args, **kwargs)
            
        else:
        	flash("Not the Llama you are looking for.","danger")
        	return redirect(url_for('transaction'))
            
    return wrap

def special_chps(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'newpass' in session and 'otp' in session:
        	
        	return f(*args, **kwargs)
            
        else:
        	flash("Not the Llama you are looking for.","danger")
        	return redirect(url_for('profile'))
            
    return wrap




########################################    INDEX BLOCK   ##########################################

@app.route("/",defaults={'width':None,'height':None})
@app.route("/<width>/<height>")
@is_logged_out
def index(width=None,height=None):
	if not width or not height:
		return """
		<script>
		(() => window.location.href = ['',window.innerWidth,window.innerHeight].join('/'))()
		</script>
		"""
	if int(width) > 992:
		return render_template('index-pc.html')
	else:
		return render_template('index-mb.html')

########################################    REGISTRATION BLOCK   ########################################

@app.route("/register",methods=['GET','POST'])
@is_logged_out						
def register():
	form = Registerform(request.form)
	users = Table("users","name","email","roll","password","confirm",primary_key='roll')

	if request.method == 'POST' and form.validate():
		roll = form.roll.data
		email = form.email.data
		name = form.name.data
		confirm = '0'
				
		if isnewuser(roll): 						
			password = sha256_crypt.hash(form.password.data)
							
			users.insert(name,email,roll,password,confirm)
					
			confirm_link_sender(email,roll,func_to='confirm_email',
										salt='email-confirm',purpose='EmailVerify')
							
			return render_template('tq.html')
						
		else:
			flash('user already exists','danger')
			return redirect(url_for('login'))
			
	return render_template('register.html',form=form)

########################################     EMAIL CONFIRMATION BLOCK  #################################

def confirm_link_sender(email,roll,func_to,salt,purpose):
	email = email
	roll = roll
	token = s.dumps(roll, salt=salt)
	link = url_for(func_to, token=token, _external=True)
	send(email,message=link,purpose=purpose)


@app.route('/confirm_email/<token>')
def confirm_email(token):
	try:
		roll = s.loads(token, salt='email-confirm', max_age=3600)
	except SignatureExpired:
		return '<h1>The token is expired!</h1>'
	users = Table("users","name","email","roll","password","confirm")
	user = users.getone("roll",roll)
	email = user.get('email')
	password = user.get('password')
	roll = roll
	name = user.get('name')
	confirm = '1'
	users.replace(name,email,roll,password,confirm)
	log_in_user(roll)
	return redirect(url_for('dashboard'))

########################################     LOGIN BLOCK  ##########################################

@app.route("/login", methods=['GET','POST'])
@is_logged_out			#login page
def login():
	if request.method == 'POST':
		roll = request.form['roll']
		candidate = request.form['password']

		users = Table("users","name","email","roll","password","confirm")
		user = users.getone("roll",roll)
		accpass = user.get('password')
		confirm = user.get('confirm')

		if accpass is None:
			flash("roll not found",'danger')
			return redirect(url_for('login'))

		else:
			if sha256_crypt.verify(candidate,accpass):
				if confirm == '1':	
					log_in_user(roll)
					flash("You are logged in",'success')
					return redirect(url_for("dashboard"))
				else:
					flash("Your Email is not confirmed",'danger')
					return redirect(url_for('register'))			
			else:
				flash("Invalid Password",'danger')
				return redirect(url_for('login'))

	return render_template('login.html')

########################################     USER BLOCK  ##########################################

@app.route("/dashboard")
@is_logged_in								#user dashboard
def dashboard():
	
	blockchain = get_blockchain().chain
	ct = time.strftime("%I:%M %p")
	if not verifyBlockchain():
		flash("Corrupt blockchain.","danger")
		return redirect(url_for('index'))
	return render_template('dashboard.html',
		session=session,ct=ct,blockchain=blockchain,
		page='dashboard')

########################################    TRANSACTION HISTORY BLOCK  ###################################

@app.route("/activities")
@is_logged_in								
def activities():
	if "roll" in session:
		blockchain = get_blockchain().chain
		roll = session["roll"]
		balance = get_balance(session.get('roll'))
		return render_template('activities.html',balance=balance,
			session=session,roll=roll,blockchain=blockchain,
			page='activities')

########################################     TRANSACTION BLOCK  ##########################################

@app.route("/transaction",methods=["GET","POST"])
@is_logged_in
def transaction():
	form = SendCCForm(request.form)
	balance = get_balance(session.get('roll'))
	if request.method == 'POST':
		
		roll = session['roll']
		candidate = request.form['password']
		
		users = Table("users","name","email","roll","password","confirm")
		user = users.getone("roll",roll)
		
		accpass = user.get('password')
		
		

		
		if float(form.amount.data) <= float(balance):
			try:
				if sha256_crypt.verify(candidate,accpass):
					if not isnewuser(form.roll.data):
						OTP = otp_gen()
						session['recepient'] = form.roll.data
						session['amount'] = form.amount.data
						recipient = session['recepient']
						email=session['email']
						send(email,OTP,purpose='Transaction')
						session['otp'] = OTP
						return redirect(url_for('verifytrans'))
					else:
						raise InvalidTranscationException("User Does Not Exist")
				else:
					
					flash("Invalid Password",'danger')
					return redirect(url_for('transaction'))
			except Exception as e:
				flash(str(e),'danger')

			return redirect(url_for('transaction'))
		else:
			flash("Insuffient Balance",'danger')
	return render_template("transaction.html",balance=balance,form=form,
														page='transaction')

########################################     OTP BLOCK  ##########################################


@is_logged_in
@app.route("/verifytrans",methods=["POST","GET"])
@special_trans
def verifytrans():
	
	recepient = session['recepient']
	amount = session['amount']
	otp = session['otp']
	if request.method == 'POST':
		ps = request.form['ps']
		if str(ps) == str(otp):
			send_campus_coins(session.get('roll'),recepient,amount)
			session.pop('otp',None)
			session.pop('recepient',None)
			session.pop('amount',None)
			flash("Money Sent","success")
			return redirect(url_for('transaction'))

	return render_template("verify.html")

########################################    PURCHASE BLOCK  ##########################################

@app.route("/buy",methods=["GET","POST"])
@is_logged_in
def buy():
	form = BuyCCForm(request.form)
	balance = get_balance(session.get('roll'))

	if request.method == 'POST':
		try:
			if int(form.amount.data)<10000000:
				send_campus_coins("BANK",session.get('roll'),form.amount.data)
				flash("Purchase Successfull","success")
			else:
				raise InvalidTranscationException("Amount too High!")

		except Exception as e:
			flash(str(e),'danger')

		return redirect(url_for('buy'))
	return render_template("buy.html",balance=balance,form=form, page='buy')

########################################    SESSION BLOCK  ########################################

def log_in_user(roll):
	users = Table("users","name","email","roll","password","confirm")
	user = users.getone("roll",roll)
	session["logged_in"] = True
	session["roll"] = roll
	session["name"] = user.get('name')
	session["email"] = user.get('email')
	session['confirm'] = user.get('confirm')

#######################################    PROFILE BLOCK  ########################################

@app.route("/profile")
@is_logged_in
def profile():
	if "roll" in session:
		balance = get_balance(session.get('roll'))
		return render_template('profile.html',page='profile',session=session,balance=balance)

########################################    CHANGE PASS BLOCK  ########################################

@app.route("/passchange",methods=['GET','POST'])
@is_logged_in
def passchange():
	if request.method == 'POST':
		oldpass = request.form['password']
		newpass = request.form["newpassword"]
		confirmnew = request.form["newconfirm"]
		roll = session["roll"]
		users = Table("users","name","email","roll","password","confirm")
		user = users.getone("roll",roll)
		accpass = user.get('password')
		if sha256_crypt.verify(oldpass,accpass):
			if newpass == confirmnew:
				OTP = otp_gen()
				email = session['email']
				send(email,OTP,purpose='ChangePass')
				session['otp'] = OTP
				session["newpass"] = sha256_crypt.hash(newpass)
				
				return redirect(url_for('verifypc'))

	if "roll" in session:
		return render_template('passchange.html',session=session)

########################################   VERIFY CHANGE PASS BLOCK  ########################################

@is_logged_in
@app.route("/verifypc",methods=["POST","GET"])
@special_chps
def verifypc():
	
	
	users = Table("users","name","email","roll","password","confirm")
	roll = session["roll"]
	name = session["name"]
	email = session["email"]
	confirm = session["confirm"]
	otp = session['otp']
	if request.method == 'POST':
		ps = request.form['ps']
		if str(ps) == str(otp):
			session.pop('otp',None)
			password = session["newpass"]
			users.replace(name,email,roll,password,confirm)
			session.pop('newpass',None)
			flash("Password Changed","success")
			return redirect(url_for('profile'))

	return render_template("verify.html")

########################################   FORGOT PASS BLOCK  ########################################

@app.route("/forgotpass",methods=['GET','POST'])
def forgotpass():
	if request.method == 'POST':
		roll = request.form["roll"]
		if not isnewuser(roll):
			users = Table("users","name","email","roll","password","confirm")
			user = users.getone("roll",roll)
			email = user.get('email')
			confirm_link_sender(email,roll,func_to='check',salt='password-reset',purpose='ResetPass')
			return render_template('resetlinkmail.html')
			
	return render_template('forgotpassreq.html')

########################################    FORGOT PASS VERIFY BLOCK  ########################################

@app.route("/check/<token>",methods=['GET','POST'])
def check(token):
	try:
		roll = s.loads(token, salt='password-reset', max_age=300)
		if request.method == 'POST':
			if request.form["password"] == request.form["confirmreset"]:
				newpass = request.form["password"]
				password = sha256_crypt.hash(newpass)
				users = Table("users","name","email","roll","password","confirm")
				user = users.getone("roll",roll)
				name = user.get('name')
				email = user.get('email')
				roll = roll
				confirm = user.get('confirm')				

				users.replace(name,email,roll,password,confirm)
				flash("Password Changed","success")
				return redirect(url_for('login'))

		return render_template("resetpass.html")


	except SignatureExpired:
		return '<h1>The token is expired!</h1>'
		


########################################    LOGOUT BLOCK  ##########################################

@app.route("/logout")									#logout
@is_logged_in
def logout():
	session.clear()
	flash("Logout success","success")
	return redirect(url_for('login'))


########################################    ERROR HANDLER BLOCK  ##########################################

@app.errorhandler(404)
def page_not_found(e):
    return render_template('handlers/404.html'), 404
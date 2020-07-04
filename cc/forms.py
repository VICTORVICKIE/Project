from wtforms import Form,StringField,DecimalField,IntegerField,TextAreaField,PasswordField, validators
import re

class Registerform(Form):
	name = StringField('Full Name',[validators.InputRequired(message="Name required"),validators.Length(min=1,max=50,message="Full name must be between 1 and 50")],id="name")
	roll = StringField('Roll Number',[validators.InputRequired(message="Roll/Staff Number required"),validators.Length(min=1,max=15,message="Roll/Staff Number must be between 1 and 15")])
	email = StringField('Email',[validators.InputRequired(message="Email required"),validators.Length(min=6,max=50,message="Email must be between 6 and 50")])
	password = PasswordField('Password',[validators.DataRequired(),validators.EqualTo('confirm',message='Password Doesnot match!')])
	confirm = PasswordField('Confirm Password')
	
	
	def validate_email(self,email):
		email = email.data 
		regex1 = '^[a-zA-Z0-9_.+-]+@rajalakshmi+\.[edu.in]+$'
		regex2 = '^[a-zA-Z0-9_.+-]+@gmail+\.[com]+$'
		if "-" not in email:
			if(re.search(regex1,email)) or (re.search(regex2,email)): 
				pass 
			
			else: 
				raise validators.ValidationError("Domain Name not Supported")
		else:
			raise validators.ValidationError("Field got an unsupported character as input")
	def validate_name(self,name):
		name = name.data
		if ("-" in name):
			raise validators.ValidationError("Field got an unsupported character as input")
		else:
			pass
	def validate_roll(self,roll):
		roll = roll.data
		if ("-" in roll):
			raise validators.ValidationError("Field got an unsupported character as input")
		else:
			pass
	def validate_password(self,password):
		password = password.data
		if ("-" in password):
			raise validators.ValidationError("Field got an unsupported character as input")
		else:
			pass
	def validate_confirm(self,confirm):
		confirm = confirm.data
		if ("-" in confirm):
			raise validators.ValidationError("Field got an unsupported character as input")
		else:
			pass


class SendCCForm(Form):
	roll = StringField('Recipient`s ID',[validators.InputRequired(message="Recipient Roll/Staff Number required"),validators.Length(min=1,max=15,message='Recipient Roll/Staff Number')])
	amount = StringField('Amount',[validators.InputRequired(message="Transaction Amount required"),validators.Length(min=1,max=50)])
	password = PasswordField('Password',[validators.DataRequired()],id="pass")

class BuyCCForm(Form):
	amount = StringField('Amount',[validators.InputRequired(message="Transaction Amount required"),validators.Length(min=1,max=50)])


class OTPinput(Form):
	otp = StringField('OTP',[validators.InputRequired(message="OTP required"),validators.Length(min=6,max=6,message="OTP must be 6 digits")])


	 

 
	 

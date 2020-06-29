from wtforms import Form,StringField,DecimalField,IntegerField,TextAreaField,PasswordField, validators

class Registerform(Form):
	name = StringField('Full Name',[validators.InputRequired(message="Name required"),validators.Length(min=1,max=50,message="Full name must be between 1 and 50")],id="name")
	roll = StringField('Roll Number',[validators.InputRequired(message="Roll/Staff Number required"),validators.Length(min=1,max=15,message="Roll/Staff Number must be between 1 and 15")])
	email = StringField('Email',[validators.InputRequired(message="Email required"),validators.Length(min=6,max=50,message="Email must be between 6 and 50")])
	password = PasswordField('Password',[validators.DataRequired(),validators.EqualTo('confirm',message='Password Doesnot match!')])
	confirm = PasswordField('Confirm Password')


class SendCCForm(Form):
	roll = StringField('Roll Number',[validators.InputRequired(message="Recipient Roll/Staff Number required"),validators.Length(min=1,max=15,message='Recipient Roll/Staff Number')])
	amount = StringField('Amount',[validators.InputRequired(message="Transaction Amount required"),validators.Length(min=1,max=50)])
	password = PasswordField('Password',[validators.DataRequired()],id="pass")

class BuyCCForm(Form):
	amount = StringField('Amount',[validators.InputRequired(message="Transaction Amount required"),validators.Length(min=1,max=50)])


class OTPinput(Form):
	otp = StringField('OTP',[validators.InputRequired(message="OTP required"),validators.Length(min=6,max=6,message="OTP must be 6 digits")])
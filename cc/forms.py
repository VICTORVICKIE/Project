from wtforms import Form,StringField,DecimalField,IntegerField,TextAreaField,PasswordField, validators

class Registerform(Form):
	name = StringField('Full Name',[validators.Length(min=1,max=50)])
	roll = StringField('roll',[validators.Length(min=1,max=20)])
	email = StringField('Email',[validators.Length(min=6,max=50)])
	password = PasswordField('Password',[validators.DataRequired(),validators.EqualTo('confirm',message='Password Doesnot match!')])
	confirm = PasswordField('Confirm Password')


class SendCCForm(Form):
	roll = StringField('roll',[validators.Length(min=4,max=25)])
	amount = StringField('Amount',[validators.Length(min=1,max=50)])
	password = PasswordField('Password',[validators.DataRequired()])
class BuyCCForm(Form):
	amount = StringField('Amount',[validators.Length(min=1,max=50)])


class OTPinput(Form):
	otp = StringField('otp',[validators.Length(min=6,max=6)])
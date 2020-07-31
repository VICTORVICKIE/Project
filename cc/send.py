from email.message import EmailMessage
import smtplib


def send(email, message, purpose):
    msg = EmailMessage()
    to_email_addrs = email
    from_email_addrs = 'campuscoins2020@gmail.com'
    msg['From'] = from_email_addrs
    msg['To'] = to_email_addrs

    if purpose == 'Transaction':
        msg['Subject'] = 'OTP - Transaction'
        msg.set_content(f'The OTP for your Transaction is, {message}')

    if purpose == 'ChangePass':
        msg['Subject'] = 'OTP - Change Password'
        msg.set_content(f'The OTP to change your password is, {message}')

    if purpose == 'EmailVerify':
        msg['Subject'] = 'Verification Link'
        msg.set_content(f"""\
			<!DOCTYPE html>
			<html>
			<body>
			<h3>Click below to Verify Your Account</h3>
			
<div style="width: 100%;
  text-align: center;">
  <a style="padding:1em;
    text-align: center;
    display:inline-block;
    text-decoration: none !important;
    margin:0 auto;

    -webkit-transition: all 0.2s ease-in-out;
    -moz-transition: all 0.2s ease-in-out;
    -ms-transition: all 0.2s ease-in-out;
    -o-transition: all 0.2s ease-in-out;
    transition: all 0.2s ease-in-out;
    padding: 8px 12px; border: 1px solid #ED2939;
    border-radius: 2px;font-family: Helvetica, Arial, sans-serif;
    font-size: 14px; color: #0000FF;text-decoration: none;
    font-weight:bold;display: inline-block;" href="{message}" class="button" target="_blank" >Verify</a>
</div>

						</body>
						</html>""", subtype='html')

    if purpose == 'ResetPass':
        msg['Subject'] = 'Password Reset Link'
        msg.set_content(f"""\
			<!DOCTYPE html>
			<html>
			<body>
			<h3>Click below to Reset Password</h3>
			
<div style="width: 100%;
  text-align: center;">
  <a style="padding:1em;
    text-align: center;
    display:inline-block;
    text-decoration: none !important;
    margin:0 auto;

    -webkit-transition: all 0.2s ease-in-out;
    -moz-transition: all 0.2s ease-in-out;
    -ms-transition: all 0.2s ease-in-out;
    -o-transition: all 0.2s ease-in-out;
    transition: all 0.2s ease-in-out;
    padding: 8px 12px; border: 1px solid #ED2939;
    border-radius: 2px;font-family: Helvetica, Arial, sans-serif;
    font-size: 14px; color: #0000FF;text-decoration: none;
    font-weight:bold;display: inline-block;" href="{message}" class="button" target="_blank" >Reset</a>
</div>

						</body>
						</html>""", subtype='html')

    if purpose == 'receiver':
        msg['Subject'] = 'Amount Credited'
        amount = message.split("-")[1]
        sender = message.split("-")[0]
        msg.set_content(
            f'You received {amount} cc from {sender}\r\nTo check open: victorvickie.pythonanywhere.com')

    if purpose == 'sender':
        msg['Subject'] = 'Amount Debited'
        amount = message
        msg.set_content(
            f'You have been debited {amount} cc\r\nTo check open: victorvickie.pythonanywhere.com')

    p = 'bisfhskwmnkbpfac'

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(from_email_addrs, p)
        smtp.send_message(msg)

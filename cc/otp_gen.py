import math,random

def otp_gen():
	digits = "0123456789"
	otplen = 6
	OTP = ""
	for i in range(otplen):
		OTP += digits[math.floor(random.random() * 10)]

	return OTP
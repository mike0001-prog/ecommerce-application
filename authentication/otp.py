import time
import pyotp
from django.core.mail import send_mail
def generate_otp():
    secret = pyotp.random_base32()
    totp = pyotp.TOTP(secret, interval=300)
    otp = totp.now()
    return secret,otp
def send_email_otp(user,email,otp):
    subject = "OTP request"
    content = f"{user} your otp is {otp}"
    send_mail(subject,content,"kehindeoyeniyi08@gmail.com",[email])
    

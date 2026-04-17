import random ,os
from django.core.cache import cache
from django.core.mail import send_mail
from dotenv import load_dotenv


load_dotenv()

def gen_otp():
    return str(random.randint(100000,999999))

def send_otp_mail(user):

    otp = gen_otp()

    cache.set(
        f"otp:{user.email}",
        otp,
        timeout=300
    )

    print("OTP:", otp) 
    
    send_mail(
        subject="Your Email Verification Code",
        message= f"Your OTP is {otp}",
        from_email=os.getenv('EMAIL_HOST_USER'),
        recipient_list=[user.email],
    )
     
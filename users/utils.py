from django.core.mail import EmailMessage
from django.core.mail import send_mail as sm
from django.conf import settings
from cryptography.fernet import Fernet
from smtplib import SMTPException
import traceback




class Util:
    @staticmethod
    def send_email(email_content):
        try:
            sm(
                    subject = email_content['email_subject'],
                    message = email_content['email_body'],
                    from_email = 'security-noreply@insightupservices.com',
                    recipient_list  = [email_content['email_reciver']],
                    fail_silently= False,
                )
        except SMTPException as e:
            traceback.print_exc()
            print('There was an error sending an email: ', e) 


    @staticmethod
    def cryptograpy_text(text, encrypt = True):
        fernet = Fernet(settings.ENCRYPT_KEY)
        if encrypt:
            res = str(fernet.encrypt(bytes(text, 'utf-8')), 'utf-8')
        else:
            res = str(fernet.decrypt(bytes(text, 'utf-8')), 'utf-8')
        return res
        
        
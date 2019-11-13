import argparse
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from settings import *

def send_mail(to_email, message):
    server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
    server.starttls()
    server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
    server.sendmail(EMAIL_HOST_USER, to_email, message.as_string(),)
    server.quit()

def add_arguments(**options):
    parser = argparse.ArgumentParser(description='Processing mailer related arguements', usage='%(prog)s[options]')
    parser.add_argument('-e', '--to_email', default=None, nargs='+', help='Enter email-id with comma separated to send summary (e.g. \'a, b, c\')')
    args = parser.parse_args()
    return args

def mail_arguements(**options):
    args = add_arguments()
    if [args.to_email]:
        to_email = args.to_email
    else:
        to_email = 'avibilasgupta@gmail.com'
    return to_email 

message = MIMEMultipart()

message['subject'] = 'Automated Mailer Template'
message['From'] = EMAIL_HOST_USER
to_email = mail_arguements()
to_email = ', '.join(to_email)
message['To'] = to_email

body = 'Dear User, <br/>This mailer is a template for any random automated mailing system.<br/><br/>The table given below is a part of the template for providing with any table format while sending a mail.<br/><br/>'

body=MIMEText(body, 'html')
message.attach(body)

try:
    send_mail(to_email, message)
    print("Email successfully sent to ", to_email)
except:
    print("SMTPAuthenticationError")
    print("Email not sent")
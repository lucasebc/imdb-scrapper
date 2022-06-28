import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders

SENDER_MAIL = ''
SENDER_PASS = ''

SMTP_PROVIDER = [
    'smtp.office365.com'
    'smtp.gmail.com' # não testado
]

def writeMail(to, subject, body):
    msg = MIMEMultipart()
    msg['From'] = 'lucasebc@outlook.com'
    msg['To'] = to
    msg['Subject'] = subject
    body = body
    msg.attach(MIMEText(body, 'html'))

    return msg

def sendMail(mail, prov):
    p = SMTP_PROVIDER[0] if prov == 'outlook' else SMTP_PROVIDER[1]
    server = smtplib.SMTP(p, 587)  ### put your relevant SMTP here
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(SENDER_MAIL, SENDER_PASS)  ### if applicable
    server.send_message(mail)
    server.quit()
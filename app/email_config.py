
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

mail_id = "iosynctech@gmail.com"
app_pass = "nfzqqhxnxyzeizxg"


def setup_smtp():
    mail_conn = smtplib.SMTP('smtp.gmail.com', 587)
    mail_conn.ehlo()
    mail_conn.starttls()
    mail_conn.ehlo()
    mail_conn.login(mail_id, app_pass)
    
    return mail_conn

def send_mail(to, subject, mail_body):
    msg = MIMEMultipart()
    msg['From'] = mail_id
    msg['To'] = to
    msg['Subject'] = subject + f" {datetime.now().strftime('%d-%b-%Y')}"
    
    message = MIMEText(mail_body, 'html')
    msg.attach(message)  
    #msg.set_content(message)
    
    mail_conn = setup_smtp()

    mail_conn.sendmail(mail_id, to, msg.as_string()) 
    mail_conn.quit()

def send_missed_mail(to):
     with open('missed.html', 'r') as file:
            file_data = file.read()
            send_mail(to=to, subject="IOSync Missed Task", mail_body= file_data)


    

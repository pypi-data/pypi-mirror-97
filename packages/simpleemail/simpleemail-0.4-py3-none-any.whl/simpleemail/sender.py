import smtplib
from email.mime.multipart import MIMEMultipart


def send_email(email_message: MIMEMultipart, smtp_server: str, test_run: bool, user='', password=''):
    if not email_message:
        raise ValueError('email_message must exist.')
    sender = email_message['From']
    recipient = email_message['To'].split(', ')
    if test_run:
        print("{} -> {} \n {}\n\n".format(sender, recipient, email_message.as_string()))
    else:
        with smtplib.SMTP(smtp_server) as s:
            if user and password:
                s.login(user, password)
            s.sendmail(sender, recipient, email_message.as_string())
            s.quit()

import smtplib
from email.mime.text import MIMEText

SENDER = "mdshahnawazmomin2@gmail.com"
PASSWORD = "momin@123"
RECEIVER = "ibraheemmomin24@gmail.com"


def send_email(subject, body):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SENDER
    msg["To"] = RECEIVER

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(SENDER, PASSWORD)
    server.send_message(msg)
    server.quit()

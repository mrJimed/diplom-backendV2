import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr

from settings import FROM_EMAIL, EMAIL_PASSWORD, SMTP_PORT, SMTP_HOST


def send_email(to_email: str, subject: str, text: str):
    message = MIMEMultipart()
    message['From'] = formataddr(('Annotation', FROM_EMAIL))
    message['To'] = to_email
    message['Subject'] = subject
    message.attach(MIMEText(text, 'plain'))

    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(FROM_EMAIL, EMAIL_PASSWORD)
        server.sendmail(FROM_EMAIL, to_email, message.as_string())

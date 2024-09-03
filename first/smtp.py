import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_username = 'maghadheera03@gmail.com'
smtp_password = 'maheshwar@123'
sender_email = smtp_username
recipient_email = 'hotcoder97@gmail.com'
#bendakay9@gmail.com  -- >  28-929
message = MIMEMultipart()
message['From'] = sender_email
message['To'] = recipient_email
message['Subject'] = 'Test Email'
body = 'This is a test email.'
message.attach(MIMEText(body, 'plain'))

try:
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_username, smtp_password)
    server.sendmail(sender_email, recipient_email, message.as_string())
    print('Email sent successfully')
except Exception as e:
    print(f'Error sending email: {e}')
finally:
    server.quit()

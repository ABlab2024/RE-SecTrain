import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# Hardcoded credentials as requested by user
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = "ablab2024@gmail.com"
SMTP_PASSWORD = "zesp xxdf tckf gome"
EMAIL_FROM = "ablabs2024@gmail.com"

def send_email(target_email, subject, body, tracking_link):
    """
    Sends an HTML email using Gmail SMTP.
    Appends a tracking link to the body.
    """
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_FROM
        msg['To'] = target_email
        msg['Subject'] = subject

        # Append tracking link to the body
        html_body = f"""
        <html>
        <body>
            {body}
            <br><br>
            <hr>
            <p>To verify your account or take action, please click the link below:</p>
            <a href="{tracking_link}">Secure Action Link</a>
        </body>
        </html>
        """

        msg.attach(MIMEText(html_body, 'html'))

        # Connect to SMTP server
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        
        # Send email
        server.send_message(msg)
        server.quit()
        return True, "Email sent successfully"
    except Exception as e:
        return False, str(e)

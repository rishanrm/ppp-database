import smtplib
import ssl

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from config import Config

class Email():

    @staticmethod
    def send_email(form):
        sender_email = Config.CONTACT_EMAIL_ADDR
        receiver_email = Config.CONTACT_EMAIL_ADDR

        message = MIMEMultipart("alternative")
        message["Subject"] = f"PPP Data Contact Form Submission: {form.email.data}"
        message["From"] = sender_email
        message["To"] = receiver_email

        # Create the plain-text and HTML version of your message
        text = f"""\
PPP Data Contact Form Submission

Name: {form.name.data}

Email: {form.email.data}

Organization: {form.organization.data}

Message: {form.message.data}"""

        html = f"""\
        <html>
        <body>
            <h2>PPP Data Contact Form Submission</h2>
            <p>
                <b style='color: #037AFB;'>Name:</b> {form.name.data}<br><br>
                <b style='color: #037AFB;'>Email:</b> {form.email.data}<br><br>
                <b style='color: #037AFB;'>Organization:</b> {form.organization.data}<br><br>
                <b style='color: #037AFB;'>Message:</b> {form.message.data}
            </p>
        </body>
        </html>
"""

        # Turn these into plain/html MIMEText objects
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part1)
        message.attach(part2)

        # Create secure connection with server and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            # with smtplib.SMTP_SSL("smtp.gmail.com", 587, context=context) as server:
            server.login(Config.CONTACT_EMAIL_ADDR, Config.CONTACT_EMAIL_PASS)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )
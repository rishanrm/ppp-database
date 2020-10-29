from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length
import smtplib
from app.config import Config

# class ContactForm(FlaskForm):
#     """Contact form."""
#     name = StringField('Name', validators=[DataRequired()])
#     email = StringField('Email', validators=[DataRequired(), Email(message=('Not a valid email address.'))])
#     organization = StringField('Organization (optional)')
#     message = TextAreaField('Message',
#                         validators=[DataRequired(), Length(min=4, message=('Your message is too short.'))])
#     # recaptcha = RecaptchaField()
#     submit = SubmitField('Submit')


class ContactForm(FlaskForm):
    """Contact form."""
    # name = StringField('Name', validators=[DataRequired()])
    # email = StringField('Email', validators=[DataRequired(), Email(message=('Not a valid email address.'))])
    # organization = StringField('Organization (optional)')
    # message = TextAreaField('Message',
    #                         validators=[DataRequired(), Length(min=4, message=('Your message is too short.'))])
    # # recaptcha = RecaptchaField()
    # submit = SubmitField('Submit')

    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    organization = StringField('Organization (optional)')
    message = TextAreaField('Message',
        validators=[DataRequired(), Length(min=4, message=('Your message is too short.'))])
    recaptcha = RecaptchaField()
    submit = SubmitField('Submit')

    email_message = f"""Message from the PPP Contact Form:

Name: {name}

Email: {email}

Organization: {organization}

Message: {message}
"""
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(Config.CONTACT_EMAIL_ADDR, Config.CONTACT_EMAIL_PASS)
    # server.sendmail(Config.CONTACT_EMAIL_ADDR, Config.CONTACT_EMAIL_ADDR, email_message)
    # server.login('rishanrm@gmail.com', Config.CONTACT_EMAIL_PASS)
    server.sendmail(Config.CONTACT_EMAIL_ADDR,
                    Config.CONTACT_EMAIL_ADDR, email_message)

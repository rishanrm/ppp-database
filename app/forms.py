from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length

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
    # recaptcha = RecaptchaField()
    submit = SubmitField('Submit')

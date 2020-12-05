from flask import current_app, render_template, request, Blueprint, url_for, flash, redirect, send_file

# from config import Config
from get_data import Data
from forms import ContactForm
from send_email import Email

main = Blueprint('main', __name__)

@main.route("/", methods=['GET', 'POST'])
@main.route("/index", methods=['GET', 'POST'])
@main.route("/home", methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@main.route("/data-under-150k")
def data_under_150k():
    return render_template('data-under-150k.html', data="", headers=current_app.config["HEADERS_UNDER_150K"])

@main.route("/data-150k-and-up")
def data_150k_and_up():
    print(current_app.config)
    return render_template("data-150k-and-up.html", data="", headers=current_app.config["HEADERS_150K_AND_UP"])

@main.route("/about")
def about():
    return render_template('about.html')

@main.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        Email.send_email(form)
        flash("Your message has been sent!", "success")
        return redirect(url_for('main.index'))
    return render_template('contact.html', title='Contact', form=form)

@main.route("/privacy")
def privacy():
    return render_template('privacy.html')

@main.route("/terms")
def terms():
    return render_template('terms.html')

@main.route('/data/')
def data():
    return Data.get_data(request)

@main.route('/header_options/')
def header_options():
    try:
        return send_file('static\data\column_options.json')
    except Exception as e:
        return str(e)
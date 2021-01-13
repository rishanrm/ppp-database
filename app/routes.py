from flask import current_app, render_template, request, Blueprint, url_for, flash, redirect, send_file, send_from_directory

from get_data import Data
from forms import ContactForm
from send_email import Email

main = Blueprint('main', __name__)

@main.route("/", methods=['GET', 'POST'])
# @main.route("/index", methods=['GET', 'POST'])
# @main.route("/home", methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@main.route("/all-data")
def all_data():
    return render_template("all-data.html", data="", headers=current_app.config["HEADERS_ALL_DATA"])

@main.route("/summary-stats")
def summary_stats():
    return render_template("summary-stats.html", data="", headers=current_app.config["HEADERS_DATA_SUMMARY"])

@main.route("/data-notes")
def data_notes():
    return render_template("data-notes.html", data="")

@main.route("/data-notes-download")
def data_notes_download():
    path = "./static/data/ppp_data_state_changes.csv"
    return send_file(path, as_attachment=True)

@main.route("/all-data-test")
def all_data_test():
    return render_template("all-data-test.html", data="", headers=current_app.config["HEADERS_ALL_DATA"])

@main.route("/data-under-150k")
def data_under_150k():
    return render_template('data-under-150k.html', data="", headers=current_app.config["HEADERS_UNDER_150K"])

@main.route("/data-150k-and-up")
def data_150k_and_up():
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

@main.route('/robots.txt')
@main.route('/sitemap.xml')
def static_from_root():
    return send_from_directory(current_app.static_folder, request.path[1:])


@main.app_errorhandler(403)
def page_forbidden(e):
    return render_template('errors/403.html'), 403

@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404

@main.app_errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html'), 500

@main.app_errorhandler(503)
def service_unavailable(e):
    return render_template('errors/503.html'), 503


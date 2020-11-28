import json
from flask import render_template, request, Blueprint, current_app, send_from_directory, jsonify, url_for, flash, redirect, send_file
#from flask import Flask, url_for, render_template, redirect
# from flask import url_for, redirect
from ..forms import ContactForm

#from app.models import Post
from app import db
#from app import app
from app.config import Config
from app.database import DatabaseConnection
import os
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

main = Blueprint('main', __name__)


@main.route("/", methods=['GET', 'POST'])
@main.route("/index", methods=['GET', 'POST'])
@main.route("/home", methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@main.route("/data-under-150k")
def data_under_150k():
    return render_template('data-under-150k.html', data="", headers = Config.HEADERS_UNDER_150K)

@main.route("/data-150k-and-up")
def data_150k_and_up():
    return render_template('data-150k-and-up.html', data="", headers=Config.HEADERS_150K_AND_UP)

@main.route("/about")
def about():
    return render_template('about.html')

# @main.route("/contact")
# def contact():
#     return render_template('contact.html')

@main.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        sender_email = Config.CONTACT_EMAIL_ADDR
        receiver_email = Config.CONTACT_EMAIL_ADDR
        # password = input("Type your password and press enter:")

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


#         email_message = f"""Message from the PPP Contact Form:

# Name: {form.name.data}

# Email: {email.data}

# Organization: {organization.data}

# Message: {message.data}
# """
#     server = smtplib.SMTP("smtp.gmail.com", 587)
#     server.starttls()
#     server.login(Config.CONTACT_EMAIL_ADDR, Config.CONTACT_EMAIL_PASS)
#     # server.sendmail(Config.CONTACT_EMAIL_ADDR, Config.CONTACT_EMAIL_ADDR, email_message)
#     # server.login('rishanrm@gmail.com', Config.CONTACT_EMAIL_PASS)
#     server.sendmail(Config.CONTACT_EMAIL_ADDR,
#                     Config.CONTACT_EMAIL_ADDR, email_message)
        flash("Your message has been sent!", "success")
        # return redirect(url_for('main.contact'))
        return redirect(url_for('main.index'))
    return render_template('contact.html', title='Contact', form=form)




@main.route("/privacy")
def privacy():
    return render_template('privacy.html')

@main.route("/terms")
def terms():
    return render_template('terms.html')


@main.route("/wf")
def wf():
    return render_template('wf.html')

@main.route("/barba")
def barba():
    return render_template('barba.html')

@main.route("/barba-services")
def barba_services():
    return render_template('barba-services.html')

@main.route("/barba2")
def barba2():
    return render_template('barba2.html')

@main.route("/barba2page2")
def barba2page2():
    return render_template('barba2page2.html')

@main.route("/bnew")
def bnew():
    return render_template('bnew.html')

@main.route("/bnew2")
def bnew2():
    return render_template('bnew2.html')

@main.route("/navbar")
def navbar():
    return render_template('navbar.html')

@main.route("/gsap")
def gsap():
    return render_template('gsap.html')

@main.route("/table_examples")
def table_examples():
        return render_template('table_examples.html', title='Table Examples')

@main.route('/<int:number>/')
def incrementer(number):
        return "Incremented number is " + str(number+1)

@main.route('/person/')
def specific_person():
        return jsonify({'name':'Alice',
                                        'address':'USA'})

@main.route('/params/')
def params():
    state = ""
    db_name = ""
    table_name = ""

    if "filter" in request.args:
        print(request.args["filter"])
        substr = 'state":"'
        state_index = request.args["filter"].index(substr)+len(substr)
        state = request.args["filter"][state_index:state_index+2]
    else:
        print("NO STATE")

    print(request.args["page"])
    # sub_url = request.args["page"]
    if request.args["page"] == "data-under-150k":
        db_name = Config.DB_NAME_ROOT_UNDER_150K
        table_name = Config.DB_NAME_ROOT_UNDER_150K + "_" + state.lower()
    elif request.args["page"] == "data-150k-and-up":
        db_name = Config.DB_NAME_ROOT_150K_AND_UP
        table_name = Config.DB_NAME_ROOT_150K_AND_UP
    print(db_name)
    print(table_name)

    print("REQUEST START:")
    print(request.args)
    print("REQUEST END")

    with current_app.app_context():
        db = DatabaseConnection("local", db_name, table_name)
        # db = DatabaseConnection("local", Config.DB_NAME, Config.TABLE_NAME)
#        db = DatabaseInitialization.initialize_database("local")

    total_count = db.fetch_total_count()
    total_count_str = db.get_json_component(total_count, "total")

    filtered_results_count = db.run_sql_query(request.args, ["search", "filter"], "count")
    filtered_count_str = "\"total\": " + str(filtered_results_count)
    
    results_data = db.run_sql_query(request.args, ["search", "filter", "sort", "offset", "limit"], "data")
    results_str = db.get_json_component(results_data, "data")

    table_data_json = db.build_table_json(filtered_count_str, total_count_str, results_str)
    print(type(table_data_json))

    print("PARAMS ROUTE")
    print(type(json.loads(table_data_json)))

    return json.loads(table_data_json)

@main.route('/query-example')
def query_example():
        language = request.args.get('language') #if key doesn't exist, returns None
        args = request.args
        return f'''<h1>The language value is: {language}</h1><h1>{args}</h1>'''

@main.route('/form-example', methods=['GET', 'POST']) #allow both GET and POST requests
def form_example():
        return '''<form method="POST">
                                    Language: <input type="text" name="language"><br>
                                    Framework: <input type="text" name="framework"><br>
                                    <input type="submit" value="Submit"><br>
                            </form>'''

# @main.route('/fetch_OLD')
# def fetch_OLD():
#     language = request.args.get('language') #if key doesn't exist, returns None
#     args = request.args
#     return f'''<h1>The language value is: {language}</h1><h1>{args}</h1>'''
#     #fetch_from_db

@main.route('/fetch')
def fetch():
#    db = DatabaseInitialization.initialize_database("local")
    db = DatabaseConnection("local", Config.DB_NAME, Config.TABLE_NAME)
#    db.fetch_most_recent(5)

#    db.fetch_json(5)
    total_count = db.fetch_total_count()
    total_count_str = db.get_json_component(total_count, "total")
    results_data = db.fetch_from_db()
    results_str = db.get_json_component(results_data, "data")
    table_data_json = db.build_table_json(total_count_str, len(results_data), results_str)
#    return jsonify(table_data_json)
#    return json.dumps(table_data_json)
    return json.loads(table_data_json)

@main.route('/data_test/<column>.json')
def data_test(column):
    db = DatabaseConnection("local", Config.DB_NAME, Config.TABLE_NAME)
    
    column_options = db.get_column_options(column)    
    options_dict = db.get_column_options_dict(column_options, column)
    return json.loads(json.dumps(options_dict))
    
@main.route('/header_options/')
def header_options():
    print("In new header_options")
    try:
        return send_file('static\data\data.json')
    except Exception as e:
        return str(e)


@main.route("/data", methods=['GET'])
def data():
        # path = './static/example_copy.json'
        # return path
        all_data = db.Table(Config.TABLE_NAME, db.metadata, autoload=True, autoload_with=db.engine)
        data = db.session.query(all_data).all()
        return jsonify(data)

@main.route("/complete")
def complete():
        return render_template('complete.html')
    
@main.route("/data2")
def data2():
        return render_template('data2.html')

@main.route("/get_datax")
def get_datax():
        import collections
        return render_template('get_datax.html')
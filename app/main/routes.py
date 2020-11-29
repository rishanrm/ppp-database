import json
from flask import render_template, request, Blueprint, current_app, url_for, flash, redirect, send_file

from app.config import Config
from app.database import DatabaseConnection
from app.forms import ContactForm
from app.email import Email

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
        state = "unstated"

    print(request.args["page"])
    # sub_url = request.args["page"]
    if request.args["page"] == "data-under-150k":
        db_name = Config.DB_NAME_ROOT_UNDER_150K
        table_name = Config.DB_NAME_ROOT_UNDER_150K + "_" + state.lower()
    elif request.args["page"] == "data-150k-and-up":
        db_name = Config.DB_NAME_ROOT_150K_AND_UP
        table_name = Config.DB_NAME_ROOT_150K_AND_UP
    # print(db_name)
    # print(table_name)

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

@main.route('/header_options/')
def header_options():
    print("In new header_options")
    try:
        return send_file('static\data\data.json')
    except Exception as e:
        return str(e)


from flask import render_template, request, Blueprint, current_app
#from app.models import Post
from ppp_dashboard import db
#from ppp_dashboard import app
from ppp_dashboard.config import Config
from ppp_dashboard.database import DatabasePopulation

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():

    with current_app.app_context():
        all_data = db.Table(current_app.config.TABLE_NAME, db.metadata, autoload=True, autoload_with=db.engine)
        data = db.session.query(all_data).all()
        csv_column_headers = DatabasePopulation.get_csv_column_headers(current_app.config.SOURCE_FILE_NAME)
#        for r in data:
#            print(r)
#    page = request.args.get('page', 1, type=int)
#    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=current_app.config['RESULTS_PER_PAGE'])
#    return render_template('home.html', posts=posts)
#    return render_template('home.html', data = data)
    return render_template('home.html', data=data, headers = csv_column_headers)

@main.route("/about")
def about():
    return render_template('about.html', title='About')

@main.route("/index")
def index():
    return render_template('index.html')

@main.route("/data")
def data():
    return render_template('data.html')


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
    return jsonify({'name': 'Alice',
                    'address': 'USA'})


@main.route('/query-example')
def query_example():
    # if key doesn't exist, returns None
    language = request.args.get('language')
    args = request.args
    return f'''<h1>The language value is: {language}</h1><h1>{args}</h1>'''


# allow both GET and POST requests
@main.route('/form-example', methods=['GET', 'POST'])
def form_example():
    return '''<form method="POST">
                                    Language: <input type="text" name="language"><br>
                                    Framework: <input type="text" name="framework"><br>
                                    <input type="submit" value="Submit"><br>
                            </form>'''


@main.route('/fetch')
def fetch():
    #    db = DatabaseInitialization.initialize_database("local")
    db = DatabaseConnection(
        current_app.config.DB_LOCATION, current_app.config.DB_NAME, current_app.config.TABLE_NAME)
#    db.fetch_most_recent(5)

#    db.fetch_json(5)
    total_count = db.fetch_total_count()
    total_count_str = db.get_json_component(total_count, "total")
    results_data = db.fetch_from_db()
    results_str = db.get_json_component(results_data, "data")
    table_data_json = db.build_table_json(
        total_count_str, len(results_data), results_str)
#    return jsonify(table_data_json)
#    return json.dumps(table_data_json)
    return json.loads(table_data_json)

# @main.route('/fetch_OLD')
# def fetch_OLD():
#     language = request.args.get('language') #if key doesn't exist, returns None
#     args = request.args
#     return f'''<h1>The language value is: {language}</h1><h1>{args}</h1>'''
#     #fetch_from_db


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


@main.route('/data_test/<column>.json')
def data_test(column):
    db = DatabaseConnection(current_app.config.DB_LOCATION, current_app.config.DB_NAME, current_app.config.TABLE_NAME)

    column_options = db.get_column_options(column)
    options_dict = db.get_column_options_dict(column_options, column)
    return json.loads(json.dumps(options_dict))


@main.route("/data", methods=['GET'])
def data():
    # path = './static/example_copy.json'
    # return path
    all_data = db.Table(current_app.config.TABLE_NAME, db.metadata,
                        autoload=True, autoload_with=db.engine)
    data = db.session.query(all_data).all()
    return jsonify(data)

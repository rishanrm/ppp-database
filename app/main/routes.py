from flask import render_template, request, Blueprint, current_app, send_from_directory
#from app.models import Post
from app import db
#from app import app
from app.config import Config
from app.database import DatabasePopulation

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():

    with current_app.app_context():
        all_data = db.Table(Config.TABLE_NAME, db.metadata, autoload=True, autoload_with=db.engine)
        data = db.session.query(all_data).all()
        csv_column_headers = DatabasePopulation.get_csv_column_headers(Config.SOURCE_FILE_NAME)
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
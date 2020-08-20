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
        all_data = db.Table(Config.TABLE_NAME, db.metadata, autoload=True, autoload_with=db.engine)
        data = db.session.query(all_data).all()
        csv_column_headers = DatabasePopulation.get_csv_column_headers(Config.SOURCE_FILE_NAME)
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

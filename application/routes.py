from application import app
from application.forms import BasicForm
from flask import render_template, request, g, flash,redirect, url_for
import pymysql
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

auth = HTTPBasicAuth()

users = {
	"admin": generate_password_hash("admin"),
	"DV8staff": generate_password_hash("password")
}
roles = {
	"admin": ['admin'],
	"DV8staff": []
}
@auth.verify_password
def verify_password(username, password):
	if username in users and \
			check_password_hash(users.get(username), password):
		return username

@auth.get_user_roles
def get_user_roles(user):
	return roles[user]

def connect_db():
    return pymysql.connect(
        user = 'root', password = 'password', database = 'dv8',
        autocommit = True, charset = 'utf8mb4',
        cursorclass = pymysql.cursors.DictCursor)

def get_db():
    if not hasattr(g, 'db'):
        g.db = connect_db()
    return g.db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'db'):
        g.db.close()

def get_date():

    today = "Today"
    app.logger.info(f"In get_date function! Update so it returns the correct date! {today}")
    return today

@app.route('/', methods = ['GET','POST'])
def home():
    cursor = get_db().cursor()
    cursor.execute()
    result = cursor.fetchall()
    app.logger.info(result)
    return render_template(
                'home.html',
                title="",
                description=f"Python, MySQL, Flask & Jinja. {get_date()}",
                records=result,
        user = auth.current_user()
    )

@app.route('/register1', methods = ['GET','POST'])
@auth.login_required
def register():

    error = ""
    form = BasicForm() # create form instance

    # if page is loaded as a post i.e. user has submitted the form
    if request.method == "POST":
        first_name = form.first_name.data
        last_name = form.last_name.data

        app.logger.info(f"We were given: {first_name} {last_name}")

        if len(first_name) == 0 or len(last_name) == 0:
            error = "Please supply both first and last names."
        else:
            return 'Thank you!'

    return render_template(
                'form1.html',
                title="Simple form!",
                description=f"Using Flask with  a form on {get_date()}",
                form=form,
                message=error,
    user = auth.current_user()
    )
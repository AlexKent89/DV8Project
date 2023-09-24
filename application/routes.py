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
        user = 'root', password = 'password', database = 'mydb',
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

@app.route('/', methods=['GET', 'POST'])
def home():
    cursor = get_db().cursor()
    cursor.execute("SELECT * from dv8customers order by name desc")
    result = cursor.fetchall()
    app.logger.info(result)
    return render_template(
        'home.html',
        title="",
        description=f"Python, MySQL, Flask & Jinja. {get_date()}",
        records=result,  # Pass the result data to the template
        user=auth.current_user()
    )
@app.route('/register', methods = ['GET','POST'])
@auth.login_required
def register():
    """ Basic form.
    """
    error = ""
    form = BasicForm() # create form instance

    # if page is loaded as a post i.e. user has submitted the form
    if request.method == "POST":
        name = form.name.data
        address = form.address.data
        post_code = form.post_code.data
        email = form.email.data

        app.logger.info(f"We were given: {name} {address} {post_code} {email}")

        if len(name) == 0 or len(address) == 0 or len(post_code) ==0 or len(email) ==0:
            error = "Please supply name, address, post code and email."
        else:
            return 'Thank you!'

    return render_template(
                'registerform.html',
                title="Simple form!",
                description=f"Using Flask with  a form on {get_date()}",
                form=form,
                message=error,
    user = auth.current_user()
    )
@app.route('/register2',  methods = ['GET','POST'])
@auth.login_required
def register2():
    """ Second form.
    """
    message = ""
    form = BasicForm() # create form instance
    if form.validate_on_submit():
        name = form.name.data
        address = form.address.data
        post_code = form.post_code.data
        email = form.email.data

        app.logger.info(f" {name} {address} {post_code} {email} being added.")
        try:
            cursor = get_db().cursor()
            sql = "INSERT INTO `dv8customers` (name, address, post code, email) VALUES (%s, %s)"
            app.logger.info(sql)
            cursor.execute(sql, (name(), address(), post_code.upper(), email()))
            message = "Record successfully added"
            app.logger.info(message)
            flash(message)
            return redirect(url_for('home'))
        except Exception as e:
            message = f"error in insert operation: {e}"
            flash(message)
    return render_template('registerform.html', message=message, form=form, title='Customer Registration Form', description='DB Connect', user = auth.current_user()
)
@app.route('/records', methods=['GET', 'POST'])
@auth.login_required
def display_records():
    cursor = get_db().cursor()
    cursor.execute("SELECT * from dv8customers order by name desc")
    result = cursor.fetchall()
    app.logger.info(result)
    return render_template(
        'records.html',
        records=result,  # Pass the result data to the template
        user=auth.current_user()
    )
@app.route('/dv8customers/delete/<int:id>')
@auth.login_required(role='admin')
def dv8customers_delete(id):
    """ Fourth route. Param for deleting from dv8customers table
    """
    app.logger.info(id)
    try:
        cursor = get_db().cursor()
        cursor.execute("DELETE FROM dv8customers WHERE customers_id=%s ",id)
        message=f"Deleted customers id {id}"
        app.logger.info(message)
        flash(message)
    except Exception as e:
        message = f"error in insert operation: {e}"
        flash(message)
    return redirect(url_for('home'))
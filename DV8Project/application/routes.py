import pymysql
from flask import Flask

from flask import render_template,request,redirect,url_for
from flask_bootstrap import Bootstrap
app = Flask(__name__)
# MySQL configuration
#db = mysql.connector.connect(
   # host="your_database_host",
    #user="root",
    #password="password",
    #database="mydb"
#)

def connect_db():
    return pymysql.Connect(
        user="root",
        password="password",
        database="mydb"
            )


@app.route('/')
def index():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        name = request.form['Name']
        address = request.form['Address']
        postcode = request.form['Postcode']
        email = request.form['Email']

        # Store data in the MySQL database
        cursor = db.cursor()
        cursor.execute("INSERT INTO your_table_name (Name, Address, Postcode, Email) VALUES (%s, %s, %s, %s)",
                       (name, address, postcode, email))
        db.commit()
        cursor.close()

        return "Registration successful!"
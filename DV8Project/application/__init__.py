from flask import Flask
from flask_bootstrap import Bootstrap
from flask import render_template
import _mysql_connector
app = Flask(__name__)
# MySQL configuration






app.config['SECRET_KEY'] = 'MYSECRETKEY'
import Bootstrap
if __name__ == '__main__':
    app.run(debug=True)


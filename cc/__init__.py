from flask import Flask
import os
from flask_mysqldb import MySQL



########################################    INITIALIZING  APP and DB   ##########################################

app = Flask(__name__)									 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'VIGNESHkumar14'
app.config['MYSQL_DB'] = 'CAMPUS_COINS'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config.update(SECRET_KEY=os.urandom(24))

mysql = MySQL(app)

from cc import routes
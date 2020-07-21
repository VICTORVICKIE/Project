from flask import Flask
import os
from flask_mysqldb import MySQL
from platform import system

current_system = system()


########################################    INITIALIZING  APP and DB   ##########################################
if current_system == 'Linux':
	app = Flask(__name__)
	app.config['MYSQL_HOST'] = 'victorvickie.mysql.pythonanywhere-services.com'
	app.config['MYSQL_USER'] = 'victorvickie'
	app.config['MYSQL_PASSWORD'] = 'VIGNESHkumar@14'
	app.config['MYSQL_DB'] = 'victorvickie$CAMPUS_COINS'

elif current_system == 'Windows':
	app = Flask(__name__)
	app.config['MYSQL_HOST'] = 'localhost'
	app.config['MYSQL_USER'] = 'root'
	app.config['MYSQL_PASSWORD'] = 'VIGNESHkumar14'
	app.config['MYSQL_DB'] = 'CAMPUS_COINS'

app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

app.config.update(SECRET_KEY=os.urandom(24))
mysql = MySQL(app)

from cc import routes
from flask import Flask
import os
import getpass
from flask_mysqldb import MySQL
from platform import system

current_system = system()

app = Flask(__name__)
########################################    INITIALIZING  APP and DB   ##########################################
if current_system == 'Linux':

    app.config['MYSQL_HOST'] = 'MYSQL HOST ADDRESS'
    app.config['MYSQL_USER'] = 'MYSQL USERNAME'
    app.config['MYSQL_PASSWORD'] = 'MSQL PASSWORD'
    app.config['MYSQL_DB'] = 'MYSQL DB NAME'

elif current_system == 'Windows':
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_DB'] = 'CAMPUS_COINS'
    if getpass.getuser() == 'V1ct0R':
        app.config['MYSQL_PASSWORD'] = 'VIGNESHkumar14'
    if getpass.getuser() == 'Victor':
        app.config['MYSQL_PASSWORD'] = 'VIGNESHkumar14'
    if getpass.getuser() == 'Admin':
        app.config['MYSQL_PASSWORD'] = 'naveen'
    if getpass.getuser() == 'Santhosh Raajaa':
        app.config['MYSQL_PASSWORD'] = '$Anraaj611'
    if getpass.getuser() == 'Prasath Sp10':
        app.config['MYSQL_PASSWORD'] = '22jan2001'
    if getpass.getuser() == 'Dharani':
        app.config['MYSQL_PASSWORD'] = 'Vetri@17'
    if getpass.getuser() == 'vetri':
        app.config['MYSQL_PASSWORD'] = 'Vetri@17'


app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

app.config.update(SECRET_KEY=os.urandom(24))
mysql = MySQL(app)
from cc import routes

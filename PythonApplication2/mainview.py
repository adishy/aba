#########################################################################################
#FLASK MAIN MODULE
#########################################################################################
from flask import Flask

#########################################################################################
#FLASK SOCKETIO MODULE
#########################################################################################
from flask_socketio import SocketIO

#########################################################################################
#FLASK SQLALCHEMY MODULE
#########################################################################################
from flask_sqlalchemy import SQLAlchemy

#########################################################################################
#FLASK SESSION STORAGE MODULES  
#########################################################################################
from flask_sessionstore import Session  

from flask_whooshee import Whooshee

#Create an instance of a Flask object
app = Flask(__name__)

#Set Flask object to debug mode
app.debug = True

#Set a secret key for the Flask object
app.secret_key = '''9916A2CC6BC5787E58C471A469948DCE5C4889797F96555BB8D1B89DDAD9EE1599
					16A2CC6BC5787E58C471A469948DCE5C4889797F96555BB8D1B89DDAD9EE157CEE
					B9CB84C4A4E38C4E7AE1D652E797A085FC8A5C0E1249C962BDF112E591DC9916A2
					CC6BC5787E58C471A469948DCE5C4889797F96555BB8D1B89DDAD9EE159916A2CC
					6BC5787E58C471A469948DCE5C4889797F96555BB8D1B89DDAD9EE157'''

#Set the database of the Flask object to an sqlite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///helpdesk.sqlite3'

#Set SQLAlchmey database modification tracking to False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['WHOOSHEE_ENABLE_INDEXING'] = True

#Set the storage type for the current session on the server
app.config['SESSION_TYPE'] = 'sqlalchemy'

app.config['WHOOSHEE_DIR'] = 'search_index_list/'

#Create the current session on the server
session = Session(app)

#Create the database for the current session on the server
session.app.session_interface.db.create_all()

#Create a SocketIO object from the Flask object
socketio = SocketIO(app)

#Create an SQLAlchemy object from the Flask object
db = SQLAlchemy(app)

whooshee = Whooshee(app)

whooshee.reindex()

#########################################################################################
#FLASK HELP DESK ROUTES
#########################################################################################
from mainHelpDeskRoutes import *

#########################################################################################
#SOCKETIO HELP DESK ROUTES
#########################################################################################
from socketHelpDeskRoutes import *

if __name__ == '__main__':

	socketio.run(app, host='0.0.0.0')

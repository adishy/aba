import json
#########################################################################################
#FLASK APP
#########################################################################################
from mainview import app

#########################################################################################
#FLASK SQLALCHEMY DB
#########################################################################################
from mainview import db

from dataModels import *

#########################################################################################
#FLASK MODULES
#########################################################################################
from flask import render_template

from flask import url_for

from flask import redirect

from flask import session

from flask import jsonify

from flask import request

from flask import Response
#########################################################################################
#SESSION HELPERS
#########################################################################################
from flaskSession import *

#########################################################################################
#OAUTH SIGNIN HELPERS
#########################################################################################
from OAuthLoginChecking import *

from helpDeskRouteHelpers import *

#########################################################################################
#TEMPLATE PAGE RESOURCES
#########################################################################################
from constKeys import DEFAULTUSER_RESOURCES

#########################################################################################
#TODO: Remove this route
#Deletes all records in the support ticket list
@app.route('/deleteall')
def removealltickets():
	db.session.query(supportticketslist).delete()
	db.session.commit()
	return redirect('currentsupportticketsview')
#########################################################################################

#########################################################################################
'''
ROUTE: '/'
(mainview())
Checks whether the current user has a valid session then displays the login page if 
the session is invalid otherwise displays the main page based on the type of the current
user'''
@app.route('/' + SERVER_PATH)
def mainview():
	if not sessionKeyValid(USER_SESSION_KEY):
		return redirect('/' + SERVER_PATH + 'login')

	if supportstaffuser(session[USER_SESSION_KEY]) and supportstaffadmin(session[USER_SESSION_KEY]):
		return render_template('mainviewadmin.html', **DEFAULTUSER_RESOURCES, **ADMINUSER_RESOURCES)

	if supportstaffuser(session[USER_SESSION_KEY]):
		return render_template('mainviewstaff.html', **DEFAULTUSER_RESOURCES, **ADMINUSER_RESOURCES)

	return render_template('mainview.html', **DEFAULTUSER_RESOURCES)
#########################################################################################


#########################################################################################

'''
ROUTE: '/login'
(login())
Checks whether the current user has a valid session then displays the login page if
the session is invalid otherwise redirects the user to the main page
'''

@app.route('/' + SERVER_PATH + 'login')
def login():
	if not sessionKeyValid(USER_SESSION_KEY):
		return render_template('login.html')

	else:
		return redirect('/' + SERVER_PATH)
#########################################################################################

#########################################################################################
#Checks whether the current user's OAuth token is valid then returns the url for the 
#main page if the current token valid otherwise returns the url for the login page
@app.route('/' + SERVER_PATH + 'login_request', methods = ['POST'])
def finishlogin():
	if checkSignedIn() and not sessionKeyValid(USER_SESSION_KEY):
		return jsonify(pageurl = url_for('mainview'))

	return jsonify(pageurl = url_for('login'))
#########################################################################################


#########################################################################################
#TODO: Remove this route
#Shows all the current support tickets 
@app.route('/' + SERVER_PATH + 'currentsupportticketsview')
def viewsupporttickets():
	if not sessionKeyValid(USER_SESSION_KEY):
		return redirect('/login')

	print(supportticketslist.query.all())
	
	return str(supportticketslist.query.all())
#########################################################################################


#########################################################################################
#Removes the current session token of the user
@app.route('/' + SERVER_PATH + 'logout', methods=['GET'])
def logout():
	if sessionKeyValid(USER_SESSION_KEY):
		removeSessionKey(USER_SESSION_KEY)
   
	return render_template('logout.html')
#########################################################################################

@app.route('/' + SERVER_PATH + 'createsupporttickets', methods=['GET'])
def createsupporttickets():
	if not sessionKeyValid(USER_SESSION_KEY) \
	   or not supportstaffuser(session[USER_SESSION_KEY]):
		return False

	return render_template('mainview.html', **DEFAULTUSER_RESOURCES)

@app.route('/' + SERVER_PATH + 'searchusersupporttickets', methods=['POST'])
def searchsupporttickets():
	print(request.form['search_details'])

	if not sessionKeyValid(USER_SESSION_KEY):
		return False

	some_support_tickets = somesupportticketvalues \
						   .getValue({'user_id': session[USER_SESSION_KEY]},
									 search_text = html.escape(request.form['search_details']), 
									 search_values = ('supportid', 
													  'supporttype', 
													  'supportdescription', 
													  'supportlocation', 
													  'supportstatusdescription', 
													  'supportstaffname', 
													  'supportstaffemail'))

	return jsonify(some_support_tickets)

@app.route('/'  + SERVER_PATH + 'searchstaffsupporttickets', methods=['POST'])
def searchstaffsupporttickets():
	print(request.form['search_details'])

	if not sessionKeyValid(USER_SESSION_KEY) \
	   or not supportstaffuser(session(USER_SESSION_KEY)):
		return False

	some_support_tickets = somesupportticketvalues \
						   .getValue({'supportstaffassigned': session[USER_SESSION_KEY]},
									 search_text = html.escape(request.form['search_details']), 
									 search_values = ('supportid', 
													  'supporttype', 
													  'supportdescription', 
													  'supportlocation', 
													  'supportstatusdescription', 
													  'supportstaffname', 
													  'supportstaffemail',
													  'ticketsubmissiondatetime',
													  'supportdatetime'))

	return jsonify(some_support_tickets)

@app.route('/'  + SERVER_PATH + 'searchadminsupporttickets', methods = ['POST'])
def searchadminsupporttickets():
	if not sessionKeyValid(USER_SESSION_KEY) \
	   or not supportstaffadmin(session[USER_SESSION_KEY]):
		return False

	print('Search admin support tickets')

	print(request.form['search_details'])

	some_search_text = json.loads(request.form['search_details'])

	print(some_search_text)

	'''
		INEFFICIENT:
			Unformatted matching: checks whether all fields contain the search text as a substring

		SLIGHTLY EFFICIENT:
			Formatted matching: checks whether the specified fields contain the search text as a substring

		MOST EFFICIENT:
			Formatted exact values: checks whether the specified fields contain the search text as an exact value
	'''

	if some_search_text['mode'] == 'unformatted':
		some_support_tickets = somesupportticketvalues \
							   .search(some_search_text['search_text'])

	elif some_search_text['mode'] == 'formatted':
		del some_search_text['mode']

		some_support_tickets = somesupportticketvalues \
							   .formattedSearch(some_search_text)

	elif some_search_text['mode'] == 'exact':
		del some_search_text['mode']

		some_support_tickets = somesupportticketvalues \
									.getValuesFromText(some_search_text)

	else:
		raise ValueError

	return jsonify(some_support_tickets)

@app.route('/'  + SERVER_PATH + 'ABAHelpDeskSupportTickets.csv')
def getsupportticketscsv():
	if not sessionKeyValid(USER_SESSION_KEY) \
	   or not supportstaffadmin(session[USER_SESSION_KEY]):
		return False

	def getCSVvalue(some_support_ticket):
		some_support_ticket_csv = []
		for field_name, field_value in some_support_ticket.items():
			some_support_ticket_csv.append(field_value)

		return ','.join(some_support_ticket_csv) + '\n'

	def generate():
		for some_value in somesupportticketvalues.currentData:
		   yield getCSVvalue(some_value)

	return Response(generate(), mimetype='text/csv')


@app.route('/'  + SERVER_PATH + 'ABAHelpDeskSupportStaff.csv')
def getsupportstaffcsv():
	if not sessionKeyValid(USER_SESSION_KEY) \
	   or not supportstaffadmin(session[USER_SESSION_KEY]):
		return False

	def getCSVvalue(some_support_ticket):
		some_support_ticket_csv = []
		for field_name, field_value in some_support_ticket.items():
			some_support_ticket_csv.append(str(field_value))

		return ','.join(some_support_ticket_csv) + '\n'

	def generate():
		for some_value in somesupportstaffvalues.currentData:
		   yield getCSVvalue(some_value)

	return Response(generate(), mimetype='text/csv')


@app.route('/' + SERVER_PATH + 'ABAHelpDeskSupportComments.csv')
def getsupportcommentscsv():
	if not sessionKeyValid(USER_SESSION_KEY) \
	   or not supportstaffadmin(session[USER_SESSION_KEY]):
		return False

	def getCSVvalue(some_support_ticket):
		some_support_ticket_csv = []
		for field_name, field_value in some_support_ticket.items():
			some_support_ticket_csv.append(field_value)

		return ','.join(some_support_ticket_csv) + '\n'

	def generate():
		for some_value in somesupportticketcommentvalues.currentData:
		   yield getCSVvalue(some_value)

	return Response(generate(), mimetype='text/csv')

@app.route('/' + SERVER_PATH + 'getsupportticketsfromday', methods=['POST'])
def getsupportticketsfromday():
	if not sessionKeyValid(USER_SESSION_KEY) \
	   or not supportstaffadmin(session[USER_SESSION_KEY]):
		return False

	try:
		some_support_tickets = somesupportticketvalues \
							   .getSupportTicketsFromDay(int(request.form['end_date']), 
														 int(request.form['days_from_date']))

		return jsonify(some_support_tickets)

	except Exception as database_error:
		print('Could not get support tickets from date provided')

		print(database_error)

		return jsonify({'supportticketfromdays': False})

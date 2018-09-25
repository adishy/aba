import json

import random

#########################################################################################
#SOCKETIO APP  
#########################################################################################
from mainview import socketio

#########################################################################################
#FLASK SQL ALCHEMY
#########################################################################################
from mainview import db

#########################################################################################
#OAUTH HELPERS
#########################################################################################
from constKeys import *

from dataModels import *

#########################################################################################
#FLASK MODULES
#########################################################################################
from flask import request

from flask import session

from flask import jsonify

#########################################################################################
#FLASK SOCKETIO MODULES
#########################################################################################
from flask_socketio import join_room

from flask_socketio import leave_room

#########################################################################################
#SESSION HELPERS
#########################################################################################
from flaskSession import *

#########################################################################################
#ROUTE HELPERS
#########################################################################################
from helpDeskRouteHelpers import *

#########################################################################################
#EMAIL MODULE
#########################################################################################
from supportTicketEmails import emailer


support_ticket_send_mail = emailer('helpdesksystem@abaoman.org', 
								   'abaHS2018')    

#########################################################################################
#TODO: Remove this route
#Prints a message received from 'my event'
@socketio.on('my event')
def handle_message(message):
	print(message)
#########################################################################################

#########################################################################################
#A new user connected is assigned a new room, if the new user connected is a support 
#staff member, they also join the room for connected support staff members
@socketio.on('connect')
def addusertoken():
	if not sessionKeyValid(USER_SESSION_KEY):
		return False

	currentUsers[session[USER_SESSION_KEY]] = request.sid   
	join_room(session[USER_SESSION_KEY], 
			  sid = currentUsers[session[USER_SESSION_KEY]])
	socketio.emit('connectmessage', 
				  session['email'], 
				  room = session[USER_SESSION_KEY])
	print(currentUsers)

	if supportstaffuser(session[USER_SESSION_KEY]):
		join_room(session[SUPPORT_STAFF_ROOM_TITLE_KEY], 
				  sid = currentUsers[session[USER_SESSION_KEY]])
		socketio.emit('supportstaffconnect', 
					  session['email'], 
					  room = session[SUPPORT_STAFF_ROOM_TITLE_KEY])
#########################################################################################

#########################################################################################
#A user that disconnected is removed from their room, if the user that disconnected was 
#a support staff member, they are removed from the room for connected support staff 
#members
@socketio.on('disconnect')
def removeusertoken():
	if not sessionKeyValid(USER_SESSION_KEY):
		return False

	leave_room(session[USER_SESSION_KEY], 
			   sid = currentUsers[session[USER_SESSION_KEY]])

	if supportstaffuser(session[USER_SESSION_KEY]):
		leave_room(session[SUPPORT_STAFF_ROOM_TITLE_KEY], 
				   sid = currentUsers[session[USER_SESSION_KEY]])

	del currentUsers[session[USER_SESSION_KEY]]
	print(currentUsers)
#########################################################################################

#########################################################################################
#TODO: Add similar routes according to ticket status, limit number of tickets returned in
#      JSON
#Collects all of the assigned tickets of a support staff member from the support ticket 
#list and returns it in JSON
@socketio.on('viewassignedtickets')
def viewallassignedtickets():
	if not sessionKeyValid(USER_SESSION_KEY) or not supportstaffuser(session[USER_SESSION_KEY]):
		return False

	socketio.emit('assignedtickets', 
				  json.dumps(somesupportticketvalues.getValue({'supportstaffassigned': session[USER_SESSION_KEY]}, 
															  not_equal = {'supportstatustype': 'Complete'})), 
				  room = session[USER_SESSION_KEY], 
				  broadcast = False)
#########################################################################################

#########################################################################################
#TODO: Add similar routes according to ticket status, limit number of tickets returned in
#      JSON
#Collects all of the unassigned tickets from the support ticket list and returns it in 
#JSON
@socketio.on('viewunassignedtickets')
def viewallunassignedtickets():
	if not sessionKeyValid(USER_SESSION_KEY) or not supportstaffuser(session[USER_SESSION_KEY]):
		return False

	socketio.emit('unassignedtickets', 
				  json.dumps(somesupportticketvalues.getValue({'supportstaffassigned': UNASSIGNED_SUPPORT_TICKET}, 
															  not_equal = {'supportstatustype': 'Complete'})), 
				  room = session[USER_SESSION_KEY], 
				  broadcast = False)
#########################################################################################

#########################################################################################
#Collects all of the completed tickets from the support ticket list and returns it in 
#JSON
@socketio.on('viewcompletedtickets')
def viewallcompletedtickets():
	if not sessionKeyValid(USER_SESSION_KEY) or not supportstaffuser(session[USER_SESSION_KEY]):
		return False

	socketio.emit('completedtickets', 
				  json.dumps(somesupportticketvalues.getValue({'supportstaffassigned': session[USER_SESSION_KEY], 
															   'supportstatustype': 'Complete'})), 
				  room = session[USER_SESSION_KEY], 
				  broadcast = False)
#########################################################################################

#########################################################################################
#Creates a new support ticket in the support ticket list for the current user from 
#ticket details provided in JSON then assigns the ticket to a staff member or adds 
#it to the common ticket list and pushes a ticket event to the room of the assigned 
#support staff member or to the room of all staff members connected
@socketio.on('addsupportticket')
def addsupportticketprovided(someticketprovided):
	if not sessionKeyValid(USER_SESSION_KEY):
		return False

	print('Adding ticket provided')

	print(someticketprovided)

	if someticketprovided['csrfidvalue'] != session[CSRF_ID_TEXT_KEY]:
		return False

	try:
		print('A')
		supportticketslistdetails = getsupportticket(someticketprovided)
		
		print('B')
		print(supportticketslistdetails)

		
		print('C')
		somesupportticketvalues.append(supportticketslistdetails)

		
		print('D')
		print('Added ticket provided')

		socketio.emit('addedsupportticket', 
					  'Added user ticket', 
					  room = session[USER_SESSION_KEY])

		somesupportticketnotificationvalues.addnotification(title = 'New support ticket', 
															notificationbody = str.format('Support ticket {} added', 
																						supportticketslistdetails['supportid']),
															userid = session[USER_SESSION_KEY])

		socketio.emit('notificationchanged', room = session[USER_SESSION_KEY])

		if supportticketslistdetails['supportstaffassigned'] == UNASSIGNED_SUPPORT_TICKET:
			socketio.emit('newunassignedticket', 
						  room = SUPPORT_STAFF_ROOM_ID)

			somesupportticketnotificationvalues.addnotification(title = 'New support ticket', 
																notificationbody = str.format('Support ticket {} added to common queue', 
																							  supportticketslistdetails['supportid']),
																userid = UNASSIGNED_SUPPORT_TICKET)

			socketio.emit('notificationchanged', room = session[USER_SESSION_KEY])
		else:
			socketio.emit('newassignedticket', 
						  room = supportticketslistdetails['supportstaffassigned'])

			if supportticketslistdetails['supportstaffassigned'] == UNASSIGNED_SUPPORT_TICKET:
				addSupportStaffNotification(title = 'New support ticket', 
											notificationbody = str.format('Support ticket {} assigned', 
																		  supportticketslistdetails['supportid']))

				support_ticket_send_mail.sendemails(to_email_addresses = [supportticketslistdetails['user_email']], 
													subject = 'ABA Help Desk - Added new support ticket', 
													content=str.format('You added a support ticket (ID: {}) for support with {}. Your issue will be attended shortly by a member of the support staff. \n\n\n\n\n\n This is an automated message, please do not respond to this email.', 
																	   supportticketslistdetails['supportid'],
																	   supportticketslistdetails['supporttype']))

			
				support_ticket_send_mail.sendemails(to_email_addresses = somesupportstaffvalues.getEmails(), 
													subject = 'ABA Help Desk - You have been assigned a new support ticket', 
													content=str.format('You have been assigned a support ticket (ID: {}) for support with {}. \n\n\n\n\n\n This is an automated message, please do not respond to this email.', 
																		supportticketslistdetails['supportid'],
																		supportticketslistdetails['supporttype']))
			else:
				somesupportticketnotificationvalues.addnotification(title = 'New support ticket', 
																	notificationbody = str.format('Support ticket {} assigned', 
																								supportticketslistdetails['supportid']),
																	userid = supportticketslistdetails['supportstaffassigned'])

			
				support_ticket_send_mail.sendemails(to_email_addresses = [supportticketslistdetails['user_email']], 
													subject = 'ABA Help Desk - Added new support ticket', 
													content=str.format('You added a support ticket (ID: {}) for support with {}. Your issue will be attended shortly by a member of the support staff. \n\n\n\n\n\n This is an automated message, please do not respond to this email.', 
																	   supportticketslistdetails['supportid'],
																	   supportticketslistdetails['supporttype']))

				support_ticket_send_mail.sendemails(to_email_addresses = supportticketslistdetails['supportstaffemail'], 
													subject = 'ABA Help Desk - You have been assigned a new support ticket', 
													content=str.format('You have been assigned a support ticket (ID: {}) for support with {}. \n\n\n\n\n\n This is an automated message, please do not respond to this email.', 
																		supportticketslistdetails['supportid'],
																		supportticketslistdetails['supporttype']))

	except Exception as databaseerror:
		print('Could not add record')
		
		print(databaseerror)

		return jsonify(databasestatus = '', 
					   databaseerror = 'Could not add record')

	print(jsonify(databasestatus = 'Added ticket', 
				  databaseerror = ''))

	return jsonify(databasestatus = 'Added ticket', 
				   databaseerror = '')
#########################################################################################

#########################################################################################
#TODO: Add similar routes according to ticket status, limit number of tickets returned in
#      JSON
#Collects all of the current user's support tickets and returns it in JSON
@socketio.on('viewcurrenttickets')
def viewallcurrenttickets():
	if not sessionKeyValid(USER_SESSION_KEY):
		return False

	try:
		socketio.emit('currenttickets', 
					  somesupportticketvalues.getValue({'user_id': session[USER_SESSION_KEY]}), 
					  room = session[USER_SESSION_KEY], 
					  broadcast = False)
	except:
		print('Could not get current tickets for user')

#########################################################################################

#########################################################################################
#Modifies the support staff assigned, support staff name and support staff of a
#specified ticket from unassigned to the current user
@socketio.on('claimsupportticket')
def claimcurrentsupportticket(someticketprovided):
	if not sessionKeyValid(USER_SESSION_KEY) or not supportstaffuser(session[USER_SESSION_KEY]):
		return False

	try:    
		some_support_ticket = somesupportticketvalues[{'supportid': someticketprovided['supportid']}]

		some_user_provided = some_support_ticket['user_id']

		somesupportticketvalues.update({'supportid': someticketprovided['supportid'], 
										'supportstaffassigned': UNASSIGNED_SUPPORT_TICKET},

									   {'supportstaffassigned': session[USER_SESSION_KEY],
										'supportstaffname': session['name'],
										'supportstaffemail': session['email'],
										'supportstaffimage': session['image'],
										'supportstatusdescription': 'Your ticket has been claimed by ' + session['name'],
										'lastupdated': datetime.datetime.now()})

		addSupportStaffNotification(title = 'Support ticket claimed', 
									notificationbody = str.format('Support ticket {} claimed by {}', 
																  some_support_ticket['supportid'],
																  session['name']))

		somesupportticketnotificationvalues.addnotification(title = 'Support ticket claimed', 
															notificationbody = str.format('Your support ticket (ID: {})  is being worked on by {}', 
																							some_support_ticket['supportid'],
																							session['name']),
															userid = some_user_provided)

		socketio.emit('notificationchanged', 
					room = session[USER_SESSION_KEY])


		socketio.emit('claimedsupportticket', 
					  room = SUPPORT_STAFF_ROOM_ID)


		if activesocketioroom(some_user_provided):
			socketio.emit('claimedsupportticket', 
						  str.format('{{"supportstaffassigned": "{}"}}', 
									 session['name']),
						  room = some_user_provided)

			socketio.emit('notificationchanged', 
						   room = some_user_provided)

	except Exception as database_error:
		print('Could not claim ticket provided for the current user')
		print(database_error)
#########################################################################################

#########################################################################################
#Changes the staff assigned to unassigned
@socketio.on('unclaimsupportticket')
def unclaimcurrentsupportticket(someticketprovided):
	if not sessionKeyValid(USER_SESSION_KEY) \
	   or not supportstaffuser(session[USER_SESSION_KEY]):
		return False

	try:

		some_support_ticket = somesupportticketvalues[{'supportid': someticketprovided['supportid'], 
													   'supportstaffassigned': session[USER_SESSION_KEY]}]

		some_user_provided = some_support_ticket['user_id']

		somesupportticketvalues.update({'supportid': someticketprovided['supportid'], 
										'supportstaffassigned': session[USER_SESSION_KEY]},
								 
										{'supportstaffassigned': UNASSIGNED_SUPPORT_TICKET, 
										 'supportstaffname': UNASSIGNED_SUPPORT_TICKET, 
										 'supportstaffemail': UNASSIGNED_SUPPORT_TICKET, 
										 'supportstaffimage': UNASSIGNED_SUPPORT_TICKET, 
										 'supportstatustype': 'Ongoing', 
										 'supportstatusdescription': 'Processing',
										 'lastupdated': datetime.datetime.now()})

		socketio.emit('unclaimedsupportticket', 
					  room = SUPPORT_STAFF_ROOM_ID)

		if activesocketioroom(some_user_provided):
			socketio.emit('unclaimedsupportticket',
						  room = some_user_provided)

	except:
		print('Could not unclaim ticket provided for the current user')
#########################################################################################

@socketio.on('adminuserassignsupportticket')
def assignsupportticket(some_support_ticket_provided):
	if not sessionKeyValid(USER_SESSION_KEY) \
	   or not supportstaffadmin(session[USER_SESSION_KEY]):
		return False

	try:
		print(some_support_ticket_provided)

		some_support_ticket = somesupportticketvalues \
							  .getValue({'supportid': some_support_ticket_provided['supportid']})[0]

		current_support_staff = some_support_ticket['supportstaffassigned']

		if current_support_staff != UNASSIGNED_SUPPORT_TICKET:
			somesupportticketnotificationvalues \
			.addnotification(title = 'Support ticket reassigned', 
							 notificationbody = str.format('Your support ticket (ID: {})  has been reassigned by the IT Administrator', 
															some_support_ticket['supportid']),
							 userid = current_support_staff)
		else:
			somesupportticketnotificationvalues \
			.addnotification(title = 'Support ticket reassigned', 
							 notificationbody = str.format('Support ticket (ID: {})  has been reassigned by the IT Administrator', 
															some_support_ticket['supportid']),
							 userid = UNASSIGNED_SUPPORT_TICKET)

			socketio.emit('reassignedsupportticket', room = SUPPORT_STAFF_ROOM_ID)

			socketio.emit('notificationchanged', room = SUPPORT_STAFF_ROOM_ID)

		changed_support_staff = somesupportstaffvalues \
								.getValue({'email': some_support_ticket_provided['supportstaffemail']})[0]

		somesupportticketvalues.update({'supportid': some_support_ticket_provided['supportid']}, 
									   {'supportstaffassigned': changed_support_staff['id'],
										'supportstaffname': changed_support_staff['name'],
										'supportstaffemail': changed_support_staff['email'],
										'supportstaffimage': changed_support_staff['image']})

		socketio.emit('assignedsupportstaff', room = session[USER_SESSION_KEY])

		somesupportticketnotificationvalues \
		.addnotification(title = 'Support ticket assigned', 
						 notificationbody = str.format('The support ticket (ID: {})  has been assigned to {}', 
														some_support_ticket['supportid'],
														changed_support_staff['name']),
						 userid = session[USER_SESSION_KEY])

		socketio.emit('notificationchanged', room = session[USER_SESSION_KEY])

		somesupportticketnotificationvalues \
		.addnotification(title = 'Support ticket assigned', 
						 notificationbody = str.format('The support ticket (ID: {})  has been assigned to you', 
														some_support_ticket['supportid']),
						 userid = changed_support_staff['id'])

		if activesocketioroom(current_support_staff):
			socketio.emit('reassignedsupportticket', room = current_support_staff)
			socketio.emit('notificationchanged', room = current_support_staff )

		if activesocketioroom(changed_support_staff['id']):
			socketio.emit('newassignedsupportticket', room = current_support_staff)
			socketio.emit('notificationchanged', room = current_support_staff)

	except Exception as database_error:
		print('Could not assign support ticket to staff')
		print(database_error)

#########################################################################################
#Removes the support ticket for the user and the staff assigned
@socketio.on('cancelsupportticket')
def cancelcurrentsupportticket(someticketprovided):
	if not sessionKeyValid(USER_SESSION_KEY):
		return False

	try:
		some_support_staff_assigned = somesupportticketvalues[{'supportid': someticketprovided['supportid']}]['supportstaffassigned']

		somesupportticketvalues.remove(supportid = someticketprovided['supportid'], 
									   user_id = session[USER_SESSION_KEY])

		socketio.emit('cancelledsupportticket', 
					  room = session[USER_SESSION_KEY])

		supportstaffassignedroom = ''

		somesupportticketnotificationvalues.addnotification(title = 'Cancelled support ticket', 
															notificationbody = str.format('Support ticket {} cancelled', 
																						  someticketprovided['supportid']),
															userid = session[USER_SESSION_KEY])

		socketio.emit('notificationchanged', 
					room = session[USER_SESSION_KEY])

		if some_support_staff_assigned == UNASSIGNED_SUPPORT_TICKET:
			supportstaffassignedroom = SUPPORT_STAFF_ROOM_ID

			addSupportStaffNotification(title = 'Cancelled support ticket', 
										notificationbody = str.format('{} cancelled support ticket {}',
																	  session['name'],
																	  someticketprovided['supportid']))

			socketio.emit('notificationchanged', 
						  room = SUPPORT_STAFF_ROOM_ID)

		else:
			supportstaffassignedroom = some_support_staff_assigned

			somesupportticketnotificationvalues.addnotification(title = 'Cancelled support ticket', 
														notificationbody = str.format('{} cancelled support ticket {}',
																							  session['name'],
																							  someticketprovided['supportid']),
														userid = some_support_staff_assigned)

			socketio.emit('notificationchanged', 
						  room = some_support_staff_assigned)

		socketio.emit('cancelledsupportticket',
					  room = supportstaffassignedroom)

		support_ticket_send_mail.sendemails(to_email_addresses = [session['email']], 
											subject = 'ABA Help Desk', 
											content= 'Cancelled support ticket')
	except Exception as some_error:
		print('Could not cancel ticket')

		print(some_error)
#########################################################################################


@socketio.on('changesupportticketstatus')
def changesupportticketstatus(someticketprovided):
	if not sessionKeyValid(USER_SESSION_KEY) or not supportstaffuser(session[USER_SESSION_KEY]):
		return False
	try:
		print('Changing support ticket status')

		somesupportticketvalues.update({'supportid': someticketprovided['supportid'], 
										'supportstaffassigned': session[USER_SESSION_KEY]}, 
									   {'supportstatustype': someticketprovided['supportstatustype'],
										'lastupdated': datetime.datetime.now()})

		support_ticket = somesupportticketvalues[{'supportid': someticketprovided['supportid']}]

		socketio.emit('changedsupportticketstatus', 
					  room = session[USER_SESSION_KEY])

		somesupportticketnotificationvalues.addnotification(title = 'Changed support ticket status', 
															notificationbody = str.format('Your support ticket (ID: {}) has been marked \'{}\' ', 
																						support_ticket['supportid'],
																						support_ticket['supportstatustype']),
															userid = support_ticket['user_id'])

		if activesocketioroom(support_ticket['user_id']):
			socketio.emit('changedsupportticketstatus', 
						  room = support_ticket['user_id'])  
			
			socketio.emit('notificationchanged', 
						room = support_ticket['user_id'])

		support_ticket_send_mail.sendemails(to_email_addresses = [support_ticket['user_email']], 
											subject = 'ABA Help Desk', 
											content= 'Changed support ticket status')

	except Exception as database_error:
		print('Could not change support ticket status')
		print(database_error)

@socketio.on('changesupportstatusdescription')
def changesupportticketstatusdescription(someticketprovided):
	print('Change support status')

	if not sessionKeyValid(USER_SESSION_KEY) or not supportstaffuser(session[USER_SESSION_KEY]):
		return False

	try:
		somesupportticketvalues.update({'supportid': someticketprovided['supportid'], 
										'supportstaffassigned': session[USER_SESSION_KEY]}, 
									   {'supportstatusdescription': someticketprovided['supportstatusdescription'],
										'lastupdated': datetime.datetime.now()})

		support_ticket = somesupportticketvalues[{'supportid': someticketprovided['supportid']}]

		somesupportticketnotificationvalues.addnotification(title = 'Changed support ticket status', 
														notificationbody = str.format('The status of your support ticket (ID: {}) has been changed to  \'{}\' ', 
																					support_ticket['supportid'],
																					support_ticket['supportstatusdescription']),
														userid = support_ticket['user_id'])

		if activesocketioroom(support_ticket['user_id']):
			socketio.emit('changedsupportticketstatusdescription', 
						  room = support_ticket['user_id'])  

			socketio.emit('notificationchanged', room = support_ticket['user_id'])

		socketio.emit('changedsupportticketstatusdescription', 
					  room = SUPPORT_STAFF_ROOM_ID)

		support_ticket_send_mail.sendemails(to_email_addresses = [support_ticket['user_email']], 
										subject = 'ABA Help Desk', 
										content= 'Changed support ticket status')

	except Exception as database_error:
		print('Could not change support ticket status description')
		print(database_error)

@socketio.on('supportdescription')
def supportdescriptions(some_description_details_provided):
	#print(some_location_details_provided)
	#print(some_location_details_provided['supporttype'])
	#print(somesupportdescriptionvalues[{'supporttype': some_location_details_provided['supporttype']}])
	if not sessionKeyValid(USER_SESSION_KEY):
		return False

	print('support descriptions')

	socketio.emit('supportdescriptiontext',
				  somesupportdescriptionvalues[{'supporttype': some_description_details_provided['supporttype']}]['supportdescriptions'],
				  room = session[USER_SESSION_KEY])

@socketio.on('supportlocation')
def supportlocations(some_location_details_provided):
	if not sessionKeyValid(USER_SESSION_KEY):
		return False

	some_location_provided = some_location_details_provided['supportlocationprovided']
	
	supportlocationsfromtext  = []

	if some_location_provided == '':
		pass

	else:
		some_location_counter = 0

		for some_location_value in somesupportlocationvalues:
			some_location = some_location_value['supportlocationdetails']

			if some_location.upper().startswith(some_location_provided.upper()):
				supportlocationsfromtext.append(some_location)
				some_location_counter += 1

			if some_location_counter > 10:
				break

	socketio.emit('supportlocationtext', 
				  {'supportlocations': supportlocationsfromtext}, 
				  room = session[USER_SESSION_KEY])

@socketio.on('viewsupportlocationstext')
def viewsupportlocations():
	socketio.emit('supportlocationstext', 
				  somesupportlocationvalues.currentData, 
				  room = session[USER_SESSION_KEY])

@socketio.on('supportlocationadd')
def supportlocationadd(some_location_provided):
	if not sessionKeyValid(USER_SESSION_KEY) or not supportstaffuser(session[USER_SESSION_KEY]):
		return False

	if len(some_location_provided['supportlocation']):
		somesupportlocationvalues.append(some_location_provided['supportlocation'])

		socketio.emit('addedsupportlocation',  
					  room = session[USER_SESSION_KEY])  

@socketio.on('supportlocationremove')
def supportlocationremove(some_location_provided):
	if not sessionKeyValid(USER_SESSION_KEY) or not supportstaffuser(session[USER_SESSION_KEY]):
		return False

	somesupportlocationvalues.remove(supportlocationdetails = some_location_provided['supportlocation'])

	socketio.emit('removedsupportlocation',  
				  room = session[USER_SESSION_KEY])

@socketio.on('csrfidtext')
def csrfidvalue():
	print('csrf request')

	if not sessionKeyValid(USER_SESSION_KEY):
		return False

	csrf_id_value_provided = getCSRFtext()

	setSessionKey((CSRF_ID_TEXT_KEY, csrf_id_value_provided))

	socketio.emit('csrfid', 
				  {'csrfid': csrf_id_value_provided},  
				  room = session[USER_SESSION_KEY])

@socketio.on('supporttypeoptiontext')
def supporttypeoptions():
	if not sessionKeyValid(USER_SESSION_KEY):
		return False

	print('supporttypeoption')
	socketio.emit('supporttypeoptions', 
				  somesupportdescriptionvalues.getSupportTypes(), 
				  room = session[USER_SESSION_KEY])

@socketio.on('viewsupportstaffmembers')
def viewsupportstaffmembers():
	print('supportstaffmembers')

	if not sessionKeyValid(USER_SESSION_KEY):
		return False

	socketio.emit('supportstaffmembers', 
				  json.dumps(somesupportstaffvalues.getSupportStaffUserData(), default = str), 
				  room = session[USER_SESSION_KEY])

@socketio.on('viewsupportticketcomments')
def viewsupportticketcomments(some_support_ticket_details):
	if not sessionKeyValid(USER_SESSION_KEY):
		return False

	print('Support ticket comments')

	some_support_ticket_comments = {'supportid': some_support_ticket_details['supportid']}

	print(some_support_ticket_comments)

	some_support_ticket = somesupportticketvalues.getValue(some_support_ticket_comments)[0]

	print(some_support_ticket)

	#if supportstaffuser(session[USER_SESSION_KEY]) \
	#   and some_support_ticket['supportstaffassigned'] != session[USER_SESSION_KEY]:
	#	print('Invalid user')
	#	return False

	if not supportstaffuser(session[USER_SESSION_KEY]) \
		 and some_support_ticket['user_id'] != session[USER_SESSION_KEY]:
		return False

	print('Support ticket comments from support ticket')

	socketio.emit('supportticketcomments', 
				  somesupportticketcommentvalues \
				  .getValue(some_support_ticket_comments), 
				  room = session[USER_SESSION_KEY])

@socketio.on('addsupportticketcomments')
def addsupportticketcomment(some_support_ticket_details):
	if not sessionKeyValid(USER_SESSION_KEY):
		return False

	try:
		some_support_ticket = somesupportticketvalues \
							  .getValue({'supportid': some_support_ticket_details['supportid']})[0]

		if supportstaffuser(session[USER_SESSION_KEY]) \
		   and some_support_ticket['supportstaffassigned'] != session[USER_SESSION_KEY]:
			return False

		elif not supportstaffuser(session[USER_SESSION_KEY]) \
			 and some_support_ticket['user_id'] != session[USER_SESSION_KEY]:
			return False

		some_support_ticket_comment = {'commentid': getRandomKey(),
									   'supportid': some_support_ticket['supportid'], 
									   'commenttext': html.escape(some_support_ticket_details['commenttext']), 
									   'commentdatetime': datetime.datetime.now()}

		support_ticket_comment_author = USER_COMMENT

		some_support_staff_id = ''

		if some_support_ticket['supportstaffassigned'] == UNASSIGNED_SUPPORT_TICKET:
			some_support_staff_id = SUPPORT_STAFF_ROOM_ID

		else:
			some_support_staff_id = some_support_ticket['supportstaffassigned']

		if supportstaffuser(session[USER_SESSION_KEY]):
			some_support_ticket_comment['commentauthor'] = SUPPORT_STAFF_COMMENT
			
			support_ticket_comment_author = SUPPORT_STAFF_COMMENT

		else:
			some_support_ticket_comment['commentauthor'] = USER_COMMENT

		somesupportticketcommentvalues.append(some_support_ticket_comment)

		socketio.emit('addedsupportticketcomment', 
					  room = session[USER_SESSION_KEY], 
					  broadcast = False)

		if support_ticket_comment_author == USER_COMMENT:

			if some_support_ticket['supportstaffassigned'] == UNASSIGNED_SUPPORT_TICKET:
				addSupportStaffNotification(title = 'Comment added', 
											notificationbody = str.format('New comment by {} on support ticket (ID: {})',
																		  session['name'],
																		  some_support_ticket['supportid']))

			else:
				somesupportticketnotificationvalues.addnotification(title = 'Comment added', 
																	notificationbody = str.format('New comment by {} on support ticket (ID: {})',
																								  session['name'],
																								  some_support_ticket['supportid']),
																	userid = some_support_ticket['supportstaffassigned'])

			if activesocketioroom(some_support_ticket['supportstaffassigned']):
				socketio.emit('addedsupportticketcomment', 
							  room = some_support_ticket['supportstaffassigned'], 
							  broadcast = False)

				socketio.emit('notificationchanged', 
							  room = some_support_staff_id)

		else:
			print('Support staff support ticket comment')

			somesupportticketnotificationvalues.addnotification(title = 'Comment added', 
										notificationbody = str.format('New comment by {} on support ticket (ID: {})',
																	  session['name'],
																	  some_support_ticket['supportid']),
										userid = some_support_ticket['user_id'])

			if activesocketioroom(some_support_ticket['user_id']):
				socketio.emit('addedsupportticketcomment'   , 
							  room = some_support_ticket['user_id'], 
							  broadcast = False)

				socketio.emit('notificationchanged', 
							  room = some_support_ticket['user_id'])

	except Exception as support_ticket_error:
		print('Could not add support ticket comment')

		print(support_ticket_error)

@socketio.on('viewnotificationtext')
def notificationtext():
	print('Notification text')
	
	if not sessionKeyValid(USER_SESSION_KEY):
		return False

	some_support_ticket_notifications = somesupportticketnotificationvalues \
										.getValue({'userid': session[USER_SESSION_KEY]})

	if supportstaffuser(session[USER_SESSION_KEY]):
		some_support_ticket_notifications += somesupportticketnotificationvalues \
											.getValue({'userid': UNASSIGNED_SUPPORT_TICKET})


	socketio.emit('notificationtext', 
					json.dumps(some_support_ticket_notifications, 
								default = str), 
					room = session[USER_SESSION_KEY])

@socketio.on('clearnotifications')
def clearnotifications():
	if not sessionKeyValid(USER_SESSION_KEY):
		return False

	print('Clear notifications')
	somesupportticketnotificationvalues.remove(userid = session[USER_SESSION_KEY])
	socketio.emit('notificationchanged', 
				  room = session[USER_SESSION_KEY])

@socketio.on('addseennotifications')
def addseennotificationsprovided(some_notification_list):
	print('Add seen notifications')
	
	if not sessionKeyValid(USER_SESSION_KEY):
		return False

	print(some_notification_list)

	for some_notification in some_notification_list:
		somesupportticketnotificationvalues.update({'notificationid': some_notification, 
													'userid': session[USER_SESSION_KEY]},
													{'notificationseen': 1})

	socketio.emit('addedseennotifications', 
				  room = session[USER_SESSION_KEY])

@socketio.on('viewsupporttypestext')
def viewsupporttypestext():
	if not sessionKeyValid(USER_SESSION_KEY) or not supportstaffadmin(session[USER_SESSION_KEY]):
		return False

	socketio.emit('supporttypestext', 
				somesupportdescriptionvalues.currentData, 
				room = session[USER_SESSION_KEY])

@socketio.on('supporttypesadd')
def supporttypesadd(some_support_type):
	if not sessionKeyValid(USER_SESSION_KEY) or not supportstaffadmin(session[USER_SESSION_KEY]):
		return False

	print(some_support_type)

	if some_support_type['supporttype'] in somesupportdescriptionvalues:
		somesupportdescriptionvalues.remove(supporttype = some_support_type['supporttype'])

	somesupportdescriptionvalues.append({'supporttype': some_support_type['supporttype'], 
										 'supportdescriptions': json.dumps(some_support_type['supportdescriptions'])})

	socketio.emit('addedsupporttype', 
				  room = session[USER_SESSION_KEY])

@socketio.on('supporttypesremove')
def supporttypesremove(some_support_type):
	if not sessionKeyValid(USER_SESSION_KEY) or not supportstaffadmin(session[USER_SESSION_KEY]):
		return False

	somesupportdescriptionvalues.remove(supporttype = some_support_type['supporttype'])

	socketio.emit('removedsupporttype', 
				  room = session[USER_SESSION_KEY])

@socketio.on('supportstaffadd')
def supportstaffadd(some_support_staff_provided):
	if not sessionKeyValid(USER_SESSION_KEY) or not supportstaffadmin(session[USER_SESSION_KEY]):
		return False

	some_support_staff_provided['firstlogin'] = 0

	#if some_support_staff_provided['email'] == session['email']:
		

	#	socketio.emit('addedsupportstaff', 
	#				  room = session[USER_SESSION_KEY])

 #       return True

	if somesupportstaffvalues.hasEmail(some_support_staff_provided['email']):
		some_support_staff_provided['firstlogin'] = somesupportstaffvalues \
													.getValue({'email': some_support_staff_provided['email']})[0]['firstlogin']

		#somesupportstaffvalues.remove(email = some_support_staff_provided['email'])
		somesupportstaffvalues.update({'email': session['email']}, 
									  some_support_staff_provided)

		socketio.emit('addedsupportstaff', 
						room = session[USER_SESSION_KEY])

		return True

	somesupportstaffvalues.append(some_support_staff_provided)

	socketio.emit('addedsupportstaff', 
				  room = session[USER_SESSION_KEY])

@socketio.on('supportstaffremove')
def supportstaffremove(some_support_staff_provided):
	if not sessionKeyValid(USER_SESSION_KEY) or not supportstaffadmin(session[USER_SESSION_KEY]):
		return False

	somesupportstaffvalues.remove(**some_support_staff_provided)

	socketio.emit('removedsupportstaff', 
				room = session[USER_SESSION_KEY])

@socketio.on('viewsupportstafftext')
def supportstafftext():
	if not sessionKeyValid(USER_SESSION_KEY) or not supportstaffadmin(session[USER_SESSION_KEY]):
		return False

	socketio.emit('supportstafftext',
				  json.dumps(somesupportstaffvalues.getSupportStaffUserData(True), 
							 default = str),
				  room = session[USER_SESSION_KEY])

@socketio.on('adminuserstatstext')
def adminuserstatstext():
	admin_user_stats = {}

	admin_user_stats['supporttickets'] = len(somesupportticketvalues)
	admin_user_stats['uniqueusers'] = somesupportticketvalues \
									  .getUniqueFieldLength('user_id')
	admin_user_stats['ongoingsupporttickets'] = somesupportticketvalues \
												 .getFieldItemLength('supportstatustype', 
																	 'Ongoing')
	admin_user_stats['delayedsupporttickets'] = somesupportticketvalues \
												.getFieldItemLength('supportstatustype', 
																	'Delayed')
	admin_user_stats['completesupporttickets'] = somesupportticketvalues \
												 .getFieldItemLength('supportstatustype', 
																	 'Complete')

	admin_user_stats['weeksupporttickets'] = somesupportticketvalues \
											 .getWeekSupportTickets();
	socketio.emit('adminuserstats', 
				  admin_user_stats, 
				  room = session[USER_SESSION_KEY])


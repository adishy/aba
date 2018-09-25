import string

import random

import datetime

import pprint

import html 

from constKeys import *

from flask import session

from mainview import db

from mainview import socketio

from dataLists import *

def validatesupportticketprovided(some_support_ticket_details_provided):
	
	support_date_time_provided_valid = some_support_ticket_details_provided['supportdatetime'] > datetime.datetime.now()
	
	support_type_provided_valid = some_support_ticket_details_provided['supporttype'] in somesupportstaffvalues.supporttypes()

def supportstaffuser(some_user_id_provided):
	return some_user_id_provided in somesupportstaffvalues

def supportstaffuseremail(some_user_email_provided):
	return somesupportstaffvalues.hasEmail(some_user_email_provided)

def supportstaffadmin(some_user_id_provided):
	return somesupportstaffvalues.getValue({'id': some_user_id_provided})[0]['adminuser'] == '1'
	

def getsupportstaffforticket(some_support_type_provided):
   return somesupportstaffvalues.getSupportStaffFromSupportType(some_support_type_provided)


def getsupportdatetime(some_supportdatetime, some_ticketsubmissiondatetime):
	try:
			if some_supportdatetime == '':
				return some_ticketsubmissiondatetime

			some_datetime = datetime.datetime \
									.strptime(some_supportdatetime, 
											  '%Y-%m-%d %H:%M')

			print(some_supportdatetime)

			if some_datetime > some_ticketsubmissiondatetime:
				return some_datetime

			raise ValueError

	except Exception as supportdatetime_error:
		print('Invalid support date and time')

		print(supportdatetime_error)

def getsupportticket(someticketprovided):
		print('A')
		print('Creating support ticket provided')

		print('B')
		now_datetime = datetime.datetime.now()

		print('C')
		supportticketdetailsprovided = {'supportid': getRandomKey(),
										'user_id': session[USER_SESSION_KEY],
										'user_email': session['email'],
										'user_name': session['name'],
										'user_image': session['image'],
										'supporttype': html.escape(someticketprovided['supporttype']),
										'supportdescription': html.escape(someticketprovided['supportdescription']),
										'supportlocation': html.escape(someticketprovided['supportlocation']),
										'ticketsubmissiondatetime': now_datetime,
										'supportstatustype': 'Ongoing',
										'supportstatusdescription': 'Processing ticket',
										'supportdatetime': getsupportdatetime(someticketprovided['supportdatetime'], 
																			  now_datetime),
										'supportstaffassigned': None,
										'supportstaffname': None,
										'supportstaffemail': None,
										'supportstaffimage': None,
										'supportticketchanges': '[]',
										'lastupdated': now_datetime}

		print('D')

		supportstaffemail = somesupportticketoverridevalues.getOverride(supportticketdetailsprovided)

		if not supportstaffemail:
			supportstaffforticket = getsupportstaffforticket(html.escape(supportticketdetailsprovided['supporttype']))

		else:
			supportstaffforticket = somesupportstaffvalues.getValue({'email': supportstaffemail})

		print('E')
		print('Getting assigned staff for support type')

		supportticketdetailsprovided['supportstaffassigned'] = supportstaffforticket['id']

		supportticketdetailsprovided['supportstaffname'] = supportstaffforticket['name']

		supportticketdetailsprovided['supportstaffemail'] = supportstaffforticket['email']

		supportticketdetailsprovided['supportstaffimage'] = supportstaffforticket['image']

		print(supportticketdetailsprovided)

		print(session['name'])

		print(session['email'])

		return supportticketdetailsprovided

currentUsers = {}

def addSupportStaffNotification(**kwargs):
	try:
		for some_support_staff in somesupportstaffvalues.currentData:
			if some_support_staff['id'] == UNASSIGNED_SUPPORT_TICKET:
				continue

		somesupportticketnotificationvalues \
		.addnotification(title = kwargs['title'], 
						 notificationbody = kwargs['notificationbody'],
						 userid = some_support_staff['id'])

	except Exception as some_error:
		print('Could not add group notification')

		print(some_error)

def activesocketioroom(some_room_id_provided):
	return some_room_id_provided in currentUsers

def getCSRFtext():
	return getRandomKey(19)

somesupportstaffvalues = supportStaffData()

somesupportlocationvalues = supportLocationData()

somesupportdescriptionvalues = supportDescriptionData()

somesupportticketvalues = supportTicketData()

somesupportticketoverridevalues = supportTicketOverridesData()

somesupportticketcommentvalues = supportTicketCommentData()

somesupportticketnotificationvalues = supportTicketNotificationData()

somesupportticketnotificationvalues.remove(userid = UNASSIGNED_SUPPORT_TICKET)
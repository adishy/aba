#########################################################################################
#FLASK MODULES
#########################################################################################
from flask import request

from flaskSession import *

#########################################################################################
#Google API Client Library
#########################################################################################
from google.oauth2 import id_token

from google.auth.transport import requests

#########################################################################################
#SUPPORT STAFF USER DETAILS
#########################################################################################
from helpDeskRouteHelpers import somesupportstaffvalues, somesupportticketvalues

from helpDeskRouteHelpers import supportstaffuser, supportstaffuseremail
#########################################################################################
#CONSTANT KEYS
#########################################################################################
from constKeys import *

#########################################################################################
#Authenticates User ID token provided

def confirmOAuthSignIn(some_id_token_provided):
	try:
		# Specify the CLIENT_ID of the app that accesses the backend:
		idinfo = id_token.verify_oauth2_token(some_id_token_provided, 
											  requests.Request(), 
											  GOOGLE_APP_CLIENT)

		if idinfo['iss'] not in ['accounts.google.com', 
								 'https://accounts.google.com']:
			raise ValueError('Wrong issuer.')

			# If auth request is from a G Suite domain:
			if CLIENT_TOKEN_DOMAIN_CHECK and idinfo['hd'] != GOOGLE_DOMAIN:
				 raise ValueError('Wrong hosted domain.')

			# ID token is valid. Get the user's Google Account ID from the decoded token.
		userid = idinfo['sub']

		print(userid)
		print(idinfo['email'])
		print(idinfo['name'])
		print(idinfo['picture'])
		print(idinfo['given_name'])
		print(idinfo['locale'])

		return {'login': True, 
				'userid': idinfo['sub'], 
				'email': idinfo['email'], 
				'name': idinfo['name'],
				'image': idinfo['picture']}

	except ValueError:
		# Invalid token
		return {'login': False}
#########################################################################################
def checkUserDetails(some_user):
	print('Check user details')

	print(some_user['email'])

	print(some_user['userid'])

	if supportstaffuseremail(some_user['email']):
		print('Support staff email')
		support_staff_user = somesupportstaffvalues.getValue({'email': some_user['email']})[0]

		print(support_staff_user)

		if support_staff_user['firstlogin'] == '0':    
			somesupportstaffvalues.update({'email': some_user['email']}, 
										   {'id': some_user['userid'],
											'image': some_user['image']})

			print('Updated support staff sign in')

		some_support_ticket = somesupportticketvalues.getValue({'supportstaffassigned': some_user['userid']})

		if not len(some_support_ticket):
			return

		some_support_ticket = some_support_ticket[0]

		some_update_values = {}

		if some_support_ticket['supportstaffimage'] != some_user['image']:
			some_update_values['supportstaffimage'] = some_user['image']

		somesupportticketvalues.update({'supportstaffassigned': some_user['userid']}, some_update_values)

		
	else:
		
		some_support_ticket = somesupportticketvalues.getValue({'user_id': some_user['userid']})

		if not len(some_support_ticket):
			return

		some_support_ticket = some_support_ticket[0]

		some_update_values = {}

		if some_support_ticket['user_image'] != some_user['image']:
			some_update_values['user_image'] = some_user['image']

		somesupportticketvalues.update({'user_id': some_user['userid']}, some_update_values)

def checkSignedIn():
	print('A')
	if sessionKeyValid(USER_SESSION_KEY):
		return True

	print('B')
	some_id_token_provided = request.form.get(TOKEN_ID_VALUE_NAME)

	print('C')
	oauthusertoken = confirmOAuthSignIn(some_id_token_provided)

	print('D')
	if some_id_token_provided == None or not oauthusertoken['login']:
		return False

	setSessionKey((USER_SESSION_KEY, oauthusertoken['userid']))
	setSessionKey(('name', oauthusertoken['name']))
	setSessionKey(('email', oauthusertoken['email']))
	setSessionKey(('image', oauthusertoken['image']))

	print('E')
	checkUserDetails(oauthusertoken)

	print('F')
	if supportstaffuser(session[USER_SESSION_KEY]):
		setSessionKey((SUPPORT_STAFF_ROOM_TITLE_KEY, SUPPORT_STAFF_ROOM_ID))

	print('G')
	return True
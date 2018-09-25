import datetime

import string

import random

def getRandomKey(some_string_length = 9):
	return ''.join(random.choices(string.ascii_letters + string.digits, 
								  k = some_string_length))

SERVER_PATH = ''

GOOGLE_APP_CLIENT = '781246595138-3dkh6d0uv6icr8nt2ndu6eg19bo3ke6b.apps.googleusercontent.com'

CLIENT_TOKEN_DOMAIN_CHECK = False

#TODO: Retrieve google domain from list stored
GOOGLE_DOMAIN = 'abaoman.org'

TOKEN_ID_VALUE_NAME = 'id_token'

USER_SESSION_KEY = 'user_access'

CSRF_ID_TEXT_KEY = 'csrfidtext'

SUPPORT_STAFF_ROOM_TITLE_KEY = 'supportstaffconnected'

SUPPORT_STAFF_ROOM_ID = 'currentsupportstaff'

UNASSIGNED_SUPPORT_TICKET = 'Unassigned to staff'

ONGOING_SUPPORT_TICKET = 'Ongoing'

DELAYED_SUPPORT_TICKET = 'Delayed'

COMPLETE_SUPPORT_TICKET = 'Complete'

#########################################################################################
#SOCKETIO ROUTE NAMES
#########################################################################################


USER_CONNECTED_TO_SERVER = 'connect'

CLIENT_MESSAGE_WHEN_CONNECTED = 'connectmessage'

SUPPORT_STAFF_MESSAGE_WHEN_CONNECTED = 'supportstaffconnect'

ADD_VALUES = False

AS_EARLY_AS_POSSIBLE = datetime.datetime.fromtimestamp(276073220)

USER_COMMENT = 1

SUPPORT_STAFF_COMMENT = 0

GROUP_NOTIFICATION = 'Support staff members'


DEFAULTUSER_RESOURCES = {
	############################################################################
	#EXTERNAL STATIC RESOURCES
	############################################################################
	#FONT STYLESHEETS:
	#Title font: Raleway (URL: https://fonts.google.com/specimen/Raleway, CDN: Google Fonts)
	#Main font: Roboto (URL: https://fonts.google.com/specimen/Roboto, CDN: Google Fonts)
	'title_font_css_url': 'https://fonts.googleapis.com/css?family=Raleway:100,200,300,400,500,600,700,800,900',
	'main_font_css_url': 'https://fonts.googleapis.com/css?family=Roboto:100,300,400,500,700,900',
	############################################################################
	#ANIMATIONS STYLESHEET:
	#Animate.css (URL: https://github.com/daneden/animate.css/, CDN: cdnjs)
	'animations_css_url': 'https://cdnjs.cloudflare.com/ajax/libs/animate.css/3.5.2/animate.css',
	############################################################################
	#ICONS STYLESHEET:
	#Font Awesome (URL: https://fontawesome.com, CDN: use.fontawesome.com)
	'icons_css_url': 'https://use.fontawesome.com/releases/v5.2.0/css/all.css',
	############################################################################
	#NETWORKING SCRIPT:
	#SocketIO (URL: https://socket.io, CDN: cdnjs)
	'networking_script_url': '//cdnjs.cloudflare.com/ajax/libs/socket.io/1.3.6/socket.io.min.js',
	############################################################################
	#GOOGLE WEB SIGN IN, USER PROFILE
	#Google API (URL: https://developers.google.com/identity/sign-in/web/sign-in, CDN: apis.google.com)
	'google_api_script_url': 'https://apis.google.com/js/platform.js',
	'google_client_url': '781246595138-3dkh6d0uv6icr8nt2ndu6eg19bo3ke6b.apps.googleusercontent.com',
	############################################################################
	#INTERNAL STATIC RESOURCES
	############################################################################
	#STATIC FILE HOST
	'static_files_host': 'http://localhost/helpdesk-master/PythonApplication2/templates',
	############################################################################
	#FAVICONS
	'favicon_files_url': 'static/defaultuser/images/favicons',
	############################################################################
	#RESPONSIVE SLIDER
	#Siema JS (Responsive slider, URL: https://github.com/pawelgrzybek/siema)
	'responsive_slider_url': 'static/defaultuser/scripts/siema.js',
	############################################################################
	#HELPDESK STYLESHEETS
	#Main Desktop Stylesheet (min-width: 768px)
	'main_desktop_css_url': 'static/defaultuser/stylesheets/supportticketstyles.css',
	#Main Mobile Stylesheet (max-width: 767px)
	'main_mobile_css_url': 'static/defaultuser/stylesheets/supportticketstyles_max-width_767px.css',
	#Notifications Stylesheet
	'notifications_css_url': 'static/defaultuser/stylesheets/notificationviewstyles.css',

	#HELPDESK SCRIPTS
	#Google Sign In, User profiles
	'google_sign_in_script': 'static/defaultuser/scripts/OAuthUserSignIn.js',
	#Support Tickets: Displays and modifies support tickets in three columns on the page
	'supporttickets_script': 'static/defaultuser/scripts/supportticketsonpage.js',
	#Support Ticket Details View: Displays all details of the support ticket and provides actions
	'supportticketdetails_script': 'static/defaultuser/scripts/supportticketdetails.js',
	#Clipboard action: Copies support ticket details to clipboard
	'copy_to_clipboard_script': 'static/defaultuser/scripts/copyText.js',
	#Notification action: Displays notifications about events for the current use
	'notifications_script': 'static/defaultuser/scripts/notificationview.js',
	#New support ticket action: Adds a new support ticket for the user
	'new_support_ticket_script': 'static/defaultuser/scripts/newsupportticketview.js',
	#Socket events: Calls various functions based on socket events provided
	'socket_events_script': 'static/defaultuser/scripts/socketevents.js',
	#Page functions: Functions for loading support tickets and UI helpers
	'page_functions_script': 'static/defaultuser/scripts/pagefunctions.js',
	#Page setup: Sets up the page and adds listeners
	'page_setup_script': 'static/defaultuser/scripts/pagesetup.js',
	#Support staff action: Displays details of the support staff
	'support_staff_display_script': 'static/defaultuser/scripts/supportstaffdisplay.js',
	#Support ticket user search: Searches support tickets reported by the user
	'support_ticket_user_search': 'static/defaultuser/scripts/supportticketusersearch.js',

	#HELPDESK IMAGES
	'main_ABA_logo': 'static/defaultuser/images/mainABAlogo.PNG',
	################################################################
	'production_css': 'helpdeskstylesheet.css',
	'production_script': 'helpdeskview.js'

}

ADMINUSER_RESOURCES = {
	############################################################################
	#HELPDESK SUPPORT STAFF STYLESHEETS
	#Main Desktop Support Staff Stylesheet (min-width: 768px)
	'main_desktop_supportstaff_css_url': 'static/adminuser/stylesheets/supportticketadminstyles.css',
	############################################################################
	#ADMIN USER SCRIPTS
	#Filesaver.js (URL: https://github.com/eligrey/FileSaver.js/)
	'filesave_script': 'static/adminuser/scripts/FileSaver.js',

	#Sheet JS (URL: https://github.com/SheetJS/js-xlsx, CDN: https://cdnjs.cloudflare.com/)
	'excel_csv_data_formatter_script': 'https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.13.3/xlsx.full.min.js',

	#Chart JS (URL: https://www.chartjs.org/, CDN: https://cdnjs.cloudflare.com/)
	'chart_data_formatter_script': 'https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.7.2/Chart.min.js'
}
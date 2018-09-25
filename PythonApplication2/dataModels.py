
#########################################################################################
#FLASK SQALCHEMY MODULES
#########################################################################################
from flask_sqlalchemy import Model

from sqlalchemy import Column, Integer, String, DateTime


#########################################################################################
#DATABASE INSTANCE
#########################################################################################
from mainview import db

from mainview import whooshee
#########################################################################################
#DATETIME VALUES
#########################################################################################
from constKeys import AS_EARLY_AS_POSSIBLE

#########################################################################################
'''supportticketslist: Stores all support tickets created.

   Columns in model:
   1. supportid: The support ticket id which is a randomly generated 
				 9 character alphanumeric string
   2. user_id: The user ID provided from OAuth authentication to identify the user
   3. user_email: The user's current email address from OAuth authentication
   4. user_name: The user's current name from OAuth authentication
   5. user_image: The user's current image from OAuth authentication
   6. supporttype: The support type chosen by the user
   7. supportdescription: The support description provided by the user
   8. supportlocation: The support location provided by the user
   9. ticketsubmissiondatetime: The date and time of submission of the support ticket
   10. supportstatustype: The current status type of the support ticket 
						  (Ongoing, Delayed, Completed)
   11. supportstatusdescription: The current status description of the support ticket
								 set by the support staff member
   12. supportstaffassigned: The OAuth ID of the support staff member assigned
   13. supportstaffname: The name of the support staff member assigned
   14. supportstaffemail: The email of the support staff member assigned
   15. supportstaffimage: The image of the support staff member assigned
   16. supportticketchanges: Shows the changes to the support ticket in JSON
   17. lastupdated: The date and time of the last update to the support ticket'''
   
@whooshee.register_model('supportid', 
						 'user_email', 
						 'user_name', 
						 'supporttype', 
						 'supportdescription', 
						 'supportlocation', 
						 'supportstaffname', 
						 'supportstaffemail')

class supportticketslist(db.Model):
	 supportid = Column('supportid', 
						String(), 
						primary_key=True)

	 user_id = Column('user_id',
					  String(), 
					  nullable = False)

	 user_email = Column('user_email',
						 String(254), 
						 nullable = False)
	 
	 user_name = Column('user_name',
						String(100), 
						nullable = False)
	 
	 user_image = Column('user_image', 
						 String(), 
						 nullable=False)

	 supporttype = Column('supporttype',
						  String(100), 
						  nullable = False)
	 
	 supportdescription = Column('supportdescription',
								 String(120), 
								 nullable = False)
	 
	 supportlocation = Column('supportlocation', 
							  String(80), 
							  nullable = False);

	 ticketsubmissiondatetime = Column('ticketsubmissiondatetime',
									   DateTime(), 
									   nullable = False)

	 supportstatustype = Column('supportstatustype', 
								String(), 
								nullable=False)

	 supportstatusdescription = Column('supportstatusdescription', 
									   String(), 
									   nullable = False)

	 supportstaffassigned = Column('supportstaffassigned', 
								   String(), 
								   nullable = False)

	 supportdatetime = Column('supportdatetime', 
							  DateTime(), 
							  nullable = False)

	 supportstaffname = Column('supportstaffname', 
							   String(), 
							   nullable = False)

	 supportstaffemail = Column('supportstaffemail', 
								String(), 
								nullable = False)

	 supportstaffimage = Column('supportstaffimage', 
								String(), 
								nullable = False)

	 supportticketchanges = Column('supportticketchanges', 
								   String(), 
								   nullable = False)

	 lastupdated = Column('lastupdated', 
						  DateTime(), 
						  nullable = False)
	 #Table 
	 def __repr__(self):
		 return str.format('''{{"supportid": "{}", 
							"user_email": "{}", 
							"user_name": "{}", 
							"user_image": "{}",
							"supporttype": "{}", 
							"supportlocation": "{}", 
							"supportdescription": "{}", 
							"ticketsubmissiondatetime": "{}",
							"supportstatustype": "{}",
							"supportstatusdescription": "{}",
							"supportstaffassigned": "{}",
							"supportdatetime": "{}",
							"supportstaffname": "{}",
							"supportstaffemail": "{}",
							"supportstaffimage": "{}",
							"supportticketchanges": "{}"}}''',
								self.supportid, 
								self.user_email, 
								self.user_name,
								self.user_image,
								self.supporttype, 
								self.supportlocation,
								self.supportdescription,
								self.ticketsubmissiondatetime,
								self.supportstatustype,
								self.supportstatusdescription,
								self.supportstaffassigned,
								self.supportdatetime,
								self.supportstaffname,
								self.supportstaffemail, 
								self.supportstaffimage,
								self.supportticketchanges)
#########################################################################################


#########################################################################################
#Stores support staff details
class supportstaffmemberdetails(db.Model):
	id = Column('id', 
				String(), 
				nullable = True)

	name = Column('name', 
				  String(), 
				  nullable = False)

	email = Column('email', 
				   String(), 
				   nullable = False, 
				   primary_key = True)

	phone = Column('phone', 
				   String(), 
				   nullable = False)

	image = Column('image', 
				   String(), 
				   nullable = True)

	supporttypes = Column('supporttypes', 
						  String(), 
						  nullable = False)

	adminuser = Column('adminuser', 
					   Integer(), 
					   nullable = False)

	location = Column('location', 
					  String(), 
					  nullable = False)

	firstlogin = Column('firstlogin', 
						String(), 
						nullable = False)

	def __repr__(self):
		return str.format('''{{"id": "{}", 
							   "name": "{}", 
							   "email": "{}",
							   "phone": "{}",
							   "image": "{}",
							   "supporttypes": "{}",
							   "adminuser": "{}",
							   "location": "{}",
							   "firstlogin": "{}"}}''', 
						  self.id, 
						  self.name, 
						  self.email,
						  self.phone,
						  self.image,
						  self.supporttypes,
						  self.adminuser,
						  self.location,
						  self.firstlogin)
#########################################################################################


#########################################################################################
#Stores support locations
class supportlocation(db.Model):
	supportlocationdetails = Column(String(), 
									primary_key=True, 
									nullable = False)
#########################################################################################


#########################################################################################
#Stores support descriptions for each support type in the supporttype model
class supportdescription(db.Model):
	supporttype = Column(String(), 
						 primary_key = True, 
						 nullable = False)

	supportdescriptions = Column(String(), 
								 nullable = False)
#########################################################################################

#########################################################################################

class supportticketcomments(db.Model):
	commentid = Column('commentid', 
					   String(), 
					   primary_key = True, 
					   nullable = False)

	supportid = Column('supportid',
					  String(), 
					  nullable = False)

	commenttext = Column('commenttext',
						 String(120), 
						 nullable = False)

	commentdatetime = Column('commentdatetime',
							 DateTime(), 
							 nullable = False)

	commentauthor = Column('commentauthor',
						   Integer(), 
						   nullable = False)

class supportticketnotifications(db.Model):
	notificationid = Column('notificationid', 
							String(), 
							primary_key = True, 
							nullable = False)

	userid = Column('userid', 
					String(), 
					nullable = False)

	notificationseen = Column('notificationseen', 
							  Integer(), 
							  nullable = False)

	notificationdatetime = Column('notificationdatetime', 
								  DateTime(), 
								  nullable = False)

	notificationaction = Column('notificationaction', 
								String(), 
								nullable = True)

	notificationtext = Column('notificationtext', 
							  String(), 
							  nullable = False)


class supportticketoverrides:
	supportticketoverrideid = Column('supportticketoverrideid', 
									 String(), 
									 nullable = False, 
									 primary_key = True)

	supportticketstaffemail = Column('supportticketstaffemail', 
									 String(), 
									 nullable = False)

	supportticketpropertyname = Column('supportticketproperty', 
									   String(), 
									   nullable = False)

	supportticketpropertyvalue = Column('supportticketproperty', 
									   String(), 
									   nullable = False)

db.create_all()

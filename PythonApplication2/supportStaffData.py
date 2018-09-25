import datetime

import copy 
#########################################################################################
#databaseStorageList BASE CLASS MODULE
#########################################################################################
from databaseStorageList import databaseStorageList

#########################################################################################
#DATABASE INSTANCE
#########################################################################################
from mainview import db

#########################################################################################
#CONSTANT KEYS
#########################################################################################
from constKeys import *

#########################################################################################
#DATAMODELS
#########################################################################################
from dataModels import supportstaffmemberdetails

from dataModels import supportticketslist

#########################################################################################
#SUPPORT TYPE MODULE
#########################################################################################
from supportType import supportType

from constKeys import ADD_VALUES
'''
supportStaffData:
Handles the supportstaffmemberdetails datamodel

1. __init__:
	ARGUMENTS: 
	1. self (the current supportStaffData instance)

	Initializes the base class with the database instance db and 
	database model supportstaffmemberdetails

2. getCurrentDataEntry:
	ARGUMENTS: 
	1. self (the current supportStaffData instance)
	2. some_value: A dictionary containing all column names as keys and all column values as 
				   strings

	Overloaded method from the databaseStorageList base class which creates a dictionary 
	from the datamodel isntance and intializes an instance of supportType for each 
	support staff member, for updating the currentData list in the supportStaffData 
	instance

3. getSupportStaffFromSupportType:
   ARGUMENTS: 
   1. self (the current supportStaffData instance)
   2. some_suport_type_provided: A string indicating which support type the user selected
					  
   Returns the OAuth ID of a support staff member for a given support type
   The support staff member is chosen by first creating a list of all the support staff
   members whose supportType instance contains the given support type and then choosing
   the support staff member with the least number of tasks for the current day.
   If the support type provided is not in the supportType instance of any support staff
   members, the support ticket is made a common support ticket and the UNASSIGNED_SUPPORT_TICKET
   support staff member is returned 

4. __contains__:
   ARGUMENTS: 
   1. self (the current supportStaffData instance)
   2. some_support_staff_id_provided

   Returns a dictionary of the support staff member with the OAuth ID provided
   Wrapper for the __contains__ method of the databaseStorageList base class

'''

class supportStaffData(databaseStorageList):
#########################################################################################
	def __init__(self):
			self.START_OF_DAY = datetime.datetime \
										.combine(datetime.date.today(), 
												 datetime.time())

			super().__init__(database = db, databasemodel = supportstaffmemberdetails)	

			if ADD_VALUES:
				supportstaffmemberdetails.query.delete()

				db.session.commit()

				self.append({'id': UNASSIGNED_SUPPORT_TICKET, 
							 'name': UNASSIGNED_SUPPORT_TICKET, 
							 'email': UNASSIGNED_SUPPORT_TICKET, 
							 'phone': UNASSIGNED_SUPPORT_TICKET,
							 'image': UNASSIGNED_SUPPORT_TICKET,
							 'supporttypes': str(supportType(UNASSIGNED_SUPPORT_TICKET)),
							 'adminuser': 0,
							 'location': UNASSIGNED_SUPPORT_TICKET,
							 'firstlogin': 1
							},
			 
							{'id': '112481964862428364196', 
							 'name': 'Help Desk Staff A', 
							 'email': 'helpdeskstaffa@gmail.com',
							 'phone': '24452',
							 'image': 'https://lh6.googleusercontent.com/-qLlJtR0dZwE/AAAAAAAAAAI/AAAAAAAAAAA/AB6qoq0iZILKBu3ToJcqcRRpuAevzZFKQg/s96-c/photo.jpg',
							 'supporttypes': str(supportType('Some support type 2', 
															 'Some support type 9', 
															 'Some support type 15')),
							'adminuser': 0,
							'location': 'S21',
							'firstlogin': 1
							},

							{'id': '114146465528476061849', 
							 'name': 'IT Intern', 
							 'email': 'itintern@abaoman.org', 
							 'phone': '124422',
							 'image': 'https://lh3.googleusercontent.com/-Gj_z9rYoBLw/AAAAAAAAAAI/AAAAAAAAAAA/AB6qoq2JDPwZYeuxh2qg-3Csn7yCPx2Cjg/s96-c/photo.jpg',
							 'supporttypes': str(supportType('Some support type 1', 
															 'Some support type 9', 
															 'Some support type 19')),
							'adminuser': 1,
							'location': 'S24',
							'firstlogin': 1
							})
#########################################################################################

#########################################################################################
	#Creates a supportType instance for each support staff member from a given 
	#dictionary of a support staff member
	#Overloads getCurrentData in the databaseStorageList base class
	def getCurrentDataEntry(self, some_value):
		#Create a dictionary from the model instance
		some_value_provided = self.rowToDict(some_value)

		#Create an instance of supportType from the supporttypes entry in the dictionary
		some_value_provided['supporttypes'] = supportType(some_value_provided['supporttypes'])

		return some_value_provided
#########################################################################################

#########################################################################################
	#Creates a list of support staff members without the UNASSIGNED_SUPPORT_TICKET user 
	#and removes the id and support types for all other staff members for displaying 
	#support staff details
	def getSupportStaffUserData(self, support_staff_admin = False):
		current_staff_member_details = copy.deepcopy(self.currentData)

		current_staff_member_details.remove(current_staff_member_details[0])

		if not support_staff_admin:
			for i in range(0, len(current_staff_member_details)):
				del current_staff_member_details[i]['id']
				del current_staff_member_details[i]['supporttypes']

		return current_staff_member_details
#########################################################################################

#########################################################################################
	#Returns a dictionary of a support staff member from a given support type
	def getSupportStaffFromSupportType(self, 
									   some_support_type_provided):
		#Stores all support staff members with some_support_type_provided in their
		#supportType instance
		supportstaffmembers = []

		#Get all support staff members with some_support_type_provided in their
		#supportType instance and store it in supportstaffmembers
		for some_support_staff_member in self.currentData:
			if some_support_type_provided in some_support_staff_member['supporttypes']:
				supportstaffmembers.append(some_support_staff_member['email'])

		#If there are no support staff members with some_support_type_provided in their
		#supportType instance, return the UNASSIGNED_SUPPORT_TICKET staff member
		if not len(supportstaffmembers):
			return self.__getitem__({'name': UNASSIGNED_SUPPORT_TICKET})

		#Get the support staff member in supportstaffmembers with the least number
		#of support tickets assigned from START_OF_DAY

		supportstaffmemberforsupporttype = supportstaffmembers[0]

		supportticketnumber = -1

		for some_support_staff_member in supportstaffmembers:
			supporttickets = supportticketslist.query \
											   .filter(supportticketslist.supportstaffassigned == some_support_staff_member \
													   and supportticketslist.ticketsubmissiondatetime > self.START_OF_DAY) \
											   .count()
			if supporttickets < supportticketnumber:
				supportticketnumber = supporttickets
				supportstaffmemberforsupporttype = some_support_staff_member

		print('NMM')

		print(supportstaffmemberforsupporttype)

		return self.__getitem__({'email': supportstaffmemberforsupporttype})

#########################################################################################

#########################################################################################
	#Returns the dictionary of a support staff member from the OAuth ID of the support 
	#staff member provided
	#Wrapper for __contains__ in the base class
	def __contains__(self, 
					 some_support_staff_id_provided):
		return super().__contains__({'id': some_support_staff_id_provided})
#########################################################################################

	def hasEmail(self, 
				 some_support_staff_email_provided):
		print(some_support_staff_email_provided)
		return super().__contains__({'email': some_support_staff_email_provided})

	def getEmails(self):
		support_staff_emails = []

		for some_support_staff in self.currentData:
			support_staff_emails.append(some_support_staff['email'])

		return support_staff_emails
import datetime

import random

import string

import json

import re

from mainview import db

from dataModels import *

from constKeys import getRandomKey

from databaseStorageList import databaseStorageList

from supportTicketChanges import supportTicketChanges

from supportStaffData import supportStaffData

import booleanExpressionResult

from sqlalchemy import func

from sqlalchemy import distinct

from constKeys import ADD_VALUES

class supportLocationData(databaseStorageList):
	def __init__(self):
		super().__init__(database = db, databasemodel = supportlocation)
		
		#TODO: Remove ADD_VALUES
		if False:
			supportlocation.query.delete()

			db.session.commit()

			self.append('E-18', 'E-19', 'E-20', 'E-21', 'E-22', 'E-23', 'E-24', 'S22', 'S23', 'S24', 'S25', 'Art1', 'Art2', 'Design Lab', 'ITLab1', 'S37', 'S39', 'S41', 'S-34 IT Lab', 'S03', 'S04', 'S05', 'S06', 'S07', 'S08', 'S09', 'Secondary Counseling Suite', 'Lab S11', 'Lab S13', 'Lab S14', 'Lab S15', 'Lab S16', 'Lab S17', 'SS01 Senior Study Lounge', 'SF01', 'SF02', 'SF03', 'SF04', 'SF05', 'SF06', 'SF07', 'SF08', 'SF09 IT Support Office', 'SF10', 'SF11', 'SF12', 'SG13', 'SG14', 'SG15', 'SG16', 'SG17', 'SG18', 'SG19', 'SG20', 'SG21', 'SG22', 'SG23 Secondary Office', 'SG24 Lab', 'Library', 'Academic Center', 'Sec Library', 'Black Box', 'Music 1', 'Music 2', 'PAC', 'PAC Stage', 'PAC Upper Foyer', 'PAC Lower Foyer', 'ECE', 'E-1', 'E-2', 'E-3', 'E-4', 'E-5', 'E-6', 'E-7', 'E-8', 'E-9', 'E-10', 'E-11', 'E-12', 'E-13', 'E-14', 'E-15', 'E-16', 'E-17', 'E-24', 'E-25', 'Elem IT', 'Near Elem IT 2', 'Elem Library', 'Elem Music Room', 'GYM', 'MPH1', 'MPH2', 'MQ Field', 'Tennis Courts', 'WtRm', 'Drama Court', 'Secondary Lecture Hall', 'MS Common Room')
	
	def append(self, *args):
		for some_value in args:
			super().append({'supportlocationdetails': some_value})

	def __contains__(self, some_value_provided):
		super().__contains__({'supportlocationdetails': some_value_provided})

class supportDescriptionData(databaseStorageList):
	def __init__(self):
		super().__init__(database = db, databasemodel = supportdescription)
	
		#TODO: Remove ADD_VALUES
		if ADD_VALUES:
			supportdescription.query.delete()

			db.session.commit()

			super().append({'supporttype': 'Projector', 
							'supportdescriptions': '["No display", "Bad image quality", "Projector not turning on"]'},
					   
						   {'supporttype': 'Printer', 
							'supportdescriptions': '["Unable to print", "Additional print quota"]'},
						
						   {'supporttype': 'Google', 
							'supportdescriptions': '["Password reset", "Cannot login"]'},
						
						   {'supporttype': 'iSAMS', 
							'supportdescriptions': '["Password reset", "Cannot login"]'},
						
						   {'supporttype': 'Microsoft Office 365', 
							'supportdescriptions': '["Password reset", "Cannot login"]'},
						
						   {'supporttype': 'Dell Laptop', 
							'supportdescriptions': '["Not connecting to the Internet", "Not booting", "Cannot login"]'},
						
						   {'supporttype': 'Macbook', 
							'supportdescriptions': '["Not connecting to the Internet", "Not booting", "Cannot login"]'},

						   {'supporttype': 'iPad', 
							'supportdescriptions': '["Not connecting to the Internet"]'},
						
						   {'supporttype': 'Internet', 
							'supportdescriptions': '["Network slow", "Unable to login", "Unable to connect"]'},

						   {'supporttype': 'Lost/Damaged', 
							'supportdescriptions': '["Device lost", "Device damaged", "Lost data"]'},
						
						   {'supporttype': 'Other', 
							'supportdescriptions': '[]'})
	
	def getSupportTypes(self):
		support_types = []

		for some_value in self.currentData:
			support_types.append({'supporttypedetails': some_value['supporttype']}) 

		return support_types

	def __contains__(self, some_value_provided):
		return super().__contains__({'supporttype': some_value_provided})

class supportTicketData(databaseStorageList):
	def __init__(self):
		super().__init__(database = db, databasemodel = supportticketslist)

	def updateDataEntry(self, some_current_value, some_new_value):
		current_support_ticket = supportTicketChanges(some_current_value \
													  .supportticketchanges)

		#some_new_value['lastupdated'] = datetime.datetime.now()

		current_support_ticket.append(some_new_value)

		some_current_value.supportticketchanges = str(current_support_ticket)
		
	def append(self, some_value):
		current_support_ticket = supportTicketChanges(some_value['supportticketchanges'])

		if not len(current_support_ticket):
			current_support_ticket.append(some_value)
			some_value['supportticketchanges'] = str(current_support_ticket)

		super().append(some_value)

	def search(self, some_search_text):
		some_support_tickets = self.databaseModel \
							   .query.whooshee_search(some_search_text) \
							   .order_by(self.databaseModel.supportid.desc()) \
							   .all()

		if not len(some_support_tickets):
			return []

		for index, some_support_ticket in enumerate(some_support_tickets):
			some_support_tickets[index] = self.rowToDict(some_support_ticket)

		return some_support_tickets

	def getFieldItemLength(self, some_field_name, some_value):
		return self.databaseModel \
				   .query \
				   .filter(getattr(self.databaseModel, \
								   some_field_name) == some_value) \
				   .count()

	def getUniqueFieldLength(self, some_field_name):
		return self.databaseModel \
				   .query \
				   .distinct(getattr(self.databaseModel, \
									 some_field_name)) \
				   .group_by(getattr(self.databaseModel, 
									 some_field_name)) \
				   .count()

	def getWeekSupportTickets(self):
		START_OF_DAY = datetime.datetime \
							   .combine(datetime.date.today(), 
										datetime.time()) 

		CURRENT_TIME = datetime.datetime.now()

		week_support_tickets = []

		for i in range(0, 7):
			query_provided  = self.databaseModel.query
			query_provided = query_provided.filter(self.databaseModel
										   .ticketsubmissiondatetime > START_OF_DAY, 
										   self.databaseModel
										   .ticketsubmissiondatetime < CURRENT_TIME)
			week_support_tickets.append(query_provided.count())
			CURRENT_TIME = START_OF_DAY

			START_OF_DAY = START_OF_DAY - datetime.timedelta(days = 1)

		return week_support_tickets

	def getSupportTicketsFromDay(self, 
								 some_end_date, 
								 some_duration = 1):

		some_end_date = datetime.datetime.fromtimestamp(some_end_date/1000.0)

		some_start_date = some_end_date - datetime.timedelta(days = some_duration)

		some_support_tickets = self.databaseModel \
								   .query \
								   .filter(self.databaseModel
											   .ticketsubmissiondatetime 
											   >= some_start_date, 
										   self.databaseModel
											   .ticketsubmissiondatetime 
											   <= some_end_date).all()

		some_support_tickets_from_support_time = self.databaseModel \
								   .query \
								   .filter(self.databaseModel
											   .supportdatetime
											   >= some_start_date, 
										   self.databaseModel
											   .supportdatetime
											   <= some_end_date).all()

		for some_support_ticket in some_support_tickets_from_support_time:
			if some_support_ticket not in some_support_tickets:
				some_support_tickets.append(some_support_ticket)

		if not len(some_support_tickets):
			return []

		for index, some_value in enumerate(some_support_tickets):
			some_support_tickets[index] = self.rowToDict(some_value)

		return some_support_tickets

	def formattedSearch(self, some_search_values):
		search_results = ''

		del some_search_values['or_fieldnames']

		for some_search_field, some_search_text in some_search_values.items():
			print(some_search_field, some_search_text)

			current_search_field_result = self.databaseModel \
											  .query \
											  .filter(getattr(self.databaseModel, \
															  some_search_field) \
													  .contains(some_search_text)) \
											  .all()

			if search_results == '':
				search_results = set(current_search_field_result)

			else:
				search_results = search_results & set(current_search_field_result)

		if not len(search_results):
			return []

		search_results = list(search_results)

		for index, some_value in enumerate(search_results):
			search_results[index] = self.rowToDict(some_value)

		return search_results

	def getValuesFromText(self, some_search_values):
		search_results= []

		del some_search_values['or_fieldnames']

		query_provided = self.databaseModel.query

		def getSetsFromText(some_search_field, some_text):
			some_values = re.split('(&&|\|\|)', some_text)  

			#print(some_values)

			for index, some_search_text in enumerate(some_values):
				if some_search_text == '&&' \
					 or some_search_text == '||':
					continue

				if some_search_text[0] == '!':
					some_values[index] = set(query_provided \
										 .filter(getattr(self.databaseModel, \
														 some_search_field) \
												 != some_search_text[1:]) \
										 .all())

					continue

				some_values[index] = set(query_provided \
									 .filter(getattr(self.databaseModel, \
													some_search_field) \
											 == some_search_text) \
									 .all())

			#print(some_values)

			return some_values

		for some_search_field, some_value_text in some_search_values.items():
			search_set = booleanExpressionResult \
						 .boolean_evaluate(getSetsFromText(some_search_field, 
														   some_value_text))

			if not len(search_set):
				return []

			search_results.append(search_set)


		search_values = search_results[0]

		for some_value in search_results:
			search_values = search_values & some_value

		search_values = list(search_values)

		for index, some_value in enumerate(search_values):
			search_values[index] = self.rowToDict(some_value)

		return search_values

	def __repr__(self):
		return str(self.currentData)

class supportTicketCommentData(databaseStorageList):
	def __init__(self):
		super().__init__(database = db, databasemodel = supportticketcomments)

class supportTicketNotificationData(databaseStorageList):
	def __init__(self):
		super().__init__(database = db, databasemodel = supportticketnotifications)

	def append(self, *args):
		for some_comment in args:
			some_comment['notificationid'] = getRandomKey() 
			some_comment['notificationdatetime'] = datetime.datetime.now()

			some_comment['notificationseen'] = 0

		super().append(*args)

	def addnotification(self, **kwargs):
		if 'notificationaction' not in kwargs:
			kwargs['notificationaction'] = ''

		kwargs['notificationtext'] = json.dumps({'title': kwargs['title'], 
												 'notificationbody': kwargs['notificationbody']})

		del kwargs['title']

		del kwargs['notificationbody']

		self.append(kwargs)

class supportTicketOverridesData:
	#def __init__(self):
		#super().__init__(database = db, databasemodel = supportticketoverrides)

	def getSupportTicketOverride(self, some_support_ticket):
		#some_support_ticket_overrides = self.getValue({'supportticketpropertyname': kwargs['propertyname']})

		#if not len(some_support_ticket_overrides):
		#	return False

		for some_override in self.currentData:
			if some_support_ticket[some_override['supportticketpropertyname']] \
				== some_override['supportticketpropertyvalue']:
				return some_override['supportticketstaffemail']

		return False

	def getOverride(self, some_support_ticket):
		return False
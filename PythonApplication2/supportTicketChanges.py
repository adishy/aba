import json

import datetime

import random 

import copy

class supportTicketChanges:
	def __init__(self, 
				 some_support_ticket_changes_provided=''):
		if not len(some_support_ticket_changes_provided):
			self.currentChanges = []

		else:
			self.currentChanges = json.loads(some_support_ticket_changes_provided)

	def append(self, *args):
		for some_value in args:
			self.currentChanges.append(some_value)

	def addValue(self, some_value):
		try:
			current_support_ticket = self.getChanges()
		
			new_support_ticket = {}

			for some_support_ticket_property in some_value:
				if current_support_ticket[some_support_ticket_property] != \
				   some_value[some_support_ticket_property]:
						new_support_ticket[some_support_ticket_property] = \
						some_value[some_support_ticket_property]

			self.append(new_support_ticket)

		except ValueError:
			self.append(some_value)

	def getChanges(self, **kwargs):
		if not len(self.currentChanges):
			raise ValueError

		supportTicketChangesLength = 0

		if 'index' in kwargs:
			supportTicketChangesLength = kwargs['index']

		else:
			supportTicketChangesLength = len(self.currentChanges)

		supportTicketChangesProvided = copy.deepcopy(self.currentChanges[0])

		if not supportTicketChangesLength:
			return supportTicketChangesProvided

		for i in range(1, supportTicketChangesLength):
			supportTicketChangesProvided.update(self.currentChanges[i])

		return supportTicketChangesProvided

	def __len__(self):
		return len(self.currentChanges)

	def __repr__(self):
		return json.dumps(self.currentChanges, default = str)
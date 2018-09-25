class supportType:
	def __init__(self, *args, **kwargs):
		self.supportTypes = []
		self.DELIMITER = ','

		if 'delimiter' in kwargs:
			self.DELIMITER = kwargs['delimiter']

		self.addSupportTypeProvided(*args)
	
	def addSupportTypeProvided(self, *args):
		if len(args) == 1 and ',' in args[0]:
			try:
				self.supportTypes = args[0].split(',')
				
				return True

			except:
				print('Could not get support types from string provided')
				
				return False
			
		for some_support_type_provided in args:
			try:
				self.supportTypes.append(some_support_type_provided)
					
			except:
				print('Could not get support type from arguments provided')

		return True

	def getSupportTypeString(self):
		return ','.join(self.supportTypes)

	def __contains__(self, some_given_support_type):
		return some_given_support_type in self.supportTypes

	def __repr__(self):
		return ','.join(self.supportTypes)

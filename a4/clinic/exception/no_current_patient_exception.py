class NoCurrentPatientException(Exception):
	def __init__(self, message = 'No current patient.'):
		self.message = message
		super().__init__(self.message)
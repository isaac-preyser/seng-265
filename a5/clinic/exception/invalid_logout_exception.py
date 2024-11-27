class InvalidLogoutException(Exception):
	def __init__(self, message = 'Invalid logout.'):
		self.message = message
		super().__init__(self.message)
class IllegalAccessException(Exception):
	def __init__(self, message = 'Illegal access.'):
		self.message = message
		super().__init__(self.message)
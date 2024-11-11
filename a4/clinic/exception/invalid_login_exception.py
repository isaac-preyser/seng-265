class InvalidLoginException(Exception):
	def __init__(self, message = 'Invalid login.'):
		self.message = message
		super().__init__(self.message)
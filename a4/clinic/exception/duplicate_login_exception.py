class DuplicateLoginException(Exception):
	def __init__(self, message = 'Duplicate login.'):
		self.message = message
		super().__init__(self.message)
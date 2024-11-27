class IllegalOperationException(Exception):
	def __init__(self, message = 'Illegal operation.'):
		self.message = message
		super().__init__(self.message)
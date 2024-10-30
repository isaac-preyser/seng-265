from unittest import TestCase
from unittest import main
from customer import Customer
from controller import Controller

class ControllerTest(TestCase):

	# testing methods for Controller added here
	def setUp(self):
		self.controller = Controller()

	def test_set_get_unset_current_customer(self):
		expected_customer_1 = Customer(9798884444, "Ali Mesbah", "1980-03-03")
		expected_customer_2 = Customer(9792226666, "Jin Hu", "2002-02-28")
		expected_customer_3 = Customer(9790012000, "John Doe", "2000-10-10")
		expected_customer_4 = Customer(9790014444, "Mary Doe", "1995-07-01")
		expected_customer_5 = Customer(9792225555, "Joe Hancock", "1990-01-15")

		self.controller.create_customer(9798884444, "Ali Mesbah", "1980-03-03")
		self.controller.create_customer(9792226666, "Jin Hu", "2002-02-28")
		self.controller.create_customer(9790012000, "John Doe", "2000-10-10")
		self.controller.create_customer(9790014444, "Mary Doe", "1995-07-01")
		self.controller.create_customer(9792225555, "Joe Hancock", "1990-01-15")
			
		# cannot get current customer without setting them first
		self.assertIsNone(self.controller.get_current_customer(), "cannot get current customer without setting them first")

		# cannot set a non-existent customer to be the current customer
		self.controller.set_current_customer(9790010001)
		self.assertIsNone(self.controller.get_current_customer(), "cannot get non-existent customer as current customer")

		# set one customer to be the current customer
		self.controller.set_current_customer(9790012000)
		actual_current_customer = self.controller.get_current_customer()
		self.assertIsNotNone(actual_current_customer)
		self.assertEqual(expected_customer_3, actual_current_customer, "expected current customer is customer 3")

		# unset current customer
		self.controller.unset_current_customer()
		actual_current_customer = self.controller.get_current_customer()
		self.assertIsNone(actual_current_customer)

		# set another customer to be the current customer
		self.controller.set_current_customer(9798884444)
		actual_current_customer = self.controller.get_current_customer()
		self.assertIsNotNone(actual_current_customer)
		self.assertEqual(expected_customer_1, actual_current_customer, "expected current customer is customer 1")

		# unset current customer once again
		self.controller.unset_current_customer()
		actual_current_customer = self.controller.get_current_customer()
		self.assertIsNone(actual_current_customer)


if __name__ == '__main__':
	main()

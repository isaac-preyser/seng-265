from unittest import TestCase
from unittest import main
from product import Product
from controller import Controller

class ControllerTest(TestCase):

	# testing methods for Controller added here
	def setUp(self):
		self.controller = Controller()

	def test_create_search_product(self):
		expected_product_1 = Product(123, 'Fernwood Coffee', 14.50)
		expected_product_1a = Product(123, 'Fernwood Coffee', 14.50)
		expected_product_2 = Product(234, 'Olay Soap Bar', 10.00)
		expected_product_3 = Product(345, 'Lindt Lindor Chocolate Bar', 4.00)

		#add one product
		self.assertTrue(self.controller.create_product(123, 'Fernwood Coffee', 14.50), 
			"product Fernwood Coffee was created")
		actual_product = self.controller.search_product(123)
		self.assertIsNotNone(actual_product, "product created and searched cannot be null")
		self.assertEqual(expected_product_1, actual_product, 
			"product Fernwood Coffee was created and its data are correct")

		# the searched product is the same as the create regardless of memory reference
		actual_product = self.controller.search_product(123)
		self.assertEqual(expected_product_1a, actual_product, 
			"the searched product is the same as the create regardless of memory reference")

		# should not allow to create another product with same code
		self.assertFalse(self.controller.create_product(123, 'Olay Soap Bar', 10.00))

		# add a second product
		self.assertTrue(self.controller.create_product(234, 'Olay Soap Bar', 10.00), "product Fernwood Coffee was created")
		actual_product = self.controller.search_product(234)
		self.assertIsNotNone(actual_product, "second product created cannot be null")
		self.assertEqual(expected_product_2, actual_product, 
			"second product, Olay Soap Bar, was created and its data are correct")

		# add a third product
		self.assertTrue(self.controller.create_product(345, 'Lindt Lindor Chocolate Bar', 4.00), 
			"product Fernwood Coffee was created")
		actual_product = self.controller.search_product(345)
		self.assertIsNotNone(actual_product, "second product created cannot be null")
		self.assertEqual(expected_product_3, actual_product, 
			"second product, Lindt Lindor Chocolate Bar, was created and its data are correct")

		# creating new products should not affect previous products
		actual_product = self.controller.search_product(234)
		self.assertIsNotNone(actual_product, "product created and retrieved cannot be null regardless of search order")
		self.assertEqual(expected_product_2, actual_product, 
			"product Olay Soap Bar was created, retrieved and its data are correct regardless of search order")
		actual_product = self.controller.search_product(123)
		self.assertIsNotNone(actual_product, "product created and retrieved cannot be null regardless of search order")
		self.assertEqual(expected_product_1, actual_product, 
			"product Fernwood Coffee was created, retrieved and its data are correct regardless of search order")

if __name__ == '__main__':
	main()

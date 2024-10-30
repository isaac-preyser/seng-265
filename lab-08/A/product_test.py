from unittest import TestCase
from unittest import main
from product import Product

class ProductTest(TestCase):

	# unit testing methods for Product added here

	def test_str(self):
		product1 = Product(123, 'Fernwood Coffee', 14.50)
		product1a = Product(123, 'Fernwood Coffee', 14.50)
		product2 = Product(234, 'Olay Soap Bar', 10.00)
		product3 = Product(345, 'Lindt Lindor Chocolate Bar', 4.00)

		self.assertIsNotNone(str(product1))
		self.assertEqual("code: 123, description: Fernwood Coffee, price: 14.50", 
			str(product1), "Coffee string")
		self.assertEqual("code: 345, description: Lindt Lindor Chocolate Bar, price: 4.00", 
			str(product3), "Chocolate string")
		self.assertEqual(str(product1a), str(product1), 
			"same products, same strings")
		self.assertNotEqual(str(product2), str(product1), 
			"different products, different strings")
		self.assertNotEqual(str(product3), str(product1), 
			"different products, different strings")


	def test_eq(self):
		# replace the pass command with your test checks for product equality
		product1 = Product(123, 'Fernwood Coffee', 14.50)
		product1a = Product(123, 'Fernwood Coffee', 14.50)
		product2 = Product(234, 'Olay Soap Bar', 10.00)
		product3 = Product(345, 'Lindt Lindor Chocolate Bar', 4.00)

		self.assertTrue(product1 == product1a, "same products")
		self.assertFalse(product1 == product2, "different products")
		self.assertFalse(product1 == product3, "different products")
		


if __name__ == '__main__':
	main()
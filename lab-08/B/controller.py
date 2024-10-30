from product import Product

class Controller:
    def __init__(self):
        # change the code below to use a list of products (only list, no dictionary)
        self.products = []

    def search_product(self, key):
        # change the code below to search a product in the list of products
        for product in self.products:
            if product.code == key:
                return product
        return None

    def create_product(self, code, description, price):
        # change the code below to create a product in the list of products
        self.products.append(Product(code, description, price))

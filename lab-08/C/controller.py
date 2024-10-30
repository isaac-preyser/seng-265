from customer import Customer

class Controller:

    def __init__(self):
        self.customers = {}
    	# change the constructor to record the current customer
        self.current_customer = None


    def search_customer(self, key):
        return self.customers.get(key)

    def create_customer(self, number, name, birth_year):
        if not self.search_customer(number):
            customer = Customer(number, name, birth_year)
            self.customers[number] = customer
            return True
        else:
            return False

    def set_current_customer(self, key):
        # change this method to set the current customer
        if self.search_customer(key):
            self.current_customer = key
            return True
        else:
            return False

    def get_current_customer(self):
        # change this method to get the current customer
        return self.search_customer(self.current_customer) 

    def unset_current_customer(self):
        # change this method to unset the current customer
        self.current_customer = None
        return True
    
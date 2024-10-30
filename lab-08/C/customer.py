class Customer:
  def __init__(self, number, name, birth_year):
    # number will be the key
    self.number = number
    self.name = name
    self.birth_year = birth_year

  def __eq__(self, other):
    return self.number  == other.number and self.name == other.name \
     and self.birth_year == other.birth_year
